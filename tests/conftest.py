import os

import pytest

import PyEFVLib

MESHES = os.path.join(os.path.dirname(__file__), os.path.pardir, "meshes", "msh")

MESH_FILES = [
	"2D/3x3 tri.msh",
	"2D/3x3.msh",
	"3D/Tetras.msh",
	"3D/Hexas.msh",
	"3D/Prisms.msh",
	"3D/Pyrams.msh",
]


def readMesh(relativePath):
	return PyEFVLib.read(os.path.join(MESHES, *relativePath.split("/")))


@pytest.fixture(params=MESH_FILES)
def grid(request):
	return readMesh(request.param)
