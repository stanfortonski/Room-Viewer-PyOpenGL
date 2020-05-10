import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.base.shader import Shader
from engine.base.program import Program

class ProgramTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        cls.window = glfw.create_window(600, 400, 'Test', None, None)
        glfw.make_context_current(cls.window)

    @classmethod
    def tearDownClass(cls):
        glfw.terminate()

    def testCompile(self):
        try:
            program = Program()
            program.attachShader(Shader('resources/shaders/test_vert.vs', GL_VERTEX_SHADER))
            program.attachShader(Shader('resources/shaders/test_frag.fs', GL_FRAGMENT_SHADER))
            program.link()
            self.assertNotEqual(program.getId(), 0)
        except RuntimeError:
            self.assertTrue(False)

    def testErrorCompile(self):
        try:
            program = Program()
            program.attachShader(Shader('resources/shaders/test_vert.vs', GL_VERTEX_SHADER))
            program.attachShader(Shader('resources/shaders/error.fs', GL_FRAGMENT_SHADER))
            program.link()
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()