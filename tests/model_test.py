import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.renderable.model import Model

class ModelTest(unittest.TestCase):
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

    def testModel(self):
        model = Model('resources/models/monkey.json')
        self.assertEqual(len(model.meshes), 1)

    def testNoExistsModel(self):
        try:
            model = Model('resources/models/not.json')
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()