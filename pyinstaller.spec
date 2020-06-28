# -*- mode: python -*-
block_cipher = None
import imp
import os
import sys
import shutil

# On macOS, we always show the console to prevent the double-dock bug (although the OS does not actually show the console).
# See https://github.com/Tribler/tribler/issues/3817
show_console = os.environ.get('SHOW_CONSOLE', '0') == '1'
if sys.platform == 'darwin':
    show_console = True

excluded_libs = ['wx', 'bitcoinlib', 'PyQt4', 'FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter', 'matplotlib']

# Pony dependencies; each packages need to be added separatedly; added as hidden import
pony_deps = ['pony', 'pony.orm', 'pony.orm.dbproviders', 'pony.orm.dbproviders.sqlite']
# Hidden imports
hiddenimports = [
    'csv',
    'ecdsa',
    'pyaes',
    'scrypt', '_scrypt',
    'sqlalchemy', 'sqlalchemy.ext.baked', 'sqlalchemy.ext.declarative',
    'requests',
    'PyQt5.QtTest',
    'pyqtgraph'] + pony_deps,


sys.modules['FixTk'] = None
a = Analysis(['main.py'],
             pathex=[''],
             binaries=None,
             datas=None,
             hiddenimports=['csv', 'ecdsa', 'pyaes', 'scrypt', '_scrypt', 'sqlalchemy', 'sqlalchemy.ext.baked', 'sqlalchemy.ext.declarative', 'requests', 'PyQt5.QtTest', 'pyqtgraph'] + pony_deps,
             hookspath=[],
             runtime_hooks=[],
             excludes=excluded_libs,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# Add libsodium.dylib on OS X
if sys.platform == 'darwin':
    a.binaries = a.binaries - TOC([('/usr/local/lib/libsodium.so', None, None),])
    a.binaries = a.binaries + TOC([('libsodium.dylib', '/usr/local/lib/libsodium.dylib', None),])

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='tribler',
          debug=True,
          strip=False,
          upx=True,
          console=show_console,
          icon='build/win/resources/tribler.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='tribler')

app = BUNDLE(coll,
             name='tribler.app',
             icon='resources/tribler.icns',
             bundle_identifier='nl.tudelft.tribler',
             info_plist={'NSHighResolutionCapable': 'True', 'CFBundleInfoDictionaryVersion': 1.0, 'CFBundleVersion': "1.0", 'CFBundleShortVersionString': "1.0"},
             console=show_console)

# Replace the Info.plist file on MacOS
if sys.platform == 'darwin':
    shutil.copy('resources/Info.plist', 'dist/Tribler.app/Contents/Info.plist')
