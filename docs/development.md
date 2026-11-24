# Development

PyEFVLib requires Python 3.11 or newer. The development environment is managed with [Pixi](https://pixi.prefix.dev/latest/installation/). From the repository root, run:

```sh
pixi install
pixi run check
pixi run -e minimum check
pixi run build
pixi run check-dist
```

Commit `pixi.lock` with dependency changes. It resolves Windows and Linux environments. The default environment uses current dependencies; `minimum` exercises the supported lower bounds. A Windows local run does not validate Linux execution.

NumPy, SciPy, meshio, h5py and xmltodict are runtime dependencies. pandas is not required by the core library. Matplotlib supports examples; PETSc remains optional and is not tested in the default environment.
The Pixi development environment also includes pandas for historical converters and research scripts.

## Using a local checkout from another Pixi project

To develop PyEFVLib together with a project that depends on it, add the checkout as an editable dependency of that project:

```toml
[pypi-dependencies]
PyEFVLib = { path = "../PyEFVLib", editable = true }
```

For a pyproject.toml manifest, use `[tool.pixi.pypi-dependencies]`. Do not keep another entry for an older PyEFVLib. After release, pin a released version instead of relying on a sibling directory.

Both `propertyData.get(region_handle, property_name)` and `propertyData.get(property_name, handle=region_handle)` are supported, so applications written against either interface keep working.

Tests cover control-volume conservation, linear-gradient reconstruction, property access, expressions, dense/CSR systems and meshio output. Compilation checks do not prove numerical correctness of every research script in `workspace`; these may require additional inputs and dependencies.
