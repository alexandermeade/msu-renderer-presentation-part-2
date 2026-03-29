import pygame
import numpy as np
import pygame.color as Color
import utils.matrixs as matrixs
from utils.camera import Camera
from utils.reader import RenderBuffer, ObjReader

def main():

    objreader = ObjReader("./models/cube.obj")
    renderBuffer = objreader.parse()

    print(renderBuffer)

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
    projMat = matrixs.projection(camera)
    pygame.display.set_caption("Pygame Draw Point")

 
    WHITE:Color = (255, 255, 255)


    # game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        render(screen, renderBuffer, projMat, camera)
        

        #updates the next frame
        pygame.display.flip()

    pygame.quit()


def draw_triangle(screen, projected_points, color=(255,255,255)):
    width, height = screen.get_size()
    screen_points = []

    for p in projected_points:
        # p is gonna be of the form [x, y, z, 1]
        # We then normalize x and y with z to fit it onto R^2
        if p[3] != 0:
            x_ndc = p[0] / p[3]  # Normalize x via x' = x/z
            y_ndc = p[1] / p[3]  # Normalize y via y' = y/z
        else:
            x_ndc, y_ndc = 0, 0
        

        # convert from normalized device coords (-1..1) to screen coordinates
        x_screen = int((x_ndc + 1) * 0.5 * width)
        y_screen = int((1 - (y_ndc + 1) * 0.5) * height)  # flip y-axis
        screen_points.append((x_screen, y_screen))

    # draw triangle lines
    pygame.draw.polygon(screen, color, screen_points, width=1)  # width=0 for filled

def render(screen, renderBuffer:RenderBuffer, projMat: np.matrix , camera: Camera):
    for tris in renderBuffer.tris:
        p1 = renderBuffer.verts[tris[0]]
        p2 = renderBuffer.verts[tris[1]]
        p3 = renderBuffer.verts[tris[2]]


        # This takes our non projected points 
        tri = [p1, p2, p3]
        projected_points = np.stack([
            projMat @ tri[0],
            projMat @ tri[1],
            projMat @ tri[2]
        ])

        #draw the projected points on the screen
        draw_triangle(screen, projected_points, color=(255,0,0))


if __name__ == "__main__":
    main()
