# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew

block_cipher = None

added_files = [
	('omission/resources/audio/*.ogg','omission/resources/audio'),
	('omission/resources/content/*.txt','omission/resources/content'),
	('omission/resources/font','omission/resources/font'),
	('omission/resources/icons/*.png','omission/resources/icons')
]

a = Analysis(['omission\\__main__.py'],
             pathex=['C:\\Users\\Jason C. McDonald\\repos\\omission'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='omission',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='deploy_windows\\omission.ico')
