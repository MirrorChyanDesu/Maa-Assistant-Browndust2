# -*- coding: utf-8 -*-
"""
BD2MAA 发布包构建工具（通用版）

用法：
    python tools/build_release_zip.py                 # 版本号取自 HEAD 的 interface.json
    python tools/build_release_zip.py v26.09.5        # 显式指定版本号
    python tools/build_release_zip.py --out D:\\x.zip  # 指定输出路径
    python tools/build_release_zip.py --verify        # 只校验已有 zip
    python tools/build_release_zip.py --no-verify     # 只构建不校验

必须保持的约定：
  1. 直接读磁盘 → **未提交的改动也会进包**（所以发版前先确认工作区状态）
  2. 包内 interface.json 的 version 强制写成目标版本号；**本地文件不动**
     （本地常驻旧版本号，方便继续测试更新流程）
  3. 排除 config/ → MXU 首次启动自动生成默认实例，避免覆盖用户已有配置
  4. 排除 MaaBd2.lnk → 写死路径的快捷方式在别人机器上无效，首次启动自动重建
  5. 排除 updater_cache.json / cache / debug / updates → 运行期产物
  6. 中文文件名必须带 UTF-8 标志位（0x800），否则 Windows 解压乱码
  7. zip 内条目用固定时间戳 → 同一天重复构建得到完全相同的字节（可复现）
"""
import os, sys, json, time, zipfile, hashlib, argparse, subprocess

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


def log(msg):
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()


def head_version(base):
    """读 HEAD 版 interface.json 的版本号（仓库里的发布标记）"""
    try:
        raw = subprocess.check_output(
            ['git', '-C', base, 'show', 'HEAD:interface.json'], stderr=subprocess.DEVNULL)
        return json.loads(raw.decode('utf-8-sig')).get('version')
    except Exception:
        return None


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
    files = collect(base)
    log('[1] 待打包文件 = %d' % len(files))

    # 包内 interface.json：字节级替换版本号，保留原编码/BOM
    with open(os.path.join(base, 'interface.json'), 'rb') as f:
        wdata = f.read()
    marker = b'"version": "'
    i = wdata.find(marker)
    if i < 0:
        log('[!] 在 interface.json 中找不到 version 字段')
        packed = wdata
    else:
        j = wdata.find(b'"', i + len(marker))
        packed = wdata[:i + len(marker)] + version.encode() + wdata[j:]
        log('[2] 包内 interface.json version -> %s（本地文件不动）' % version)

    if os.path.exists(out_path):
        os.remove(out_path)
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)

    dt = time.localtime()[:6]          # 固定时间戳：同一天构建结果一致
    raw = 0
    t0 = time.time()
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for full, rel in files:
            data = packed if rel == 'interface.json' else open(full, 'rb').read()
            zi = zipfile.ZipInfo(rel, date_time=dt)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
            raw += len(data)

    size = os.path.getsize(out_path)
    log('[3] 原始 %d 字节 -> zip %d 字节 (%.2f MiB)  用时 %.1fs'
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
    ap.add_argument('version', nargs='?', help='目标版本号，如 v26.09.5；默认取 HEAD interface.json')
    ap.add_argument('--out', help='输出 zip 路径，默认 updates/MABd2<version>.zip')
    ap.add_argument('--verify', action='store_true', help='只校验已有 zip')
    ap.add_argument('--no-verify', action='store_true', help='只构建不校验')
    args = ap.parse_args()

    version = args.version or head_version(BASE)
    if not version:
        log('无法确定版本号：请显式传入，例如 v26.09.5')
        return 2
    if not version.startswith('v'):
        version = 'v' + version

    out = args.out or os.path.join(BASE, 'updates', 'MABd2%s.zip' % version)

    if args.verify:
        return 0 if verify(out, version) else 1

    build(BASE, out, version)
    if not args.no_verify:
        return 0 if verify(out, version) else 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
