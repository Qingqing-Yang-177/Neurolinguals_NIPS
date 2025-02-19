#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="/scratch/qy775/nma/BOLDMomentsDataset"
dataset_path="derivatives/versionB/"
script_path="derivatives/versionB/scripts/searchlight"
#create directory paths that mimic the openneuro dataset structure
mkdir -p "${LOCAL_DIR}/${script_path}"

#download the 3 searchlight script file
script_dir="${LOCAL_DIR}/${script_path}"
aws s3 cp --no-sign-request \
"s3://openneuro.org/ds005165/${script_path}/compute_searchlight_MNI152.py" \
"${script_dir}/"

script_dir="${LOCAL_DIR}/${script_path}"
aws s3 cp --no-sign-request \
"s3://openneuro.org/ds005165/${script_path}/compute_searchlight_noiseceiling_MNI152.py" \
"${script_dir}/"

script_dir="${LOCAL_DIR}/${script_path}"
aws s3 cp --no-sign-request \
"s3://openneuro.org/ds005165/${script_path}/plot_searchlight_noiseceiling_MNI152.py" \
"${script_dir}/"
