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

            if r == 0:
                tps = 0
            else:
                tps = r*r* math.log(r)
            # print(tps)

            
            #Set Color
            array.SetTuple(idx, [r])
            
            #Set Position
            position = np.array( polydata.GetPoint(idx))
            normal = np.array(normals.GetTuple(idx))
            newPosition = position + normal * (tps / 20000)
            polydata.GetPoints().SetPoint(idx, newPosition)


        

    polydata.GetPointData().RemoveArray("Normals")
    # polydata.GetPointData().SetScalars(array)


    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(polydata)
    writer.SetFileName("sample3.vtp")
    writer.Update()


    

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)
    mapper.SetScalarRange(0, 70)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    

    renderer.AddActor(actor)

    renderWindow.Render()

    iren.Initialize()
    iren.Start()