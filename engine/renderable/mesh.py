import numpy as np
from OpenGL.GL import *
from OpenGL.error import NullFunctionError
from engine.renderable.material import Material

class Mesh:
    def __init__(self, data, materialData):
        indicesList = self.__getIndicesList(data['faces'])
        self.__indicesLen = len(indicesList)
        indicesData = np.array(indicesList, dtype=np.uint32)
        vertexData = np.array(data['vertices'], dtype=np.float32)
        normalData = np.array(data['normals'], dtype=np.float32)
        self.material = Material(materialData)

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicesData, GL_STATIC_DRAW)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertexData, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        self.VBO_N = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_N)
        glBufferData(GL_ARRAY_BUFFER, normalData, GL_STATIC_DRAW)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def __getIndicesList(self, assimpIndices):
        indicesList = []
        for face in assimpIndices:
            for indice in face:
                indicesList.append(indice)
        return indicesList

    def draw(self, program):
        self.material.draw(program)
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.__indicesLen, GL_UNSIGNED_INT, None)

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteVertexArrays(1, self.VAO)
            glDeleteBuffers(1, self.VBO)
            glDeleteBuffers(1, self.VBO_N)
            glDeleteBuffers(1, self.EBO)
            self.VBO, self.VBO_N, self.EBO, self.VAO = 0, 0, 0, 0
        except (NullFunctionError, TypeError):
            pass 
