# OpenEnvoy Coding Test

## Prerequisites

- python 3.9
- pipenv

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

1. Clone the repository:

```bash
git clone git@github.com:dinkan-github/open-envoy-test.git
```

2. Change into the project directory:

```bash
cd open-envoy-test
```


3. Install the dependencies:

```bash
pipenv install
```

4. Run the main file:

```bash
python main.py
```

4. To run the tests:

```bash
pytest
```


You will be prompted to enter the directory or file path. If it is a directory, you will also be prompted to enter the language (java or python). The program will process the files in the specified directory or the specified file, depending on the input.

Some test files (for python and java) are provided in `sample_test_files` folder


## Features

* Processes file in the specified directory or the specified file
* Supports java and python languages
