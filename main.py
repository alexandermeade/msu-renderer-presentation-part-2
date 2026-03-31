import pygame
import numpy as np
import pygame.color as Color
import utils.matrixs as matrixs
from utils.camera import Camera
from utils.reader import RenderBuffer, ObjReader
from utils.rendering import fill_triangle


def main():

    file_path = "./models/torus.obj"
    objreader = ObjReader(file_path)
    
    renderBuffer = objreader.parse()

    print(f"File {file_path} has loaded!")

    pygame.init()

    # Set up the display
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    camera = Camera(
        fov=90, 
        zfar=1000, 
        znear= 1, 
        width= screen_width, 
        height=screen_height
    )
    
    pygame.display.set_caption("Pygame Draw Point")

    angle = 0

    WHITE:Color = (255, 255, 255)
    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
  
        angle += 0.005
        screen.fill(WHITE)

        projMat = matrixs.projection(camera)
        render(
            screen= screen, 
            rotation_angle=angle, 
            renderBuffer=renderBuffer, 
            projMat=projMat, 
            camera=camera
        )
       
        #updates the next frame
        pygame.display.flip()

    pygame.quit()

def render(screen, renderBuffer:RenderBuffer, rotation_angle: float, projMat: np.matrix , camera: Camera):

    prioirty_tris = []

    for tris in renderBuffer.tris:
        p1 = renderBuffer.verts[tris[0]]
        p2 = renderBuffer.verts[tris[1]]
        p3 = renderBuffer.verts[tris[2]]

        # This takes our non projected points 
        
        tri:list[np.ndarray] = [p1.copy(), p2.copy(), p3.copy()]

        rotate_z_mat = matrixs.rotate_z(rotation_angle)
        rotate_x_mat = matrixs.rotate_x(rotation_angle)
        rotate_y_mat = matrixs.rotate_y(rotation_angle)
        
        #rotate 
        for (i, _) in enumerate(tri):
            tri[i] = rotate_y_mat @ rotate_x_mat @ rotate_z_mat @ tri[i] 

        # translate
        for (i, _) in enumerate(tri): 
            tri[i] = tri[i] - np.array([0, 0, 2, 0]) 

        #get lines from triangle
        line1 = tri[1] - tri[0]
        line2 = tri[2] - tri[0]
        line1 = line1[:3] # cut out the homogenous cord
        line2 = line2[:3] # cut out the homogenous cord
        
        #(line1)
        #print(line2)
        #calculate normals
        normal = np.cross(line1, line2)
        normal = matrixs.unit_vector(normal)
        avg_z = (tri[0][2] + tri[1][2] + tri[2][2]) / 3

        #We can "Flip" the normals aka make it look inside out by changing this from < 0 to > 0.
        if np.dot(normal, tri[0][:3] - camera.pos) < 0:
            
            light_vec = np.array([0, 0, 1])
            light_vec = matrixs.unit_vector(light_vec)


            if np.dot(normal, tri[0][:3] - light_vec) < 0:
                light_intensity = max(0, np.dot(normal, light_vec))
            else:
                light_intensity = max(0, np.dot(-normal, light_vec))  # flip normal for back face
            

            #points for rendering
            projected_points = np.stack([
                projMat @ tri[0],
                projMat @ tri[1],
                projMat @ tri[2]
            ])
            # mid point here to find the average z depth in the projection. and

            prioirty_tris.append((avg_z, light_intensity, projected_points))

    #Sort the z depths to render the furthest ones back first and then render the cloests ones to ensure no draw overs.
    #t[0] is the index for the avg_z of each face in the tuple of prioirty points 
    prioirty_tris.sort(key=lambda t: t[0], reverse=False)

    #Draw each triangle.
    for avg_z, light_intensity, tri in prioirty_tris:
        fill_triangle(screen, tri, (255, 0, 0), light_intensity)


if __name__ == "__main__":
    main()
