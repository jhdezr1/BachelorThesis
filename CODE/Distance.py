import os
from utils.tools import makedirs
import argparse
from tqdm import tqdm

argparse = argparse.ArgumentParser()
argparse.add_argument('--out_dir')
argparse.add_argument('--slicer_path') # the slicer.5.4_linux tatata folder
args = argparse.parse_args()

trans_name = os.listdir(f'{args.out_dir}/predtrans')[0][:-7]
struct_dic = os.listdir(f'{args.out_dir}/{trans_name}')

gen_path = args.out_dir
out = f'{args.out_dir}/distance'



for trans in os.listdir(f'{args.out_dir}/predtrans'):
    try:
        int(trans.split('_')[0][-1])
        makedirs(f'{out}/{trans[:-7]}')
    except ValueError:
        imp_trans = trans[:-7]
        makedirs(f'{out}/GT')

for t in tqdm(os.listdir(f'{out}')):
    if t == 'GT':
        for st in struct_dic:
            pathslicer = f'{args.slicer_path}/Slicer'
            modulepath = f'{args.slicer_path}/slicer.org/Extensions-31938/ModelToModelDistance/lib/Slicer-5.4/cli-modules/ModelToModelDistance'
            sourcevtk = f'{args.out_dir}/{imp_trans}/{st}'
            targetvtk = f'{args.out_dir}/STAPLEVTK/{st}'
            outputvtk = f'{out}/{t}/{st[:-4]}_distance.vtk'

            os.system(f'{pathslicer} --launch {modulepath} -s {targetvtk} -t {sourcevtk} -o {outputvtk}')
    else:
        trans_path = f'{args.out_dir}/{t}'
        for st in struct_dic:
            pathslicer = f'{args.slicer_path}/Slicer'
            modulepath = f'{args.slicer_path}/slicer.org/Extensions-31938/ModelToModelDistance/lib/Slicer-5.4/cli-modules/ModelToModelDistance'
            sourcevtk = f'{trans_path}/{st}'
            targetvtk = f'{args.out_dir}/STAPLEVTK/{st}'
            outputvtk = f'{out}/{t}/{st[:-4]}_distance.vtk'

            os.system(f'{pathslicer} --launch {modulepath} -s {targetvtk} -t {sourcevtk} -o {outputvtk}')

for trans in os.listdir(f'{args.out_dir}/predtrans'):
    os.system(f'rm -r {args.out_dir}/{trans[:-7]}')
os.system(f'rm -r {args.out_dir}/STAPLEVTK')
