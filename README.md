# GitHub Actions Workflow Representaion in Python.

This package provides the representaion for GitHub Actions' Workflow  in python.  
Originally written for just a helper script of [Action-setup-swift](https://github.com/YOCKOW/Action-setup-swift).


# Usage

```python
from workflow import Workflow

workflow = Workflow({
  "name": "Some Workflow",
  "on": "push", 
  "jobs": {
    "job1": {
      "name": "Some Job",
      "runs-on": ["ubuntu-latest", "macOS-latest"],
      "steps": [
        "name": "Some Step",
        "run": "echo Hello"
      ]
    }
  }
})

print(workflow.yaml())
"""
name: Some Workflow
on: push
jobs:
  job1:
    name: Some Job
    runs-on:
      - ubuntu-latest
      - macOS-latest
    steps:
      - name: Some Step
        run: echo Hello
"""


```


# License
MIT License.  
See "LICENSE.txt" for more information.

