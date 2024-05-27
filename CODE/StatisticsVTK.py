import os
from scipy.stats import entropy
from collections import Counter
import pyvista as pv
import numpy as np
from tqdm import tqdm
from utils.tools import _entropy_, _maximum_, standard_deviation, variance
import argparse


argparse = argparse.ArgumentParser()
argparse.add_argument('--out_dir')
argparse.add_argument('--statistic')
args = argparse.parse_args()

def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Replace 'your_volume.vtk' with the path to your VTK file
distances = f'{args.out_dir}/distance'
patients = os.listdir(distances)
structure_list = os.listdir(f'{distances}/GT')




for st in structure_list:
    if st.endswith('.vtk'):
        full_array = []
        variance_array = []
        for i in patients:
            if i != 'GT':
                vtk_file_path = f'{distances}/{i}/{st}'
                # Read the VTK file
                volume = pv.read(vtk_file_path)
                # Access the point data
                point_data = volume.point_data
                scalar_values = np.array(point_data['Signed'])
                full_array.append(scalar_values)
        vtk_gt = f'{distances }/GT/{st}'
        # Read the VTK fileg
        volume = pv.read(vtk_gt)
        # Access the point data
        point_data = volume.point_data
        scalar_values = np.array(point_data['Signed'])
        full_array.append(scalar_values)
        # full_array[:,n] transformation number n;  full_array[n] point n of all 8 transformations
        full_array = np.round(np.array(full_array).reshape(scalar_values.shape[0], len(patients)), 1)

        if args.statistic == 'variance':
            variance_array = variance(full_array)
            point_data['Signed'] = variance_array
            var_path = f'{args.out_dir}/variance'
            makedirs(var_path)
            volume.save(f'{var_path}/{st}')

        elif args.statistic == 'entropy':
            entropy_array = _entropy_(full_array)
            point_data['Signed'] = entropy_array
            entropy_path = f'{args.out_dir}/entropy'
            makedirs(entropy_path)
            volume.save(f'{entropy_path}/{st}')

        elif args.statistic == 'std':
            std_array = standard_deviation(full_array)
            point_data['Signed'] = std_array
            std_path = f'{args.out_dir}/std'
            makedirs(std_path)
            volume.save(f'{std_path}/{st}')

        elif args.statistic == 'maxdistance':
            maximum_array = _maximum_(full_array)
            point_data['Signed'] = maximum_array
            max_path = f'{args.out_dir}/maxdistance'
            makedirs(max_path)
            volume.save(f'{max_path}/{st}')


"""
random_array = np.ones_like(scalar_values)
point_data['Signed'] = random_array

volume.save('/home/jhernandez2020/Escritorio/trial2/random.vtk')"""
