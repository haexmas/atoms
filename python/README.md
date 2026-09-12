# Python best practices

Behavior atom for Python projects.

- Atom id: `com.github.haexmas.atoms.python`
- Version: `0.1.0`
- Delivered atoms: `python.md` and `testing.md` under `atoms.behavior`

The atoms give coding agents a compact baseline for typing, explicit data
models, validation, exception handling, resource management, async code, and
Python testing. Project-specific conventions take precedence.

## Adopting

Add the molecule to a consumer's `.spaex.json` and pin the full commit SHA of
this publisher repository:

```json
{
  "source": "https://github.com/haexmas/atoms",
  "revision": "<full-40-char-sha>",
  "molecules": ["com.github.haexmas.atoms.python"]
}
```

Then run `spaex install`.

## Research basis

The guidance is based on the official
[Python typing documentation](https://docs.python.org/3/library/typing.html),
[asyncio documentation](https://docs.python.org/3/library/asyncio.html),
[PEP 8](https://peps.python.org/pep-0008/), and the Python Packaging User
Guide's guidance for
[`pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).
The consuming project's supported Python versions and configured tools remain
authoritative.

The testing guidance additionally follows Python's
[`unittest`](https://docs.python.org/3/library/unittest.html) documentation;
projects using another runner should keep that runner's discovery and fixture
conventions consistent.
