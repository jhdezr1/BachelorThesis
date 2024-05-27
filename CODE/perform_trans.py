from utils.tools import load_image, save_nifti, x_rotmat,y_rotmat,z_rotmat
from scipy.ndimage import affine_transform
import os
import pandas as pd
import random
import numpy as np
import argparse
import shutil

argparse = argparse.ArgumentParser()
argparse.add_argument('--path_ct')
argparse.add_argument('--ntrans')
argparse.add_argument('--out_dir')
args = argparse.parse_args()

# define the directory where the original mris are stored and where you want to store the rotated ones
path_cts = args.path_ct

# define your input files extension
ct_extension ='.nii.gz'

# define the number of transforms you will like to apply--> MUST BE SMALLER THAN 3 (need to satisfy nnunet lexic)
number_transforms_axis = int(args.ntrans)

# define empty directory to store applied transforms (to invert them afterwards in order to perform the evaluation)

out_path = args.out_dir
os.makedirs(f"{out_path}/trans")
img_transform = {}
# for each of the found mris!
for ct in os.listdir(f'{path_cts}'):
    print(ct)
    if ct[-7:] == ct_extension:
        # get the subject's id
        exam_id = str(ct.split('_')[1])


        # store transforms applied to the specific ct
        list_transf = []

        # load image and get its type
        img,h,a = load_image(f'{path_cts}/{ct}')
        t = img.dtype

        # id the rotated volume will acquire.
        # For example if we are working with BRAIN_005_0000.nii.gz volume, the resulting volume will be
        # BRAIN_005_1_0000.nii.gz, meaning its subject 005 and transformation 1 (which will be an x rotation)
        id = 1

        # apply the number of defined rotations on each axis.
        # NOTICE NOT TO DEGRADE THE VOLUME THEY ARE ACOTATED BETWEEN -027-0.27 RADIANS
        for i in range(0,number_transforms_axis):

            # get radians (randomly)
            x_rot = random.uniform(-0.05, 0.05)
            x_rot = round(x_rot, 2)
            y_rot = random.uniform(-0.05, 0.05)
            y_rot = round(y_rot, 2)
            z_rot = random.uniform(-0.05, 0.05)
            z_rot = round(z_rot, 2)
            # save transform
            list_transf.append(x_rot)
            list_transf.append(y_rot)
            list_transf.append(z_rot)
            # define rot matrix with aux functions
            M = z_rotmat(z_rot).dot(y_rotmat(y_rot)).dot(x_rotmat(x_rot))
            G = np.random.normal(0, 10, size=np.shape(img))
            # apply rot
            rotated_volume = affine_transform(img, M, output=t, order=1, mode='constant', cval=-3024,prefilter=False)
            transf_vol = rotated_volume + G
            transf_vol[transf_vol > np.max(img)] = np.max(img)
            transf_vol[transf_vol < np.min(img)] = np.min(img)
            transf_vol = transf_vol.astype(np.int16)
            # save vol
            out_name = f'SMALL{id}_{exam_id}_0000.nii.gz'
            save_nifti(transf_vol, h, a, os.path.join(out_path,'trans', out_name))
            id += 1
    img_transform[ct] = list_transf
    df = pd.DataFrame.from_dict(img_transform)
    df.to_csv(f'{args.out_dir}/applied_transforms.csv')
    shutil.copy(f'{path_cts}/{ct}', f'{out_path}/trans/{ct}')


