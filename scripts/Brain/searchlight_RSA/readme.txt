TO run the code yourself, pls download the required data from data_download_scripts folder. There is also a Readme4download.txt for illustration. To run the download script, sh download_script.sh shall do.

##############Scripts
My protocol is to run slurm job 1) to calculate the searchlight RSA, 2) to normalize the RSA with upper ceiling and average the normalized RSA across subjects

sbtach hpc_searchlightRSA_calculation.sh rdm_codellama_last

- this will call python script searchlightRSA_calculation.py to calculate the searchlight RSA, remember to change the llm_label passed in every time	

When the job is done, run 

sbatch  hpc_RSA_normalization_ave.sh rdm_codellama_last

- this will call the python script RSA_normalization_ave.py to do the normalization and average. 

helper_functions are called by 2 python scripts

#############Results

Results lie in ./results/test/llm_rdm/, sub-xxs_RSA-BetasAvg_task-test_corr-spearman_llm-xxxxx_stats-FDR-q-0.05-method-poscorr.pkl are generated for each subject and llm_label by searchlightRSA_calculation, and group10_RSA_BetasAvg_llm-xxxx_task-test_wb.nii is the final normalized and averaged RSA across the brain for each llm_label. ./results/test/llm_rdm/plots are the visualization using group10_RSA_BetasAvg_llm-xxxx_task-test_wb.nii and mask

Models' RDMs are saved in LLM_RDMs, plots inside is the visualization of rank normalized RDM 
llm_rdm_visualization.ipynb generated these RDM visualizations.

##############Appendix
Some code are borrowed from the script that the https://www.nature.com/articles/s41467-024-50310-3 shared, such as 

- how the searchlight RDM centered at each voxel is calculated:
https://s3.amazonaws.com/openneuro.org/ds005165/derivatives/versionB/scripts/searchlight/compute_searchlight_MNI152.py?versionId=wHYkLGBY75Q1EcEtKorMzCPtnrsKzZ1v

- how RSA is calculated: 
https://s3.amazonaws.com/openneuro.org/ds005165/derivatives/versionA/scripts/analysis/fig7_metadataRSA/Algonauts2021_metadataRSA_compute.py?versionId=9oFqUG60FhBs6PBD1TPp.uqWkxUrK4Ck

- how RSA is normalized and averaged across subjects:
https://github.com/blahner/BOLDMomentsDataset/blob/56da232de1007c280b6fc9c2ae205f8befe71e0f/examples/metadataRSA_versionA.ipynb
