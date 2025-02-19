#!/bin/bash
set -e
#local absolute path to where you want to download the dataset
LOCAL_DIR="/scratch/qy775/nma/BOLDMomentsDataset"
dataset_path="derivatives/versionB/analysis/metadataRSA"

data_dir="${LOCAL_DIR}/${dataset_path}/"
mkdir -p "${data_dir}"
aws s3 sync --no-sign-request \
"s3://openneuro.org/ds005165/${dataset_path}" \
"${data_dir}/"
