# hide_marker.ps1
# ---------------------------------------------------------------------------
# Guard that keeps MXU's garbled runtime marker invisible.
#
# Background: when MXU.exe is started it writes a 0-byte marker file whose
# name is the UTF-8 text "启动" mis-encoded through the system ANSI/GBK code
# page (it shows up as mojibake, e.g. 鍚?姩). The file is harmless but ugly,
# and there is no known launch-side way to stop MXU from writing it.
#
# This script therefore *hides* it instead of preventing it:
#   * delete it whenever it appears; if the handle is still held by MXU and
#     the delete fails, force the Hidden + System attributes so Explorer
#     (default settings) never shows it.
# Combined with the .gitignore rule the marker can never reach the git repo.
#
# Usage:  powershell -NoProfile -ExecutionPolicy Bypass -File hide_marker.ps1 -Root <project root> [-Seconds 120]
# ---------------------------------------------------------------------------
param(
    [string]$Root,
    [int]$Seconds = 120
)

$ErrorActionPreference = 'SilentlyContinue'

if (-not $Root) {
    $Root = Split-Path -Parent $PSScriptRoot
}

# Signature of the marker name:  U+945A  U+E21A  U+59E9
$exact = [string][char]0x945A + [char]0xE21A + [char]0x59E9
$c1 = [char]0x945A
$c3 = [char]0x59E9

function Test-MarkerName([string]$name) {
    if ($name -eq $exact) { return $true }
    if ($name.Contains($c1)) { return $true }
    if ($name.Contains($c3)) { return $true }
    return $false
}

$deadline = (Get-Date).AddSeconds($Seconds)

while ((Get-Date) -lt $deadline) {
    $items = Get-ChildItem -LiteralPath $Root -Force -File -ErrorAction SilentlyContinue
    foreach ($f in $items) {
        if (-not (Test-MarkerName $f.Name)) { continue }

        # 1) try to remove it outright (cleanest: the user never sees it)
        $deleted = $false
        try {
            Remove-Item -LiteralPath $f.FullName -Force -ErrorAction Stop
            $deleted = $true
        } catch { }

        # 2) still there (handle held by MXU) -> hide it
        if (-not $deleted) {
            try {
                $fi = Get-Item -LiteralPath $f.FullName -Force -ErrorAction Stop
                $fi.Attributes = $fi.Attributes -bor [System.IO.FileAttributes]::Hidden -bor [System.IO.FileAttributes]::System
            } catch { }
        }
    }
    Start-Sleep -Milliseconds 250
}
