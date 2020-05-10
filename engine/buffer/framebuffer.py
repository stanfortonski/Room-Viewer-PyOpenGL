import sys
from OpenGL.GL import *
from OpenGL.error import NullFunctionError

class Framebuffer:
    def create(self, buffer):
        self.FBO = glGenFramebuffers(1)
        self.bind()
        buffer.bind()
        buffer.attach()

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print('Error when creating Framebuffer.')
            sys.exit(1)
        self.unbind()

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def __del__(self):
        self.delete()

    def delete(self):
        try:
            glDeleteFramebuffers(1, self.FBO)
            self.FBO = 0
        except (NullFunctionError, TypeError):
            pass
