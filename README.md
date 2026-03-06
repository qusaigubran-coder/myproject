# myproject

A reusable Python project template for building:

- CLI tools
- FastAPI services
- Webhook consumers
- automation scripts

This template includes:

- `src/` layout
- installable Python package
- CLI entry point
- FastAPI app
- webhook signature verification
- unit tests with `pytest`
- linting and formatting with `ruff`
- type checking with `mypy`
- `pre-commit` hooks
- GitHub Actions CI
- Dev Container support

---

## Project Structure

```text
myproject
├── .devcontainer/
│   └── devcontainer.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── api.py
│       ├── cli.py
│       ├── config.py
│       ├── logging_config.py
│       ├── main.py
│       └── webhook.py
├── tests/
│   ├── test_main.py
│   └── test_webhook.py
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── pyproject.toml
└── README.md
