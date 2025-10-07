import pygame, math, time, sys, random, copy
from pygame import gfxdraw
from pygame.color import THECOLORS
import pygame.freetype



time_scale = 10000
precision = 10





global G
global px

G = 6.674*(10**-11)
px = 1000 # 1px = 1000km

'''
def draw_circle(surface, x, y, radius, color):
    x = int(x)
    y = int(y)
    radius = int(radius)
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)
'''

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def normalize(vector):
    mag = math.sqrt(vector[0]**2+vector[1]**2)
    norm_vector = [vector[0]/mag, vector[1]/mag]
    return norm_vector

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

class Planet:
    def __init__(self, radius, mass, position, velocity, color):
        self.radius = radius # * km
        self.mass = mass # kg 
        self.position = position
        self.velocity = velocity # m/s
        self.color = color

        self.line_points = []
        self.line_length = 5
        self.line_points.append([self.position[0], self.position[1]])

        self.F = 0
        self.a = 0

    def update(self, planets, precision, dt, time_scale):
        dt *= (1/precision)

        for i in range(precision):
            line_point_distance = distance(self.line_points[-1], self.position) 
            if line_point_distance > self.line_length:
                self.line_points.append([self.position[0], self.position[1]])

            if len(self.line_points)*self.line_length > 1000:
                self.line_points.pop(0)

            for planet in planets:
                if planet == self:
                    continue
                d = math.sqrt(((planet.position[0]*px*1000)-(self.position[0]*px*1000))**2 + ((planet.position[1]*px*1000)-(self.position[1]*px*1000))**2)
                d = clamp(d, self.radius*5000, 9999999999999)
                self.F = G * ((self.mass * planet.mass)/(d**2))
                self.a = self.F/self.mass # m/s^2
                dir_vec = [planet.position[0]-self.position[0], planet.position[1]-self.position[1]]
                dir_vec = normalize(dir_vec)
                # m/f
                self.velocity[0] += dir_vec[0] * self.a * dt * time_scale
                self.velocity[1] += dir_vec[1] * self.a * dt * time_scale

            for planet in planets:
                if planet == self:
                    continue
                self.position[0] += self.velocity[0] * (1/(px*1000)) * dt * time_scale 
                self.position[1] += self.velocity[1] * (1/(px*1000)) * dt * time_scale

    def display(self, camera_pos, zoom_level):
        draw_line_points = copy.deepcopy(self.line_points)
        for point in draw_line_points:
            point[0] = (point[0] - camera_pos[0]) * zoom_level
            point[1] = (point[1] - camera_pos[1]) * zoom_level
        if len(draw_line_points) > 1:
            pygame.draw.aalines(screen, self.color // pygame.Color(3, 3, 3), False, draw_line_points)

        #draw_circle(screen, (self.position[0] - camera_pos[0]) * zoom_level, (self.position[1] - camera_pos[1]) * zoom_level, (self.radius//px)*zoom_level, self.color)
        pygame.draw.circle(screen, self.color, ((self.position[0] - camera_pos[0]) * zoom_level, (self.position[1] - camera_pos[1])* zoom_level), (self.radius//px)*zoom_level)

planets = []

#planets.append(Planet(6400, (5.972*(10**24)), [640,512], [-200, 0], pygame.Color("royalblue1")))
#planets.append(Planet(3389, (6.39*(10**23)), [1025,300], [0, -800], pygame.Color("orange")))
#planets.append(Planet(1737, (7.347*(10**22)), [1025,512], [-200, 1000], pygame.Color("gray")))

#planets.append(Planet(696340, 1.989*(10**30), [640,512], [0, 0], pygame.Color("yellow")))
#planets.append(Planet(6378, (5.972*(10**24)), [148590,512], [0, 29780], pygame.Color("royalblue1")))
#planets.append(Planet(1737, (7.347*(10**22)), [148205,512], [0, 29780-1000], pygame.Color("gray")))

for i in range(10):
    radius = random.randrange(5000, 10000)
    mass = radius**2 * (2.4*(10**16))
    color = pygame.Color(random.choice(list(THECOLORS.values())))
    planets.append(Planet(radius, mass, [random.randrange(0, 1280), random.randrange(0, 1024)], [random.randrange(-200, 200), random.randrange(-200, 200)], color))

pygame.init()

screen = pygame.display.set_mode((1280,1024))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 24)


fps = 60
dt = 1/fps

camera_pos = [0, 0]
base_cam_mov_speed = 640
cam_mov_speed = base_cam_mov_speed
zoom_level = 1
zoom_speed = 1

t1 = time.time()

running = True
while running:
    dt = time.time() - t1
    t1 = time.time()

    screen.fill((0,0,0))


    cam_mov_speed = base_cam_mov_speed * (1/zoom_level)
    zoom_level = clamp(zoom_level, 0.005, 100)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_d]:
        camera_pos[0] += int(cam_mov_speed * dt * (keys[pygame.K_d] - keys[pygame.K_a]))

    if keys[pygame.K_s] or keys[pygame.K_w]:
        camera_pos[1] += int(cam_mov_speed * dt * (keys[pygame.K_s] - keys[pygame.K_w]))

    if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
        zoom_level += zoom_speed * dt * (keys[pygame.K_UP] - keys[pygame.K_DOWN])

    if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
        time_scale += 100000 * dt * (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])

    if keys[pygame.K_SPACE]:
        zoom_level = 1
        camera_pos = [0, 0]

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    for planet in planets:
        planet.update(planets, precision, dt, time_scale)
        planet.display(camera_pos, zoom_level)

    text_fps_surf = font.render(str(round(clock.get_fps())) + " fps", True, pygame.Color("gray"))
    screen.blit(text_fps_surf, (0, 1000))

    text_time_surf = font.render("time " + str(round(time_scale)) + "x", True, pygame.Color("gray"))
    screen.blit(text_time_surf, (0, 0))

    #text_calc_surf = font.render(str(round((1/dt)*precision)) + " calc/s", True, pygame.Color("gray"))
    #screen.blit(text_calc_surf, (0, 24))


    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
sys.exit()
