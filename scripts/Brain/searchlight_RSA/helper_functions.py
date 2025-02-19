import os
import pickle
import nibabel as nib
from tqdm import tqdm
import numpy as np
from nilearn import plotting
import matplotlib.pyplot as plt
from scipy import stats
from scipy.spatial.distance import squareform
from statsmodels.stats.multitest import fdrcorrection 

def load_dict(filename_):
    with open(filename_, 'rb') as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        ret_di = u.load()
    return ret_di

def visualize_RDMs(rdms, metadata_labels):
    assert(len(rdms) == len(metadata_labels))
    num_rdms = len(rdms)
    fig, axes = plt.subplots(1, num_rdms, figsize=(15, 5))

    for i, (rdm, metadata_label) in enumerate(zip(rdms, metadata_labels)):
        rdm_rank = stats.rankdata(get_lowertriangular(rdm))
        rdm_rank_norm = rdm_rank / rdm_rank.max()
        rdm_rank_square = squareform(rdm_rank_norm)
        
        ax = axes[i] if num_rdms > 1 else axes  # Handle single subplot case
        im = ax.imshow(rdm_rank_square, cmap='jet')
        ax.set_title(f"{metadata_label} rank normalized RDM")
        fig.colorbar(im, ax=ax)

    plt.tight_layout()
    plt.show()

def get_lowertriangular(rdm):
    num_conditions = rdm.shape[0]
    return rdm[np.triu_indices(num_conditions,1)]

def visualize_glass_brain(nii_save_path, visual_mask_3D, roi_path, savefig=None):
    brain_mask = os.path.join(roi_path,"groupMask_space-MNI152.nii")    
    saveasnii(brain_mask,nii_save_path,visual_mask_3D)
    if savefig:
        plotting.plot_glass_brain(nii_save_path,plot_abs=False,
                         display_mode='lyrz',colorbar=True, vmax=0.34,
                         output_file= savefig)
    else:
        plotting.plot_glass_brain(nii_save_path,plot_abs=False,
                         display_mode='lyrz',colorbar=True) 
    plt.show()

def saveasnii(brain_mask,nii_save_path,nii_data):
    img = nib.load(brain_mask)
    nii_img = nib.Nifti1Image(nii_data, img.affine, img.header)
    nib.save(nii_img, nii_save_path)