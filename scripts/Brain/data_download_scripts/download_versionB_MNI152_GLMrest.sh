#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="/scratch/qy775/nma/BOLDMomentsDataset"
dataset_path="derivatives/versionB/MNI152"

#download the mask and parcels in the GLM folder
mask_dir="${LOCAL_DIR}/${dataset_path}/GLM/mask/"
mkdir -p "${mask_dir}"
aws s3 sync --no-sign-request \
"s3://openneuro.org/ds005165/${dataset_path}/GLM/mask/" \
"${mask_dir}"

#download the parcels in the GLM folder
par_BMD="${LOCAL_DIR}/${dataset_path}/GLM/parcels/BMDgeneral/"
mkdir -p "${par_BMD}"
aws s3 sync --no-sign-request \
"s3://openneuro.org/ds005165/${dataset_path}/GLM/parcels/BMDgeneral/" \
"${par_BMD}"

par_group="${LOCAL_DIR}/${dataset_path}/GLM/parcels/group_parcels/"
mkdir -p "${par_group}"
aws s3 sync --no-sign-request \
"s3://openneuro.org/ds005165/${dataset_path}/GLM/parcels/group_parcels/" \
"${par_group}"

par_prob="${LOCAL_DIR}/${dataset_path}/GLM/parcels/probability_map/"
mkdir -p "${par_prob}"
aws s3 sync --no-sign-request \
"s3://openneuro.org/ds005165/${dataset_path}/GLM/parcels/probability_map/" \
"${par_prob}"
