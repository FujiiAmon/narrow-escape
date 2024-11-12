import pygame
from pygame.locals import *
import sys
import math
import random



class player:
    def __init__(self, coordinate : tuple, radius, screen):
        (self.x, self.y) = coordinate
        self.size = radius * ((1 / 2) ** (1 / 2))
        self.radius = radius
        self.damage = 0
        self.flash = 0
        self.screen = screen
        self.surface = pygame.draw.circle(self.screen, (0, 150, 0), (self.x, self.y), self.radius)
    
    def move(self, dx, dy, size : tuple, flash = 0):
        self.x += dx
        self.y += dy
        self.x = area_limit((self.x,self.y), size)[0]
        self.y = area_limit((self.x,self.y), size)[1]

        if self.flash ==0:
            pygame.draw.circle(self.screen, (0, 150, 0), (self.x, self.y), self.radius)
        elif self.flash >= 1 and self.flash <= flash:
            if self.flash % 2 == 0:
                pygame.draw.circle(self.screen, (150, 0, 0), (self.x + dx, self.y + dy), self.radius)
            elif self.flash % 2 != 0:
                pygame.draw.circle(self.screen, (0, 150, 0), (self.x + dx, self.y + dy), self.radius)
            self.flash -= 1

class enemy:
    def __init__(self, screen):
        (self.x, self.y) = (-200, -200)
        self.screen = screen
        self.judgement = False 
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 5)


    def jump_move(self, gravity, velocity : tuple, size : tuple, time):
        (width, height) = (size[0], size[1])
        (vx, vy) = (velocity[0], velocity[1])
        cycle_time = 2 * (vy / gravity)
        self.x = int(vx * time)
        for i in range(int(width / (cycle_time * vx) + 1)):
            if time >= cycle_time * i and time <= cycle_time * (i + 1):
                time -= i * cycle_time
                self.y = int((1 / 2) * gravity * time ** 2 - vy * time + height)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 5)
    
    def jump_move_r(self, gravity, velocity : tuple, size : tuple, time):
        (width, height) = (size[0], size[1])
        (vx, vy) = (velocity[0], velocity[1])
        cycle_time = 2 * (vy / gravity)
        self.x = width -1 * int(vx * time)
        for i in range(int(width / (cycle_time * vx) + 1)):
            if time >= cycle_time * i and time <= cycle_time * (i + 1):
                time -= i * cycle_time
                self.y = height -1 * (int((1 / 2) * gravity * time ** 2 - vy * time + height))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 5)
    
    def jump_move2(self, gravity, velocity : tuple, size : tuple, parsonal_time, time, generate_quantity, generate_interval):
        (wide, height) = (size[0], size[1])
        (vx, vy) = (velocity[0], velocity[1])
        cycle_time = 2 * (vy / gravity)
        self.x = int(vx * (parsonal_time + time))
        for i in range(-int((generate_quantity * generate_interval) / cycle_time + 1), int((generate_quantity * generate_interval) / cycle_time + 1)):
            if parsonal_time >= cycle_time * i and parsonal_time <= cycle_time * (i + 1):
                parsonal_time -= i * cycle_time
                self.y = int((1 / 2) * gravity * parsonal_time ** 2 - vy * parsonal_time + height)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 5)
    
    def jump_move_r2(self, gravity, velocity : tuple, size : tuple, parsonal_time, time, generate_quantity, generate_interval):
        (width, height) = (size[0], size[1])
        (vx, vy) = (velocity[0], velocity[1])
        cycle_time = 2 * (vy / gravity)
        self.x = width -1 * int(vx * (parsonal_time + time))
        for i in range(-int((generate_quantity * generate_interval) / cycle_time + 1), int((generate_quantity * generate_interval) / cycle_time + 1)):
            if parsonal_time >= cycle_time * i and parsonal_time <= cycle_time * (i + 1):
                parsonal_time -= i * cycle_time
                self.y = height -1 * (int((1 / 2) * gravity * parsonal_time ** 2 - vy * parsonal_time + height))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 5)

    def spiral_move(self, radius, center : tuple, time, velocity : int, degree):
        a = center[0]
        b = center[1]
        radius -= time
        if radius > 0:
            self.x = int(radius * math.cos(math.radians(25 * time)) + a)
            self.y = int(radius * math.sin(math.radians(25 * time)) + b)
        elif radius <= 0:
            self.x = velocity * math.sin(math.radians(degree)) * (-1 * radius) + a
            self.y = velocity * math.cos(math.radians(degree)) * (-1 * radius) + b
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 5)
    
    def judge(self, player : player):
        if self.x >= player.x - player.size and self.x <= player.x + player.size and self.y >= player.y - player.size and self.y <= player.y + player.size:
            self.judgement = True
        else:
            self.judgement = False

