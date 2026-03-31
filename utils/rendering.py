import pygame 

def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def apply_light(color, intensity):
    r, g, b = color
    r = int(clamp(r * intensity, 0, 255))
    g = int(clamp(g * intensity, 0, 255))
    b = int(clamp(b * intensity, 0, 255))
    return (r, g, b)

def draw_triangle(screen, projected_points, color=(255,255,255)):
    width, height = screen.get_size()
    screen_points = []

    for p in projected_points:
        # p is gonna be of the form [x, y, z, w]
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
    #print(f"-----------\n{screen_points}")
    pygame.draw.line(screen, color, screen_points[0], screen_points[1])
    pygame.draw.line(screen, color, screen_points[1], screen_points[2])
    pygame.draw.line(screen, color, screen_points[2], screen_points[0])

def interpolate_triangle(y, point_start, point_end) -> int:
    # This is to ensure division by zero doesn't happen.
    if point_end[1] == point_start[1]:
        return point_start[0]

    vertical_dist =  (y - point_start[1])
    slope_of_points = (point_end[0] - point_start[0]) / (point_end[1] - point_start[1])

    return int(
        point_start[0] + vertical_dist*slope_of_points
    )

def fill_triangle(screen, projected_points, color=(255, 255, 255), light_intensity= 1):
    width, height = screen.get_size()
    screen_points = []
    color = apply_light(color, light_intensity)
    #finish normalzing into screen position.
    for p in projected_points:
        if p[3] != 0:
            x_ndc = p[0] / p[3]
            y_ndc = p[1] / p[3]
        else:
            x_ndc, y_ndc = 0, 0
        
        x_screen = int((x_ndc + 1) * 0.5 * width)
        y_screen = int((1 - (y_ndc + 1) * 0.5) * height)
        screen_points.append((x_screen, y_screen))

    # sort points by y so v0 is top, v2 is bottom
    screen_points.sort(key=lambda p: p[1])
    v0, v1, v2 = screen_points

    # flat bottom half
    for y in range(v0[1], v1[1] + 1):
        x_start = interpolate_triangle(y, v0, v1)
        x_end = interpolate_triangle(y, v0, v2)

        # If start > end then that implies
        # Our "left side" of the triangle might actually be the 
        # right edge. 
        if x_start > x_end:
            x_start, x_end = x_end, x_start
        
        for x in range(x_start, x_end + 1):
            screen.set_at((x, y), color)
    
    # flat top half
    for y in range(v1[1], v2[1] + 1):
        x_start = interpolate_triangle(y, v1, v2)
        x_end = interpolate_triangle(y, v0, v2)
        
        # If start > end then that implies
        # Our "left side" of the triangle might actually be the 
        # right edge. 
        if x_start > x_end:
            x_start, x_end = x_end, x_start
        
        # Set the pixel in the interval of x coords.
        for x in range(x_start, x_end + 1):
            screen.set_at((x, y), color)