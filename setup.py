import os
import re

from distutils import dir_util
from setuptools import setup, find_packages


def requirements(file_name):
    with open(file_name) as requirements_file:
        return [req for req in map(
            lambda line: line.strip(),
            filter(
                lambda line: not line.startswith('#'),
                requirements_file.readlines()
            )
        )]


def get_property(prop):
    with open('botctl/__init__.py', 'r') as f:
        prop_regex = r'__{}__\s*=\s*[\'"](.+)[\'"]'.format(prop)
        return re.search(prop_regex, f.read(), re.MULTILINE).group(1)


def configure():
    from botctl.config import ConfigStore
    config_store = ConfigStore()
    config_store.setup()
    config_store.commit()


def install_manual():
    source_manpath = os.path.join(os.path.dirname(__file__), 'man')
    target_manpath = os.path.join(os.environ['HOME'], '.botctl/man')
    dir_util.copy_tree(source_manpath, target_manpath)


if __name__ == '__main__':
    package_name = get_property('name')
    setup(
        name=package_name,
        version=get_property('version'),
        url='https://github.com/wizeline/botctl',
        author=get_property('author'),
        author_email='diego.guzman@wizeline.com',
        description='Bots Platform CLI Control Tools',
        packages=find_packages(exclude=['tests']),
        include_package_data=True,
        zip_safe=False,
        classifiers=[
            'Development Status :: Development',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Programming Language :: Python 3.6.5',
            'Topic :: Utilities'
        ],
        test_require=requirements('test-requirements.txt'),
        install_requires=requirements('install-requirements.txt'),
        entry_points={
            'console_scripts': [
                'lsbot = botctl.lsbot:main',
                'mkadmin = botctl.mkadmin:main',
                'mkbot = botctl.mkbot:main',
                'rmadmin = botctl.rmadmin:main',
                'rmbot = botctl.rmbot:main',
                'showbot = botctl.showbot:main',
                'botctl = botctl.botctl:main',
                'botmod = botctl.botmod:main',
                'botusr = botctl.botusr:main',
                'readbot = botctl.readbot:main',
                'integration = botctl.integration:main'
            ]
        }
    )
    install_manual()
    configure()
