import random
import operator
TOTAL_POPULATION = 10
SELECTED_PARENTS = 5
MUTATIONS = 15
GENERATIONS = 500
TOTAL_ITEMS = 12
MAX_WEIGHT = 20

class Item:                                         # Item class to hold all items information
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value

    def display(self):
        print ( "Item Name : ", self.name, " | Weight : ", self.weight, " | Value : ", self.value, "\n")

#=======================================================================================================================
class Populations:                                  # populations class to sort in naturalSelection()
    def __init__(self, value=0, height=0):
        self.value = value
        self.height = height

    def setAll(self, index, value, weight, old):
        self.weight = weight
        self.value = value
        self._index = index
        self.old = old

#=======================================================================================================================

def generatePopulation(populations, items):         # generate first population that has weight <= MAX_WEIGHT
    total_weight = MAX_WEIGHT + 1
    for i in range(TOTAL_POPULATION):
        while total_weight > MAX_WEIGHT:
            total_weight = 0
            for j in range(TOTAL_ITEMS):
                num = random.randint(0, 1)

                if num == 1:
                    total_weight += items[j].weight

                populations[i][j] = num

        total_weight = MAX_WEIGHT + 1


def displayPopulations(populations, items, option = 0):     # option 0 = total populations ,1 = selected populations
    total_value = 0
    total_weight = 0
    cap = TOTAL_POPULATION
    if option == 1:
        cap = SELECTED_PARENTS

    for i in range(cap):
        for j in range(TOTAL_ITEMS):
            print(populations[i][j], end=" ")
            if populations[i][j] == 1:
                total_value += items[j].value
                total_weight += items[j].weight

        print(" Value : ", total_value, " | Weight : ", total_weight)
        total_value, total_weight = 0, 0


def isMutated(mutations, other_num):                # return true when mutated
    for i in range(MUTATIONS):
        if mutations[i] == other_num:
            return True

    return False

def naturalSelection(old_gen, current_gen, items):  # pick 10 best population from either new gen or current gen 
    total_weight = 0
    total_value = 0
    lists_of_populations = []
    

    for i in range(TOTAL_POPULATION):
        for j in range(TOTAL_ITEMS):
            if old_gen[i][j] == 1:
                total_weight += items[j].weight
                total_value += items[j].value

        tmp = Populations()
        tmp.setAll(i, total_value, total_weight, 1)
        lists_of_populations.append(tmp)
        total_weight, total_value = 0, 0

        for j in range(TOTAL_ITEMS):
            if current_gen[i][j] == 1:
                total_weight += items[j].weight
                total_value += items[j].value


        tmp.setAll(i, total_value, total_weight, 0)
        lists_of_populations.append(tmp)
        total_weight, total_value = 0, 0

    lists_of_populations = sorted( lists_of_populations, key = operator.attrgetter("value"))

    for i in range(TOTAL_POPULATION):
        tmp = lists_of_populations.pop()

        if tmp.weight <= MAX_WEIGHT:
            if tmp.old == 1:
                for j in range(TOTAL_ITEMS):
                    old_gen[i][j] = old_gen[tmp._index][j]
            else:
                for j in range(TOTAL_ITEMS):
                    old_gen[i][j] = current_gen[tmp._index][j]


names = [
    "Bug Repellent",        # declare each name, weight, items
    "Tent       ",
    "Stove      ",
    "Clothes  ",
    "Dried Foods",
    "First Aid Kit",
    "Flash Light",
    "Novel     ",
    "Rain Gear",
    "Sleeping Bag",
    "Water Filter",
    "Lantern",
]
weight = [2, 11, 4, 5, 3, 3, 2, 2, 2, 3, 1, 7]
value = [12, 20, 5, 11, 50, 15, 6, 4, 5, 25, 30, 10]

items = []

def main():
    for i in range(TOTAL_ITEMS):
        items.append(Item(names[i], weight[i], value[i]))

    populations = [[0 for x in range(TOTAL_ITEMS)] for y in range(TOTAL_POPULATION)]

    print("\nFirst Populations\n")  
    generatePopulation(populations, items)
    print("-----------------------------")
    displayPopulations(populations, items)


    for k in range(GENERATIONS):

        #create selected populations
        selected_populations = [ [0 for x in range(TOTAL_ITEMS)] for y in range(SELECTED_PARENTS) ]
        for i in range(SELECTED_PARENTS):
            num = random.randint(0, TOTAL_POPULATION - 1)

            for j in range(TOTAL_ITEMS):
                selected_populations[i][j] = populations[num][j]


        # declare mutations
        random_num_mutations = []

        for i in range(MUTATIONS):
            random_num_mutations.append(random.randint(0, 100))

        new_populations = [[0 for x in range(TOTAL_ITEMS)] for y in range(TOTAL_POPULATION)]

        for i in range(0, TOTAL_POPULATION, 2):
            x = random.randint(0, SELECTED_PARENTS - 1)
            y = random.randint(0, SELECTED_PARENTS - 1)

            mutations = random.randint(0, 100)

            crossover_point = random.randint(0, TOTAL_ITEMS - 1)

            for j in range(0, crossover_point):
                new_populations[i][j] = selected_populations[x][j]
                new_populations[i + 1][j] = selected_populations[y][j]

            for j in range(crossover_point, TOTAL_ITEMS):
                new_populations[i][j] = selected_populations[y][j]
                new_populations[i + 1][j] = selected_populations[x][j]

            if isMutated(random_num_mutations, mutations):
                num = random.randint(0, 1)
                random_index = random.randint(0, TOTAL_ITEMS - 1)

                num = i if num == 0 else i + 1

                if new_populations[num][random_index] == 0:
                    new_populations[num][random_index] = 1
                else:
                    new_populations[num][random_index] = 0

    
        naturalSelection(populations, new_populations, items)

    print('\nBest Populations\n')

    displayPopulations(populations, items)
    print('Name\t\t\tWeight\t\tValue',end='\n==============================================\n')
    total_weight , total_value = 0 , 0

    for i in range(TOTAL_ITEMS):
        if(populations[0][i] == 1):
            total_value , total_weight = total_value + items[i].value , total_weight + items[i].weight

            print(items[i].name , '\t\t' , items[i].weight, '\t\t' , items[i].value)

    print('==============================================\n')
    print('Total\t\t\t',total_weight, '\t\t', total_value)

if __name__ == '__main__':
    main()