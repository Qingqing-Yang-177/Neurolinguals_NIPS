#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="/scratch/qy775/nma/BOLDMomentsDataset"
dataset_path="derivatives/versionB/MNI152"
#create directory paths that mimic the openneuro dataset structure
mkdir -p "${LOCAL_DIR}/${dataset_path}"

#download the README file
aws s3 cp --no-sign-request \
"s3://openneuro.org/ds005165/${dataset_path}/README.txt" \
"${LOCAL_DIR}/${dataset_path}/"

for sub in {01..10}; do
    data_dir="${LOCAL_DIR}/${dataset_path}/GLM/sub-${sub}"
    mkdir -p "${data_dir}"
    aws s3 sync --no-sign-request \
    "s3://openneuro.org/ds005165/${dataset_path}/GLM/sub-${sub}/" \
    "${data_dir}/"
done
