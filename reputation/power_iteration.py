#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 08:42:32 2018

@author: apo
"""

import numpy as np
import numpy.linalg as la


def power_iteration(matrix, p0, norm = lambda x: la.norm(x, np.inf), epsilon=0.0001, max_iterations=200):
    """
    power method for eigenvector computation
    parameters:
        matrix: a row-stochastic matrix
        p0: initial stochastic row-vector
        norm: the vector norm to use (defaults to inf-norm)
        epsilon: for stopping criterion
    return:
        p: the eigenvector for the dominant eigenvalue
        residual: the length-difference of the last two runs
        num_iter: the number of iterations required to reach the stopping criterion
    """
    p, prev = p0, p0
    residual, num_iter = 1, 0
    while residual >= epsilon and num_iter < max_iterations:
        prev = p
        num_iter += 1
        p = prev.dot(matrix)
        p = p / norm(p)
        residual = norm(p - prev)

    if num_iter >= max_iterations:
        raise Exception("Did not converge, last residual: {}".format(residual))

    return p, residual, num_iter
