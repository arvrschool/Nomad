from OpenGL.GL import *
import numpy as np
import vectormath

class OBJ:
    def __init__(self, filename, swapyz=False, negateyz=True):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
 
        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = map(float, values[1:4])
                if swapyz:
                    v = [v[0], v[2], v[1]]
                if negateyz:
                    v = [v[0], -v[1], -v[2]]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
                    v = [v[0], v[2], v[1]]
                if negateyz:
                    v = [v[0], -v[1], -v[2]]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            #elif values[0] == 'mtllib':
                #self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)

                verts = map(lambda idx: self.vertices[idx-1], face)
                normal = np.cross(np.float32(verts[1]) - np.float32(verts[0]), np.float32(verts[2]) - np.float32(verts[0]))
                saturation = vectormath.angle_between(normal, [0, 0, -1]) / (2*np.pi)
                self.faces.append((face, norms, texcoords, material, saturation))
        self.normalizeVerts()
        
    def normalizeVerts(self):
        max_val = 1
        for v in self.vertices:
            if max_val < v[0]:
                max_val = v[0]
            if max_val < v[1]:
                max_val = v[1]

        for v in self.vertices:
            v[0] /= max_val
            v[1] /= max_val
            v[2] /= max_val
