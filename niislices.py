#nii threshold contour
import nibabel as nib
import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy

test_load = nib.load('/Users/TH/Desktop/2022S/rat brain/o20190801_092845s123a1000.nii').get_fdata() #nii 파일 읽기

tl_shape = test_load.shape  #tuple, tl_shape[0, 1, 2] = 256
len = tl_shape[2]
slices = []

for i in range(len):
    slice = test_load[:, :, i]
    #grayscale
    img_2d = slice.astype(float)
    img_2d_scaled = (np.maximum(img_2d, 0) / img_2d.max()) * 255.0
    img_2d_scaled = np.uint8(img_2d_scaled)
    #rotate
    img_2d_scaled_rotated = cv2.rotate(img_2d_scaled, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #append in list
    img_array = np.array(img_2d_scaled_rotated)
    slices.append(img_array)

#grayscale 해줬으니까
#threshold 이용해서 이진화하고 밝은 거 추출?
#or edge 써서 구조 따기?

mean_slices = []
mean_slices = copy.deepcopy(slices)
gaussian_slices = []
gaussian_slices = copy.deepcopy(slices)

# 슬라이드쇼 용으로 모든 슬라이스에 대해 adaptive threshold + contour 처리
for i in range(len):
    #ADAPTIVE + CONTOUR 시도
    mean_adaptive = cv2.adaptiveThreshold(mean_slices[i], 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 0)
    gaussian_adaptive = cv2.adaptiveThreshold(gaussian_slices[i], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0)

    #mean adaptive + contour
    mean_ret, mean_imthres = cv2.threshold(mean_adaptive, 127, 255, cv2.THRESH_BINARY_INV)
    mean_contour, mean_hierarchy = cv2.findContours(mean_imthres, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    #gaussian adaptive + contour
    gaussian_ret, gaussian_imthres = cv2.threshold(gaussian_adaptive, 127, 255, cv2.THRESH_BINARY_INV)
    gaussian_contour, gaussian_hierarchy = cv2.findContours(gaussian_imthres, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    #draw contour
    cv2.drawContours(mean_slices[i], mean_contour, -1, (255, 255, 255), 1)
    cv2.drawContours(gaussian_slices[i], gaussian_contour, -1, (255, 255, 255), 1)

#슬라이드쇼
index = 0
while True:
    resize_img = cv2.resize(mean_slices[index], (1500, 1500))   # image resize
    #cv2.imshow('nii slice %d'%(index + 1), mean_slices[index])  #adaptive mean threshold + contour
    cv2.imshow('nii slice %d'%(index + 1), resize_img)  #adaptive mean threshold + contour
    #cv2.imshow('nii slice %d'%(index + 1), gaussian_slices[index])  #adaptive gaussian threshold + contour

    if cv2.waitKey(3000) == 27:		# 3초에 한 장씩, ESC 누르면 종료
        break

    cv2.destroyWindow('nii slice %d'%(index + 1))   # 자동으로 이전 슬라이드쇼 윈도우 종료

    index += 1      
    if index >= len:
        index = 0


cv2.destroyAllWindows()