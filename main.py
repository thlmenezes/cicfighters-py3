import pygame
# ----------- Game Initialization -------------------
pygame.init()

displayWidth, displayHeight = 700, 800

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Basic Pygame Template')
clock = pygame.time.Clock()

# ----------- Constants ---------------
FPS = 60
backgroundColor = "black"


# ----------- Main Game Function ---------------
def runGame():
    # Game Variables
    gameRunning = True
    gameOver = False

# ----------- Start Of Game Loop ---------------
    while gameRunning:
        gameDisplay.fill(backgroundColor)

# ----------- Game Over Menu -------------------
# Use this loop as a template for any other screens you want to add.
        while gameOver:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                        gameRunning = False
                        gameOver = False
                    if event.key == pygame.K_c:
                        runGame()

# ----------- Gameplay Handling -------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
            if event.type == pygame.MOUSEBUTTONUP:
                print(f'Mouse was clicked at {pygame.mouse.get_pos()}')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    print('left')
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    print('right')
                if event.key == pygame.K_UP or event.key == ord('w'):
                    print('up')
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    print('down')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    print('left stop')
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    print('right stop')
                if event.key == pygame.K_UP or event.key == ord('w'):
                    print('up stop')
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    print('down stop')
                if event.key == ord('q'):
                    pygame.quit()
                    gameRunning = False
                    exit()
                    # NOTE: exit on ESC key press
                # if event.key == pygame.K_ESCAPE:
                #     pygame.quit()
                #     gameRunning = False
                #     exit()

#  ----------- Game Code -------------------
        # Draw

        # Update
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    runGame()
