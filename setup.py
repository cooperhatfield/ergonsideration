import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ergonsideration',
    version='0.0.1',
    author='Cooper Hatfield',
    author_email='cooperhatfield@yahoo.ca',
    description='Ergonomics reminder that\'s considerate of your life!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cooperhatfield/ergonsideration',
    project_urls = {
        "Bug Tracker": "https://github.com/cooperhatfield/ergonsideration/issues"
    },
    license='',
    packages=['ergonsideration'],
    install_requires=['sched', 'winsdk', 'importlib', 'glob', 'json'],
)