# MRI_CV2

BMRLab 인턴 중 python과 openCV를 이용해 개발.

nifti 영상들의 용량이 커서 단일 파일만 업로드.

nifti 영상을 파이썬을 이용해 읽은 후, 쥐의 뇌에 대한 contour를 그리는 프로젝트입니다.

영상을 이진화해도 밝기가 뚜렷하지 않기에 adaptive threshold를 이용했으나, 여전히 너무 많은 contour들이 그려짐.

데이터를 이용해 적절한 threshold에 대한 학습을 시킨다면 개선시킬 수 있을 것이지만, 부족한 시간과 머신러닝에 대한 이해가 부족하여 미구현.
