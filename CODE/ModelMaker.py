import os
import numpy as np
from skimage import measure
from stl import mesh
import nibabel as nib
import pyvista as pv
from utils.tools import smoothing
import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument('--out_dir')
args = argparse.parse_args()

img_path1 = f'{args.out_dir}/STAPLE.nii.gz'
img_path2 = f'{args.out_dir}/predtrans'

img = nib.load(img_path1).get_fdata()
hdr = nib.load(img_path1).header
aff = nib.load(img_path1).affine
voxelSize = hdr["pixdim"]

label_values = np.unique(img)

for l in label_values:
    if not l == 0:
        # Use marching cubes to obtain the surface mesh of the anatomical structures of interest
        verts, faces, normals, values = measure.marching_cubes(img == l, 0)


        # Compute correct position of the vertices (non-homogeneous coordinates)
        verts = np.hstack((verts, np.ones((len(verts), 1)))) @ aff.T
        verts = verts[:, 0:3]
        verts[:, 0:2] = - verts[:, 0:2]

        # Create the mesh of the desired structure cartilage
        structure = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                structure.vectors[i][j] = verts[f[j], :]
        verts_flat = verts.reshape((-1, 3))  # Ensure vertices are flat
        faces_flat = np.insert(faces, 0, 3, axis=1).flatten()  # Include number of points for each face
        pv_mesh = pv.PolyData(verts_flat, faces_flat)
        # Step 2: Apply smoothing to the PyVista mesh
        structure = smoothing(pv_mesh, len(faces))
        # Write the mesh to file "structure.stl"
        out_path = f'{args.out_dir}/STAPLEVTK'
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        filename = f'{out_path}/Label_{int(l)}.vtk'
        structure.save(filename)

for file in os.listdir(img_path2):
    img = nib.load(f'{img_path2}/{file}').get_fdata()
    hdr = nib.load(f'{img_path2}/{file}').header
    aff = nib.load(f'{img_path2}/{file}').affine
    voxelSize = hdr["pixdim"]

    for l in label_values:
        if not l == 0:
            # Use marching cubes to obtain the surface mesh of the anatomical structures of interest
            verts, faces, normals, values = measure.marching_cubes(img == l, 0)

            # Compute correct position of the vertices (non-homogeneous coordinates)
            verts = np.hstack((verts, np.ones((len(verts), 1)))) @ aff.T
            verts = verts[:, 0:3]
            verts[:, 0:2] = - verts[:, 0:2]

            # Create the mesh of the desired structure cartilage
            structure = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            for i, f in enumerate(faces):
                for j in range(3):
                    structure.vectors[i][j] = verts[f[j], :]
            verts_flat = verts.reshape((-1, 3))  # Ensure vertices are flat
            faces_flat = np.insert(faces, 0, 3, axis=1).flatten()  # Include number of points for each face
            pv_mesh = pv.PolyData(verts_flat, faces_flat)
            # Step 2: Apply smoothing to the PyVista mesh
            structure = smoothing(pv_mesh, len(faces))
            # Write the mesh to file "structure.stl"
            out_path = f'{args.out_dir}/{file[:-7]}'
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            filename = f'{out_path}/Label_{int(l)}.vtk'
            structure.save(filename)
