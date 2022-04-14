import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
from scipy.fftpack import dct as _dct
from toolz import dicttoolz
from typing import Optional
from PIL import Image
import random

def histogram(photo:np.array, bins:int = 30):
    """Calculate histogram of given image

    Args:
        photo (np.array): original image
        bins (int): number of buns. Default to 30.

    Returns:
        _type_: _description_
    """    
    return cv.calcHist([photo],[0], None, [bins],[0,256])

def dft(photo:np.array, window_size:int):
  dft = np.fft.fft2(photo)
  dft = np.abs(dft[0:window_size,0:window_size])
  return dft

def dct(image, mat_side = 13):
    c = _dct(image, axis=1)
    c = _dct(c, axis=0)
    c = c[0:mat_side, 0:mat_side]
    return c

def sift(image:np.array):
  sift = cv.SIFT_create()
  _, desc = sift.detectAndCompute(image,None)
  desc = cv.resize(desc,image.shape)
  desc = desc.reshape(image.shape)
  return desc

def scale(image: np.array, scale: int = 2):
    h = image.shape[0]
    w = image.shape[1]
    m, n = h // scale, w // scale
    X = image.copy().astype(np.int32)
    image_sc = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            image_sc[i, j] = np.sum(
                X[
                    i * scale: min((i + 1) * scale, h),
                    j * scale: min((j + 1) * scale, w),
                ]
            )
    image_sc = cv.resize(image_sc, image.shape)
    image_sc = image_sc.reshape(image.shape)
    return image_sc


def laplac_grad(image:np.array, ksize:int = 3):
  if ksize % 2 == 0:
    ksize = ksize+1
  laplacian = cv.Laplacian(image,cv.CV_64F,ksize=ksize)
  return np.uint8(np.absolute(laplacian))

def feature_select(image:np.array,
                   hist_param:int = 30, 
                   dft_param:int = 8,
                   dct_param:int = 13,
                   grad_param:int = 3):
  features = {}
  features['hist'] = histogram(image,hist_param)
  features['dft'] = dft(image, dft_param)
  features['dct'] = dct(image, dct_param)
  features['sift'] = sift(image)
  features['grad'] = laplac_grad(image,grad_param)
  return features


