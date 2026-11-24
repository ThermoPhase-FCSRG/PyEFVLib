import numpy as np
import pytest


def test_control_volumes_fill_the_elements(grid):
	elementVolume = sum(element.volume for element in grid.elements)
	controlVolume = sum(vertex.volume for vertex in grid.vertices)
	assert controlVolume == pytest.approx(elementVolume)


def test_control_volume_surfaces_are_closed(grid):
	balance = np.zeros((grid.numberOfVertices, 3))
	for element in grid.elements:
		for innerFace in element.innerFaces:
			backward, forward = innerFace.getNeighborVertices()
			area = innerFace.area.getCoordinates()
			balance[backward.handle] += area
			balance[forward.handle] -= area
	for boundary in grid.boundaries:
		for facet in boundary.facets:
			for outerFace in facet.outerFaces:
				balance[outerFace.vertex.handle] += outerFace.area.getCoordinates()
	scale = max(vertex.volume for vertex in grid.vertices) ** ((grid.dimension - 1) / grid.dimension)
	assert np.abs(balance).max() < 1e-10 * max(scale, 1.0)


def test_linear_field_gradient_is_exact(grid):
	slope = np.array([2.0, -3.0, 0.5])[:grid.dimension]
	field = np.array([vertex.getCoordinates()[:grid.dimension] @ slope for vertex in grid.vertices])
	for element in grid.elements:
		values = field[[vertex.handle for vertex in element.vertices]]
		for innerFace in element.innerFaces:
			assert innerFace.globalDerivatives @ values == pytest.approx(slope)


def test_stencil_is_sorted_and_symmetric(grid):
	assert len(grid.stencil) == grid.numberOfVertices
	for handle, neighbors in enumerate(grid.stencil):
		assert neighbors == sorted(set(neighbors))
		assert handle in neighbors
		for neighbor in neighbors:
			assert handle in grid.stencil[neighbor]
