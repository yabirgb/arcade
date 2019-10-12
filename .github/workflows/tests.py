name: Python application

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v1
    - name: Set up Python 3.7
      uses: actions/setup-python@v1
      with:
        python-version: 3.7
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
        pipenv lock --requirements > requirements.txt
        pip install -r requirements.txt
    - name: Test with pytest
      run: |
        pip install pytest
        pytest tests/*.py
