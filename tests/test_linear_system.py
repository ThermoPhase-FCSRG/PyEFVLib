import importlib

import numpy as np
import pytest

from PyEFVLib import LinearSystem, LinearSystemCSR
from conftest import readMesh

linearSystemModule = importlib.import_module("PyEFVLib.LinearSystem")


def assembleLaplacian(system, grid):
	for element in grid.elements:
		for innerFace in element.innerFaces:
			backward, forward = innerFace.getNeighborVertices()
			coefficients = innerFace.area.getCoordinates()[:grid.dimension] @ innerFace.globalDerivatives
			for local, vertex in enumerate(element.vertices):
				system.addValueToMatrix(backward.handle, vertex.handle, coefficients[local])
				system.addValueToMatrix(forward.handle, vertex.handle, -coefficients[local])


def test_csr_and_dense_systems_match():
	grid = readMesh("2D/3x3 tri.msh")
	dense = LinearSystem(grid.stencil, 1)
	sparse = LinearSystemCSR(grid.stencil, 1)
	for system in (dense, sparse):
		system.initialize()
		assembleLaplacian(system, grid)
		system.matZeroRow(0, 1.0)

	sparseMatrix = sparse.getDense()
	assert isinstance(sparseMatrix, np.ndarray) and not isinstance(sparseMatrix, np.matrix)
	np.testing.assert_allclose(sparseMatrix, dense.getDense(), atol=1e-12)
	np.testing.assert_allclose(sparseMatrix[1:].sum(axis=1), 0.0, atol=1e-12)


def test_csr_rejects_entries_outside_the_stencil():
	system = LinearSystemCSR([[0, 1], [0, 1], [2]], 1)
	system.initialize()
	with pytest.raises(ValueError, match=r"\(0, 2\)"):
		system.addValueToMatrix(0, 2, 1.0)


def test_petsc_backend_requires_petsc4py(monkeypatch):
	monkeypatch.setattr(linearSystemModule, "PETSc", None)
	with pytest.raises(ImportError, match="petsc4py"):
		LinearSystemCSR([[0]], 1, PETSc_backend=True)
