from setuptools import setup
setup(name='metaknowledge',
    version='0.0.1',
    author="Reid McIlroy-Young, John McLevey",
    author_email = "rmcilroy@uwaterloo.ca, john.mclevey@uwaterloo.ca",
    packages=['caMarkdown', 'caMarkdown.tests'],
    test_suite='caMarkdown.tests',
)
