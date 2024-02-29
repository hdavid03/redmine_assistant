from setuptools import find_packages
from setuptools import setup

setup(
    name="redmine_assistant",
    include_package_data=True,
    author="David Hajdu",
    author_email="hdavid998@gmail.com",
    description="Python CLI tool for Redmine REST API with useful features",
    url="https://github.com/hdavid03/redmine_assistant",

    project_urls={
        "Bug Tracker": "https://github.com/hdavid03/redmine_assistant/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    package_dir={'': "src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
)
