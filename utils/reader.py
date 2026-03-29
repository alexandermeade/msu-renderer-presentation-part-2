from pathlib import Path
import numpy as np

class RenderBuffer:
    verts: list[np.ndarray] 
    tris: list[tuple[int, int, int]]
    
    def __init__(self):
        self.verts = []
        self.tris = []
    def __repr__(self):
        return f"vertexs: {self.verts}\nindex order {self.tris}"

class ObjReader: 
    path: Path

    def __init__(self, filepath: str):
        self.path = Path(filepath)

    def parse(self) -> RenderBuffer:
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

        return render_buffer
    
