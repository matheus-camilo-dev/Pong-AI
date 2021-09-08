import pygame
from pygame.locals import *
from random import randint
import AG

pygame.init()

#class
r = 0
ag = AG.AG()

#Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
royal_blue = (65, 105, 225)

#Text
pygame.font.init()

font_padrao = pygame.font.get_default_font()
fontf = pygame.font.SysFont(font_padrao, 20)
fontg = pygame.font.SysFont(font_padrao, 50)

text_name =fontg.render("IA Pong", 1, white)

#Screen
tela = pygame.display.set_mode((650,580))
pygame.display.set_caption("Ping - Pong")
tela.fill(royal_blue)

#Directions
LEFT = 0
RIGHT = 1
STOP = 2
direction = STOP

#game
game = pygame.Surface((400, 500))
game.fill(white)

#explicação
label1 = pygame.Surface((190, 90))
label1.fill(white)
text_exp0 = fontf.render(f"Genes:", 1, red)
text_exp1 = fontf.render(f"1- 4. Pais", 1, blue)
text_exp2 = fontf.render(f"5 - 8. Filhos", 1, blue)
text_exp3 = fontf.render(f"9 - 10. Filhos com mutação", 1, blue)

#Ball
ball = pygame.Surface((10, 10))
xb = randint(150, 300)
ball.fill(red)

#Racket
racket = pygame.Surface((100, 10))
racket.fill(black)

#Time
time = pygame.time.Clock()

print("Jogo do ping - pong")
while True:
    r = 0
    ag.initialize_fitness()
    while r < 10:
        b = 3
        posracket = [175, 510]
        posball = [xb, 40]

        print(f"Peso {r+1}: {ag.weights[r]}")
        while b != 0:

            ag.get_r(r)
            text_balls = fontf.render(f"Bolas: {b}", 1, black)
            text_fitness = fontf.render(f"Fitness: {ag.fitness[r]}", 1, black)
            text_champion = fontf.render(f"Temos um vencedor!", 1, black)
            text_geration = fontf.render(f"Geration: {ag.geration + 1}", 1, black)
            text_gene = fontf.render(f"Gene: {r+1}", 1, black)
            
            time.tick(50)

            xrInput = posracket[0] + 50
            xbInput = posball[0] + 5

            ag.get_input(xbInput, xrInput)
            ag.calculing_the_moviments()

            if ag.y[3] and ag.y[4] > 0:
                if ag.y[3] > ag.y[4]:
                    direction = RIGHT
                elif ag.y[3] == ag.y[4]:
                    direction = STOP
                else:
                    direction = LEFT
            elif ag.y[3] > 0:
                direction = RIGHT
            else:
                direction = LEFT

            if posball[1] == posracket[1]:        
                if posball[0] >= posracket[0] and posball[0] <= posracket[0] + 90:
                    ag.fitness[r] += 1
                else:
                    b -= 1
                posball[0] = randint(150, 300)
                posball[1] = 50
            #The fall of the ball
            if posball[1] < 530:
                posball[1] += 10

            if direction == RIGHT and posracket[0] + 100 < 415:
                posracket[0] += 20
            elif direction == LEFT and posracket[0] > 40:
                posracket[0] -= 20

            tela.fill(royal_blue)
            tela.blit(game, (25, 55))
            tela.blit(ball,posball)
            tela.blit(text_balls, (35, 60))
            tela.blit(text_geration, (35, 80))
            tela.blit(text_gene, (35, 100))
            tela.blit(text_fitness, (35, 120))
            tela.blit(racket, posracket)
            tela.blit(label1, (440, 55))
            tela.blit(text_exp0, (450, 65))
            tela.blit(text_exp1, (450, 85))
            tela.blit(text_exp2, (450, 105))
            tela.blit(text_exp3, (450, 125))
            tela.blit(text_name, (250, 10))
                        
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    break

            pygame.display.update()
        r +=1
    ag.selection_of_the_bests()
    print(f"\nMelhores: {ag.bestw}")
    ag.reproduce_the_bests()
    print(f"Filhos: {ag.reprodutionw}")
    ag.mutatinon_()
    print(f"Filhos com mutação: {ag.mutation}\n")
    ag.new_population()

    ag.geration = ag.geration + 1
