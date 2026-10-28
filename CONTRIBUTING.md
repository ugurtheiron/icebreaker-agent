# Contributing

Thanks for taking the time to look at this project. Bug reports, fixes and small improvements are welcome.

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) first. To report a security problem, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Before you start

- For anything larger than a small fix, open an issue first so we can agree on the direction before you spend time on it.
- Check the **Known limitations** section of the [README](README.md#known-limitations). Some things are deliberate, for example the pinned LangChain 0.3 dependency line.
- Tests never call a paid or networked service. Please keep it that way: replace HTTP clients, LLMs and Firecrawl with fakes.

## Set up

You need Python 3.12 (CI uses 3.12). The commands below are the same as the README Quickstart.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env             # only needed to run the scripts, not the tests
```

## Check your change

Run both commands before you push. They are the same two steps the [CI workflow](.github/workflows/ci.yml) runs.

```bash
ruff check .
pytest
```

- New behavior needs a test in `tests/`. A bug fix needs a test that fails without the fix.
- Imports are sorted by ruff (`I` rules); `ruff check . --fix` fixes most findings.
- Follow `.editorconfig`: UTF-8, LF line endings, 4 spaces for Python, 2 for JSON, YAML and TOML.

## Dependencies

Versions in `requirements.txt` are pinned on purpose because the code was written against them. Please do not bump them in an unrelated pull request. Dependabot opens grouped update pull requests every week; if one of them fails CI, the fix goes into that pull request.

## Commit messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short summary in the imperative mood>
```

Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `ci`, `chore`. Keep one logical change per commit.

## Pull requests

1. Fork the repository and create a branch from `main` (for example `fix/parser-empty-category`).
2. Keep the pull request small and focused. Do not mix formatting changes with behavior changes.
3. Fill in the pull request template: what changed, why, and how you tested it.
4. Make sure CI is green. A maintainer reviews the change and may ask for edits.

## License of contributions

By contributing you agree that your contribution is released under the project's [MIT License](LICENSE). Files that derive from the original course code stay under the Apache License 2.0 (see [NOTICE](NOTICE)); if you change one of them, keep its header and add a line describing your change.
