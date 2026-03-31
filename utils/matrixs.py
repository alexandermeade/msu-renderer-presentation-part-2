import numpy as np
import pygame
from utils.camera import Camera
import math

# normalize
#[x, y, z, 1] -> [(h/w)fx, fy, z]
# f = 1/tan(theta/2)
# zfar - znear = 9
# zfar/(zfar-znear) -> normalizes this between zfar and znear
#
# [(w/h)fx, fy, z(zfar/(zfar-znear))-(zfar*znear/(zfar-znear))
#  
# x' = x/z, y'=y/z
#
# a = aspect ratio = (w/h) 
# q = zfar/(zfar-znear)
# f = 1/tan(theta/2)
#
# [afx/z, fy/z, zq-znear*q]

# proj = [af, 0, 0, 0]
#        [0 f 0 0]
#        [0 0 q 1]
#        [0 0 -znear*q 0]
# 1/z * [afx, fy, zq-znq, z] * proj
#The projection =1/z * [afx, fy, zq-znq, z] * proj 
def projection(camera: Camera) -> np.ndarray:
    aspect = camera.aspect_ratio()
    f = 1 / math.tan(math.radians(camera.fov) / 2)
    znear = camera.znear
    zfar = camera.zfar

    return np.array([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, -(zfar + znear)/(zfar - znear), -1],
        [0, 0, -2*znear*zfar/(zfar - znear), 0]
    ], dtype=np.float32)

def rotate_x(theta: float) -> np.ndarray:
    return np.array([
        [1, 0,                0,               0],
        [0, math.cos(theta), -math.sin(theta), 0],
        [0, math.sin(theta),  math.cos(theta), 0],
        [0, 0,                0,               1]
    ])

def rotate_z(theta: float) -> np.ndarray:

    return np.array([
        [math.cos(theta), -math.sin(theta), 0, 0],
        [math.sin(theta),  math.cos(theta), 0, 0],
        [0,                0,               1, 0],
        [0,                0,               0, 1]
    ])

def rotate_y(theta: float) -> np.ndarray:
    return np.array([
        [ math.cos(theta), 0, math.sin(theta), 0],
        [ 0,               1, 0,               0],
        [-math.sin(theta), 0, math.cos(theta), 0],
        [ 0,               0, 0,               1]
    ])

def projection2(camera: Camera) -> np.ndarray:
    aspect_ratio = camera.width / camera.height
    fov = 1/math.tan(math.radians(camera.fov)/2)
    zplane = camera.zfar / (camera.zfar - camera.znear)

    return np.array([
        [aspect_ratio*fov, 0, 0, 0],
        [0, fov, 0, 0],
        [0, 0, zplane, 1],
        [0, 0, -camera.znear * zplane, 0]
    ])


def unit_vector(vector: np.ndarray):
    norm_value = np.linalg.norm(vector)
    if norm_value == 0:
        return vector
    return vector / norm_value
