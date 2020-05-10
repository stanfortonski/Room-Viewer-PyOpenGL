from OpenGL.GL import *
from OpenGL.error import NullFunctionError

class CubeDepthbuffer:
    def create(self, width, height):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)
        for i in range(6):
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_DEPTH_COMPONENT, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

    def attach(self):
        glFramebufferTexture(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, self.texture, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)

    def bind(self):
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)

    def unbind(self):
        glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteTextures(1, self.texture)
            self.texture = 0
        except (NullFunctionError, TypeError):
            pass