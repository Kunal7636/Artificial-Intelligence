import sys

class Node():
    def __init__(self, state, parent, action):       #action is basically nathing but the root i took
        self.state=state
        self.parent=parent
        self.action=action



class StackFrontier():  # stack frontier is used for dfs(depth first search)
    def __init__(self):
        self.frontier = []     #an empty frontier to store the current state visted

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)       # any return true if the value is present else return false
    # for is to iterate in the frontier
    def empty(self):
        return len(self.frontier) == 0      #returns if the frontier is Zero

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]        # we stored the node we are going to delte so that it can be put into explored node list
            self.frontier = self.frontier[:-1]        #removing the node from the frontier
            return node


class QueueFrontier(StackFrontier):     # this class QueueFrontier is to impliment bfs(breadth first search it inherits the Stack

    def remove(self):# these functions will not work as same that of stack but will be of QueueFrontier
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0] #in que we delete the data from front and delete from end
            self.frontier=self.frontier[1:]# deleting the first node
            return node

class Maze():

    def __init__(self,filename):  # file that we recievd from the comand line

        # read the file and set height and weidht of the maze
        with open(filename) as f:   # gave the file as name f to be sused ahead
             contents = f.read()     # reads the file line by line
            # now we have to find the starting and end points and the walss and the way

        if contents.count("A")!=1:
            raise Exception("must have one start point")
        if contents.count("B")!=1:
            raise Exception("must have one end pont")

        #determine the height and weidth of the maze

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line)for line in contents)         # pich each line checks length and then returns the max
        #keep the track of walls
        self.walls=[]                       # further this wall will used to store whole row
        for i in range(self.height):    # i goes from 0 to height
            row=[]                      # empty row created for each i
            for j in range(self.width):
                try:
                    if contents[i][j]=="A":         # we can access the contents by [i][j] idex imagining it as 2d array
                        self.start = (i, j)            # we give i,j as a pair value to start
                        row.append(False)           # we are taking true for the walls
                    elif contents[i][j]=="B":
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)  # this is after completing the hj loop

        self.solution = None        # initially

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i,row in enumerate(self.walls):
            for j, col in enumerate(row):   # j takes it iteration from 0 and col take iteration of values
                if col:                     # If the value is true it will run this else itt will not
                    print("█",end="")
                elif (i,j) ==self.start:
                    print("A",end="")
                elif (i,j)==self.goal:
                    print("B",end="")
                elif solution is not None and (i,j) in solution:
                    print("*",end="")
                else:
                    print(" ",end="")
            print()
        print()

    def neighbour(self,state):
        row,col = state
        candidate = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("left", (row, col-1)),
            ("right",(row,col+1))
        ]
        result = []
        for action, (r,c) in candidate: #iterate throug action with respect to i,j
            if 0<= r < self.height and 0 <= c <self.width and not self.walls[r][c]: # whole if is true that implies whren r condition satisfy
                #c condition satisfy and wall at r,c is false
                result.append((action, (r, c)))     # appending the action and i,j
        return result


    def solve(self):
        self.num_explored=0
        start = Node(state=self.start, parent=None, action=None)        # here start is node and the start we are sending to the Node class is the ij of Arepresenting the state
        frontier = QueueFrontier()# we can choose any bsf or dfs change the frontier here by choosing from stack or queue
        frontier.add(start) # we added node start here
        #inintialize an empty explored set
        self.explored = set()# created an empty set

        while True:
            #if nothing is left in frontier ,then no path id there
            if frontier.empty():    # calling the function that we declared
                raise Exception("no solution")
            # Deleting the node from the frontier
            node = frontier.remove() # called the frontier functions
            self.num_explored += 1  #increasing that we explored one more path
            # if the node is the goal the we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)         # actions are nothing just the up or down we moved in the cell
                    cells.append(node.state)    # again these are combinations of i and j
                    node = node.parent
                actions.reverse()   #beacuse the would be upside down as we are back tracking
                cells.reverse()
                self.solution = (actions, cells)
                return
            # Mark the node as explored
            self.explored.add(node.state)

            # add neighbour to frontier

            for action, state in self.neighbour(node.state):    # sending just the state part of the whole node
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self,filename,show_solution=True,show_explored=False):
        from PIL import Image,ImageDraw
        cell_size=50
        cell_border=2
        #create a blank canvas
        img=Image.new("RGBA",(self.width * cell_size,self.height * cell_size),"black")
        draw=ImageDraw.Draw(img)
        solution=self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
            img.save(filename)


if len(sys.argv)!=2:
    sys.exit("Usage:python maze.py maze1.txt")


m=Maze(sys.argv[1])
print("Maze")
m.print()
print("Solving ....")
m.solve()
print("States Explored:",m.num_explored)
print("solution:")
m.print()
m.output_image("maze.png",show_explored=True)