class spear:
    def __init__(self, half_long, screen):
        self.half_long = int(half_long)
        (cx, cy) = (-200, -200)
        self.degree = 0
        self.edge1 = (int(self.half_long * math.cos(math.radians(self.degree)) + cx), int(self.half_long * math.sin(math.radians(self.degree)) + cy))
        self.edge2 = (int(self.half_long * math.cos(math.radians(self.degree + 180)) + cx), int(self.half_long * math.sin(math.radians(self.degree + 180)) + cy))
        self.judgement = False
        self.screen = screen
        pygame.draw.polygon(self.screen, (255, 255, 255), [self.edge1, self.edge2], 10)
    
    def panetrate(self, degree, center_point : tuple, velocity : int, time):
        (cx, cy) = center_point
        self.degree = degree
        start_edge1 = (int(self.half_long * math.cos(math.radians(self.degree)) + cx), int(self.half_long * math.sin(math.radians(self.degree)) + cy))
        start_edge2 = (int(self.half_long * math.cos(math.radians(self.degree + 180)) + cx), int(self.half_long * math.sin(math.radians(self.degree + 180)) + cy))
        move_distance = (int(velocity * math.cos(math.radians(self.degree)) * time), int(velocity * math.sin(math.radians(self.degree)) * time))
        self.edge1 = (start_edge1[0] + move_distance[0], start_edge1[1] + move_distance[1])
        self.edge2 = (start_edge2[0] + move_distance[0], start_edge2[1] + move_distance[1])
        pygame.draw.polygon(self.screen, (255, 255, 255), [self.edge1, self.edge2], 10)

    def panetrate2(self, degree, center_point : tuple, velocity : int, time):
        (cx, cy) = center_point
        self.degree = degree
        start_edge1 = (int(self.half_long * math.cos(math.radians(self.degree)) + cx), int(self.half_long * math.sin(math.radians(self.degree)) + cy))
        start_edge2 = (int(self.half_long * math.cos(math.radians(self.degree + 180)) + cx), int(self.half_long * math.sin(math.radians(self.degree + 180)) + cy))
        move_distance = (int(velocity * math.cos(math.radians(self.degree + 90)) * time), int(velocity * math.sin(math.radians(self.degree + 90)) * time))
        self.edge1 = (start_edge1[0] + move_distance[0], start_edge1[1] + move_distance[1])
        self.edge2 = (start_edge2[0] + move_distance[0], start_edge2[1] + move_distance[1])
        pygame.draw.polygon(self.screen, (255, 255, 255), [self.edge1, self.edge2], 10)

    def rotate(self, center_point, velocity, time):
        (cx, cy) = center_point
        self.degree = velocity * time
        self.edge1 = (int(self.half_long * math.cos(math.radians(self.degree)) + cx), int(self.half_long * math.sin(math.radians(self.degree)) + cy))
        self.edge2 = (int(self.half_long * math.cos(math.radians(self.degree + 180)) + cx), int(self.half_long * math.sin(math.radians(self.degree + 180)) + cy))
        pygame.draw.polygon(self.screen, (255, 255, 255), [self.edge1, self.edge2], 10)
    
    def rotate2(self, center_point, velocity_r, velocity_l, direction_degree, time):
        vx = velocity_l * math.cos(math.radians(direction_degree))
        vy = velocity_l * math.sin(math.radians(direction_degree))
        self.degree = velocity_r * time
        (cx, cy) = (center_point[0] + vx * time, center_point[1] + vy * time)
        self.edge1 = (int(self.half_long * math.cos(math.radians(self.degree)) + cx), int(self.half_long * math.sin(math.radians(self.degree)) + cy))
        self.edge2 = (int(self.half_long * math.cos(math.radians(self.degree + 180)) + cx), int(self.half_long * math.sin(math.radians(self.degree + 180)) + cy))
        pygame.draw.polygon(self.screen, (255, 255, 255), [self.edge1, self.edge2], 10)
    
    def rotate3(self, center_point, velocity_r, fixed_point : tuple, time):
        (cx, cy) = center_point
        (fx, fy) = fixed_point
        rotated_edge1 = (fx, fy)
        rotated_edge2 = (int(self.half_long * math.cos(math.radians(velocity_r * time + 180)) + cx), int(self.half_long * math.sin(math.radians(velocity_r * time + 180)) + cy))
        pygame.draw.polygon(self.screen, (255, 255, 255), [rotated_edge1, rotated_edge2], 10)

    def judge(self, player : player):
        xs = self.edge1[0]
        xl = self.edge2[0]
        if xs < xl:
            XG = [xi for xi in range(xs, xl+1)]
        elif xl < xs:
            XG = [xi for xi in range(xl, xs+1)]
        elif xs == xl:
            XG = [xs for xi in range(self.half_long + 1)]
        YG = grid(self.edge1[0], self.edge1[1], XG, self.degree)
        JG = []
        for grid_i in range(len(XG)):
            if XG[grid_i] >= player.x - player.size and YG[grid_i] >=  player.y - player.size and XG[grid_i] <= player.x + player.size and YG[grid_i] <= player.y + player.size:
                ji = [True]
            else:
                ji = [False]
            JG += ji
        if True in JG:
            self.judgement = True
        else:
            self.judgement = False

