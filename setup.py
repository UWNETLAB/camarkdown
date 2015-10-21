from setuptools import setup
setup(name='caMarkdown',
    version='0.0.1',
    author="Reid McIlroy-Young, John McLevey",
    author_email = "rmcilroy@uwaterloo.ca, john.mclevey@uwaterloo.ca",
    packages=['caMarkdown'],
    test_suite='caMarkdown.tests',
    entry_points={'console_scripts': [
              'camd = caMarkdown.bin:cli',
          ]},
)
