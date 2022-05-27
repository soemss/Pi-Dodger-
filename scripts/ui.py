from scripts.config import *

def menu():
    click = False
    menuTitle = font.render('Vehicle', False, (255, 255, 255))
    menuTitle2 = font.render('Dodge', False, (255, 255, 255))
    playText = font.render('Play', False, (0, 0, 0))
    while True:
        background()
        screen.blit(menuTitle, (200, 100))
        screen.blit(menuTitle2, (225, 160))
        mouseX, mouseY = pygame.mouse.get_pos()
        startButton = pygame.Rect(200, 450, 200, 60)

        if startButton.collidepoint((mouseX, mouseY)):
            if click:
                game()
        pygame.draw.rect(screen, (255, 255, 255), startButton)
        screen.blit(playText, (startButton.x + 50, startButton.y + 5))
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.flip()


def gameOver():
    click = False
    g = font.render('Game ', False, (255, 0, 0))
    over = font.render("Over", False, (255, 0, 0))
    restartText = font.render("Retry", False, (0, 0, 0))
    while True:
        screen.blit(over, (screenWidth / 2, 130))
        screen.blit(g, (screenWidth / 2, 70))

        mouseX, mouseY = pygame.mouse.get_pos()
        restart = pygame.Rect(125, 460, 250, 60)

        if restart.collidepoint((mouseX, mouseY)):
            if click:
                game()
        pygame.draw.rect(screen, (255, 255, 255), restart)
        screen.blit(restartText, (restart.x + 8, restart.y + 7))
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.flip()