#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="/scratch/qy775/nma/BOLDMomentsDataset"
dataset_path="derivatives/versionB/MNI152"

data_dir="${LOCAL_DIR}/${dataset_path}/prepared_searchlight_pkl/"
mkdir -p "${data_dir}"
aws s3 sync --no-sign-request \
"s3://openneuro.org/ds005165/${dataset_path}/prepared_searchlight_pkl/" \
"${data_dir}/"
