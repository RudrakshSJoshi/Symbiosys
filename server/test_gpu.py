import torch
print("CUDA available:", torch.cuda.is_available())
print("CUDA version (PyTorch):", torch.version.cuda)
print("Device name:", torch.cuda.get_device_name(0))