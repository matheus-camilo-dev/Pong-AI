from random import randint

class GA():
    def __init__(self):
        self.genes = list(range(0, 10))
        self.geration = 0
        self.weights = list(range(0, 12))
        self.reprodution = list(range(0, 10))
        self.best = [-1 for i in range(4)]
        
        for i in range(0, len(self.reprodution)):
            for j in range(0, len(self.weights)):
                self.weights[j] = randint(-100, 100)
                self.reprodution[i] = list(self.weights)

        self.weights = self.reprodution[:]

    def initialize_fitness(self):
        self.fitness = [0 for i in range(10)]

    def get_inputs(self, inputs:int):
        self.inputs = inputs

    def get_current_individual(self, current_individual:int):
        self.actual_individual = current_individual
        
    def calculing_the_moviments(self):
            self.y = [0 for i in range(5)]
            for i in range(0, 3):
                node = i*2
                weights = [
                    self.weights[self.actual_individual][node],
                    self.weights[self.actual_individual][node+1]
                ]
                for index, weight in enumerate(weights):
                    self.y[i] += weight * self.inputs[index]
                weights.clear()

            for i in range(0, 1):
                node = i*3+6
                weights = [ 
                    self.weights[self.actual_individual][node],
                    self.weights[self.actual_individual][node+1],
                    self.weights[self.actual_individual][node+2]
                ]
                for index, weight in enumerate(weights):
                    self.y[i+3] += weight * self.y[index]
                weights.clear()

            weights = [
                self.weights[self.actual_individual][9],
                self.weights[self.actual_individual][10],
                self.weights[self.actual_individual][11]
            ]
            for index, weight in enumerate(weights):
                self.y[4] += weight * self.y[index]
            weights.clear()

    def selection_of_the_bests(self):
        best_fitness = self.fitness[:]
        self.best = [-1 for i in range(4)]
        self.best_weights = self.best[:]
        for i in range(0, len(self.best)):
            for j in range(0, len(best_fitness)):
                if best_fitness[j] > self.best[i]:
                    self.best[i] = best_fitness[j]
                    best_fitness_index = j
                    self.best_weights[i] = self.weights[j]
            best_fitness[best_fitness_index] = 0

    def reproduce_the_bests(self):
        self.reprodution = []
        self.reprodution_weights = []
        for i in range(0, 4):
            self.reprodution.append(self.best_weights[i])
            self.reprodution_weights.append(self.reprodution[i])

        point = randint(0,11)

        for i in range(0, 2):
            self.reprodution_weights[i*2] = self.reprodution[i*2+1][:point] + \
                self.reprodution[i*2][point:]
            self.reprodution_weights[i*2+1] = self.reprodution[i*2][:point] + \
                self.reprodution[i*2+1][point:]

    def generate_gens_mutations(self):
        self.mutation = [0,0]
        for i in range(0, len(self.mutation)):
            rd = randint(0, 11)
            pos = randint(0, 3)
            self.mutation[i] =  self.reprodution_weights[pos]
            self.mutation[i][rd] += randint(-100, 100)
            if  self.mutation[i][rd] < -100:
                self.mutation[i][rd] = -100
            elif  self.mutation[i][rd] > 100:
                self.mutation[i][rd] = 100
        
    def new_population(self):
        self.weights[:4] = self.reprodution[:]
        self.weights[4:8] = self.reprodution_weights[:]
        self.weights[8:] = self.mutation[:]
