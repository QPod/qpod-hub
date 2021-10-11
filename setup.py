from setuptools import setup
from datetime import datetime

now = datetime.now()

pack_extensions = {
    'base': True,
    'home': True,
    'proxy': True
}

include_packages = ['qpod.%s' % x for x in pack_extensions if pack_extensions[x]]
print("Pack extensions: %s." % str(include_packages))

include_packages_data = {
    'qpod': [k.replace('.', '/') + '/static/*' for k in pack_extensions]
}
print(include_packages_data)

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='qpod-hub',
    version='%s.%s.%s' % (now.year, now.month, now.day),
    author='QPod',
    author_email='45032326+QPod0@users.noreply.github.com',
    url='https://github.com/QPod/qpod-hub',
    license='BSD',

    packages=['qpod'],  # find_packages(include=include_packages),
    include_package_data=True,
    package_data=include_packages_data,
    platforms='Linux, Mac OS X, Windows',
    zip_safe=False,
    install_requires=[
        'jupyter_server_proxy'
    ],

    description='A hub portal UI and proxy service for QPod.',
    long_description=long_description,
    long_description_content_type="text/markdown",

    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    data_files=[
        ('etc/jupyter/jupyter_server_config.d', ['qpod/base/etc/qpod_hub-jpserverextension.json']),
        ('etc/jupyter/jupyter_notebook_config.d', ['qpod/base/etc/qpod_hub-nbserverextension.json']),
        ('etc/jupyter/nbconfig/tree.d', ['qpod/base/etc/qpod_hub-nbextension.json'])
    ],
    entry_points={
        'console_scripts': [
            'qpod = qpod:main',
        ]
    },
)
