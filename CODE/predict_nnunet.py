import os
import torch
import argparse

argparse = argparse.ArgumentParser()
argparse.add_argument('--results')
argparse.add_argument('--fold')
argparse.add_argument('--database')
argparse.add_argument('--mod')
argparse.add_argument('--out_dir')
args = argparse.parse_args()

os.makedirs(f"{args.out_dir}/predicted")

nnUNet_results_database = args.results
os.environ['nnUNet_results'] = nnUNet_results_database

os.system(f"nnUNetv2_predict -i '{args.out_dir}/trans' -o '{args.out_dir}/predicted' -d {args.database} -c {args.mod} -f {args.fold}")

