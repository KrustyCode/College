import numpy as np

def rosenbrock_function(x):
    return np.sum(100.0 * (x[1:] - x[:-1]**2)**2 + (x[:-1] - 1)**2)

def shifted_sphere_function(x):
    return np.sum(np.square((x+0.5)))

def rosenbrock_boundaries():
    lb = -30
    ub = 30
    return lb, ub

def shifted_sphere_boundaries():
    lb = -100
    ub = 100
    return lb, ub