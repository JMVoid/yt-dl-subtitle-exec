# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(
    ['cli.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[
        ('youtube', 'youtube'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'youtube',
        'youtube.yt_subtitle_dl',
        'youtube.yt_metadata_dl',
        'utils',
        'utils.constant',
        'utils.utils',
        'pytubefix',
        'dotenv',
        'asyncio',
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
