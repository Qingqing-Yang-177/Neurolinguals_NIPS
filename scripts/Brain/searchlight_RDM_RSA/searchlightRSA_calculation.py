import os
import sys
import pickle
import nibabel as nib
from tqdm import tqdm
import numpy as np
from nilearn import plotting
import matplotlib.pyplot as plt
from scipy import stats
from scipy.spatial.distance import squareform
from statsmodels.stats.multitest import fdrcorrection 
from helper_functions import load_dict 
from helper_functions import visualize_RDMs 
from helper_functions import get_lowertriangular 
from helper_functions import visualize_glass_brain 
from helper_functions import saveasnii

llmlabels=[str(sys.argv[1])]

# Setup path
task='test'
radius = 4
dataset_root = "/scratch/qy775/nma/BOLDMomentsDataset"
save_root = f'/scratch/qy775/nma/results/{task}/llm_rdm/'
searchlight_root=os.path.join(dataset_root, "derivatives", "versionB", "MNI152","prepared_searchlight_pkl")

# Define the path for the new directory
plot_dir = os.path.join(save_root, "plots")

# Create the directory, including any intermediate directories
os.makedirs(save_root, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# Load Group Brain Mask
mask_root = os.path.join(dataset_root,'derivatives/versionB/MNI152/GLM/mask')

# metadata RDM path
#metadata_rdm_root = os.path.join(dataset_root,"derivatives","versionA","analysis","metadataRSA","rdms")

# LLM RDM root
llm_rdm_root = os.path.join("/scratch/qy775/nma/LLM_RDMs/")

# load prepared searchlight RDMs
subjects = ['01','02','03','04','05','06','07','08','09','10']
#mlabels=["actions"] #["actions", "scenes", "objects", "ActionsObjectsScenes", "text_descriptions", 'GIT_image_caption']

#llmlabels=["rdm_codellama_last","rdm_codellama","rdm_llama_last","rdm_llama"]
llm_rdms = []

# Calculate RSA result for each 
for model_label in llmlabels: 
    for s, sub in enumerate(subjects):
        # load meta RDM
        #if metadata_label == 'GIT_image_caption':
        #    meta = np.load(os.path.join(metadata_rdm_root, "MetadataRDM_GITAnnotated_label-" + metadata_label + "_task-" + task + "_metric-cosine.npy"))
        #else:
        #    meta = np.load(os.path.join(metadata_rdm_root, "MetadataRDM_humanAnnotated_label-" + metadata_label + "_task-" + task + "_metric-cosine.npy"))

        # load model RDM
        llm=np.load(os.path.join(llm_rdm_root + model_label + ".npy"))
        
        # load the prepared searchlight RDMs
        fname = f"sub-{sub}_searchlight-BetasAvg_task-{task}_corr-pearson_radius-{radius}.pkl"
        data = load_dict(os.path.join(searchlight_root, fname))
        search = data[0]
        image = data[1]
        dims = image.shape
        n_voxels = dims[0]*dims[1]*dims[2]
        print(n_voxels)
        
        #nan_indices = data[2
        nan_columns = []
        del data

        # make sure it's a long vector
        if llm.ndim==2:
            llm_ltrdm = get_lowertriangular(llm)
            
        corr = np.zeros((search.shape[1],))
        pval = np.zeros((search.shape[1],))
        
        for r in tqdm(range(search.shape[1])):
            # Check if the entire column search[:,r] is NaN
            if np.all(np.isnan(search[:,r])):
                nan_columns.append(r)
                continue  # Skip further processing for this column if it's all NaN
            
            tmp = stats.spearmanr(llm_ltrdm, search[:,r])
            corr[r] = tmp[0]
            pval[r] = tmp[1]

        # Log or process the indices that were all NaN if needed
        print(f"Subject {sub} had {len(nan_columns)} columns with all NaNs.")

        # FDR stats
        method = 'poscorr'
        fdr_tuple = fdrcorrection(pval, alpha = 0.05, method = method, is_sorted = False)
        
        corr_significant = corr * fdr_tuple[0]
        
        # Save RSA results
        fname = 'sub-'+sub + '_RSA-BetasAvg_task-' + task + '_corr-spearman_' + 'llm-' + model_label + '_stats-FDR-q-0.05-method-' + method + '.pkl'
        with open(os.path.join(save_root, fname), 'wb') as fh:
            data = (corr, pval, fdr_tuple, nan_columns)
            pickle.dump(data, fh)