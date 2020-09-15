import pygame
from Object import Object
from maze import Maze
import random
import os
from collections import deque
import time

random_data =os.urandom(4)
seed = int.from_bytes(random_data, byteorder='big')
random.seed(seed)

TX_SCALE = 50
VISITED_COL = (100,100,100)
WALL_COL = (0,255,200)
CELL_WIDTH = CELL_HEIGHT = 20
GRID_WIDTH = 40
GRID_HEIGHT = 30
NPC_TEXTURE = pygame.image.load('rami.png')
NPC_TEXTURE = pygame.transform.scale(NPC_TEXTURE, (CELL_WIDTH+TX_SCALE,CELL_HEIGHT+TX_SCALE))
GOAL_TEXTURE = pygame.image.load('monolit.png')
#GOAL_TEXTURE = pygame.transform.scale(GOAL_TEXTURE, (CELL_WIDTH,CELL_HEIGHT))



class NPC(Object):

    def __init__(self, scene, x, y):
        super(NPC, self).__init__( scene, x, y, CELL_WIDTH, CELL_HEIGHT, NPC_TEXTURE)
        self.moves = 0

    def update(self):
        events = self.scene.gameEngine.events

        for i,event in enumerate(events):
            if event.type == pygame.KEYUP:
                cur_location = (self.rectangle.left/CELL_WIDTH,
                                self.rectangle.top/CELL_HEIGHT)

                destination = list(cur_location)
                command=[0,0]
                if event.key == pygame.K_DOWN:
                    command = [0,1]
                if event.key == pygame.K_UP:
                    command = [0,-1]
                if event.key == pygame.K_RIGHT:
                    command = [1,0]
                if event.key == pygame.K_LEFT:
                    command = [-1,0]

                for i, elem in enumerate(command):
                    destination[i]+=elem

                self.__move(cur_location, destination)


    # Move from one cell to another.
    # Protected
    def __move(self, begin, end):

        # Check if inside the grid
        if (end[0] < 0 or end[0] > GRID_WIDTH - 1
                or end[1] < 0 or end[1] > GRID_HEIGHT - 1):
            return None

        # Check for walls
        walls = self.scene.maze.wallBetween(begin, end)
        wall_list = walls[0]
        wall_loc = [int(walls[1][0]),int(walls[1][1])]

        if wall_list[wall_loc[0]][wall_loc[1]]:
            pygame.mixer.Sound("ost/" + random.choice(self.scene.gameEngine.song_lib_crash)).play()
            return None

        self.rectangle.left = end[0]*CELL_WIDTH
        self.rectangle.top = end[1]*CELL_HEIGHT
        self.pos = end
        self.scene.addVisited(end)
        self.moves += 1

class AI(NPC):
    def __init__(self,scene,x,y):
        super(AI, self).__init__( scene, x, y)

    def maze2graph(self,maze):
        width,height = CELL_WIDTH,CELL_HEIGHT
        self.graph = {(i,j):[] for i in range(width) for j in range(height)}


        for row,col in self.graph.keys():
            if row < height - 1:
                walls = self.scene.maze.wallBetween((row,col),(row + 1, col))
                wall_list = walls[0]
                wall_loc = [int(walls[1][0]),int(walls[1][1])]

                #print(self.graph)
                if not wall_list[wall_loc[0]][wall_loc[1]]:
                    self.graph[(row, col)].append(("S", (row + 1, col)))
                    self.graph[(row + 1, col)].append(("N", (row, col)))

            if col < width - 1:
                walls = self.scene.maze.wallBetween((row,col),(row, col+1))
                wall_list = walls[0]
                wall_loc = [int(walls[1][0]),int(walls[1][1])]

                if not wall_list[wall_loc[0]][wall_loc[1]]:
                    self.graph[(row, col)].append(("E", (row,col + 1)))
                    self.graph[(row ,col+1)].append(("W", (row,col)))

        return self.graph

    def find_route(self):
        start, goal = (0,0),(CELL_WIDTH, CELL_HEIGHT)
        queue = deque([("", start)])
        visited = set()
        while queue:
            self.path, current = queue.popleft()
            if current == goal:
                return self.path
            if current in visited:
                continue
            visited.add(current)
            for direction, neighbour in self.graph[current]:
                queue.append((self.path + direction, neighbour))

    def render_path(self):
        start = (0,0)
        dict_dir = {"S":(1,0),"W":(0,-1),"E":(0,1),"N":(-1,0)}
        cur_cell = start
        for dir in self.path:

            cur_cell = tuple((cur_cell[i]+dict_dir[dir][i]) for i in range(2))
            rec_point = pygame.Rect(cur_cell[0]*20,cur_cell[1]*20,20,20)
            pygame.draw.rect(self.scene.gameEngine.screen,(0,160,0),rec_point)

