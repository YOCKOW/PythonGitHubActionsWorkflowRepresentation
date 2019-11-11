from setuptools import setup, find_packages

setup(
    name='GitHub Actions Workflow Representation',
    version='0.1.0-dev',
    description='Workflow representation for GitHub Actions.',
    long_description='See README.md',
    author='YOCKOW',
    url='https://github.com/YOCKOW/PythonGitHubActionsWorkflowRepresentation',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)