def area_limit(point : tuple, size : tuple):
    x = point[0]
    y = point[1]
    w = size[0]
    h = size[1]
    if x < 0:
        x = 0
    if x > w:
        x = w
    if y < 0:
        y = 0     
    if y > h:
        y = h
    return (x, y)

def grid(x, y, X, degree):
    tilt = math.tan(math.radians(degree))
    segment = y - tilt * x
    Y = []
    for xi in X:
        yi = [int(tilt * xi + segment)]
        Y += yi
    return Y

def jump_enemy(E, E_r, size, velocity : tuple, time, term, generate_quantity, generate_interval):
    for e in E:
        e.jump_move(2, velocity, size, time - generate_interval * E.index(e))
    for e in E_r:
        e.jump_move_r(2, velocity, size, time - generate_interval * E_r.index(e))

    if E[generate_quantity-1].x >= size[0]:
        time = 0
        term += 1
    return (time, term)

def jump_enemy2(E, E_r, size, velocity : tuple, time, term, generate_quantity, generate_interval):
    for e in E:
        e.jump_move2(2, velocity, size, time - generate_interval * E.index(e), time, generate_quantity, generate_interval)
    for e in E_r:
        e.jump_move_r2(2, velocity, size, time - generate_interval * E_r.index(e), time, generate_quantity, generate_interval)

    if E[generate_quantity-1].x >= size[0]:
        time = 0
        term += 1

    return (time, term)

def spiral_enemy(E, time, term, radius, center, velocity):
    for spiral_i in range(36):
        E[spiral_i].spiral_move(radius, center, time, velocity, 10 * spiral_i)
    
    if radius - time < 0:
        x0 = E[0].x
        y0 = E[0].y
        a = center[0]
        b = center[1]
        if (x0 - a) ** 2 + (y0 - b) ** 2 >= 16 * radius ** 2:
            time = 0
            term += 1
    
    return (time, term)

def sweep(S, time, term, size, velocity):
    (w, h) = size
    S[0].panetrate2(0, (w / 4, 0), velocity, time)
    S[1].panetrate2(0, (w * 3 / 4, h), -velocity, time)
    if  h <= velocity * time:
        time = 0
        term += 1
    return(time, term)

def sweep2(S, time, term, size, velocity):
    (w, h) = size
    S[0].panetrate2(180, (w / 4, h), velocity, time)
    S[1].panetrate2(180, (w * 3 / 4, 0), -velocity, time)
    if  h <= velocity * time:
        time = 0
        term += 1
    return(time, term)

