import os
import nibabel as nib
import SimpleITK as sitk
import numpy as np
import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument('--out_dir')
args = argparse.parse_args()

imglist = []

staple_path = args.out_dir
for file in os.listdir(f'{args.out_dir}/predtrans'):
    img = nib.load(f'{args.out_dir}/predtrans/{file}').get_fdata()
    imglist.append(img)

hdr = nib.load(f'{args.out_dir}/predtrans/{file}').header
aff = nib.load(f'{args.out_dir}/predtrans/{file}').affine
complete_stable = np.zeros(np.shape(imglist[0]))
label_values = np.unique(imglist[0])

for i in range(1, int(np.max(label_values))+1):
    prov_stack = []
    for img in imglist:
        prov_imgP = sitk.GetImageFromArray((img == i).astype(np.int16))
        prov_stack.append(prov_imgP)
    STAPLE_ITK = sitk.STAPLE(prov_stack, 1)
    STAPLE = sitk.GetArrayFromImage(STAPLE_ITK).astype(np.int16)
    complete_stable[STAPLE == 1] = i
    print(f'label {i} done')
new_img = nib.nifti1.Nifti1Image(np.round(complete_stable).astype(np.int8), header=hdr, affine=aff)
nib.save(new_img, f'{staple_path}/STAPLE.nii.gz')
print('------------done----------------')

