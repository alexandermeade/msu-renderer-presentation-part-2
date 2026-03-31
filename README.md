# Info 
This is a continuation of the "Building a CPU Renderer" series. The first part of which can be found [here](https://github.com/alexandermeade/msu-renderer-presentation).

# Math Prerequisites (Vector Operations)

A unit vector is defined as

$$
  \hat{v} = \frac{\vec{v}}{|\vec{v}|}
$$

Where $\hat{v}$ is the direction where $\vec{v}$ is pointing towards. 

All vectors can be constructed as

$$
\hat{v} \cdot \|\vec{v}\| = \vec{v}
$$

The cross product, denoted as ${\vec{v}\mathrel{\times} \vec{r}}$ is an operation used to determine the line orthogonal to two other lines.

<p align = "center">
  <img width="480" height="375" alt="image" src="https://github.com/user-attachments/assets/297b1d8b-3ed3-4dcc-bc2e-d4a86dd32306" />
</p>

Let $\vec{v}$, $\vec{r}$ be vectors. 

$$
  \vec{v} \mathrel{\times}  \vec{r} = \left|\begin{matrix} 
    i & j & k \\
    v_x & v_y & v_z \\
    r_x & r_y & r_z
  \end{matrix}\right| 
$$

This determinate form gives us what we need from the cross product, but it can be dense if you don't know how to solve for a determinant. The good news is that since we are using `NumPy`, this operation is already `predefined as np.cross(vector1, vector2)`.

However if you aren't using `NumPy` we can instead expand this determinate as

$$
  c_x = v_x r_z - v_z r_y 
$$
$$
  c_y = v_z r_x - v_x r_z
$$
$$
  c_z = v_x r_y - v_y r_x
$$

And then we can put it back into vector form as

$$
  \vec{c} = \begin{bmatrix}
    c_x \\
    c_y \\
    c_z
  \end{bmatrix}
$$

With $\vec{c}$ being our result from the cross product.



The Dot product notated as 

$$\vec{v} \cdot \vec{r}$$

is a vector operation that returns a scalar values (Not a vector or a matrix). 
It shows how much two vectors point in the same direction.
<p align = "center" >
<img width="1146" height="344" alt="image" src="https://github.com/user-attachments/assets/bf2cf561-e5c5-4740-9c61-8c29ca9dd327" />
</p>

It is defined in terms of component addition so if we let

Using `NumPy` it has this operation defined under `numpy.dot(vector1, vector2)`

If you aren't using `NumPy` you can implement it the way describe below

$$
  \vec{v} = \begin{bmatrix}
    v_x \\
    v_y \\
    v_z 
  \end{bmatrix}
$$
$$
  \vec{r} = \begin{bmatrix}
    r_x \\
    r_y \\
    r_z  
  \end{bmatrix}
$$

Then we can define the dot product as

$$
  \vec{v} \cdot \vec{r} = v_x r_x + v_y r_y + v_z r_z 
$$

## Properties of Dot products
Let $\vec{v}$ and $\vec{r}$ be vectors.
if

$$
  \vec{v} \cdot \vec{r} = 0
$$

This shows that the two vectors are orthogonal and point in oposite direction. 

if

$$
    \vec{v} \cdot \vec{r} = \text{$0$ or $180$}
$$

This shows that $\vec{v}$ and $\vec{r}$ are parallel to each other.

# Culling
One big issue that exists with our renderer is that it draws every single triangle even if we shouldn't see it. We can fix it using culling.

Culling utilizes the cross product to produce a vector that points orthogonal to a triangle's face, leaving us with a sense of where it is facing.

construct the face of the triangle and we can do that we let $t_{n}$ be our triangle at some $n$-th point.  

Let $\vec{\ell_1}$, $\vec{\ell_2}$ be lines via

$$
  \vec{\ell_1} = \vec{t_1} - \vec{t_0}
$$

$$
  \vec{\ell_2} = \vec{t_2} - \vec{t_0} 
$$

With this we can now take the cross product of these two to find our normal vector.

$$
  \vec{norm} = \vec{\ell_1} \times \vec{\ell_2}
$$

However, we are only interested in the direction of the $\vec{norm}$ so to do that we need the unit vector which is defined as

$$
  \hat{norm} = \frac{\vec{norm}}{|\vec{norm}|}
$$

<details>
  <summary>
    Python Implementation
  </summary>
  
  ```py
  #get lines from triangle
  line1 = tri[1] - tri[0]
  line2 = tri[2] - tri[0]
  line1 = line1[:3] # cut out the homogenous cord
  line2 = line2[:3] # cut out the homogenous cord
  normal = np.cross(line1, line2)
  normal = matrixs.unit_vector(normal)
  #calculate normals
  ```

  with 

  ```py
    def unit_vector(vector: np.ndarray):
        norm_value = np.linalg.norm(vector)
        if norm_value == 0:
            return vector
        return vector / norm_value
  ```
  
</details>

Now, using the culling technique, we can see in the diagram below that the green arrows are gonna be the normals for our faces, and we want to see how aligned they are with our camera vector. 

<p align = "center">
  <img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/2a83915a-1014-41c8-8d4e-9d30f9d532dd" />
</p>

We can do this with a dot product.

Using our normal vector and our triangles positional coordinates we can take the first vertex of the triangle and subtract it by our camera's position

$$
  \hat{norm} \cdot ( \vec{t_0} - \vec{\text{cam}})
$$

Using the result above, we can now know how aligned the norm is with our camera's line to the first vertex $t_0$. 

Since we are subtracting from $t_0$ here, our typical dot product interaction of $dot < 90$ being positive gets flipped, so the result $dot < 90$ is negative, and that's why we cull for the dot product being less than zero.

<details>
  <summary>
    Python Implementation
  </summary>

  ```py
#We can "Flip" the normals aka make it look inside out by changing this from < 0 to > 0.
if np.dot(normal, tri[0][:3] - camera.pos) < 0:

    #points for rendering
    projected_points = np.stack([
        projMat @ tri[0],
        projMat @ tri[1],
        projMat @ tri[2]
    ])

    #draw the projected points on the screen
    draw_triangle(screen, projected_points, color=(255,0,0))
  ```
</details>


With all these culling steps combined we should be able to see this happen to our cube now.


https://github.com/user-attachments/assets/28c5e8ef-3ff4-4b33-9eae-c5408d5709d6



# Intro to Rasterization
Rasterization is the process of turning a set of geometric points into pixels on a screen. Now the first question you might have is (Isn't that what projection is) and yes techniqually. However, rasterization gives us a way to convert the space surrounding those points into pixels as well.

With this information, we can build an algorithm to render the empty space in our faces. 


Before we can start talking about the algorithm we're gonna use, we first need to arrive at the concept of how to begin to reason about getting the space around these points in screen space $\mathbb{Z}^2$. 

Well we can first try and frame the problem around what we wanna draw which is a triangle with 3 verteices $t = \{v_0, v_1, v_2\}$.
<p align = "center">
    <img width="771" height="591" alt="image" src="https://github.com/user-attachments/assets/bf80f5af-5323-425c-92d5-7a4ce57aac9d" />
</p>
So if we choose a vertex to be our start point, then we can try to build a region we want to rasterize. 

So let's choose $s = \vec{v_0}$ to be our starting point, we are gonna rasterize from and $r = \vec{v_1}$ to be the end vertex.

We want to draw each line of the triangle that these two vertices border. Well lets try a scanline approach where we draw one line of the triangle at a time. Below is a diagram which visualizes what we need to do.

<p align = "center">
     <img width="940" height="480" alt="image" src="https://github.com/user-attachments/assets/a957ea28-0942-49c8-a838-edca7f96a333" />
</p>

## Interpolation
This will require us to have some kind of $Y$ parameter to keep track of the vertical position of our scan line.

But where does this $Y$ parameter live? 

Well, we know we are drawing all the lines in between our veretexs so it will be in 

$$Y \in [s_y, r_y]$$

So we know each line we'll have to render, we'll be at some step in that interval.

The other issue we run into is, what vertex is the top of the triangle?
Without knowing this, we could be heading towards the flat part of the triangle instead of to the apex of the triangle. 

So we need to sort with respect to the $y$ component of the vectors.

Now the issue comes in from. 

We know what pixels we need to draw vertically since we know where our $Y$ value sits relative to these points, but how do we actually know where they start horizontally? 

This is where the concept of interpolation comes in. It is good to know that the vertices we are working with here are points since we have already converted them into screen space.

Let's first define our interpolation function and some relevant info. 

$$
  \text{Interpolate}(Y, \vec{S}, \vec{E}) = \left\lfloor \vec{S}_x + (Y - \vec{S}_y) \frac{\Delta x}{\Delta y} \right\rfloor
$$

with

$$
  \Delta x = \vec{E}_x - \vec{S}_x, \quad \Delta y = \vec{E}_y - \vec{S}_y
$$

What this interpolation function does is at traces the path of a line and at a given $Y$ gives us that point in screen space $\mathbb{Z}^2$

And given the way it is set up we know this will only generate values with in the range of 

$$ \text{interpolate}(Y, \vec{S}, \vec{E}) \in [\vec{S}_x, \vec{E}_x] $$


<details>
  <summary>
    Python Implementation
  </summary>
  
  ```py
    def interpolate_triangle(y, point_start, point_end) -> int:
      # This is to ensure division by zero doesn't happen.
      if point_end[1] == point_start[1]:
          return point_start[0]
  
      vertical_dist =  (y - point_start[1])
      slope_of_points = (point_end[0] - point_start[0]) / (point_end[1] - point_start[1])
  
      return int(
          point_start[0] + vertical_dist*slope_of_points
      )
  ```
</details>

## Actually Rasterizing 
Now armed with the interpolation function, we can start filling in our triangle.

Since we know that our $Y$ value lives in the interval of 

$$Y \in [\vec{S}_y, \vec{E}_y]$$ 

Then we can go ahead and step through each of those values.

The good thing to remember is that the interpolate function gives back an integer in the range of 

$$\text{interpolation}(Y, \vec{S}, \vec{E}) \in [\vec{S}_x, \vec{E}_x]$$

A thing to also note is that we mentioned sorting our vertices to have the one with the highest $y$ component as the starting point. So we always know we are drawing down. 

So lets go ahead and try and fill it in knowing all of this. 

$$
  left = \text{interpolate}(Y, \vec{v}_0, \vec{v}_1)
$$

And our right 

$$
  right = \text{interpolate}(Y, \vec{v}_0, \vec{v_2}) 
$$

A good thing to note about our interpolation function is that it doesn't know what an edge is so our left and right values might be reversed and we want them to go along in one direction. 

So we can easily fix that via.

$$
  left = min(left, right)
$$

and

$$
  right = max(left, right)
$$


now using this we can just set each point on our screen at each $x\in [left, end]$

<details>
  <summary>
    Python Implementation
  </summary>
  
 ```py
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
 ```
</details>


and we should end up with something like this

https://github.com/user-attachments/assets/d8fb783a-3c2b-4753-a5c0-38ca5a4cc735

Which is pretty darn close!

The issue is we are only rendering triangles that lay in a spacific way. In order to render the other half of the triangles we'll have to do the same process we did for the interval from 

$$
  Y \in [\vec{v}_1, \vec{v}_2]
$$


The middle vertex $v_1$ creates a kink in the left edge of the triangle. Our interpolation function draws straight lines, so it can't follow that kink in one pass thus we split it at $v_1$ and draw to $v_2$ to fill it in.

<details>
  <summary>
    Python Implementation
  </summary>
  
 ```py
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
 ```
</details>

And with that we should have our complete model being rendered!



And this is looking pretty good now!

# Lighting

We have a pretty good renderer now but lets give it some lighting as a cherry on top.

Lets define a Light as some position in world space $\vec{\ell}$.

We want the direction of this light so actually only consider the unit vector of this light $\hat{\ell}$.

Since we know that the face most facing the light source will have the highest intensity of light, we know the norm of our face has to be similar to the unit vector of the light. 
<p align = "center">
    <img width="602" height="289" alt="image" src="https://github.com/user-attachments/assets/22cb4de9-b2fc-408f-b63b-7ca0e753b0b3" />
</p>
To do this we can use a similar formula we used for culling which will check how similar the dot product is to the light.

So we'll Let $\hat{norm}$ be the unit vector for the norm of the face, $t$ the triangle with vertexs $t_0, t_1, t_2$ and the light unit vector $$\hat{\ell}$

$$
  \text{light intensity} = max(0, \vec{norm} \cdot \hat{\ell})
$$

However this doesn't work if the normal is on the back of the model so we need to back cull for the lighting by flipping the normal
for it based on if the face is front facing the light.

$$
\text{light intensity} = \begin{cases}
     max(0, \vec{norm} \cdot \hat{\ell}) , & \hat{norm} \cdot (\vec{t} - \hat{\ell}) < 0 \\
     max(0, -\vec{norm} \cdot \hat{\ell}), & \text{otherwise}
\end{cases}
$$



<details>
  <summary>
    Python Implementation
  </summary>
  
 ```py
light_vec = matrixs.unit_vector(light_vec)
if np.dot(normal, tri[0][:3] - light_vec) < 0:
    light_intensity = max(0, np.dot(normal, light_vec))
else:
    light_intensity = max(0, np.dot(-normal, light_vec))  # flip normal for back face
 ```
</details>

And this does give us the correct light intesnity values. However how do we actually apply it?

Well we apply it through the rendered face's color. 

Let $\vec{c}$ be a color vector with the values

$$
  \vec{c} = \begin{bmatrix}
    r \\
    g \\
    b \\
  \end{bmatrix}
$$

now we want to multiply this by our color intensity which is a scalar value so we just multiply each coordinate by it.

The good thing to know is that color values are in the interval from $[0, 255]$ and they are discrete values so we need to `clamp` each coordinate in our color vector by that amount so our final matrix should look like.

$$
  (\vec{c})(\text{light intensity}) = \begin{bmatrix}
    \lfloor clamp(r(\text{light intensity}), 0, 255) \rfloor  \\
    \lfloor clamp(g(\text{light intensity}), 0, 255) \rfloor \\
    \lfloor clamp(b(\text{light intensity}), 0, 255) \rfloor \\
  \end{bmatrix}
$$

<details>
  <summary>
    Python Implementation
  </summary>
  
 ```py
def apply_light(color, intensity):
    r, g, b = color
    r = int(clamp(r * intensity, 0, 255))
    g = int(clamp(g * intensity, 0, 255))
    b = int(clamp(b * intensity, 0, 255))
    return (r, g, b)
 ```
</details>

The purppose of the `clamp` function is to ensure a value is between two other values and we can do that via

So clamp functions like $\text{clamp}: \mathbb{R} \to [a, b]$

$$
  \text{clamp}(x, a, b) = max(a, min(b, x))
$$

<details>
  <summary>
    Python Implementation
  </summary>
  
 ```py
def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))
 ```
</details>

And with all of that lets see some nice renderering!

https://github.com/user-attachments/assets/f5e73c7d-e22d-47c0-aef9-b7fa5d95b54b

# Depth buffering

So far our renderer looks really great!

However there is a pretty serious underling issue and that's for elements that are back facing can get rendered on top of our front facing elements and within the case of the case of the torus you can see it pretty well.

https://github.com/user-attachments/assets/cee35fff-bc25-4e3b-89c7-88c02136c100

The easiest way of fixing this is to insure that the elements that are closest to the camera get rendered last ensuring that we will see the closest faces. 

So to find the average depth of a face we'll have to average the three cordinate making up that face and since all faces are triangles it'll be the average of each vertex. So we'll take the triangle $t$ with vertexs $\vec{a}, \vec{b}, \vec{c}$

$$
  avg_{z} = \frac{a_z + b_z + c_z}{3}
$$
  
We can then collect these averages and sort them in ascending order, and the reason we do this is that the way we have this set up is for translating in a negative direction. Meaning that our closest elements would come first; however, this does mean that translating into a different sign would change how culling and lighting bounds would work. This is actually a design decision made by all renderers to make these calculations easier. 



And with this we can just sort our accumalated list of $avg_z$ and display them and we should get something like this.

<details>
  <summary>
    Python Implementation
  </summary>
  
 ```py
 prioirty_tris.sort(key=lambda t: t[0], reverse=False)

    #Draw each triangle.
    for avg_z, light_intensity, tri in prioirty_tris:
        fill_triangle(screen, tri, (255, 0, 0), light_intensity)
 ```
</details>


https://github.com/user-attachments/assets/5ebfd9c4-769e-4782-8c17-b711c4c81b8e

# Fin

Hopefully that helps!

Below you can see the full render implementation
<details>
  <summary>
    Python Implementation
  </summary>
  
 ```py
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
 ```
</details>
