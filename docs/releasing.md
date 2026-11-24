# Release and conda-forge preparation

The proposed next version is 1.1.0. No external release or upload has been performed. Pixi manages development environments; conda-forge publishes packages through reviewed feedstocks, so the conda recipe is kept in the feedstock and not in this repository.

1. Run the checks in `development.md` and review the changes. Confirm the version and who will maintain the conda-forge feedstock.
2. Create a release tag and publish the package on PyPI (coordinate with the current owners of the `PyEFVLib` PyPI project).
3. Submit a recipe to [`conda-forge/staged-recipes`](https://github.com/conda-forge/staged-recipes) (or update the existing feedstock, if one exists). The recipe should point to the released source archive and its real checksum, for example:

```yaml
source:
  url: https://pypi.org/packages/source/p/pyefvlib/pyefvlib-{{ version }}.tar.gz
  sha256: <SHA256 of the released archive>
```

Run-time requirements must match `[project.dependencies]` in `pyproject.toml`.

4. Publication happens after the conda-forge review and CI, not through a Pixi command.

Follow the [official conda-forge contribution process](https://conda-forge.org/docs/maintainer/adding_pkgs/).
