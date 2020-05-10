import glm
from OpenGL.GL import *
from engine.buffer.cubedepthbuffer import CubeDepthbuffer
from engine.buffer.framebuffer import Framebuffer

class Shadow:
    def __init__(self, nearPlane, farPlane):
        self.nearPlane = nearPlane
        self.farPlane = farPlane
    
    def create(self, width, height):
        self.width = width
        self.height = height
        self.depthbuffer = CubeDepthbuffer()
        self.framebuffer = Framebuffer()
        self.depthbuffer.create(width, height)
        self.framebuffer.create(self.depthbuffer)

    def castShadow(self, depthProgram, lightPos):
        self.lightPos = lightPos
        depthProgram.use()
        depthProgram.setFloat('farPlane', self.farPlane)
        depthProgram.setVec3('lightPos', self.lightPos)
        transforms = self.__getTransforms()
        for i in range(6):
            depthProgram.setMat4(f'shadowMatrices[{i}]', transforms[i])

        glViewport(0, 0, self.width, self.height)
        self.framebuffer.bind()
        glClear(GL_DEPTH_BUFFER_BIT)

    def endCastShadow(self, program):
        self.framebuffer.unbind()
        program.use()
        program.setFloat('farPlane', self.farPlane)
        program.setInt('depthMap', 0)
        glActiveTexture(GL_TEXTURE0)
        self.depthbuffer.bind()

    def __getTransforms(self):
        st = []
        pos = self.lightPos
        proj = glm.perspective(glm.radians(90), 1, self.nearPlane, self.farPlane)
        st.append(proj * glm.lookAt(pos, pos + glm.vec3(1, 0, 0),  glm.vec3(0, -1, 0)))
        st.append(proj * glm.lookAt(pos, pos + glm.vec3(-1, 0, 0), glm.vec3(0, -1, 0)))
        st.append(proj * glm.lookAt(pos, pos + glm.vec3(0, 1, 0),  glm.vec3(0, 0, 1)))
        st.append(proj * glm.lookAt(pos, pos + glm.vec3(0, -1, 0), glm.vec3(0, 0, -1)))
        st.append(proj * glm.lookAt(pos, pos + glm.vec3(0, 0, 1),  glm.vec3(0, -1, 0)))
        st.append(proj * glm.lookAt(pos, pos + glm.vec3(0, 0, -1), glm.vec3(0, -1, 0)))
        return st

    def delete(self):
        self.framebuffer.delete()
        self.depthbuffer.delete()