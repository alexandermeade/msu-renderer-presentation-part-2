# Info 
This is a continuation of the "Building a cpu renderer" series. The first part of which can be found [here](https://github.com/alexandermeade/msu-renderer-presentation)

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

The cross product notated as ${\vec{v}\mathrel{\times} \vec{r}}$ is an oepration used to get the line perpendicular to two other lines.

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

This determinate form gives us what we need from the cross product but can be dense if you don't know how to solve for a determinate. The good news is since we are using `NumPy` this operation is already predefined as `np.cross(vector1, vector2)`

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
One big issue that exist with our renderer is that it draws every single triangle even if we shouldn't see it. We can fix it using culling.

Culling utalizes the cross product to produce a vector that points orthogonal to a triangles face leaving us with a sense of where it is facing.

To do this we first need to construct the face of the triangle and we can do that we let $t_{n}$ be our triangle at some $n$-th point.  

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

Now using the culling technique we can see in the diagram below that the green arrows are gonna be the normals for our faces and we want to see how aligned they are with our camera vector. 

<p align = "center">
  <img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/2a83915a-1014-41c8-8d4e-9d30f9d532dd" />
</p>

We can do this with a dot product.

Using our normal vector and our triangles positional coordinates we can take the first vertex of the triangle and subtract it by our camera's position

$$
  \vec{norm} \cdot ( \vec{t_0} - \vec{\text{cam}})
$$

Using the result above we can now know how aligned the norm is with our camera's line to the first vertex $t_0$. 

Since we are substracting from $t_0$ here our typical dot product interaction of $dot < 90$ being positive gets flipped so the result $dot < 90$ is negative and that's why we cull for the dot product being less than zero.

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


# Rasterization and interpolation.
