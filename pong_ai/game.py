import pygame
from pygame.locals import *
from random import randint
from pong_ai.ga import GA

class Game:
    def __init__(self, title='Pong AI', size=(650,580), **kwargs):
        self.title_window = title
        self.size_window = size
        
        self.balls_per_game = kwargs.get('balls', 3)
        self.fps = kwargs.get('fps', 50)
        
        self.colors = Colors()
        self.ga_manager = GA()
        self.all_directions = {
            'left' : 0,
            'right' : 1,
            'stop' : 2,
        }
        self.direction = self.all_directions['stop']
        
        pygame.init()
        self.init_font()
        self.setup_screen()
        
    def init_font(self):
        pygame.font.init()
        font_padrao = pygame.font.get_default_font()
        self.fontf = pygame.font.SysFont(font_padrao, 20)
        self.fontg = pygame.font.SysFont(font_padrao, 50)

        text_name = self.fontg.render(self.title_window, 1, self.colors.white)

    def setup_screen(self):
        self.screen = pygame.display.set_mode(self.size_window)
        pygame.display.set_caption(self.title_window)
        self.screen.fill(self.colors.royal_blue)

        self.add_elements_to_screen()
        
        self.time = pygame.time.Clock()
    
    def add_elements_to_screen(self):
        self.game_surface = pygame.Surface((400, 500))
        self.game_surface.fill(self.colors.white)
        self.text_name = self.fontg.render(
            "IA Pong",
            1,
            self.colors.white
        )
        self.add_ga_info()
        self.create_ball()
        self.create_racket()

    def add_ga_info(self):
        self.surfaces_info = [
            {'size': (190, 90)},
            {'size': (190, 90)}
        ]
        for surface in self.surfaces_info:
            surface.update({'surface': pygame.Surface(surface['size'])})
            surface['surface'].fill(self.colors.white)
        
        self.info_texts = [
            self.fontf.render(f"Genes:", 1, self.colors.red),
            self.fontf.render(f"1 - 4. Pais", 1, self.colors.blue),
            self.fontf.render(f"5 - 8. Filhos", 1, self.colors.blue),
            self.fontf.render(
                f"9 - 10. Filhos com mutação", 1, self.colors.blue
            )
        ]

    def create_ball(self):
        self.ball_surface = pygame.Surface((10, 10))
        self.racket_pos_initial = randint(150, 300)
        self.ball_surface.fill(self.colors.red)

    def create_racket(self):
        self.racket_surface = pygame.Surface((100, 10))
        self.racket_surface.fill(self.colors.black)

    def run_project(self):
        while True:
            current_individual = 0
            self.ga_manager.initialize_fitness()
            
            self.run_generation()
            
            self.ga_manager.selection_of_the_bests()
            print(f"\nMelhores: {self.ga_manager.best_weights}")
            self.ga_manager.reproduce_the_bests()
            print(f"Filhos: {self.ga_manager.reprodution_weights}")
            self.ga_manager.generate_gens_mutations()
            print(f"Filhos com mutação: {self.ga_manager.mutation}\n")
            self.ga_manager.new_population()
            self.ga_manager.geration += 1

    def run_generation(self):
        while current_individual < 10:
            posracket = [175, 510]
            posball = [self.racket_pos_initial, 40]
            player_balls = self.balls_per_game
            print(f"Peso {current_individual+1}: "
                    f"{self.ga_manager.weights[current_individual]} ")
            while player_balls != 0:

                self.ga_manager.get_current_individual(current_individual)
                text_balls = self.fontf.render(
                    f"Bolas: {player_balls}", 1, self.colors.black
                )
                text_fitness = self.fontf.render(
                    "Fitness: "
                    f"{self.ga_manager.fitness[current_individual]}", 
                    1, self.colors.black
                )
                text_champion = self.fontf.render(
                    f"Temos um vencedor!", 1, self.colors.black
                )
                text_geration = self.fontf.render(
                    f"Geration: {self.ga_manager.geration + 1}", 
                    1, self.colors.black
                )
                text_gene = self.fontf.render(
                    f"Gene: {current_individual + 1}", 1, 
                    self.colors.black
                )
                
                self.time.tick(self.fps)

                xrInput = posracket[0] + 50
                xbInput = posball[0] + 5

                self.ga_manager.get_inputs((xbInput, xrInput))
                self.ga_manager.calculing_the_moviments()
                
                _, _, _,output1, output2 = self.ga_manager.y

                if output1 and output2 > 0:
                    if output1 > output2:
                        self.direction = self.all_directions['right']
                    elif output1 == output2:
                        self.direction = self.all_directions['stop']
                    else:
                        self.direction = self.all_directions['left']
                elif output1 > 0:
                    self.direction = self.all_directions['right']
                else:
                    self.direction = self.all_directions['left']

                if posball[1] == posracket[1]:        
                    if posball[0] >= posracket[0] and \
                        posball[0] <= posracket[0] + 90:
                        self.ga_manager.fitness[current_individual] += 1
                    else:
                        player_balls -= 1
                    posball[0] = randint(150, 300)
                    posball[1] = 50
                #The fall of the ball
                if posball[1] < 530:
                    posball[1] += 10

                if all([
                        self.direction == self.all_directions['right'],
                        posracket[0] + 100 < 415
                    ]):
                    posracket[0] += 20
                elif all([
                        self.direction == self.all_directions['left'],
                        posracket[0] > 40
                    ]):
                    posracket[0] -= 20

                self.screen.fill(self.colors.royal_blue)
                self.screen.blit(self.game_surface, (25, 55))
                self.screen.blit(self.ball_surface,posball)
                self.screen.blit(text_balls, (35, 60))
                self.screen.blit(text_geration, (35, 80))
                self.screen.blit(text_gene, (35, 100))
                self.screen.blit(text_fitness, (35, 120))
                self.screen.blit(self.racket_surface, posracket)
                for index, surface in enumerate(self.surfaces_info):
                    self.screen.blit(surface['surface'], (440, index*100+55))
                for index, text in enumerate(self.info_texts):
                    self.screen.blit(text, (450, index*20+65))        
                self.screen.blit(self.text_name, (250, 10))
                            
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                        break
                    if event.type == KEYDOWN:
                        if event.key == K_n:
                            player_balls = 0
                pygame.display.update()
            print('Fitness: ',self.ga_manager.fitness[current_individual], '\n')
            current_individual += 1

class Colors:
    def __init__(self):
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.royal_blue = (65, 105, 225)

class Ball:
    def __init__(self, position=[0, 0]):
        self.position = position
        self.x, self.y = position