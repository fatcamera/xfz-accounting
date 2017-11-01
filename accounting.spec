# -*- mode: python -*-

block_cipher = None

a = Analysis(
    ['accounting.py'],
    pathex=[
      r'D:\Documents\develop\xfz-accounting',
      r'D:\Python35\Lib\site-packages\PyQt5\Qt\bin'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher)
             
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas,
    debug=False, strip=False, upx=False,
    name='accounting', console=False, icon='images/app.ico')
