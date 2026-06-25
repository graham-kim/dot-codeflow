# AGENTS.md

## Quick start
- Install dependencies: `pip install -r requirements.txt`.
- Run the shorthand parser: `python shortflow.py <filenames>`.
- Run the full parser: `python flow.py <filenames>`.
- Generate example input files: `python shortflow.py --gen-inputs <filenames>`.
- Run tests: `python run_tests.py` or `python -m unittest`.

## Important details
- The repository is a plain Python project; import modules from the root.
- `parsers` is a package; ensure `__init__.py` files exist.
- `shortflow.py` reads `categories.json` for category → DOT attribute mapping.
- `shortflow.py` expects lines like `< x ABC | label` where `x` is a category.
- `flow.py` supports clusters (`/@ name`), nodes (`- name`), links (`> name`, `< name`, `<> name`), attributes (`= key=value`), and ranksame (`@ name`).
- `pretty_print_with_global_attr` writes a temporary `temp.dot` and prints formatted graph; open `temp.dot` to view the graph.
- `pydot` requires Graphviz; ensure it is installed on the system.
- `categories.json` contains mapping such as `"r": "fillcolor="#FF9999"`. Be aware of typos (missing quotes, stray quotes). The parser uses the file as is.
- No CI or packaging config; run scripts directly.
- Tests use `unittest` in `tests/shortflow.py`; `run_tests.py` simply calls `unittest.main()`.

## Common pitfalls
- Forgetting to add the repository root to `PYTHONPATH` will cause `ModuleNotFoundError`.
- Using `shortflow.py` without `categories.json` will fail.
- `pydot` may raise errors if Graphviz is not available.
- Typos in `categories.json` may lead to incorrect DOT attributes.

---
This file is meant to guide agents and developers quickly to the essential commands and project structure. No additional generic advice is included.
