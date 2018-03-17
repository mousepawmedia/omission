
NAME = 'Omission'
import os
from os.path import join
from kivy.utils import platform

if platform == 'win':
    from kivy.deps import sdl2, glew
else:
    glew = sdl2 = None


IS_LINUX = os.name == 'posix' and os.uname()[0] == 'Linux'
if IS_LINUX:
    from PyInstaller.depend import dylib
    dylib._unix_excludes.update({
        r'.*nvidia.*': 1,
        r'.*libdrm.*': 1,
  r'.*hashlib.*': 1,
        })

    dylib.exclude_list = dylib.ExcludeList()

from kivy.tools.packaging.pyinstaller_hooks import get_hooks

binexcludes = [
     'gobject', 'gio', 'gtk', 'gi', 'wx', 'twisted', 'curses',
     'gstreamer', 'libffi', 'libglib', 'libmikmod', 'libflac', 'libvorbis',
     'libgstreamer', 'libvorbisfile', 'include', 'libstdc++.so.6',
     'gst_plugins', 'liblapack', 'pygame', 'lib/', 'include', 'kivy_install/modules',
]

a = Analysis(['omission/__main__.py'],
             pathex=['.'],
             hiddenimports=['numpy.core.multiarray'],
             excludes=binexcludes,
             **get_hooks())

pyz = PYZ(a.pure)

name = '%s%s' % (NAME, '.exe' if os.name == 'nt' else '')

def not_in(x, binexcludes):
    return not any(y in x.lower() for y in binexcludes)

a.binaries = [
    x for x in a.binaries
    if not_in(x[0], binexcludes)
]

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=name,
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon=join('deploy_windows', 'omission.ico'))

with open('blacklist.txt') as f:
    excludes = [x.strip() for x in f.readlines()]

coll = COLLECT(exe,
               Tree('.', excludes=excludes),
               a.binaries,
               a.zipfiles,
               a.datas,
               *([Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)] if sdl2 else []),
               strip=None,
               upx=True,
               name=NAME)
