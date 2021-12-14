import numpy as np
import torch

from torch import nn
from torch.functional import F


class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = nn.Linear(512, 1024)
        self.linear2 = nn.Linear(1024, 1024)
        self.linear3 = nn.Linear(1024, 32)
        self.linear4 = nn.Linear(32, 1)
    
    def forward(self, input):
        x = F.leaky_relu(self.linear1(input))
        x = F.leaky_relu(self.linear2(x))
        x = F.leaky_relu(self.linear3(x))
        x = F.relu(self.linear4(x))
        return x
