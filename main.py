from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=3)
scene.set_floor(-10, (0.6, 0.6, 0.6))
scene.set_background_color((0.1, 0.4, 0.8))
scene.set_directional_light((0, 1, 1), 0.2, (1, 0.8, 0.6))
char3=[[2,1], [1,2], [1,3], [1,4], [1,5], [2,6], [3,7], [4,7], [5,6], [6,5], [6,4], [7,6], [8,7], [9,7], [10,6], [11,5], [11,4], [11,3], [11,2], [10,1]]
char_3 = ti.Matrix(char3)
chard = [[1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1], [8,1], [9,1], [10,1], [11,1], [1,2], [1,3], [2,4], [2,5], [3,6], [4,7], [5,7], [6,7], [7,7], [8,7], [9,6], [10,5], [10,4], [11,2], [11,3]]
char_d = ti.Matrix(chard)

@ti.func
def draw_cylinder(pos, radius, height, color, color_noise):
    for I in ti.grouped(ti.ndrange((-radius, 1+radius), (0, height), (-radius, 1+radius))):
        if (I[0]**2 + I[2]**2 <= radius**2):
            scene.set_voxel(pos+I, 1, color + color_noise * ti.random())

@ti.func
def draw_cone(pos, radius, height, color, color_noise):
    for I in ti.grouped(ti.ndrange((-radius, 1+radius), (0, height), (-radius, 1+radius))):
        if (I[0]**2 + I[2]**2 <= radius**2 * (1- I[1]/height)):
            if (I[1] == 0):
                scene.set_voxel(pos+I, 1, vec3(0.1, 0.1, 1.0))
            else:
                scene.set_voxel(pos+I, 1, color + color_noise * ti.random())        

@ti.func
def draw_fire(pos, radius, height, color, color_noise):
    for I in ti.grouped(ti.ndrange((-2*radius, 1+2*radius), (0, height), (-2*radius, 1+2*radius))):
        if (I[0]**2 + I[2]**2 <= radius**2 * (1+3*I[1]/height)) and (ti.random() < (1- I[1]/height)**2):
            scene.set_voxel(vec3(pos[0]+I[0], pos[1]-I[1], pos[2]+I[2]), 20, color + color_noise * ti.random()) 

@ti.kernel
def initialize_voxels():
    draw_cylinder(pos=(0,0,0), radius=10, height=150, color=(1, 1, 1), color_noise=vec3(0.1))
    draw_cylinder(pos=(15,0,0), radius=5, height=50, color=(1, 1, 1), color_noise=vec3(0.1))
    draw_cylinder(pos=(-15,0,0), radius=5, height=50, color=(1, 1, 1), color_noise=vec3(0.1))
    draw_cylinder(pos=(0,0,15), radius=5, height=50, color=(1, 1, 1), color_noise=vec3(0.1))
    draw_cylinder(pos=(0,0,-15), radius=5, height=50, color=(1, 1, 1), color_noise=vec3(0.1))
    draw_cone(pos=(0,150,0), radius=10, height=30, color=(1,1,1), color_noise=vec3(0.1))    
    draw_cone(pos=(15,50,0), radius=5, height=15, color=(1,1,1), color_noise=vec3(0.1))    
    draw_cone(pos=(-15,50,0), radius=5, height=15, color=(1,1,1), color_noise=vec3(0.1))    
    draw_cone(pos=(0,50,15), radius=5, height=15, color=(1,1,1), color_noise=vec3(0.1))    
    draw_cone(pos=(0,50,-15), radius=5, height=15, color=(1,1,1), color_noise=vec3(0.1))
    # draw 3
    for key in ti.static(range(20)):
        scene.set_voxel(vec3(-4+char_3[key,1], 130+char_3[key,0], 10), 1, vec3(0.1, 0.1, 1.0))
    # draw d
    for key in ti.static(range(26)):
        scene.set_voxel(vec3(-4+char_d[key,1], 114+char_d[key,0], 10), 1, vec3(0.1, 0.1, 1.0))
    # draw flag
    for I in ti.static(ti.ndrange((-4,5), (-3,3))):
        scene.set_voxel(vec3(I[0], I[1]+106, 10), 1, vec3(1.0, 0.1, 0.1))
        
    draw_fire(vec3(0,0,0), 10, 120, vec3(0.8, 0.4, 0.0), vec3(0.1))
    draw_fire(vec3(15,0,0), 5, 80, vec3(0.8, 0.4, 0.0), vec3(0.1))
    draw_fire(vec3(0,0,15), 5, 80, vec3(0.8, 0.4, 0.0), vec3(0.1))
    draw_fire(vec3(-15,0,0), 5, 80, vec3(0.8, 0.4, 0.0), vec3(0.1))
    draw_fire(vec3(0,0,-15), 5, 80, vec3(0.8, 0.4, 0.0), vec3(0.1))

initialize_voxels()
scene.finish()