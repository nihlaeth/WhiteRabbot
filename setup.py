from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='rabbot',
    version='0.0.1-dev',
    description='A Telegram bot to track schedule mutations',
    url='https://github.com/nihlaeth/WhiteRabbot',
    author='Tamara van Haarlem, Sietse Brouwer',
    author_email='nihlaeth@nihlaeth.com',
    license=license,
    packages=['rabbot'],
)
