import pygame
import math
import random


# Constants
WIDTH = 1200  # 1200
HEIGHT = 500  # 500
GRAVITY = 0.5  # Gravity effect
BOUNCE_FACTOR = 0.7  # Energy loss on bounce
FPS = 60
TIME = .05

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
RED = (255, 0, 0)
LIME_GREEN = (50, 205, 50)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()

font = pygame.font.Font(None, 30)
trajectory_autoclear = True
pointer_radius = 3
two_lines = True
trajectory_highligher = False

# Variables
# fix_checker = 0
fix_value_axis = ()


# Main screen
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion")

# Value screen
value_screen_height = 200
value_screen_width = 300

value_screen = pygame.Surface(
    (value_screen_width, value_screen_height))
value_screen_react = value_screen.get_rect()
value_screen_react.topleft = (3, 3)
value_screen.fill(GREY)

# Trajectory screen
trajectory_screen = pygame.Surface((WIDTH, HEIGHT))
trajectory_screen.fill(GREY)
MAX_TRAJECTORY_POINTS = 1000


class Ball(object):
    def __init__(self, x, y, radius, color, max_range, max_height, mrf=[], mhf=[], trajectory=[]):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.max_range = max_range
        self.max_height = max_height
        self.trajectory = trajectory
        self.velocity_y = 0
        self.lock_x = False
        self.lock_y = False
        # self.lock_c = values = 0
        self.fix_checker = 0
        self.temp_pos_checker = False
        self.temp_pos = ()
        self.mrf = mrf
        self.mhf = mhf

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius - 1)

    @staticmethod
    def ball_path(start_x, start_y, power, angle, time):
        vel_x = math.cos(angle) * power
        vel_y = math.sin(angle) * power

        dis_x = vel_x * time
        dis_y = (vel_y * time) + ((-4.9 * (time**2)) / 2)
        # dis_y = (vel_y * time) - (0.5 * GRAVITY * time**2)

        new_x = round(dis_x + start_x)
        new_y = round(start_y - dis_y)

        return new_x, new_y, dis_x, dis_y


def redraw_window():
    win.fill(GREY)
    gb.draw(win)
    win.blit(value_screen, value_screen_react)

    pygame.draw.line(win, (0, 0, 0), line[0], line[1])
    draw_line(pos)
    # gravity_bounc()

    # trajectory()
    pygame.display.update()


def find_angle(pos):
    x = gb.x
    y = gb.y

    mouse_x, mouse_y = pos[0], pos[1]

    try:
        angle = math.atan((y - mouse_y) / (x - mouse_x))
    except:
        angle = math.pi / 2

    if mouse_y < y and mouse_x > x:
        angle = abs(angle)
    elif mouse_y < y and mouse_x < x:
        angle = math.pi - angle
    elif mouse_y > y and mouse_x < x:
        angle = math.pi + abs(angle)
    elif mouse_y > y and mouse_x > x:
        angle = (math.pi * 2) - angle

    return angle  # In randain


def draw_line(pos):
    # global mrf, mhf
    x, y = pos
    axis = font.render(str(f"{x}, {y}"), False, WHITE, GREY)
    degree = math.degrees(angle)
    degree = font.render(f"Angle:'{str(round(degree, 4))}", True, WHITE, GREY)
    real_time_degree = math.degrees(find_angle(pos))
    real_time_degree = font.render(
        f"Real Time Angle: {str(round(real_time_degree, 4))}", True, WHITE, GREY)
    gb.mrf.append(gb.max_range)
    gb.mhf.append(gb.max_height)
    gb.max_range = max(gb.mrf)
    gb.max_height = max(gb.mhf)

    print(type(gb.max_height), type(gb.max_range))

    # mrf, mhf = [], []

    max_height = font.render(
        f"Max height: {str(round(gb.max_height, 3))}", True, WHITE, GREY)
    max_range = font.render(
        f"Max Range: { str(round(gb.max_range, 3))}", True, WHITE, GREY)

    value_screen.blit(axis, (10, 10))
    value_screen.blit(degree, (10, 40))
    value_screen.blit(max_height, (10, 70))
    value_screen.blit(max_range, (10, 100))
    value_screen.blit(real_time_degree, (10, 130))

    if two_lines:
        pygame.draw.line(win, RED, (0, pos[1]), (WIDTH, pos[1]))  # Horizontal
        pygame.draw.line(win, GREEN, (pos[0], 0), (pos[0], HEIGHT))  # Vertical
        # pygame.draw.line(win, WHITE, pos, (gb.x, gb.y))  # Hipotenise

    if len(gb.trajectory) > 1:
        # Draw lines between points
        pygame.draw.lines(win, BLUE, False, gb.trajectory, 2)

    if len(gb.trajectory) > MAX_TRAJECTORY_POINTS:
        gb.trajectory.pop(0)  # Remove the oldest point


