import random


class Maze:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.__createWalls()
        self.__generateMaze()

    def __createWalls(self):
        self.walls_vert = []

        self.walls_gorizontal = []

        for x in range(self.width):
            self.walls_vert.append([])
            self.walls_gorizontal.append([])
            for y in range(self.height):
                self.walls_vert[x].append(True)
                self.walls_gorizontal[x].append(True)

    # Generate maze using DFS to find solution
    def __generateMaze(self):
        
        cells = []

        visited_cells = []

        for x in range(self.width):
            visited_cells.append([])
            for y in range(self.height):
                visited_cells[x].append(False)

        # Select random start
        current_cell = (random.choice(range(self.width)),
                        random.choice(range(self.height)))

        visited_cells[current_cell[0]][current_cell[1]] = True

        num_visited = 1

        total_cells = self.width * self.height

        while num_visited < total_cells:
            neighbours = self.__findNeighbors(current_cell)

            not_visited = lambda cell: visited_cells[cell[0]][cell[1]] is False
            neighbours = list(filter(not_visited, neighbours))

            if len(neighbours) is not 0:
                new_cell = random.choice(neighbours)

                wall_between = self.wallBetween(current_cell, new_cell)
                
                array = wall_between[0]
                wall = wall_between[1]
               
                array[wall[0]][wall[1]] = False

                cells.append(current_cell)

                current_cell = new_cell

                num_visited += 1
                visited_cells[new_cell[0]][new_cell[1]] = True

            else:
                if len(cells) is 0:
                    break

                current_cell = cells[len(cells)-1]
                cells.remove(current_cell)

    def __findNeighbors(self, cell):
        neighbours = []

        x = cell[0]
        y = cell[1]

        if x > 0:
            neighbours.append((x-1,y))
        if x < self.width - 1:
            neighbours.append((x+1,y))
        if y > 0 :
            neighbours.append((x,y-1))
        if y < self.height - 1:
            neighbours.append((x,y+1))

        return neighbours 

    def wallBetween(self,cell1, cell2):
        array = None
        wall = None

        x1 = cell1[0]
        y1 = cell1[1]
        x2 = cell2[0]
        y2 = cell2[1]

        if x1 == x2:
            array = self.walls_gorizontal
            if y1<y2:
                wall = cell1
            else:
                wall = cell2

        if y1 == y2:
            array = self.walls_vert
            if x1<x2:
                wall = cell1
            else:
                wall = cell2
        return (array, wall)

