# -*- coding: utf-8 -*-
"""
BD2MAA 发布包构建工具

用法：
    python tools/build_release_zip.py                 # 无参 → 交互式询问版本号
    python tools/build_release_zip.py v26.09.6        # 显式指定版本号
    python tools/build_release_zip.py --dry-run       # 只打印要做什么，不动磁盘也不出包
    python tools/build_release_zip.py --no-bump       # 不改 interface.json，按磁盘当前版本打包
    python tools/build_release_zip.py --out D:\\x.zip  # 指定输出 zip 路径
    python tools/build_release_zip.py --verify        # 只校验已有 zip

约定：
  1. **默认会把 interface.json 的 version 字段改为目标版本号**，再开始打包。
     这样 git 提交记录里自带版本号变更，发版 PR 语义清晰。
  2. 直接读磁盘 → **未提交的改动也会进包**（所以发版前先确认工作区状态）。
  3. 排除 config/ → MXU 首次启动自动生成默认实例，避免覆盖用户已有配置。
  4. 排除 MaaBd2.lnk → 写死路径的快捷方式在别人机器上无效，首次启动自动重建。
  5. 排除 updater_cache.json / cache / debug / updates / tools/build_release_zip.py 自身。
  6. 中文文件名必须带 UTF-8 标志位（0x800），否则 Windows 解压乱码。
  7. zip 内条目用固定时间戳 → 同一天重复构建得到完全相同的字节（可复现）。

需要修改的"版本号文件"只有 interface.json。version.json 放的是依赖版本（maafw/mxu），
updater_config.json 是用户配置；都不参与本工具。
"""
import os, sys, json, time, re, zipfile, hashlib, argparse, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCLUDE_DIRS  = {'.git', '.workbuddy', 'cache', 'config', 'debug', 'updates', '_stage'}
# 按包内相对路径匹配
EXCLUDE_FILES = {'MaaBd2.lnk', 'updater_cache.json', 'tools/build_release_zip.py'}
EXCLUDE_EXT   = {'.lnk', '.tmp', '.pyc'}

REQUIRED_FILES = [
    'interface.json', 'updater_config.json', 'version.json', 'launcher.bat',
    'BD2MAA-Updater.ps1', 'mxu.exe', 'mxu.ico', 'mxu_icon.png', 'LICENSE', 'README.md',
    '应用图标.bat', '更新功能说明.md', '注意事项1-----使用前必看！！！.txt',
]
REQUIRED_DIRS = ['agent/', 'maafw/', 'misc/', 'tasks/', 'resource/', 'tools/']

VERSION_RE = re.compile(r'^v\d+\.\d+\.\d+$')


def log(msg):
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()


def head_version(base):
    """HEAD 中 interface.json 的版本号（仓库里最近一次发布的标记）"""
    try:
        raw = subprocess.check_output(
            ['git', '-C', base, 'show', 'HEAD:interface.json'], stderr=subprocess.DEVNULL)
        return json.loads(raw.decode('utf-8-sig')).get('version')
    except Exception:
        return None


def disk_version(base):
    """磁盘上 interface.json 当前的版本号（工作区）"""
    try:
        with open(os.path.join(base, 'interface.json'), 'rb') as f:
            raw = f.read()
        return json.loads(raw.decode('utf-8-sig')).get('version')
    except Exception:
        return None


def bump_interface(base, new_version):
    """就地更新 interface.json 的 version 字段，保留编码 / BOM / 缩进 / 换行。
       返回 (old, new)；已是目标版本时 old == new 且磁盘不写。"""
    path = os.path.join(base, 'interface.json')
    with open(path, 'rb') as f:
        data = f.read()
    marker = b'"version": "'
    i = data.find(marker)
    if i < 0:
        raise RuntimeError('interface.json 找不到 "version" 字段')
    j = data.find(b'"', i + len(marker))
    old = data[i + len(marker):j].decode('utf-8')
    if old == new_version:
        return old, new_version     # 已是目标版本，不写盘
    new_data = data[:i + len(marker)] + new_version.encode('utf-8') + data[j:]
    with open(path, 'wb') as f:
        f.write(new_data)
    return old, new_version