def sweep3(S, time, term, size, velocity):
    (w, h) = size
    interval = w / (3 * velocity)
    for sweep_i in range(len(S) // 2):
        S[sweep_i].panetrate2(0, (w / 4, 0), velocity, time - sweep_i * interval)
        S[len(S) // 2 - 1 + sweep_i].panetrate2(0, (w * 3 / 4, h), -velocity, time - sweep_i * interval)
    if time >= 15 * interval:
        time = 0
        term += 1  
    return(time, term)

def sweep4(S, time, term, size, velocity):
    (w, h) = size
    interval = w / (3 * velocity)
    for sweep_i in range(len(S) // 2):
        S[sweep_i].panetrate2(180, (w / 4, h), velocity, time - sweep_i * interval)
        S[len(S) // 2 - 1 + sweep_i].panetrate2(180, (w * 3 / 4, 0), -velocity, time - sweep_i * interval)
    if time >= 15 * interval:
        time = 0
        term += 1  
    return(time, term)

def crawl(S, time, term, size, velocity):
    (w, h) = size
    S[0].rotate2((0, h / 4), velocity, velocity / 3, 0, time)
    S[1].rotate2((w, h * 3 / 4), -velocity, -velocity / 3, 0, time)
    if w <= velocity / 3 * time:
        time = 0
        term += 1
    return(time, term)

def crawl2(S, time, term, size, velocity):
    (w, h) = size
    S[0].rotate2((w / 4, 0), velocity, velocity / 3, 90, time)
    S[1].rotate2((w * 3 / 4, h), -velocity, -velocity / 3, 90, time)
    if h <= velocity / 3 * time:
        time = 0
        term += 1
    return(time, term)

def skewered(S1, time, interval, term, size, velocity):
    if time <= interval:
        (w, h) = size
        degree_list= [math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2)), math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2))]
        center_point_list = [(0, 0), (0, h / 2), (0, h), (w / 2, h), (w, h), (w, h / 2), (w, 0),(w / 2, 0)]
        for panetrate_i in range(8):
            if panetrate_i >= 0 and panetrate_i <= 3: 
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], velocity, 0)
            if panetrate_i >= 4 and panetrate_i <= 7:
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], -velocity, 0)
    elif time > interval:
        (w, h) = size
        degree_list= [math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2)), math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2))]
        center_point_list = [(0, 0), (0, h / 2), (0, h), (w / 2, h), (w, h), (w, h / 2), (w, 0),(w / 2, 0)]
        for panetrate_i in range(8):
            if panetrate_i >= 0 and panetrate_i <= 3: 
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], velocity, time - interval)
            if panetrate_i >= 4 and panetrate_i <= 7:
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], -velocity, time - interval)
        if S1[0].edge2[1] >= h:
            time = 0
            term +=1
    return(time, term)

def skewered2(S1, S2, time, interval, term, size, velocity):
    if time <= interval:
        (w, h) = size
        degree_list= [math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2)), math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2))]
        center_point_list = [(0, 0), (0, h / 2), (0, h), (w / 2, h), (w, h), (w, h / 2), (w, 0),(w / 2, 0)]
        for panetrate_i in range(8):
            if panetrate_i >= 0 and panetrate_i <= 3: 
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], velocity, 0)
            if panetrate_i >= 4 and panetrate_i <= 7:
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], -velocity, 0)
        S2[0].rotate((w / 2, h / 2), velocity, time)
    elif time > interval:
        (w, h) = size
        degree_list= [math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2)), math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2))]
        center_point_list = [(0, 0), (0, h / 2), (0, h), (w / 2, h), (w, h), (w, h / 2), (w, 0),(w / 2, 0)]
        for panetrate_i in range(8):
            if panetrate_i >= 0 and panetrate_i <= 3: 
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], velocity, time - interval)
            if panetrate_i >= 4 and panetrate_i <= 7:
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], -velocity, time - interval)
        if S1[0].edge2[1] >= h:
            time = 0
            term +=1
    return(time, term)

