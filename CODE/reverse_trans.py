"""
Script intended to perform inverse rotations over 3D volumes (TTA UQ)
Last edition: 26/04/2024 by Javier Hernández Rubia (j.hernandezr.2020@alumnos.urjc.es)
Author: Blanca Rodríguez González (blanca.rodriguez@urjc.es)
"""

import pandas as pd
from utils.tools import load_image, save_nifti, x_rotmat, y_rotmat, z_rotmat
from scipy.ndimage import affine_transform
import os
import shutil
from skimage import morphology
import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument('--out_dir')
argparse.add_argument('--in_dir')
argparse.add_argument('--ntrans')
args = argparse.parse_args()

# path_i_2d = "/home/brodriguez2018/NAS/MATERIA_OSCURA/TFMs/Blanca_Rodriguez_TFM/001-Data/UQ/001_predicted_labels/2d"
path_st = f"{args.out_dir}/predicted"
# path_i_3d_lr = "/home/brodriguez2018/NAS/MATERIA_OSCURA/TFMs/Blanca_Rodriguez_TFM/001-Data/UQ/001_predicted_labels/3d_lowres"
# path_i_3d_c = "/home/brodriguez2018/NAS/MATERIA_OSCURA/TFMs/Blanca_Rodriguez_TFM/001-Data/UQ/001_predicted_labels/3d_cascade"

os.makedirs(f"{args.out_dir}/predtrans")
# path_o_2d = "/home/brodriguez2018/NAS/MATERIA_OSCURA/TFMs/Blanca_Rodriguez_TFM/001-Data/UQ/002_reoriented_labels/2d"
def_path_o = f"{args.out_dir}/predtrans"
# path_o_3d_lr = "/home/brodriguez2018/NAS/MATERIA_OSCURA/TFMs/Blanca_Rodriguez_TFM/001-Data/UQ/002_reoriented_labels/3d_low_res"
# path_o_3d_c = "/home/brodriguez2018/NAS/MATERIA_OSCURA/TFMs/Blanca_Rodriguez_TFM/001-Data/UQ/002_reoriented_labels/3d_Cascade"



mri_extension = '.nii.gz'
applied_transforms = pd.read_csv(f'{args.out_dir}/applied_transforms.csv')

for file in os.listdir(path_st):
    try:
        rot_id = int(file.split('_')[0][-1])
        if file[-7:] == mri_extension and file != 'SMALL_009.nii.gz':
            print(f'Time to process {file[:-7]}.....')

            # read input images
            # img2d, h2d, a2d = load_image(os.path.join(path_i_3d_fr, file))
            img3df, h3df, a3df = load_image(os.path.join(path_st, file))
            # img3dl, h3dl, a3dl = load_image(os.path.join(path_i_3d_Fr, file))
            # img3dc, h3dc, a3dc = load_image(os.path.join(path_i_3d_c, file))

            # consult transforms applied for the image
            id_pat = f"{str(file.split('_')[1])[:3]}"
            for st in os.listdir(args.in_dir):
                search_t = f'{st.split("_")[0]}_{id_pat}_0000{file[-7:]}'
            transforms_list = list(applied_transforms[search_t])

            # get 'transform' applied --> last number id

            # get rotation angle (negative since we want to reverse)
            rot_angle = - float(transforms_list[rot_id])

            # define transform matrix depending on id (0,1 x rot; 2,3 y rot; 4,5 z rot)
            for i in range(1, int(args.ntrans)+1):
                if i == rot_id:
                    print(rot_id)
                    rot_x = - float(transforms_list[((i*3)-3)])
                    rot_y = - float(transforms_list[((i*3)-2)])
                    rot_z = - float(transforms_list[((i*3)-1)])
                    M = x_rotmat(rot_x).dot(y_rotmat(rot_y)).dot(z_rotmat(rot_z))

            rotated3d_fr = affine_transform(img3df, M, output=int, order=0, prefilter=False)
            save_nifti(rotated3d_fr, h3df, a3df, os.path.join(def_path_o, file))
            # apply transforms to images and save results
            # rotated2d = affine_transform(img2d, M, output=int, order=1, prefilter=False)
            # save_nifti(rotated2d,h2d,a2d,os.path.join(path_o_2d,file))

            # rotated3d_lr = affine_transform(img3dl, M, output=int, order=1, prefilter=False)
            # save_nifti(rotated3d_lr, h3dl, a3dl, os.path.join(path_o_3d_lr, file))

            # rotated3d_c = affine_transform(img3dc, M, output=int, order=1, prefilter=False)
            # save_nifti(rotated3d_c, h3dc, a3dc, os.path.join(path_o_3d_c, file))

            print('--------------------------------------------------------------------------')

    except ValueError:
        shutil.copyfile(os.path.join(path_st, file), os.path.join(def_path_o, file))