def prompt_version(current, head_v):
    """交互式询问版本号（仅在 stdin 是 TTY 时调用）。
       无效输入会循环追问；空回车返回 None（视为取消）。"""
    cur = current or '?'
    while True:
        if head_v and head_v != current:
            sys.stdout.write('[?] 当前: %s  (HEAD 上次发布: %s)\n' % (cur, head_v))
        else:
            sys.stdout.write('[?] 当前: %s\n' % cur)
        sys.stdout.write('[?] 目标版本号 (例 v26.09.6，回车取消): ')
        sys.stdout.flush()
        try:
            line = sys.stdin.readline()
        except (EOFError, KeyboardInterrupt):
            return None
        line = line.strip()
        if not line:
            return None
        v = line if line.startswith('v') else 'v' + line
        if VERSION_RE.match(v):
            return v
        sys.stdout.write('[!] 格式不对，应为 v<主>.<次>.<修订>，例如 v26.09.6\n')


def confirm(msg):
    """仅在 stdin 是 TTY 时询问 y/N；非交互环境默认 True（CI / 管道场景）。"""
    if not sys.stdin.isatty():
        return True
    sys.stdout.write('[?] %s [y/N] ' % msg)
    sys.stdout.flush()
    try:
        ans = sys.stdin.readline().strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return ans in ('y', 'yes')


def collect(base):
    """按排除规则收集要打包的文件，返回 [(绝对路径, 包内相对路径)]"""
    out = []
    for root, dirs, fnames in os.walk(base):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in fnames:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, base).replace('\\', '/')
            if rel.split('/')[0] in EXCLUDE_DIRS:
                continue
            if rel in EXCLUDE_FILES or fn in EXCLUDE_FILES:
                continue
            if os.path.splitext(fn)[1].lower() in EXCLUDE_EXT:
                continue
            out.append((full, rel))
    out.sort(key=lambda x: x[1])
    return out


def build(base, out_path, version):
    """按磁盘状态打包。版本号已在上游通过 bump_interface 写进 interface.json。"""
    files = collect(base)
    log('[1] 待打包文件 = %d' % len(files))

    if os.path.exists(out_path):
        os.remove(out_path)
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)

    dt = time.localtime()[:6]          # 固定时间戳：同一天构建结果一致
    raw = 0
    t0 = time.time()
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for full, rel in files:
            data = open(full, 'rb').read()
            zi = zipfile.ZipInfo(rel, date_time=dt)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
            raw += len(data)

    size = os.path.getsize(out_path)
    log('[2] 原始 %d 字节 -> zip %d 字节 (%.2f MiB)  用时 %.1fs'
        % (raw, size, size / 1048576.0, time.time() - t0))
    return out_path


