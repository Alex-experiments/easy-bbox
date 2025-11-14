# Contributing

Contribution are welcome! Please feel free to submit a Pull Request. Here are the steps to contribute to the project:

## Prerequisites

- Python 3.9+

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/Alex-experiments/easy-bbox.git
cd easy-bbox

# 2. Set-up the venv
uv venv
uv pip install -e .[dev]
```

## Testing

Run tests using pytest:

```bash
pytest
```

## Code Quality

This project uses pre-commit hooks for code quality:

```bash
pre-commit install
```

This will set up the git hook scripts. Now pre-commit will run automatically on git commit.

## Documentation

Documentation is build automatically when the main branch is updated. You can generate it locally using Sphinx:

```bash
cd docs
make html
```

But you might need to install these packages beforehand:
```bash
pip install sphinx sphinx_rtd_theme sphinx-autodoc-typehints
```