from setuptools import setup, find_packages
from setuptools.command.install import install
import glob
import os

VERSION = "0.5.1"

data_files = [
        ('/usr/share/applications/', ['resources/qomui.desktop']),
        ('/etc/systemd/system/', ['resources/qomui.service']),
        ('/etc/dbus-1/system.d/', ['resources/org.qomui.service.conf']),
        ('/usr/share/icons/hicolor/scalable/apps/', ['resources/qomui.svg',
                                                     'resources/qomui_off.svg']),
        ('/usr/share/qomui/', [
                                'resources/Airvpn_config',
                                'resources/PIA_config',    
                                'resources/default_config.json',
                                'resources/firewall_default.json',
                                'resources/Mullvad_config',
                                'resources/ssl_config',
                                'resources/qomui.png',
                                'resources/hop.sh',
                                'resources/hop_down.sh',
                                'resources/VERSION']
                            ),
        ('/usr/share/qomui/flags/', glob.glob('resources/flags/*'))
        ]

def post_install(i):
    try:
        for f in data_files:
            for o in f[1]:
                fmod = os.path.join(f[0], os.path.basename(o))
                if os.path.splitext(fmod)[1] == ".sh":
                    os.chmod(fmod, 0o774)
                else:
                    os.chmod(fmod, 0o664)
    
    except FileNotFoundError:
        pass
    

class CustomInstall(install):
    def run(self):
        install.run(self)
        self.execute(post_install, (self.install_lib,), msg="Running post-install script to fix file permissions")


setup(name="qomui",
      version=VERSION,
      packages=['qomui'],
      include_package_data=True,
      install_requires=[
        'beautifulsoup4',
        'pexpect',
        'psutil',
        'pycountry',
        'requests',
        'lxml'
        ],
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Security',
        ],
      data_files = data_files,
      license='GPLv3+',
      entry_points={
        'gui_scripts': [
            'qomui-gui=qomui.qomui_gui:main' 
            ],
        'console_scripts': [
            'qomui-service=qomui.qomui_service:main'
            ]},
      cmdclass={'install': CustomInstall}
      )

    
    
    
