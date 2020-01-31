import random, time, sys
from optparse import OptionParser

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.dead = False
        self.neighbours = []


class CellFamily:
    def __init__(self, cells_count: int, height: int, width: int):
        if height <= 0 or width <= 0:
            print("Size for desk should be > 0", f"\nYour height: {height}, width:{width}")
            return None
        self.cells_count = cells_count
        self.height = height
        self.width = width
        self.mat = [[" " for j in range(width)] for i in range(height)]
        self.cells = {}
        self.life = cells_count
        self.__generate_cells() # generation
        self.__init_neighbours() # neighbours meet

    # Create cells with initialized count of cells
    def __generate_cells(self, my_locs=None):
        if self.cells_count > self.height*self.width:
            print("cell_count should be <= max_height*max_width\n"
                  f"Your cell_count: {self.cells_count}, max_height*max_width: {self.height*self.width}")
            return

        self.cells = {}
        # generate free position
        free_positions = []
        for i in range(self.height):
            for j in range(self.width):
                free_positions.append((j, i))

        # generate cells and check positions
        i = 0
        locs = []
        while i < self.cells_count:
            # location(x , y)
            location = (random.randint(0, self.width-1), random.randint(0, self.height-1))
            if location in free_positions:
                locs.append(location)
                # like address x_y
                self.cells.update({f"{location[0]}_{location[1]}": Cell(x=location[0], y=location[1])})
                # mark cell in matrix
                self.mat[location[1]][location[0]] = "1"
                free_positions.remove(location)
                i += 1
        self.print()##

    # Find neighbours and add it for each cell
    def __init_neighbours(self):
        for i, cell_key in enumerate(self.cells.keys()):
            curr_cell = self.cells[cell_key]
            for neigbour_key in list(self.cells.keys())[i+1:]:
                potential_neighbour = self.cells[neigbour_key]
                # if distance is normal and this neighbour not in list
                if abs((curr_cell.x - potential_neighbour.x)) <= 1 and abs((curr_cell.y - potential_neighbour.y)) <= 1 \
                        and neigbour_key not in curr_cell.neighbours:
                    # add neig. to current cell
                    self.cells[cell_key].neighbours.append(neigbour_key)
                    # add this cell to neigh
                    self.cells[neigbour_key].neighbours.append(cell_key)

    # check status for neighbours and update status for cells
    def __check_neighbours(self):
        for key, cell in self.cells.items():
            dead_neighbours = 0
            for neighbour_id in cell.neighbours:
                if self.cells[neighbour_id].dead:
                    dead_neighbours += 1
            live_neighbours = len(cell.neighbours) - dead_neighbours

            # Живая клетка, у которой меньше двух живых соседей, погибает
            # Живая клетка, у которой больше трёх живых соседей, погибает.
            if (live_neighbours < 2 or live_neighbours > 3) and not self.cells[key].dead:
                self.cells[key].dead = True
                self.life -= 1
                # mark like dead cell
                self.mat[cell.y][cell.x] = "0"
                continue
            # Мёртвая клетка, у которой три живых соседа, возрождается.
            if cell.dead and live_neighbours == 3:
                self.cells[key].dead = False
                self.life += 1
                # mark like live cell
                self.mat[cell.y][cell.x] = "1"
                continue
            # Живая клетка, у которой два или три живых соседа, выживает. - continue

    def print(self):
        print("-" * (self.width*4))
        for i in range(self.height):
            str_row = "| "
            for j in range(self.width):
                str_row += self.mat[i][j]+" | "
            print(str_row)
            print("-" * (self.width * 4))
        print(f"Live: {self.life}, dead: {self.cells_count - self.life}")

    def start_life(self, interval=1.):
        try:
            while self.life >= 1:
                self.__check_neighbours()
                self.print()
                time.sleep(interval)
        except KeyboardInterrupt as key:
            print(key)
            print("User stopped with ctrl+c")


def main():
    parser = OptionParser()
    parser.add_option('-c', '--cells', dest="cells", help="Count of cells", default=5)
    parser.add_option('-r', '--rows', dest="height", help="Height of the desk", default=5)
    parser.add_option('-w', '--width', dest="width", help="Width of the desk", default=5)
    parser.add_option('-f', '--file-name', dest="filename", help="Your filename.txt")

    (args, v) = parser.parse_args()

    try:
        if args.filename is None:
            if int(args.cells) <= 0:
                print(f"cells should be >= 1. Your value = "+ args.cells)
            elif int(args.height) <= 0:
                print(f"cells should be >= 1. Your value = "+ args.height)
            elif int(args.width) <= 0:
                print(f"cells should be >= 1. Your value = "+ args.width)
        elif not args.filename.endwith(".txt"):
            print("Unknown file format. Use .txt format")
            sys.exit(2)
    except Exception as e:
        print("Incorrect attributes\nPrint -h for help")
        print(e)
        sys.exit(2)

    return args


if __name__ == "__main__":
    cells, width, height = None, None, None
    if sys.stdin.isatty():
        args = main()
        if args.filename is None:
            cells = int(args.cells)
            width = int(args.width)
            height = int(args.height)
        else:
            with open(args.filename, 'r') as f:
                text = f.read().rstrip().replace("\n", " ")
            splited_vars = [int(var) for var in text]
            cells, width, height = splited_vars[0], splited_vars[1], splited_vars[2]
    print(f"Your cells count: {cells}, desk width: {width}, desk height: {height}")
    family = CellFamily(cells_count=cells, height=height, width=width)
    family.start_life()
