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

# Load Group Brain Mask
mask_root = os.path.join(dataset_root,'derivatives/versionB/MNI152/GLM/mask')

subjects = ['01','02','03','04','05','06','07','08','09','10']
#llmlabels=["rdm_codellama_last","rdm_codellama","rdm_llama_last","rdm_llama"]

#load the upper noise ceiling for noise normalization
fname = os.path.join(searchlight_root, f"noiseceiling-upper_searchlight-BetasAvg_task-{task}_radius-4.pkl")
with open(os.path.join(searchlight_root,fname),'rb') as fh:
    upper,mask_master = pickle.load(fh)
mask_data = mask_master.get_fdata()
#n_voxels = int(np.sum(mask_data > 0))
dims = mask_data.shape
n_voxels = dims[0]*dims[1]*dims[2]

zero_indices = np.where(mask_data==0)
zero_indices = np.ravel_multi_index(zero_indices, mask_data.shape)
non_zero_indices = np.where(mask_data>0)
non_zero_indices = np.ravel_multi_index(non_zero_indices, mask_data.shape)

for model_label in llmlabels: 
    corr_1D_all = np.zeros((len(subjects), n_voxels))
    for s, sub in enumerate(subjects): #load all subject's searchlight rsa and store them in a 4D array
        print(sub)
        #load the subject's searchlight-metadata correlations
        fname =  f"sub-{sub}_RSA-BetasAvg_task-{task}_corr-spearman_llm-{model_label}_stats-FDR-q-0.05-method-poscorr.pkl"
        with open(os.path.join(save_root, fname), 'rb') as fh:
            corr, _, _, nan_indices = pickle.load(fh) #(corr, pval, fdr_tuple, nan_indices)

        # Clip nan_indices to ensure they are within the range of n_voxels
        nan_indices = np.array(nan_indices)  # Convert to NumPy array
        union_inval_indices = np.union1d(zero_indices, nan_indices)
        
        #mask correlations by nans and add to the all subject array
        corr_1D = np.ones((n_voxels,))
        corr_1D[union_inval_indices] = 0
        corr_1D[corr_1D == 1] = corr[corr_1D == 1]
        corr_1D_all[s,:] = corr_1D

        del corr, nan_indices, corr_1D
        
    #Plot the glass brain of average RSA correlations per voxel masked by FDR significance
    #do ttest
    pval = np.zeros((n_voxels,))
    for vox in tqdm(range(n_voxels)): 
        #performs a ttest at each voxel over the 10 subjects. Gets a p-value for each voxel. The null hypothesis is that the searchlight-metadata correlation is zero
        pval[vox] = stats.ttest_1samp(corr_1D_all[:,vox], popmean=0, alternative='two-sided')[1]

    #do FDR correction
    rejected, pval_corrected = fdrcorrection(pval[~np.isnan(pval)], alpha=0.05,  method='poscorr', is_sorted=False) #to address multiple comparisons, FDR correct over all voxels that are not nans (inside the brain)

    #plot average correlation masked by FDR significance
    #create significance mask from FDR
    pval_mask = np.ones((n_voxels,))
    pval_mask[np.isnan(pval)] = 0
    pval_mask[pval_mask==1] = rejected #1D array of 1's and 0's where 1 means that voxel survived FDR correction
    pval_mask_3D = pval_mask.reshape(dims) #reshape to a 3D matrix

    #manipulate the upper noise ceiling a bit to be compatible with our correlation matrix
    upper_1D_all = np.zeros((len(subjects),n_voxels))
    upper_1D_all[:,non_zero_indices] = upper[:len(subjects),:]
    upper_1D_all[:,zero_indices] = np.nan

    corr_1D_norm = corr_1D_all / upper_1D_all #normalizes each subject's searchlight-metadata correlations by their upper noise ceiling
    corr_1D_norm[:,zero_indices] = 0 #go back to changing nans to zeros
    corr_3D_norm = corr_1D_norm.reshape((len(subjects),dims[0],dims[1],dims[2])) #reshape these normalized values into 3D

    corr_3D_norm_avg = np.nanmean(corr_3D_norm, axis=0) #simply average the normalized values over the 10 subjects at each voxel (mirrors the unnomralized computation above)
    corr_3D_norm_avg_masked = corr_3D_norm_avg * pval_mask_3D #now mask the subject-averaged result by those voxels that survived FDR correction

    #mask results by significance and visualize
    nii_save_path = os.path.join(save_root,'group'+str(len(subjects))+'_RSA_BetasAvg_llm-' + model_label + '_task-' + task + '_wb.nii')
    savefig = os.path.join(save_root,"plots","group"+str(len(subjects))+"_RSA_BetasAvg_llm-" + model_label + "_task-" + task + "_" + sub + "_spearmancorr_glassbrain.svg")

    #corr_3D_norm_avg_masked[corr_3D_norm_avg_masked<0] = 0 #threshold at 0
    visualize_glass_brain(nii_save_path, corr_3D_norm_avg_masked, mask_root, savefig=savefig)


    ## also plot the non-thresholded results
    corr_3D_norm_avg = np.nanmean(corr_3D_norm, axis=0) #simply average the normalized values over the 10 subjects at each voxel (mirrors the unnomralized computation above)
    corr_3D_norm_avg_masked = corr_3D_norm_avg #* pval_mask_3D #now mask the subject-averaged result by those voxels that survived FDR correction

    #mask results by significance and visualize
    nii_save_path = os.path.join(save_root,'group'+str(len(subjects))+'-non_threshold'+'_RSA_BetasAvg_llm-' + model_label + '_task-' + task + '_wb.nii')
    savefig = os.path.join(save_root,"plots","group"+str(len(subjects))+'-non_threshold'+"_RSA_BetasAvg_llm-" + model_label + "_task-" + task + "_" + sub + "_spearmancorr_glassbrain.svg")

    #corr_3D_norm_avg_masked[corr_3D_norm_avg_masked<0] = 0 #threshold at 0
    visualize_glass_brain(nii_save_path, corr_3D_norm_avg_masked, mask_root, savefig=savefig)