# -*- mode: python ; coding: utf-8 -*-
import os

# Get certifi cert data directory for bundling
import certifi
_certifi_dir = os.path.dirname(certifi.where())
_certifi_datas = [(_certifi_dir, 'certifi')]

a = Analysis(
    ['cli.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[
        ('youtube', 'youtube'),
        ('utils', 'utils'),
    ] + _certifi_datas,
    hiddenimports=[
        'youtube',
        'youtube.yt_subtitle_dl',
        'youtube.yt_metadata_dl',
        'utils',
        'utils.constant',
        'utils.utils',
        'yt_dlp',
        'yt_dlp.extractor',
        'yt_dlp.downloader',
        'yt_dlp.postprocessor',
        'dotenv',
        'asyncio',
        'certifi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['whisper', 'deepgram-sdk'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='yt-dl-subtitle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