def skewered3(S1, S2, time, interval, term, size, velocity):
    if time <= interval:
        (w, h) = size
        degree_list= [math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2)), math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2))]
        center_point_list = [(0, 0), (0, h / 2), (0, h), (w / 2, h), (w, h), (w, h / 2), (w, 0),(w / 2, 0)]
        rotate_center_point_list = [(w / 4, h / 4), (w / 4, h * 3 / 4), (w * 3 / 4, h / 4), (w * 3 / 4, h * 3 / 4)]
        for panetrate_i in range(8):
            if panetrate_i >= 0 and panetrate_i <= 3: 
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], velocity, 0)
            if panetrate_i >= 4 and panetrate_i <= 7:
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], -velocity, 0)
        for rotate_i in range(4):
            S2[rotate_i].rotate(rotate_center_point_list[rotate_i], velocity, time)
    elif time > interval:
        (w, h) = size
        degree_list= [math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2)), math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2))]
        center_point_list = [(0, 0), (0, h / 2), (0, h), (w / 2, h), (w, h), (w, h / 2), (w, 0),(w / 2, 0)]
        for panetrate_i in range(8):
            if panetrate_i >= 0 and panetrate_i <= 3: 
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], velocity, time - interval)
            if panetrate_i >= 4 and panetrate_i <= 7:
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], -velocity, time - interval)
        if S1[0].edge2[1] >= h:
            time = 0
            term +=1
    return(time, term)

def skewered4(S1, S2, time, interval, term, size, velocity):
    if time <= interval:
        (w, h) = size
        degree_list= [math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2)), math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2))]
        center_point_list = [(0, 0), (0, h / 2), (0, h), (w / 2, h), (w, h), (w, h / 2), (w, 0),(w / 2, 0)]
        for panetrate_i in range(8):
            if panetrate_i >= 0 and panetrate_i <= 3: 
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], velocity, 0)
            if panetrate_i >= 4 and panetrate_i <= 7:
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], -velocity, 0)
        S2[0].rotate2((0, h / 4), velocity, velocity / 2, 45, time)
        S2[1].rotate2((w, h * 3 / 4), -velocity, -velocity / 2, 45, time)
    elif time > interval:
        (w, h) = size
        degree_list= [math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2)), math.degrees(math.atan(h / w * 2)), math.degrees(-math.atan(h / w * 2) + math.pi / 2), math.degrees(math.atan(h / w * 2) - math.pi / 2), math.degrees(-math.atan(h / w * 2))]
        center_point_list = [(0, 0), (0, h / 2), (0, h), (w / 2, h), (w, h), (w, h / 2), (w, 0),(w / 2, 0)]
        for panetrate_i in range(8):
            if panetrate_i >= 0 and panetrate_i <= 3: 
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], velocity, time - interval)
            if panetrate_i >= 4 and panetrate_i <= 7:
                S1[panetrate_i].panetrate(degree_list[panetrate_i], center_point_list[panetrate_i], -velocity, time - interval)
        if S1[0].edge2[1] >= h:
            time = 0
            term +=1
    return(time, term)    

