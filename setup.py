from setuptools import setup

from caMarkdown import version

setup(name='caMarkdown',
    version=version,
    author="Reid McIlroy-Young, John McLevey",
    author_email = "rmcilroy@uwaterloo.ca, john.mclevey@uwaterloo.ca",
    install_requires= ['dulwich', 'pyyaml'],
    packages=['caMarkdown'],
    test_suite='caMarkdown.tests',
    entry_points={'console_scripts': [
              'camd = caMarkdown.commandline:cli',
          ]},
)
