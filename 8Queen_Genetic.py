
# from random import random
import random
fitnessGoal = 28


def view(invididual, index):
    print()
    print(f"Solution number {index + 1}: ", end='')
    print(invididual)
    print()
    
    for i in range(len(invididual),0,-1):
        print(i, end='')
        for j in range(len(invididual)):
            if invididual[j]==i:
                print('[Q]', end='')
            else:
                print('[ ]', end='')
        print()
    for i in range(len(invididual)):
        print(f'  {i+1}', end='')
    print()
def init(individual:list):
    for i in range(len(individual)):
        individual.append(random.randit(1, 8))
def createPopulation(population: list):
    while (len(population) != 200):
        individual = []
        for i in range(8):
            individual.append(random.randint(1, 8))
        if individual not in population and getFitness(individual)>14:
            population.append(individual)
            # print(individual)
def deleteIndividual(population, individual):
    if (len(individual) != 0):
        k = population.index(individual)
        population.remove(population[k])
def getFitness(invididual: list):  # lấy ra giá trị thích nghi của một cá thể
    conflict = 0  # giá trị xung đột
    #hàng dọc
    length = len(invididual)
    for i in range(length- 1):
        for j in range(i + 1, length):
            if invididual[i] == invididual[j]:
                conflict += 1
    #hàng ngang và chéo
    for i in range(length - 1):
        for j in range(i + 1, length):
            if abs(invididual[j] - invididual[i]) == abs(j - i):
                conflict += 1
    return fitnessGoal - conflict
def getBestIndividual(population: list):
    maxFitness = -1
    individual = []
    for x in population:
        if (getFitness(x) > maxFitness):
            maxFitness = getFitness(x)
            individual = x
    temp = individual.copy()
    deleteIndividual(population, temp)
    return individual
def crossOver1(father:list, mother:list, pointCrossOver):
    child=[]
    for i in range(pointCrossOver):# father[x,x,x,x,_,_,_,_]
        child.append(father[i])
    for i in range(pointCrossOver, len(mother)):  # mother[_,_,_,_,x,x,x,x]
        child.append(mother[i])
    return child


def crossOver2(father: list, mother: list, pointCrossOver):
    child = []
    for i in range(pointCrossOver):
        child.append(father[random.randint(0,7)])
    for i in range(pointCrossOver, len(mother)):
        child.append(mother[random.randint(0, 7)])
    return child
def getHuristic(individual: list):  # trả về một mảng gồm vị trí sai khác của các một cá thể
    # kiểm tra một quân hậu đụng độ với bao nhiêu quân hậu khác
    huristic = []
    for i in range(len(individual)):
        huristic.append(0)
        for j in range(len(individual)):
            if i != j and individual[i] == individual[j] or (abs(individual[i] - individual[j]) == abs(i - j)):
                huristic[i] += 1
    return huristic
def mutation(child: list):  # đột biến để tìm ra child có fitness tốt nhất
    global pointCrossOver, father, mother
    newchange = -1
    while newchange != 0:
        newchange = 0
        tempChild = child.copy()
        huristic = getHuristic(tempChild)  
        index = huristic.index(max(huristic))
        maxFitness = getFitness(tempChild) 
        for i in range(1, 9):
            tempChild[index] = i
            # nếu mà fitness tại con mới mà lớn fitness của hiện tại thì đột biến nó bằng cái vị trí khác
            if getFitness(tempChild) > maxFitness:
                maxFitness = getFitness(tempChild)
                newchange = i
            tempChild = child.copy()
        #phương án 2 đột biến chấp nhận luôn cái xấu nhất
        if newchange == 0:
            for i in range(len(child) - 1):
                for j in range(i + 1, len(child)):
                    if child[i] == child[j]:
                        child[i] = random.randint(1, 8)
        else:
            child[index] = newchange

def goal(fitness):
    return fitness == fitnessGoal
def solve(numberOfSolutions, solutions:list):
    explore = 0
    population = []
    createPopulation(population)
    while len(solutions) < numberOfSolutions:
        if(len(population)==0):
            createPopulation(population)
        #1. chọn lọc
        father = getBestIndividual(population)
        mother = getBestIndividual(population)
        if len(father) == 0 or len(mother) == 0 :
            continue
        #2. tìm giải pháp
        if goal(getFitness(father)) == True and father not in solutions:
            solutions.append(father)
        if goal(getFitness(mother)) == True and mother not in solutions:
            solutions.append(mother)
        #3.lai tạo
        pointCrossOver=random.randint(0,7)
        child1 = crossOver1(father, mother, pointCrossOver)
        child2 = crossOver1(mother, father, pointCrossOver)
        '''-->hàm lai tạo thứ 2 cho kết quả đa dạng hơn và nhiều phương án hơn<--'''
        # child1 = crossOver2(father, mother, pointCrossOver)
        # child2 = crossOver2(mother, father, pointCrossOver)
        #4.đột biến 
        mutation(child1) 
        mutation(child2)
        #5.thêm vào quần thể
        if child1 not in population and child1!=father and child1!=mother:
            population.append(child1)
        if child2 not in population and child2 != father and child2!= mother:
            population.append(child2)
        print(explore)
        print(f'{child1}:{getFitness(child1)}')
        print(f'{child2}:{getFitness(child2)}')
        print(f'length of population: {len(population)}')
        print(f'length of solutions: {len(solutions)}')
        explore += 1
    

if __name__ == "__main__":
    numberOfSolutions = int(input("Number of solutions:"))
    solutions=[]
    solve(numberOfSolutions, solutions)
    print("********************** Solutions **********************")
    print(f"The number of solutions you wanted: {numberOfSolutions}")
    for i in range(numberOfSolutions):
        view(solutions[i], i)

    print("*******************************************************")
