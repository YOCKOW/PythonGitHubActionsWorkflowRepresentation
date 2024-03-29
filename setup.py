from setuptools import setup, find_packages

setup(
    name='GitHub Actions Workflow Representation',
    version='0.9.2',
    description='Workflow representation for GitHub Actions.',
    long_description='See README.md',
    author='YOCKOW',
    url='https://github.com/YOCKOW/PythonGitHubActionsWorkflowRepresentation',
    license='MIT',
    packages=find_packages(exclude=('workflow_tests', 'docs')),
    test_suite='workflow_tests'
)