"""    if trajectory_highligher:
        color = []
        for i in range(len("RAM")):
            color.append(random.randrange(0, 255))
        for points in gb.trajectory:
            pygame.draw.circle(win, tuple(
                color), (points[0], points[1]), radius=pointer_radius)

    else:
        for points in gb.trajectory:
            pygame.draw.circle(
                win, RED, (points[0], points[1]), radius=pointer_radius)"""


def tempp_pos(pos):
    if gb.temp_pos_checker == False:
        gb.temp_pos_checker = True
        gb.temp_pos = pos
    else:
        return None


def locker(pos):
    # tem_pos = pygame.mouse.get_pos()
    tem_pos = tempp_pos(pos)
    if tem_pos == None:
        pos = pygame.mouse.get_pos()
    elif gb.lock_x:
        pos = (tem_pos[0], pygame.mouse.get_pos()[1])
    elif gb.lock_y:
        pos = (pygame.mouse.get_pos()[0], tem_pos[1])
    else:
        pos = pygame.mouse.get_pos()

    pygame.display.update()


def gravity_bounc():
    gb.y += gb.velocity_y
    gb.velocity_y += GRAVITY  # Apply gravity effect

    # Check for collision with ground
    if gb.y >= HEIGHT - 10 - gb.radius:  # 10 pixels for the ground
        gb.y = HEIGHT - 10 - gb.radius  # Place the ball on the ground
        # Reverse and reduce velocity for bounce
        gb.velocity_y = -gb.velocity_y * BOUNCE_FACTOR
        if abs(gb.velocity_y) < 1:  # Stop bouncing if the velocity is small enough
            gb.velocity_y = 0


run = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()
gb = Ball(300, 494, 5, (255, 255, 255), 0, 0)

gb = Ball(300, 494, 5, (255, 255, 255), 0, 0)
while run:
    pos = pygame.mouse.get_pos()
    if shoot:
        draw_line(pos)

        if gb.y < 500 - gb.radius:
            time += .1
            new_ball_pos = Ball.ball_path(x, y, power, angle, time)
            gb.x = new_ball_pos[0]
            gb.y = new_ball_pos[1]
            gb.max_range = new_ball_pos[2]
            gb.max_height = new_ball_pos[3]
            gb.trajectory.append((gb.x, gb.y))
        else:
            shoot = False
            time = 0
            gb.y = 494

    line = [(gb.x, gb.y), pygame.mouse.get_pos()]

    redraw_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                trajectory_autoclear = not trajectory_autoclear

            elif event.key == pygame.K_c:
                gb.trajectory = []
                gb.mrf = []
                gb.mhf = []
                win.fill(GREY)

            elif event.key == pygame.K_h:
                trajectory_highligher = not trajectory_highligher

            elif event.key == pygame.K_KP_PLUS:
                pointer_radius += 1

            elif event.key == pygame.K_KP_MINUS:
                if pointer_radius >= 1:
                    pointer_radius -= 1

            elif event.key == pygame.K_t:
                two_lines = not two_lines

            elif event.key == pygame.K_q:
                gb.lock_x = not gb.lock_x

            elif event.key == pygame.K_x:
                if gb.fix_checker == 0:
                    locker(pos)
                    gb.fix_checker = 1
                    # print("x toggeled")

            elif event.key == pygame.K_y:
                if gb.fix_checker == 0:
                    gb.lock_y = not gb.lock_y
                    gb.fix_checker = 1

            else:
                # print(fix_value_axis)
                pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            if trajectory_autoclear:
                # Debugging
                print("Clearing trajectory, mrf, and mhf")
                gb.trajectory = []
            gb.max_range = .0
            gb.max_height = .0
            # print("After clearing:", gb.trajectory,
            #   gb.mrf, gb.mhf)  # Debugging

            pygame.display.flip()
            if not shoot:
                # if True:
                x = gb.x
                y = gb.y
                shoot = True
                power = math.sqrt((line[1][1] - line[0][1])
                                  ** 2 + (line[1][0] - line[0][1])**2)/8
                angle = find_angle(pos)

pygame.quit()
quit()