class Goal(Object):

    def __init__(self, scene, x, y):
        super(Goal, self).__init__(scene, x, y, CELL_WIDTH, CELL_HEIGHT,
                        GOAL_TEXTURE)

    def render(self):
        pygame.draw.rect(self.scene.gameEngine.screen,(255,255,255),self.rectangle)

class Scene:

    def __init__(self, Engine):
        self.gameEngine = Engine
        self.npc = NPC(self, 0, 0)

        self.maze = Maze(CELL_WIDTH, CELL_HEIGHT)

        self.goal = Goal(self,9*GRID_WIDTH,
                                12*GRID_HEIGHT)

        self.ai = AI(self,0,0)
        self.ai.maze2graph(self.maze)
        self.ai.find_route()
        # Uncomment for testing
        #self.goal = Goal(self, 0,20)


        self.__initVisited()
        self.addVisited((0,0))

    def render(self):
        self.__renderVisited()
        self.ai.render_path()



        self.__renderMaze()
        self.npc.render()
        self.goal.render()

    def update(self):
        self.npc.update()
        self.__ifWin()

    def draw_walls(self, walls, ifvertical):
        for x in range(len(walls)):
            for y in range(len(walls[x])):
                if walls[x][y] is False:
                    continue

                offset_x = 0 if ifvertical else CELL_WIDTH
                offset_y = CELL_HEIGHT if ifvertical else 0

                pygame.draw.line(self.gameEngine.screen, WALL_COL,
                                    (x*CELL_WIDTH + offset_x,y*CELL_HEIGHT + offset_y),
                                        (x*CELL_WIDTH + CELL_WIDTH,y*CELL_HEIGHT+CELL_HEIGHT),2)

    def __ifWin(self):
        npc = (self.npc.rectangle.left,self.npc.rectangle.top)
        goal = (self.goal.rectangle.left,self.goal.rectangle.top)
        #print("npc:{}".format(npc))
        #print("goal:{}".format(goal))
        if npc[0]==goal[0] and npc[1]==goal[1]:
            self.gameEngine.gameOver()

    def __renderVisited(self):
        for x in range(0, GRID_WIDTH):
            for y in range(0, GRID_HEIGHT):
                if self.visited[x][y]:
                    rect = pygame.Rect(x*CELL_WIDTH,y*CELL_HEIGHT,CELL_WIDTH,CELL_HEIGHT)
                    pygame.draw.rect(self.gameEngine.screen, VISITED_COL,rect)

    def __renderMaze(self):
        walls_vert = self.maze.walls_vert

        self.draw_walls(walls_vert,ifvertical=False)

        walls_gorizontal = self.maze.walls_gorizontal

        self.draw_walls(walls_gorizontal,ifvertical=True)

    def __initVisited(self):
        self.visited = []

        for x in range(GRID_WIDTH):
            self.visited.append([])

            for y in range(GRID_HEIGHT):
                self.visited[x].append(False)

    def addVisited(self, cell):

        self.visited[int(cell[0])][int(cell[1])] = True
