import vtk
import numpy as np
import math
import random

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())



if __name__ == "__main__":
    
    plane = vtk.vtkPlaneSource()
    plane.SetResolution(99, 99)
    plane.Update()

    polydata = plane.GetOutput()

    #Triangulate
    triangleFilter = vtk.vtkTriangleFilter()
    triangleFilter.SetInputData(polydata)
    triangleFilter.Update()
    polydata =  triangleFilter.GetOutput()

    normals = polydata.GetPointData().GetNormals()

    array = vtk.vtkFloatArray()
    array.SetNumberOfComponents(1)
    array.SetNumberOfTuples(polydata.GetNumberOfPoints())
    array.SetName("height")



    target_position = [50, 50]
    target_height = 1


    for x in range(100):
        for y in range(100):
            
            idx = 100*x +y

            distance = np.array(target_position) - np.array([x, y])
            r = math.sqrt(distance[0]*distance[0] + distance[1]*distance[1])


            if x == 50 and y < 50:            
                array.SetTuple(idx, [1])
            else:
                array.SetTuple(idx, [0])

    newCell = vtk.vtkCellArray()
    #Remopve Cell
    for cellId in range(polydata.GetNumberOfCells()):
        cell = polydata.GetCell(cellId)

        invalid = array.GetTuple1( cell.GetPointId(0)) + array.GetTuple1( cell.GetPointId(1)) + array.GetTuple1( cell.GetPointId(2))
    
        if not invalid:
            newCell.InsertNextCell(cell)

    polydata.SetPolys(newCell)

    cleanPoly = vtk.vtkCleanPolyData()
    cleanPoly.SetInputData(polydata)
    cleanPoly.Update()

    polydata = cleanPoly.GetOutput()

    polydata.GetPointData().RemoveArray("Normals")


    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(polydata)
    writer.SetFileName("sample5.vtp")
    writer.Update()


    

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.SetScalarRange(0, 1)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    

    renderer.AddActor(actor)

    renderWindow.Render()

    iren.Initialize()
    iren.Start()