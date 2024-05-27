#!/bin/bash

echo 'WELCOME TO UQ'

echo 'There is a display with the following information:'
echo 'Number of transformations: this indicates the amount of times the CT will be rotated for prediction'
echo 'Number of Fold and Dataset: specifications regading the particular nnUNet pretrained model desired for prediction'
echo 'Modality: the different kinds of modalities from the nnUNet will be displayed, please choose the preferred one'
echo 'UQ statistic: choose the statistic preferred for the study'

# Display Zenity form and get user inputs
inputs=$(zenity --forms \
               --title="Input Form" \
               --text="Fill in the required information" \
               --add-entry="Number of Transformations" \
               --add-entry="Number of Fold" \
               --add-entry="Number of Dataset" \
               --add-combo="Modality:" \
               --combo-values="2d|3d_fullres|3d_lowres|3d_cascade" \
               --add-combo="Uncertainty Quantification Statistic:" \
               --combo-values="variance|std|maxdistance|entropy" \
               --separator="|")

case $? in
	0)
	;;
	*)
	zenity --warning --text="EXITING" 
	exit
	;;
esac
# Split the inputs into variables
ntrans=$(echo $inputs | cut -d '|' -f 1)
fold=$(echo $inputs | cut -d '|' -f 2)
database=$(echo $inputs | cut -d '|' -f 3)
mod=$(echo $inputs | cut -d '|' -f 4)
statistic=$(echo $inputs | cut -d '|' -f 5)

echo 'Form filled up successfully!'
echo '-----------------------------------------------------------------'
echo 'Please select the CT path desired for the study'

path_ct=$(zenity --file-selection --directory --title="CT path")

case $? in
	0)
	;;
	*)
	zenity --warning --text="EXITING" 
	exit
	;;
esac

echo 'Selected successfully!'
echo '------------------------------------------------------------------'
echo 'Choose the desired Output path. In there, the STAPLE and the statistical models will be stored'

output_folder=$(zenity --file-selection --directory --title="Out path")

case $? in
	0)
	;;
	*)
	zenity --warning --text="EXITING" 
	exit
	;;
esac

echo 'Selected successfully!'
echo '------------------------------------------------------------------'
echo 'Choose the desired Results path, where the nnUNet saves all trainings and weights.'

results_folder=$(zenity --file-selection --directory --title="nnUNet Results path")
case $? in
	0)
	;;
	*)
	zenity --warning --text="EXITING" 
	exit
	;;
esac

echo 'Selected successfully!'
echo '------------------------------------------------------------------'
echo 'Choose the desired Slicer path. In there, It needs to be the folder where Slicer is stored. In it, the folder "slicer.org" is kept.'

slicer_path=$(zenity --file-selection --directory --title="Select where Slicer is located")
case $? in
	0)
	;;
	*)
	zenity --warning --text="EXITING" 
	exit
	;;
esac

echo 'Selected successfully!'
echo '------------------------------------------------------------------'
echo 'Check all inputs!!'

# Displaying the results
zenity --info --title="User Inputs" --text="CT path: $path_ct\nNumber of Transformations: $ntrans\nOutput folder: $output_folder\nNumber of Fold: $fold\nNumber of Dataset: $database\nModality: $mod\nnnUNet Results path: $results_folder\nSlicer Path: $slicer_path\nUncertainty Quantification Statistic: $statistic"

echo "Let's start the process!"

echo Installing neccesary packages
python -m venv $output_folder/venv
source $output_folder/venv/bin/activate
pip install -r req.txt
pip install nnunetv2 >/dev/null


echo Set up done! Starting with UQ process..

python CODE/perform_trans.py --path_ct="$path_ct" --ntrans="$ntrans" --out_dir="$output_folder" >/dev/null && echo "Transformations Done"
python CODE/predict_nnunet.py --results="$results_folder" --fold="$fold" --database="$database" --mod="$mod" --out_dir="$output_folder">/dev/null && echo "Predictions Done"


rm $output_folder/predicted/*.json

python CODE/reverse_trans.py --out_dir="$output_folder" --in_dir="$path_ct" --ntrans="$ntrans"
echo "Calculating the STAPLE..."

rm -r $output_folder/predicted
rm -r $output_folder/trans
rm $output_folder/applied_transforms.csv

python CODE/STAPLE.py --out_dir="$output_folder" && echo "STAPLE calculated. Creating VTK models..."

python CODE/ModelMaker.py --out_dir="$output_folder" && echo "VTK created. Starting with the statistics..."

python CODE/Distance.py --out_dir="$output_folder" --slicer_path="$slicer_path" && echo "Distance Calculated. Producing the statistics"

rm -r $output_folder/predtrans

python CODE/StatisticsVTK.py --out_dir="$output_folder" --statistic="$statistic" && echo "Done! Check the results folder!"

rm -r $output_folder/distance

rm -rf $output_folder/venv