def main_play(flagc):

    flags = False
    (w, h) = (400, 400)
    (x, y) = (w/2, h/2)
    size = (w, h)
    center = (x, y)
    pygame.init()
    pygame.display.set_mode((w, h))
    font1 = pygame.font.Font(None, 50)
    screen = pygame.display.get_surface()
    pygame.display.update()
    p = player(center, 7, screen)
    generate_interval = 0.5
    generate_quantity = 200
    speed = 6
    life = 10
    flash = 30
    E = [enemy(screen) for q in range(generate_quantity)]
    E_r = [enemy(screen) for q in range(generate_quantity)]
    S1 = [spear(h / 3, screen) for q in range(8)]
    S2 = [spear(h / 5, screen) for q in range(8)]
    S3 = [spear(h / 4, screen) for q in range(24)]
    term = 0
    
    time = -1
    while 1:

        time += 1
        
        pygame.time.wait(30)
        pygame.display.update()
        screen.fill((0, 20, 0))

        text1 = font1.render(f"YOUR LIFE:{life - p.damage}", True, (100, 100, 100))
        screen.blit(text1, (0, 0))

        (dx, dy) = (0, 0)
        pressed_key = pygame.key.get_pressed() 
        if pressed_key[K_LEFT]:
            dx = -speed
        if pressed_key[K_RIGHT]:
            dx = speed
        if pressed_key[K_UP]:
            dy = -speed
        if pressed_key[K_DOWN]:
            dy = speed

        p.move(dx, dy, size, flash)
        
        if term == 0:
            (time, term) = jump_enemy(E, E_r, size, (5, 28), time, term, generate_quantity, generate_interval)
        
        if term == 1 or term == 2:
            (time, term) = jump_enemy2(E, E_r, size, (5, 28), time, term, generate_quantity, generate_interval)
        
        if term == 3:
            (time, term) = spiral_enemy(E, time, term, w / 4, (w / 4, h / 4), 4)
            spiral_enemy(E_r, time, term, 100, (w * 3 / 4, h * 3 / 4), 4)

        if term == 4:
            (time, term) = spiral_enemy(E, time, term, w / 4, (w / 2, h / 3), 4)
            spiral_enemy(E_r, time, term, 100, (w / 3, h * 2 / 3), 4)
            spiral_enemy(E_r, time, term, 100, (w * 2 / 3, h * 2 / 3), 4)
        
        if term == 5:
            (time, term) = spiral_enemy(E, time, term, w / 4, (w / 4, h / 4), 4)
            spiral_enemy(E_r, time, term, 100, (w * 3 / 4, h / 4), 4)
            spiral_enemy(E_r, time, term, 100, (w / 4, h * 3 / 4), 4)
            spiral_enemy(E_r, time, term, 100, (w * 3 / 4, h * 3 / 4), 4)

        if term == 6:
            (time, term) = spiral_enemy(E, time, term, w / 2, (w / 2, h / 2), 10)
        
        if term == 7:
            (time, term) = sweep(S1, time, term, size, 5)
        
        if term == 8:
            (time, term) = sweep2(S1, time, term, size, 5)
        
        if term == 9:
            (time, term) = crawl(S1, time, term, size, 10)
        
        if term == 10:
            (time, term) = crawl2(S1, time, term, size, 10)
        
        if term == 11:
            (time, term) = skewered(S1, time, 30, term, size, 15)
        
        if term == 12:
            (time, term) = skewered2(S1, S2, time, 30, term, size, 15)
        
        if term == 13:
            (time, term) = skewered3(S1, S2, time, 30, term, size, 15)
        
        if term == 14:
            (time, term) = sweep3(S3, time, term, size, 4)
        
        if term == 15:
            (time, term) = sweep4(S3, time, term, size, 4)

        if term == 16:
            flags = True
            flagc = True
            break

        if p.flash == 0:
            for e in E:
                e.judge(p)
                if e.judgement == True:
                    p.damage += 1
                    p.flash = flash
            for e in E_r:
                e.judge(p)
                if e.judgement == True:
                    p.damage += 1
                    p.flash = flash
            for s in S1:
                s.judge(p)
                if s.judgement == True:
                    p.damage += 1
                    p.flash = flash
            for s in S2:
                s.judge(p)
                if s.judgement == True:
                    p.damage += 1
                    p.flash = flash
            for s in S3:
                s.judge(p)
                if s.judgement == True:
                    p.damage += 1
                    p.flash = flash
        
        if p.damage >= life:
            flags = True
            break
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                flags = True
                break
        
        if flags:
            break
    
    return flagc
            
