# Pytorch

## Installation

```bash
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
```

Validate the installation

```python
>>> import torch
>>> x = torch.rand(3)
>>> x
torch.cuda5447, 0.1600, 0.5200])
>>> torch.cuda.is_available()
True
```

### Tensors
