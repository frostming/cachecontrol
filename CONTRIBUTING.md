# Contribute to CacheYou

## Project Management

The CacheYou project is managed by [PDM](https://pdm.fming.dev/). You need to install it first:

```bash
pipx install pdm
```

For other installation methods, please refer to [PDM's documentation](https://pdm.fming.dev/#installation).

After the installation, initialize the plugins and install the dependencies:

```bash
pdm install --plugins
pdm install
```

## Run the Tests

We use [tox](https://tox.readthedocs.io/en/latest/) to run the tests. You can run the tests by:

```bash
pdm run tox
```

View the available environments and pick one to run:

```bash
pdm run tox -l
```

You can also run `pytest` directly in the project environment by:

```bash
pdm test
```

## Watch the Docs

Run the following command to start a live-reloading docs server:

```bash
pdm docs
```

## Code Style and Linters

We use [Black](https://github.com/psf/black) to format the code and [Ruff](https://github.com/charliermarsh/ruff) as the linter.
They are all integrated into [pre-commit](https://pre-commit.com/). You can enable it by:

```bash
pre-commit install
```

and run the checks by:

```bash
pre-commit run --all-files
```

## Create a Release

Before releasing, make sure you add the change summary to the `docs/release_notes.rst` file.
Then, run the following command to create a release and corresponding tag commit:

```bash
pdm release
```

For simplicity, we use a version schema of `YY.BUILD_NUMBER`, where `YY` is the last two digits of the current year and `BUILD_NUMBER` increases by one for each release.