def main_start():
    
    flagq = False
    flags = False
    flagp = False
    size = (400, 400)
    (w, h) = size
    
    white = (255, 255, 255)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Let's start!!")
    font1 = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)
    text1 = font1.render("NARROW ESCAPE!!", True, white)
    text2 = font2.render("Press space key to start", True, white)
    text1_width = text1.get_width()
    text1_height = text1.get_height()
    text2_width = text2.get_width()
    p = player((w / 2, h * 3 / 4), 7, screen)
    speed = 5
    Triangle = [3,4,5]
    n =  random.choice(Triangle)

    time = -1
    while 1:
        
        if time >= 300:
            time = 0
        
        time += 1
        pygame.time.wait(30)
        screen.fill((0, 0, 0))
        for m in range (n):
            pygame.draw.polygon(screen, (100, 100, 100), [((m*w/6*n)+time, (2*h/3) - time),((w*m/12*n)-time, (h/5)+ 2*time), ((w*(2*m+1)/15*n)-time, (h/10) + time/2)], 3)
        screen.blit(text1, (w / 2 - text1_width / 2, h / 2 - text1_height / 2))
        if time % 20 in range(10):
            screen.blit(text2, (w / 2 - text2_width / 2, h / 2 + text1_height / 2))
        (dx, dy) = (0, 0)
        pressed_key = pygame.key.get_pressed() 
        if pressed_key[K_LEFT]:
            dx = -speed
        if pressed_key[K_RIGHT]:
            dx = speed
        if pressed_key[K_UP]:
            dy = -speed
        if pressed_key[K_DOWN]:
            dy = speed
        p.move(dx, dy, size)

        pygame.display.update()

        for event in pygame.event.get(eventtype=None):
            if event.type == QUIT:
                pygame.quit()
                flagq = True
                break
                
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pygame.quit()
                    flags = True
                    break
        
        if flagq:
            break
        if flags:
            flagp = True
            break

    return flagp

def main_continue():

    flagq = False
    flags = False
    flagp = False
    size = (400, 400)
    (w, h) = size
    white = (255, 255, 255)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Challange again!!")
    font1 = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)
    text1 = font1.render("GAME OVER", True, white)
    text2 = font2.render("Press space key to continue", True, white)
    text1_width = text1.get_width()
    text1_height = text1.get_height()
    text2_width = text2.get_width()
    Triangle = [3,4,5]
    n =  random.choice(Triangle)

    time = -1
    while 1:

        if time >= 300:
            time = 0

        time += 1
        pygame.time.wait(30)
        screen.fill((0, 0, 0))
        for m in range (n):
            pygame.draw.polygon(screen, (100, 100, 100), [((m*w/6*n)+time, (2*h/3) - time),((w*m/12*n)-time, (h/5)+ 2*time), ((w*(2*m+1)/15*n)-time, (h/10) + time/2)], 3)
        screen.blit(text1, (w / 2 - text2_width / 2, h / 2 - text1_height / 2))
        if time % 20 in range(10):
            screen.blit(text2, (w / 2 - text2_width / 2, h / 2 + text1_height / 2))
        pygame.display.update()
        
        for event in pygame.event.get(eventtype=None):
                if event.type == QUIT:
                    pygame.quit()
                    flagq = True
                    break
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pygame.quit()
                        flags = True
                        break
        
        if flagq:
            flagp = False
            break
        if flags:
            flagp = True
            break
            
    return flagp

def main_end():
    size = (400, 400)
    (w, h) = size
    white = (255, 255, 255)
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Congratsration!!")
    font1 = pygame.font.Font(None, 30)
    font2 = pygame.font.Font(None, 25)
    text1 = font1.render("Congratsration, you are saved!", True, white)
    text2 = font2.render("Press space key to end", True, white)
    text1_width = text1.get_width()
    text1_height = text1.get_height()
    text2_width = text2.get_width()
    Triangle = [3,4,5]
    n =  random.choice(Triangle)

    time = -1
    while 1:
        time += 1
        pygame.time.wait(30)
        screen.fill((0, 0, 0))
        for m in range (n):
            pygame.draw.polygon(screen, (100, 100, 100), [((m*w/6*n)+time, (2*h/3) - time),((w*m/12*n)-time, (h/5)+ 2*time), ((w*(2*m+1)/15*n)-time, (h/10) + time/2)], 3)
        screen.blit(text1, (w / 2 - text1_width / 2, h / 2 - text1_height / 2))
        if time % 20 in range(10):
            screen.blit(text2, (w / 2 - text2_width / 2, h / 2 + text1_height / 2))
        pygame.display.update()
        
        for event in pygame.event.get(eventtype=None):
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pygame.quit()
                        break

if __name__ == "__main__":
    flagc = False
    flagp = main_start()
    while flagp:
        flagc = main_play(flagc)
        if not flagc:
            flagp = main_continue()
        if flagc:
            main_end()
            break
    