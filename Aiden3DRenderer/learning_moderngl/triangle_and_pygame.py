import pygame
import moderngl
import numpy as np

pygame.init()
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

program = ctx.program(
    vertex_shader="""
        #version 330

        in vec2 in_vert;
        in vec3 in_color;

        out vec3 v_color;

        void main() {
            v_color = in_color;
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    """,
    fragment_shader="""
        #version 330

        in vec3 v_color;

        out vec3 f_color;

        void main() {
            f_color = v_color;
        }
    """,
)

draw_surf = pygame.Surface((800, 600))

x = np.linspace(-1.0, 1.0, 50)
y = np.random.rand(50) - 0.5
r = np.zeros(50)
g = np.ones(50)
b = np.zeros(50)

vertices = np.array([
    [-0.5,-0.5,1,0,0],
    [0.5,-0.5,0,1,0],
    [0.0,0.5,0,0,1]
])

print(vertices)

indicies = np.array(
    [0,1,2]
)

vbo = ctx.buffer(vertices.astype("f4").tobytes())
ibo = ctx.buffer(indicies.astype("i4").tobytes())

vao = ctx.vertex_array(program, vbo, "in_vert", "in_color", index_buffer=ibo)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.clear(0.0, 0.0, 0.0, 1.0)
    ctx.viewport = (0, 0, 800, 600)
    vao.render(moderngl.TRIANGLES)

    pygame.display.flip()

pygame.quit()