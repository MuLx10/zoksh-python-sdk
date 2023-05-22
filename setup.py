from setuptools import setup, find_packages

setup(
    name='zoksh',
    version='1.0.0',
    description='Description of your package',
    author='Mehul Nirala',
    author_email='your@email.com',
    packages=find_packages(),
    install_requires=[
        "urllib3",
        "requests"
    ],
)
