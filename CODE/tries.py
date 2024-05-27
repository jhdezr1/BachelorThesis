import os
import pyvista as pv


def smoothing(path_vtk):
    vol = pv.read(path_vtk)
    # Iterate through the faces array
    faces = vol.faces
    triangle_count = 0
    i = 0
    while i < len(faces):
        n = faces[i]  # Number of points in this face
        if n == 3:  # It's a triangle
            triangle_count += 1
        i += n + 1  # Move to the next face (number of points + 1 for the count)

    if triangle_count >= 5000:
        vol = vol.decimate_boundary(target_reduction=0.7)
        surf = vol.extract_geometry()
        smooth = surf.smooth(n_iter=100)
        return smooth
    elif 5000 > triangle_count >= 3000:
        vol = vol.decimate_boundary(target_reduction=0.7)
        surf = vol.extract_geometry()
        smooth = surf.smooth(n_iter=75)
        return smooth
    elif 3000 > triangle_count >= 1000:
        vol = vol.decimate_boundary(target_reduction=0.7)
        surf = vol.extract_geometry()
        smooth = surf.smooth(n_iter=50)
        return smooth
    elif triangle_count < 1000:
        vol = vol.decimate_boundary(target_reduction=0.7)
        surf = vol.extract_geometry()
        smooth = surf.smooth(n_iter=25)
        return smooth



for v in os.listdir('/home/jhernandez2020/Escritorio/2020_JavierHernandez/001_Process_Dataset4/000_STAPLE'):
    if v.endswith('.vtk'):
        path_vtk = f'/home/jhernandez2020/Escritorio/2020_JavierHernandez/001_Process_Dataset4/000_STAPLE/{v}'

        l = smoothing(path_vtk)
        l.save(f'/home/jhernandez2020/Escritorio/trial_smooth/00_{v}')
"""if v.endswith('.vtk'):
    print(v)
    vol = pv.read(path_vtk)
    # Iterate through the faces array
    faces = vol.faces
    print(len(faces))
    triangle_count = 0
    i = 0
    while i < len(faces):
        n = faces[i]  # Number of points in this face
        if n == 3:  # It's a triangle
            triangle_count += 1
        i += n + 1  # Move to the next face (number of points + 1 for the count)
    # decimated_vol = vol.decimate_boundary(target_reduction=0.7)
    # faces = decimated_vol.faces
    # print(len(faces))
    if triangle_count >= 5000:
        # vol = vol.decimate_boundary(target_reduction=0.7)
        surf = vol.extract_geometry()
        smooth = surf.smooth(n_iter=500)
        vol.save(f'/home/jhernandez2020/Escritorio/07{v}')
    elif 5000 > triangle_count >= 3000:
        vol = vol.decimate_boundary(target_reduction=0.7)
#             surf = vol.extract_geometry()
#             smooth = surf.smooth(n_iter=150)
        vol.save(f'/home/jhernandez2020/Escritorio/07{v}')
    elif 3000 > triangle_count >= 1000:
        vol = vol.decimate_boundary(target_reduction=0.7)
#             surf = vol.extract_geometry()
#             smooth = surf.smooth(n_iter=100)
        vol.save(f'/home/jhernandez2020/Escritorio/07{v}')
    elif triangle_count < 1000:
        vol = vol.decimate_boundary(target_reduction=0.7)
        surf = vol.extract_geometry()
        smooth = surf.smooth(n_iter=25)
        smooth.save(f'/home/jhernandez2020/Escritorio/07{v}')
    # Count the number of triangles

"""


