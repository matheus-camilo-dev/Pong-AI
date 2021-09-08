from random import randint

class AG(object):
    def __init__(self):
        #Genes and fitness
        self.genes = list(range(0, 10))
        self.geration = 0
        self.weights = list(range(0, 12))
        self.reprodution = list(range(0, 10))
        self.best = [-1, -1, -1, -1]
        
        for i in range(0, len(self.reprodution)):
            for j in range(0, len(self.weights)):
                self.weights[j] = randint(-100, 100)
                self.reprodution[i] = list(self.weights)

        self.weights = self.reprodution[:]

    def initialize_fitness(self):
        self.fitness = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def get_input(self,xbInput, xrInput):
        self.xbInput = xbInput
        self.xrInput = xrInput

    def get_r(self, r):
        self.r = r
        
    def calculing_the_moviments(self):
            self.y = list(range(0, 5))
            for i in range(0, 3):
                v = i*2
                p1 = self.weights[self.r][v]
                p2 = self.weights[self.r][v+1]
                self.y[i] = p1 * self.xrInput + p2 * self.xbInput

            for i in range(0, 1):
                v = i*3+6
                p1 = self.weights[self.r][v]
                p2 = self.weights[self.r][v+1]
                p3 = self.weights[self.r][v+2]
                self.y[i+3] = p1 * self.y[0] + p2 * self.y[1] + p3 * self.y[2]

            p4 = self.weights[self.r][9]
            p5 = self.weights[self.r][10]
            p6 = self.weights[self.r][11]
            self.y[4] = p4 * self.y[0] + p5 * self.y[1] + p6 * self.y[2]

    def selection_of_the_bests(self):
        fitnessb = self.fitness[:]
        self.best = [-1, -1, -1, -1]
        self.bestw = self.best[:]
        for i in range(0, len(self.best)):
            for j in range(0, len(fitnessb)):
                if fitnessb[j] > self.best[i]:
                    self.best[i] = fitnessb[j]
                    m = j
                    self.bestw[i] = self.weights[j]
            fitnessb[m] = 0

    def reproduce_the_bests(self):
        self.reprodution = []
        self.reprodutionw = []
        for i in range(0, 4):
            self.reprodution.append(self.bestw[i])
            self.reprodutionw.append(self.reprodution[i])

        point = randint(0,11)

        for i in range(0, 2):
               self.reprodutionw[i*2] = self.reprodution[i*2+1][:point] + self.reprodution[i*2][point:]
               self.reprodutionw[i*2+1] = self.reprodution[i*2][:point] + self.reprodution[i*2+1][point:]

    def mutatinon_(self):
        self.mutation = [0,0]
        for i in range(0, len(self.mutation)):
            rd = randint(0, 11)
            pos = randint(0, 3)
            self.mutation[i] =  self.reprodutionw[pos]
            self.mutation[i][rd] += randint(-100, 100)
            if  self.mutation[i][rd] < -100:
                self.mutation[i][rd] = -100
            elif  self.mutation[i][rd] > 100:
                self.mutation[i][rd] = 100
        
    def new_population(self):
        self.weights[:4] = self.reprodution[:]
        self.weights[4:8] = self.reprodutionw[:]
        self.weights[8:] = self.mutation[:]
    

    
