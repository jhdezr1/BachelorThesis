import nibabel as nib
import numpy as np
import pathlib
import os
import cv2
from scipy.stats import entropy
from collections import Counter


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def load_image(img_path):
    extensions = pathlib.Path(img_path).suffixes
    # print(extensions)
    if '.npz' in extensions or '.npy' in extensions:
        im = np.load(img_path)
        im = im[list(im.keys())[0]]

    elif ('.nii' and '.gz') in extensions:
        im = nib.load(img_path).get_fdata()
        hdr = nib.load(img_path).header
        aff = nib.load(img_path).affine
        print(f"Nifti Image {img_path} correctly loaded!")

    elif '.nii' in extensions:
        im = nib.load(img_path).get_fdata()
        hdr = nib.load(img_path).header
        aff = nib.load(img_path).affine
        print(f"Nifti Image {img_path} correctly loaded!")

    else:
        print('The extension file of the image is not known!')

    return im, hdr, aff


def save_nifti(volume, hdr, aff, save_path):
    new_img = nib.nifti1.Nifti1Image(volume, header=hdr, affine=aff)
    nib.save(new_img, save_path)
    print(f"Nifti Image {save_path} correctly saved!")


def check_and_create_directory(path: str):
    print('...........................')
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory ¨{path} was succesfully created")
    else:
        print(f"Directory ¨{path} already existed!")
    print('........................... \n')


def dice_coef(groundtruth_mask, pred_mask):
    overlap = np.sum(pred_mask * groundtruth_mask)
    sum_vol = np.sum(pred_mask) + np.sum(groundtruth_mask)
    dice = np.mean(2 * overlap / sum_vol)
    return round(dice, 5)  # round up to 3 decimal places


def iou(groundtruth_mask, pred_mask):
    i = np.sum(pred_mask * groundtruth_mask)
    u = np.sum(pred_mask) + np.sum(groundtruth_mask) - i
    iou = np.mean(i / u)
    return round(iou, 5)

def x_rotmat(theta):
    """ Rotation matrix for rotation of `theta` radians around x axis

    Parameters
    ----------
    theta : scalar
        Rotation angle in radians

    Returns
    -------
    M : shape (3, 3) array
        Rotation matrix
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return np.array([[1, 0, 0],
                     [0, cos_t, -sin_t],
                     [0, sin_t, cos_t]])


def y_rotmat(theta):
    """ Rotation matrix for rotation of `theta` radians around y axis

    Parameters
    ----------
    theta : scalar
        Rotation angle in radians

    Returns
    -------
    M : shape (3, 3) array
        Rotation matrix
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return np.array([[cos_t, 0, sin_t],
                     [0, 1, 0],
                     [-sin_t, 0, cos_t]])


def z_rotmat(theta):
    """ Rotation matrix for rotation of `theta` radians around z axis

    Parameters
    ----------
    theta : scalar
        Rotation angle in radians

    Returns
    -------
    M : shape (3, 3) array
        Rotation matrix
    """
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return np.array([[cos_t, -sin_t, 0],
                     [sin_t, cos_t, 0],
                     [0, 0, 1]])


def add_gaussian_noise(X_imgs):
    gaussian_noise_imgs = []
    row, col = X_imgs[0].shape
    # Gaussian distribution parameters
    mean = 0
    var = 0.1
    sigma = var ** 0.5

    for X_img in X_imgs:
        gaussian = np.random.random((row, col, 1)).astype(np.float32)
        gaussian = np.concatenate((gaussian, gaussian, gaussian), axis=2)
        gaussian_img = cv2.addWeighted(X_img, 0.75, 0.25 * gaussian, 0.25, 0)
        gaussian_noise_imgs.append(gaussian_img)
    gaussian_noise_imgs = np.array(gaussian_noise_imgs, dtype=np.float32)
    return gaussian_noise_imgs

def smoothing(mesh, faces):

    # Iterate through the faces array
    triangle_count = faces

    if triangle_count >= 5000:
        mesh = mesh.decimate_boundary(target_reduction=0.7)
        smooth = mesh.smooth(n_iter=200)
        return smooth
    elif 5000 > triangle_count >= 3000:
        mesh = mesh.decimate_boundary(target_reduction=0.7)
        smooth = mesh.smooth(n_iter=150)
        return smooth
    elif 3000 > triangle_count >= 1000:
        mesh = mesh.decimate_boundary(target_reduction=0.7)
        smooth = mesh.smooth(n_iter=100)
        return smooth
    elif triangle_count < 1000:
        mesh = mesh.decimate_boundary(target_reduction=0.7)
        smooth = mesh.smooth(n_iter=50)
        return smooth

def variance(full_array):
    variance_array = []
    for e in range(0, full_array.shape[0]):
        v = np.var(full_array[e])
        variance_array.append(v)
    variance_array = np.array(variance_array)
    return variance_array

def _maximum_(full_array):
    maximum_array = []
    for e in range(0, full_array.shape[0]):
        mx = np.max(full_array[e])
        mn = np.min(full_array[e])
        if np.abs(mx) >= np.abs(mn):
            maximum_array.append(mx)
        if np.abs(mx) < np.abs(mn):
            maximum_array.append(mn)
    maximum_array = np.array(maximum_array)
    return maximum_array

def _entropy_(full_array):
    entropy_array = []
    for e in range(0, full_array.shape[0]):
        probabilities = [count / len(full_array[e]) for count in Counter(full_array[e]).values()]
        entropy_value = entropy(probabilities, base=2)
        entropy_array.append(entropy_value)
    entropy_array = np.array(entropy_array)
    return entropy_array

def standard_deviation(full_array):
    std_array = []
    for e in range(0, full_array.shape[0]):
        std = np.std(full_array[e])
        std_array.append(std)
    std_array = np.array(std_array)
    return std_array
