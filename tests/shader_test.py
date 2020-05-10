import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.base.shader import Shader

class ShaderTest(unittest.TestCase):
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
        shader = Shader('resources/shaders/test_vert.vs', GL_VERTEX_SHADER)
        shader.compile()
        self.assertNotEqual(shader.getId(), 0)

    def testShaderFileNotExist(self):
        try:
            shader = Shader('resources/shaders/not_exist.vs', GL_VERTEX_SHADER)
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

    def testCompileError(self):
        shader = Shader('resources/shaders/error.fs', GL_FRAGMENT_SHADER)
        self.assertRaises(RuntimeError, shader.compile)
        
if __name__ == '__main__':
    unittest.main()