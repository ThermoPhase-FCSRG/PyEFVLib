import os

import numpy as np
import pytest

from PyEFVLib import NumericalSettings, ProblemData, PropertyData
from conftest import MESHES


def createProblemData(**kwargs):
	propertyData = PropertyData({"Body": {"Conductivity": 2.0, "Density": 3.0}})
	return ProblemData(
		meshFilePath=os.path.join(MESHES, "2D", "3x3.msh"),
		propertyData=propertyData,
		**kwargs,
	)


def test_output_path_and_numerical_settings_are_optional():
	problemData = createProblemData()
	assert problemData.outputFilePath is None
	assert problemData.timeStep == 0.0


def test_explicit_numerical_settings():
	problemData = createProblemData(numericalSettings=NumericalSettings(1.0, finalTime=10.0))
	assert problemData.timeStep == 1.0
	assert problemData.finalTime == 10.0


@pytest.mark.parametrize("arguments", [
	("Conductivity", 0),
	(0, "Conductivity"),
	(np.int64(0), "Conductivity"),
])
def test_property_access_supports_both_argument_orders(arguments):
	problemData = createProblemData()
	assert problemData.propertyData.get(*arguments) == 2.0


def test_property_access_by_keyword():
	problemData = createProblemData()
	assert problemData.propertyData.get("Density", handle=0) == 3.0
