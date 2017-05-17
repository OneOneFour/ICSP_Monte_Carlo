import pygame
import monte

BLACK = (0,0,0)


isRunning = True
width,height = 800,480
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.flip()
font = pygame.font.Font(None,25)
predtext = font.render("Predator",1,(0,0,0))
preytext = font.render("Prey",1,(0,0,0))
world = monte.World()
world.SpawnNow(monte.Predator(0.66,0.3,1.0,0.5,2,1,"Predator"),10)
world.SpawnNow(monte.Prey(0.66,0.3,4.0,2.0,"Prey"),15)
while isRunning:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                world.step()
    screen.fill((255, 255, 255))
    #Render code here
    screen.blit(font.render("Year: " + str(world.t),1,BLACK),(width/2,10))
    for i in range(len(world.getPredators())):
        pred = world.getPredators()[i]
        pDetail = font.render("Predator #"+ str(pred.id) +": Age " + str(pred.age) ,1,BLACK)
        screen.blit(pDetail,(25,15*i +45))
    for i in range(len(world.getPrey())):
        prey = world.getPrey()[i]
        pDetail = font.render("Prey #"+str(prey.id)+": Age " + str(prey.age),1,BLACK)
        screen.blit(pDetail,(width-25-pDetail.get_width(),15*i +45))
    screen.blit(predtext,(25,10))
    screen.blit(preytext,(width-25-preytext.get_width(),10))
    pygame.display.flip()


