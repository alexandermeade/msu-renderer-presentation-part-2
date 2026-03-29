# The Goal of this Repo
A friendly walkthrough of how 3D rendering works from scratch, using Python. By the end you'll get a feel for the full graphics pipeline from loading a 3D model to getting it on screen. 

# What is a cpu renderer 
A CPU renderer is a primitive style of renderer mostly used to show off how a renderer works without having to worry about implementing the techniques for a GPU. 

There are heavy limitations put ontop of a CPU renderer and I would highly advise against using one for making anything serious. However most of these techniques should carry over if you were to use a tool like [Vulkan](https://www.vulkan.org/) or [OpenGL](https://www.opengl.org/) for GPU rendering. 

# Software Prequisites 
This tutorial was written using the [Python](https://www.python.org/) programming language with the [UV](https://docs.astral.sh/uv/guides/install-python/) package and project manager. 

> You do not need [UV](https://docs.astral.sh/uv/guides/install-python/) to complete this tutorial however python is essential.

The packages used in this tutorial are as follows
-  Pygame (Window and Rendering)
-  NumPy (Matrix Math)

The optional dependenices include
-  Pydantic (Better Data Representation)
-  Pathlib (Makes working with file paths nicer)


## What is a `.obj` file? 
An `.obj` file is a file type used for 3D models and is an export option in most modern 3D modeling software. For our purposes we'll be using [Blender](https://www.blender.org/) as that software.

In the example of the `cube.obj` file found in the [models](https://github.com/alexandermeade/msu-renderer-presentation/tree/main/models) subdirectory, we can open in it blender and it should look like this

<p align = "center">
  <img width="307" height="276" alt="image" src="https://github.com/user-attachments/assets/4c19b759-5f56-43dd-9ffb-38622da0183c" />
</p>

But we can export this using these settings. 
<p align = "center">
  <img width="262" height="400" alt="image" src="https://github.com/user-attachments/assets/f4a31ea5-342e-4ad0-a8d8-30b43a3c014e" />
</p>

> [!WARNING]
> Make sure to triangulate, if not the faces will generate in different pairings than what we would want.

When done correctly we should get to a result like
```
# Blender 3.6.5
# www.blender.org
o Cube
v 1.000000 1.000000 -1.000000
v 1.000000 -1.000000 -1.000000
v 1.000000 1.000000 1.000000
v 1.000000 -1.000000 1.000000
v -1.000000 1.000000 -1.000000
v -1.000000 -1.000000 -1.000000
v -1.000000 1.000000 1.000000
v -1.000000 -1.000000 1.000000
s 0
f 5 3 1
f 3 8 4
f 7 6 8
f 2 8 6
f 1 4 2
f 5 2 6
f 5 7 3
f 3 7 8
f 7 5 6
f 2 4 8
f 1 3 4
f 5 1 2
```

Looking at this we can pretty quickly see that each line starting with a `v` is gonna be some point in 3D space. Where as every `f` is gonna be some pairings of points to form a triangle. 

The way this cube gets subsected and rerendered back out in triangles looks like this with each triangle highlighted. 

<p align = "center">
  <img width="294" height="285" alt="image" src="https://github.com/user-attachments/assets/e27a2945-ff26-448c-961f-c15807859688" />
</p>


We can read this file using this algorithm

```py
lines:list[str] = self.path.read_text().splitlines()
render_buffer = RenderBuffer()
for line in lines: 
    line = line.strip()
    if line[0] == 'v':
        values = line[1:] 

        values:list[str] = values.strip().split(' ')
        float_values:list[float] = [] 
        
        for value in values:
            float_values.append(float(value))
        float_values.append(1)
        render_buffer.verts.append(float_values)
        continue

    if line[0] == 'f':
        values = line[1:] 

        values:list[str] = values.strip().split(' ')
        index_values:list[tuple[int, int, int]] = [] 
        
        for value in values:
            index_values.append(int(value) - 1)

        render_buffer.tris.append(tuple(index_values))
        continue
```

With `RenderBuffer` being a class for holding our vertexs and triangles.
```py
class RenderBuffer:
    verts: list[np.ndarray] 
    tris: list[tuple[int, int, int]] 

    def __init__(self):
      self.verts = []
      self.tris = []
    
    def __repr__(self):
        return f"vertexs: {self.verts}\nindex order {self.tris}"
```

Now you may notice that as we are appending the points into a vertexs we actually extend the vertexs by one extra coordiniate and we set it to 1 for all vertexs. The reason we do this is revealed later in the README. 


# Math Prerequisites 
As you have probably noticed when building a 3D renderer there is a pretty clear and hard issue that gets presented almost immeditatly.
How do we go from a set of vertexs $\mathbb{R}^4$ into a set of points on a screen $\mathbb{R}^2$. 

To do this we are going to utalize Linear Algebra which is a set of mathematics created for dealing with problems in $n$-th dimensional space via matrixs.

A few things to know about matrixs are the following. 

Matrixs are notated as a set of values within a number of rows and colmns
A $2\times 2$ example of a matrix would look like

$$
  M = \begin{bmatrix}
    1 & 2 \\
    3 & 4 
  \end{bmatrix}
$$

Matrix multiplication has an algoirthm to it and is preformed the way listed in the diagram below
<p align = "center">
  <img width="800" height="400" alt="Multiplication-of-3-by-3-Matrices-01" src="https://github.com/user-attachments/assets/0a96ca9c-3274-4d1d-815f-fb6a00c311dd" />
</p>
Matrix multiplication is not commutative meaning if A and B are matrixs and

$$A \not = B$$ $$ B \not = A^{-1}$$

then

$$
  AB \not = BA 
$$

Vectors are a special case of matrixs where there is a $1 \times n$ matrix.

$$
  \vec{v} = \begin{bmatrix} 
    x \\ 
    y \\ 
    \vdots \\
    n
    \end{bmatrix} 
$$

# Camera

A camera's job in rendering is to mimic looking through a camera at some kind of scene. So using that we can reflect some of the properties a camera will have. 

<p>
  <img width="800" height="400" alt="image" src="https://github.com/user-attachments/assets/500c8cbe-f1d3-4b37-b8ad-cd45dc1799a2" />
</p>

- `fov` aka field of view represents how wide of an angle you are capabale of seeing.
- `zfar` represents the far plane on the z-axis which shows how far away you can see something
- `znear` represents how close something can be to the camera and still be in your sight
- `width` and height represent the amount of space elegible for you to see. In this case the whole screen is what we want to see so we instantiate the `Camera` class with our screen's height and width.


```py 
@dataclass
class Camera: 
    fov: float
    zfar: float
    znear: float
    width: float
    height: float

    def aspect_ratio(self) -> float:
        return self.width/self.height
```


# Space

In 3D rendering we have two spaces we worry about and that is world space (Where our objects live) and screen space (Where we want them to be)

<p align = "center">
  <img width="526" height="571" alt="image"  src="https://github.com/user-attachments/assets/94ad4396-96a9-4901-95b7-9b660e4ed31b" />
</p>


# The Projection Matrix

The purpose of the Projection Matrix is to project our vertexs in $\mathbb{R}^4$ onto our screen of points which is of $\mathbb{R}^2$

Below is a more viual representation of what that would look like

<p align = "center">
  <img width="722" height="522" alt="image" src="https://github.com/user-attachments/assets/62c58ecd-8b50-45c1-8945-48648f8ac34b" />
</p>

Let $\theta = \text{Field of View}$

Let $a = \text{aspect ratio} = width / height$

Let $f = tan^{-1}(\theta / 2)$ 

$$ 
\begin{bmatrix} 
  \frac{f}{a} & 0 & 0 & 0\\
  0 & f & 0 & 0 \\
  0 & 0 & \frac{-z_{far} - z_{near}}{z_{far} - z_{near}} & -1 \\
  0 & 0 & -2\cdot \frac{z_{near} \cdot z_{far}}{z_{far} - z_{near}} & 0 \\
\end{bmatrix}
$$

We can represent this projection in Python using NumPy 

```py
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
```

Using the `cube.obj` file we should be able to produce the front of a cube through using the projected points of each vertex and then drawing it in order of the faces for each triangle (This is also known as the winding order)

So if we take each triangle we want to render as $t$ noting that each triangle has three points represneted as vectors.
We can project each point from the triangle using the projection matrix while notating each vertex of the triangle as $t_{n}$ like so

$$
  \vec{p_n} = (proj) (\vec{t_{n}})
$$

With this we have no offically gone from world space to screen space!

Now we are almost done with the matrix manipulation, We have our coordinates in the form of 

$$
  \vec{p_n} = \begin{bmatrix}
    x \\
    y \\
    z \\
    w
  \end{bmatrix}
$$

The issue is we still have yet to get to our end result of $\mathbb{R}^4 \to \mathbb{R}^2$ 

To do this we must normalize or coordinates into $\mathbb{R}^2$ and this is done via

$$
  \vec{p_n}\prime = \begin{bmatrix}
    x' \\
    y' \\
    z' \\
    1
  \end{bmatrix} = \begin{bmatrix}
    x/w \\
    y/w \\
    z/w \\
    w/w
  \end{bmatrix} 
$$

You may notice that we still have $z'$ here in our "$\mathbb{R}^2$" vector and that's because $z'$ represents the depth in relation to our $z_{near}$ and $z_{far}$ planes, so $x'$ and $y'$ are the only things accounting for location here. So we can effectivly ignore $z'$ for drawing and only worry about $x'$ and $y'$

With our new $\vec{p_n}'$ we now have a vertex of the triangle in screen coordinates which means we can draw the pixel (I lied). What we actually have is the projected coordinate into normalized device coordinates meaning that our point will be in the interval of $(-1, 1)$ on the screen. 

So if we want to scale it to our resolution we must multiply it using this formula

$$
  x_{\text{screen}} = \left\lfloor \frac{x' + 1}{2} \cdot \text{screen width} \right\rfloor
$$
$$
  y_{\text{screen}} = \left\lfloor 1 - \frac{y' + 1}{2} \cdot \text{screen height} \right\rfloor 
$$

We floor it here because screen space exists as a grid of cells meaning that our coordinates must be in $\mathbb{Z}^2$.


Now we have gotten to the part of glory! we can finally draw each vertex of each triangle onto the screen!

```py
width, height = screen.get_size()
screen_points = []

for p in projected_points:
    # p is gonna be of the form [x, y, z, w]
    # We then normalize x and y with w to fit it onto R^2
    if p[3] != 0:
        x_ndc = p[0] / p[3]  # Normalize x via x' = x/w
        y_ndc = p[1] / p[3]  # Normalize y via y' = y/w
    else:
        x_ndc, y_ndc = 0, 0
    

    # convert from normalized device coords (-1..1) to screen coordinates
    x_screen = int((x_ndc + 1) * 0.5 * width)
    y_screen = int((1 - (y_ndc + 1) * 0.5) * height)  # flip y-axis
    screen_points.append((x_screen, y_screen))
# draw triangle lines
pygame.draw.polygon(screen, color, screen_points, width=1) 
```

If you draw it the way followed here you may arrive at a similar result to what is below. 

<p align = "center">
  <img width="796" height="632" alt="image" src="https://github.com/user-attachments/assets/5e651f9a-77ba-4e46-b323-838e3b3217dd" />
</p>
