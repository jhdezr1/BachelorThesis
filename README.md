# Uncertainty Quantification

This Bachelor's thesis highlights the importance of UQ studies when it comes to proton therapy planning. For that the nnUNet was trained with a partially labeled dataset that underwent manual inspection searching for typos, leading to a thorough process of data curation. After that, a preprocessing stage of the images was performed, so that a robust GT is built. Once that was obtained, the model underwent a traditional evaluation method that ended up having promising results, leading to a UQ study. In it, surface models were created to quantify a point-by-point statistic calculation. It showed that this model is robust for this specific task, obtaining visualization models that will lead to an improvement of the planning workflow. All this was encapsulated in a tool that calculates the STAPLE segmentation and seventeen surface models corresponding to each of the structures with the statistic that was chosen at the begining of the execution. 

This repository contains the following:

## Executable File (UncertaintyQuantification.sh)

It is the main file. Before its use, permissions need to be given to the file by in the terminal.

``` chmod u+x UncertaintyQuantification.sh ```

After that, it is only needed to do in the terminal and follow the directions given in the terminal.

```./UncertaintyQuantification.sh```

## Requirements (req.txt)

In it we can find the modules needed for the executable to work. It will be installed as the UncertaintyQuantification.sh is run. It is temporal and the folder with the virtual environment will be deleted as soon as the process finishes.

## CODE
In this folder, all code needed is stored. It will be called throughout the execussion automatically. The following scrips are included:
- *perform_trans.py* starts rotating the input CT to start the UQ process.
- *predict_nnunet.py* predicts n transformations and the input CT with no rotation applied.  
- *reverse_trans.py* converts the predicted structures to the original coordinates to be able to perform the study between them.
- *STAPLE.py* creates the STAPLE segmentation for all predictions previously performed to set  GT for the study.
- *ModelMaker.py* generates the surface volumes with no data for further calculations.
- *Distance.py* calculates the distance between a transformation and the STAPLE segmentation.
- *Statistics.py* performs statistical analysis over the previously calculated distances.
