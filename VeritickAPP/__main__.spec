# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
    ('vtKinterClass.py','.'),
    ('__init__.py','.'),
    ('notes_for_fillin.py','.'),
    ('popUpBox.py','.'),
    ('ticket_search.py','.'),
    ('veriTableClass.py','.'),
    ('veritick.py','.'),
    ('doorKey.py','.'),
    (r'c:\users\mbrown\desktop\gca-coding\projects\python\html_gui_py39\venv\lib\site-packages\customtkinter','customtkinter'),
    (r'C:\Users\Mbrown\Desktop\GCA-Coding\Projects\Python\html_gui_py39\venv\Lib\site-packages\connectpyse','connectpyse'),
    (r'C:\Users\Mbrown\Desktop\GCA-Coding\Projects\Python\html_gui_py39\venv\Lib\site-packages\fuzzywuzzy','fuzzywuzzy')
     
    ]

hidden_added_files = [
    "tkinter",
    "customtkinter",
    "loguru",
    "xlwings",
    "fernet",
    "fuzzywuzzy"

]

a = Analysis(
    ['__main__.py'],
    pathex=[],
    binaries=[],
    datas= added_files,
    hiddenimports= hidden_added_files,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='__main__',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='__main__',
)
