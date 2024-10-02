import torch

# CUDA 사용 가능 여부 확인
if torch.cuda.is_available():
    print(f"CUDA 사용 가능: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA 사용 불가")
