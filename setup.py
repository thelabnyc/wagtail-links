from setuptools import setup, find_packages

setup(
    name="wagtail-links",
    version="1.0.1",
    author="David Burke",
    author_email="david@thelabnyc.com",
    description="Wagtail links provides a consistent way to refer to links in a wagtail page",
    license="Apache License",
    keywords="django wagtail",
    url="https://gitlab.com/thelabnyc/wagtail-links",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=[
        'wagtail>=1.6.2',
    ]
)

