# Info 
This is a continuation of the "Building a cpu renderer" series. The first part of which can be found [here](https://github.com/alexandermeade/msu-renderer-presentation)

# Math Prerequisites (Vector Operations)

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