def verify(path, version):
    ok = True
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        names = z.namelist()
        log('[V1] testzip() = %s' % bad)
        if bad:
            ok = False
        log('[V2] 条目数 = %d' % len(names))

        v = json.loads(z.read('interface.json').decode('utf-8-sig')).get('version')
        log('[V3] interface.json 版本 = %s %s' % (v, 'OK' if v == version else '<= 不符预期'))
        if v != version:
            ok = False

        miss = [k for k in REQUIRED_FILES if k not in names]
        miss += ['%s(%d)' % (d, sum(1 for x in names if x.startswith(d)))
                 for d in REQUIRED_DIRS if not any(x.startswith(d) for x in names)]
        log('[V4] 缺失必需项 = %s' % (miss if miss else '无'))
        if miss:
            ok = False

        leaked = [x for x in names
                  if x.split('/')[0] in ('config', 'cache', 'debug', 'updates', '.git', '.workbuddy')
                  or x.endswith('.lnk') or x == 'updater_cache.json']
        log('[V5] 排除项泄漏 = %s' % (leaked[:5] if leaked else '无'))
        if leaked:
            ok = False

        nonascii = [x for x in names if any(ord(c) > 127 for c in x)]
        bad_flag = [x for x in nonascii if not (z.getinfo(x).flag_bits & 0x800)]
        log('[V6] 中文名条目 = %d，缺 UTF-8 标志位 = %s'
            % (len(nonascii), bad_flag if bad_flag else '无'))
        if bad_flag:
            ok = False

    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    log('[V7] sha256 = %s' % h.hexdigest())
    log('[V8] size   = %d bytes' % os.path.getsize(path))
    log('=== %s ===' % ('全部通过' if ok else '存在问题'))
    return ok


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('version', nargs='?', help='目标版本号，如 v26.09.6；不传则交互询问')
    ap.add_argument('--out', help='输出 zip 路径，默认 updates/MABd2<version>.zip')
    ap.add_argument('--verify', action='store_true', help='只校验已有 zip')
    ap.add_argument('--no-verify', action='store_true', help='只构建不校验')
    ap.add_argument('--no-bump', action='store_true', help='不改 interface.json，按磁盘当前版本打包')
    ap.add_argument('--dry-run', action='store_true', help='只打印发布计划，不动磁盘也不出包')
    args = ap.parse_args()

    head_v = head_version(BASE)
    cur_v = disk_version(BASE)

    # ---- 1. 版本号解析 ----
    version = args.version
    if not version:
        if sys.stdin.isatty():
            version = prompt_version(cur_v, head_v)
            if not version:
                log('已取消（无输入）')
                return 1
        else:
            log('无版本号且 stdin 非 TTY，无法交互询问。请显式传入，例如 v26.09.6')
            return 2

    if not version.startswith('v'):
        version = 'v' + version
    if not VERSION_RE.match(version):
        log('版本号格式不对：%r（应为 v<主>.<次>.<修订>，例 v26.09.6）' % version)
        return 2

    out = args.out or os.path.join(BASE, 'updates', 'MABd2%s.zip' % version)

    # ---- 2. 打印发布计划 ----
    log('=== 发布计划 ===')
    log('  目标版本: %s' % version)
    log('  HEAD   :  %s' % (head_v or '?'))
    log('  磁盘    :  %s' % (cur_v or '?'))
    log('  输出    :  %s' % out)
    will_bump = (not args.no_bump) and (cur_v != version)
    if will_bump:
        log('  将改    :  interface.json  %s -> %s' % (cur_v, version))
    elif args.no_bump:
        log('  将改    :  interface.json  不动（--no-bump）')
    else:
        log('  将改    :  interface.json  不动（已是 %s）' % version)

    if args.dry_run:
        log('[dry-run] 已打印计划，未执行任何写入')
        return 0

    # ---- 3. 只校验 ----
    if args.verify:
        if not os.path.exists(out):
            log('找不到 zip：%s' % out)
            return 2
        return 0 if verify(out, version) else 1

    # ---- 4. 改动前确认 ----
    if will_bump and not confirm('将 interface.json 从 %s 改为 %s 并开始打包？' % (cur_v, version)):
        log('已取消')
        return 1

    # ---- 5. 写盘 ----
    if will_bump:
        old, new = bump_interface(BASE, version)
        log('[0] interface.json: %s -> %s' % (old, new))
    else:
        log('[0] interface.json: 保持 %s' % version)

    # ---- 6. 打包 + 校验 ----
    build(BASE, out, version)
    if not args.no_verify:
        ok = verify(out, version)
    else:
        ok = True

    if ok:
        log('')
        log('下一步：')
        log('  git add -A && git commit -m "%s" && git push' % version)
        log('  把 %s 上传到 GitHub Release 的 assets（**不要改文件名**）' % os.path.basename(out))
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
