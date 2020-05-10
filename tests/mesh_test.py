import sys, unittest, glfw
sys.path.insert(0, '..')
from OpenGL.GL import *
from engine.renderable.mesh import Mesh

class MeshTest(unittest.TestCase):
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

    def testMesh(self):
        data = {
            'vertices': [1, 2, 3],
            'faces': [[1]],
            'normals': [1, 2, 3]
        }

        materialData = [0, 0,
            {'value': [1, 2, 3]},
            {'value': [1, 2, 3]},
            {'value': [1, 2, 3]},
            {'value': 2}
        ]

        mesh = Mesh(data, materialData)
        self.assertNotEqual(mesh.VAO, 0)
        self.assertNotEqual(mesh.VBO, 0)
        self.assertNotEqual(mesh.VBO_N, 0)
        self.assertNotEqual(mesh.EBO, 0)

if __name__ == '__main__':
    unittest.main()