import numpy as np

def rosenbrock(x):
    return np.sum(100.0 * (x[1:] - x[:-1]**2)**2 + (x[:-1] - 1)**2)

def shifted_sphere_function(x):
    return np.sum(np.square((x+0.5)))