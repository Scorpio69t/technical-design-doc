# Contributing

Thank you for improving `technical-design-doc`. Contributions should make the skill more accurate, portable, readable, or easier to validate without turning `SKILL.md` into an all-purpose prompt.

## Before opening an issue

- Use GitHub Discussions for installation questions and general usage help.
- Search existing issues before reporting a bug or proposing a change.
- Do not disclose vulnerabilities or prompt-injection concerns publicly; follow `SECURITY.md`.

## Development setup

Python 3.9 or newer is sufficient. The repository has no third-party runtime or test dependencies.

```bash
git clone https://github.com/Scorpio69t/technical-design-doc.git
cd technical-design-doc
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
```

## Change guidelines

- Preserve the distinction between architecture models, runtime interactions, and business flows.
- Keep `SKILL.md` focused; move detailed guidance to `references/` and reusable content to `assets/`.
- Do not add product-specific architecture assumptions to the generic templates.
- Keep examples fictitious and remove credentials, internal hosts, personal data, and proprietary names.
- Update `VERSION`, `CHANGELOG.md`, and `SKILL.md` metadata together for a release.
- Add or update tests when changing Python tooling.
- Prefer standard-library Python so the skill remains portable.

## Validate a change

Run all checks from the repository root:

```bash
python scripts/validate_skill.py .
python scripts/lint_design_doc.py examples/sample-detailed-design.md --strict
python -m unittest discover -s tests -v
python scripts/package_skill.py --output-dir dist
```

Open the generated ZIP and confirm it contains one top-level `technical-design-doc/` directory and no cache, test, CI, or editor files.

## Pull requests

Keep pull requests focused. Explain the problem, the design choice, affected skill behavior, and validation performed. Screenshots are useful for rendered diagram changes, but diagram source must remain reviewable in the repository.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
