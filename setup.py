from setuptools import setup, find_packages

setup(
    name='verbs_counter',
    version='1.0',
    packages=find_packages(),
	install_requires=[
		'nltk ~= 3.4',
    ]
)