import numpy as np

def cosine_metric(a, b):
    d = 1 - ((a / np.sqrt(a @ a)) @ (b /np.sqrt(b @ b))/2+0.5)
    return d