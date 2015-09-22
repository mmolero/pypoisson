import numpy as np
from vtk import vtkPLYReader, vtkPolyData, vtkPLYWriter, vtkPoints, vtkCellArray,  vtkTriangle
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk, get_numpy_array_type, get_vtk_to_numpy_typemap



from pypoisson import poisson_reconstruction

import pandas as pd



filename = r"buildings_0.100._normals.xyz"


df = pd.read_csv(filename, sep=' ')
data = df.as_matrix()

points = data[:,0:3]
normals = data[:,3:]

faces, vertices = poisson_reconstruction(points, normals, 10)

print np.shape(faces), np.shape(vertices)
print vertices, faces


def savePLYfromNumpy(points, tr_re, outputFile):

    numberPoints = len(points)

    Points = vtkPoints()
    ntype = get_numpy_array_type(Points.GetDataType())
    points_vtk = numpy_to_vtk(np.asarray(points, order='C',dtype=ntype), deep=1)
    Points.SetNumberOfPoints(numberPoints)
    Points.SetData(points_vtk)

    Triangles = vtkCellArray()
    for item in tr_re:
        Triangle = vtkTriangle()
        Triangle.GetPointIds().SetId(0,item[0])
        Triangle.GetPointIds().SetId(1,item[1])
        Triangle.GetPointIds().SetId(2,item[2])
        Triangles.InsertNextCell(Triangle)

    polydata = vtkPolyData()
    polydata.SetPoints(Points)
    polydata.SetPolys(Triangles)

    polydata.Modified()
    polydata.Update()

    writerPLY = vtkPLYWriter()
    if not outputFile.endswith(".ply"):
        outputFile += ".ply"

    writerPLY.SetFileName(outputFile)
    writerPLY.SetInput(polydata)
    writerPLY.SetFileTypeToASCII()
    writerPLY.Write()


savePLYfromNumpy(vertices, faces, "outputFile_osx.ply")
