import os, json, glm
import numpy as np
from OpenGL.GL import *
from engine.renderable.mesh import Mesh 

class Model:
    def __init__(self, path):
        self.meshes = []
        if not os.path.exists(path):
            raise RuntimeError(f'Model source file {path} does not exists.')
        self.path = path
        self.model = glm.mat4()
        data = self.__loadAndGetData()
        for i in range(len(data['meshes'])):
            meshData = data['meshes'][i]
            self.meshes.append(Mesh(meshData, data['materials'][meshData['materialindex']]['properties']))

    def __loadAndGetData(self):
        data = None
        with open(self.path) as file:
            data = json.load(file)
        return data

    def draw(self, program):
        program.use()
        program.setMat4('model', self.model)
        for mesh in self.meshes:
            mesh.draw(program)

    def __del__(self):
        self.delete()

    def delete(self):
        self.meshes.clear()