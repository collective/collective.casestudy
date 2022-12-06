"""Installer for the collective.casestudy package."""
from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
{Path("CHANGELOG.md").read_text()}\n
"""

setup(
    name="collective.casestudy",
    version="1.0.0a1",
    description="Case Study content type for Plone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Plone Community",
    author_email="ericof@plone.org",
    url="https://github.com/collective/collective.casestudy",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/collective.casestudy",
        "Source": "https://github.com/collective/collective.casestudy",
        "Tracker": "https://github.com/collective/collective.casestudy/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=True,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "Plone",
        "plone.api",
    ],
    extras_require={
        "test": [
            "gocept.pytestlayer",
            "zest.releaser[recommended]",
            "plone.app.testing>=7.0.0a3",
            "plone.restapi[test]",
            "pytest",
            "pytest-cov",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.casestudy.locales.update:update_locale
    """,
)
