import pygame
import moderngl
import numpy as np
from aiden3drenderer import obj_loader
import math

def perspective(fov_deg, aspect, near, far):
    f = 1.0 / math.tan(math.radians(fov_deg) / 2.0)

    return np.array([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
        [0, 0, -1, 0]
    ], dtype='f4')

def view_matrix(position):
    x, y, z = position
    return np.array([
        [1, 0, 0, -x],
        [0, 1, 0, -y],
        [0, 0, 1, -z],
        [0, 0, 0,  1]
    ], dtype='f4')

def rotation_y(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1]
    ], dtype='f4')

def rotation_x(angle, prev_rot=None):
    c = math.cos(angle)
    s = math.sin(angle)
    rot_x = np.array([
        [1, 0, 0, 0],
        [0, c,-s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype='f4')

    if prev_rot is not None:
        return rot_x @ prev_rot
    return rot_x

pygame.init()
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

program = ctx.program(
    vertex_shader="""
        #version 330

        in vec3 in_vert;
        in vec3 in_color;

        uniform mat4 projection;

        uniform mat4 view;

        out vec3 v_color;

        void main() {
            v_color = in_color;
            gl_Position = projection * view * vec4(in_vert, 1.0);
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

obj = obj_loader.get_obj("./assets/cobe.obj")

vertices3D = np.array(obj[0])

verts = []
vert_len = len(vertices3D)
i = 0
for x, y, z in vertices3D:
    verts.append([x, y, z, np.random.randint(0,255)/255, np.random.randint(0,255)/255, np.random.randint(0,255)/255])
    #verts.append([x, y, z, i/(vert_len), 0, i/(vert_len)])
    i += 1

vertices = np.array(verts, dtype="f4")

indicies = np.array(obj[1])

camera_pos = np.array([0.0, 0.0, 5.0])
camera_facing = np.array([0.0, 0.0]) # 0 = pitch, 1 = yaw

view = view_matrix(camera_pos)
program['view'].write(view.T.tobytes())

proj = perspective(60, 800/600, 0.1, 100.0)
program['projection'].write(proj.T.tobytes())

vbo = ctx.buffer(vertices.tobytes())
ibo = ctx.buffer(indicies.astype("i4").tobytes())

vao = ctx.vertex_array(program, [(vbo, "3f 3f", "in_vert", "in_color")], index_buffer=ibo)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    dt = clock.tick(120) / 1000.0
    speed = 3.5 * dt
    turn_speed = 1.8 * dt

    yaw = camera_facing[1]
    forward_x = math.sin(yaw)
    forward_z = -math.cos(yaw)
    right_x = math.cos(yaw)
    right_z = math.sin(yaw)

    if keys[pygame.K_w]:
        camera_pos[0] += forward_x * speed
        camera_pos[2] += forward_z * speed
    if keys[pygame.K_s]:
        camera_pos[0] -= forward_x * speed
        camera_pos[2] -= forward_z * speed
    if keys[pygame.K_a]:
        camera_pos[0] -= right_x * speed
        camera_pos[2] -= right_z * speed
    if keys[pygame.K_d]:
        camera_pos[0] += right_x * speed
        camera_pos[2] += right_z * speed

    if keys[pygame.K_RIGHT]:
        camera_facing[1] -= turn_speed
    if keys[pygame.K_LEFT]:
        camera_facing[1] += turn_speed
    if keys[pygame.K_UP]:
        camera_facing[0] = min(camera_facing[0] + turn_speed, 1.4)
    if keys[pygame.K_DOWN]:
        camera_facing[0] = max(camera_facing[0] - turn_speed, -1.4)

    r_y = rotation_y(-camera_facing[1])
    rot = rotation_x(-camera_facing[0], r_y)
    trans = view_matrix(camera_pos)
    view = rot @ trans
    program['view'].write(view.T.tobytes())

    ctx.clear(0.0, 0.0, 0.0, 1.0)
    ctx.viewport = (0, 0, 800, 600)
    vao.render(moderngl.TRIANGLES)

    pygame.display.flip()

pygame.quit()