import os

import meshio
import numpy as np
import pytest

from PyEFVLib import MeshioSaver, XDMFReader
from conftest import readMesh


@pytest.mark.parametrize("extension", ["vtu", "cgns"])
def test_meshio_saver_writes_point_data(tmp_path, extension):
	grid = readMesh("2D/3x3.msh")
	field = np.array([vertex.x + 2.0 * vertex.y for vertex in grid.vertices])

	saver = MeshioSaver(grid, str(tmp_path), str(tmp_path), extension)
	saver.save("phi", field, 0.0)
	saver.finalize()

	assert os.path.isfile(saver.outputPath)
	if extension == "vtu":
		mesh = meshio.read(saver.outputPath)
		np.testing.assert_allclose(mesh.point_data["phi"], field)
		assert mesh.cells[0].type == "quad"
		assert len(mesh.cells[0].data) == len(grid.elements)


def test_xdmf_dimension_comes_from_the_cell_types():
	points = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
	mesh = meshio.Mesh(points, [("line", np.array([[0, 1]])), ("triangle", np.array([[0, 1, 2]]))])
	assert XDMFReader(".", "mesh.xdmf").getDimension(mesh) == 2


def test_xdmf_reads_meshio_cell_blocks_and_multi_block_tags():
	points = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [2.0, 0.0], [2.0, 1.0]])
	mesh = meshio.Mesh(
		points,
		[("triangle", np.array([[0, 1, 2], [0, 2, 3]])), ("quad", np.array([[1, 4, 5, 2]]))],
		cell_data={"region": [np.array([1, 1]), np.array([2])]},
	)
	reader = XDMFReader(".", "mesh.xdmf")

	assert reader.getEntityConnectivities(mesh) == [[0, 1, 2], [0, 2, 3], [1, 4, 5, 2]]
	assert reader.getRegionIndexes(mesh, "region") == [[0, 1], [2]]

	shapes = reader.updateShapes(reader.getShapes(), mesh, "region")
	assert shapes["triangle"] == [(1, [0, 1, 2]), (1, [0, 2, 3])]
	assert shapes["quadrilateral"] == [(2, [1, 4, 5, 2])]
