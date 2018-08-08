# -*- mode: python -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=[
                 'C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x86',
                 'D:\\charaswapper',
                 'C:\\Users\\rebel1324\\AppData\\Roaming\\Python\\Python36\\site-packages',
                 'C:\\Users\\rebel1324\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyQt5'
                 ],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon="iconia.ico" )
