import glfw, glm, math, json
from OpenGL.GL import *
from engine.base.program import Program
from engine.base.shader import Shader
from engine.renderable.model import Model
from engine.renderable.shadow import Shadow

with open('config.json') as file:
    config = json.load(file)

width, height = config['window_width'], config['window_height']

def main():
    if not glfw.init():
        print('Failed to initialize GLFW.')
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.SAMPLES, config['sampling_level'])
    
    if config['fullscreen']:
        global width, height
        mode = glfw.get_video_mode(glfw.get_primary_monitor())
        width, height = mode.size.width, mode.size.height
        window = glfw.create_window(mode.size.width, mode.size.height, config['app_name'], glfw.get_primary_monitor(), None)
    else:
        window = glfw.create_window(width, height, config['app_name'], None, None)
    if not window:
        print('Failed to create GLFW Window.')
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, resizeCallback)
    glfw.set_key_callback(window, keyCallback);

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

    program = Program()
    program.attachShader(Shader('resources/shaders/vert.vs', GL_VERTEX_SHADER))
    program.attachShader(Shader('resources/shaders/frag.fs', GL_FRAGMENT_SHADER))
    program.link()

    depthProgram = Program()
    depthProgram.attachShader(Shader('resources/shaders/depth.vs', GL_VERTEX_SHADER))
    depthProgram.attachShader(Shader('resources/shaders/depth.gs', GL_GEOMETRY_SHADER))
    depthProgram.attachShader(Shader('resources/shaders/depth.fs', GL_FRAGMENT_SHADER))
    depthProgram.link()

    shadow = Shadow(config['near_plane'], config['far_plane'])
    shadow.create(config['shadow_width'], config['shadow_height'])

    lightPos = glm.vec3(0, 2, 0)
    viewPos = glm.vec3(0, 0.5, 0)
    perspective = glm.perspective(45, width/height, config['near_plane'], config['far_plane'])

    room = Model('resources/models/room.json')
    room.model = glm.rotate(glm.mat4(), glm.radians(160), glm.vec3(0, 1, 0)) # bugfix

    lastTime = glfw.get_time()
    while not glfw.window_should_close(window):
        if config['debug_mode']:
            print(glGetError())
        currentTime = glfw.get_time()
        deltaTime = currentTime - lastTime
        lastTime = currentTime

        camX = math.sin(currentTime*0.2)
        camZ = math.cos(currentTime*0.2)
        viewDir = glm.vec3(camX, -0.3, camZ)
        view = glm.lookAt(viewPos, viewPos + viewDir, glm.vec3(0, 1, 0))

        shadow.castShadow(depthProgram, lightPos)
        room.draw(depthProgram)
        shadow.endCastShadow(program)

        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        program.use()
        program.setMat4('viewProject', perspective * view)
        program.setVec3('viewPos', viewPos)
        program.setVec3('lightPos', lightPos)
        room.draw(program)

        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()

def resizeCallback(window, w, h):
    global width, height
    width, height = w, h
    perspective = glm.perspective(45, width/height, config['near_plane'], config['far_plane'])

def keyCallback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, glfw.TRUE);

if __name__ == '__main__':
    main()