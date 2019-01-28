from setuptools import setup

pack_extensions = {
    'base': True,
    'home': True,
    'proxy': True
}

include_packages = ['qpod.%s' % x for x in pack_extensions.keys() if pack_extensions[x]]
print("Pack extensions: %s." % str(include_packages))

include_packages_data = {
    'qpod': [k.replace('.', '/') + '/static/*' for k in pack_extensions]
}
print(include_packages_data)

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='qpod-hub',
    version='0.0.1',
    author='QPod',
    url='https://github.com/QPod',
    license='BSD',
    
    packages=['qpod'],  # find_packages(include=include_packages),
    include_package_data=True,
    package_data=include_packages_data,
    platforms='Linux, Mac OS X, Windows',
    zip_safe=False,
    install_requires=[
        'jinja2',
        'tornado',
        'aiohttp',
        'simpervisor'
    ],

    description='QPod Hub',
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
        ('etc/jupyter/jupyter_notebook_config.d', ['qpod/base/etc/qpod_portal-serverextension.json']),
        ('etc/jupyter/nbconfig/notebook.d', ['qpod/base/etc/qpod_portal-nbextension.json'])
    ],
    entry_points={
        'console_scripts': [
            'qpod = qpod_hub:main',
        ]
    },
)
