import pygame
import time
pygame.init()

BLACK = (0, 0, 0)  # colours for use in window
P1_COLOUR = (0, 255, 255)  # player 1 trail colour
P2_COLOUR = (255, 0, 255)  # player 2 trail colour


class Player:
    def __init__(self, x, y, b, c):
        """
        init method for class
        """
        self.x = x  # player x coord
        self.y = y  # player y coord
        self.speed = 1  # player speed
        self.bearing = b  # player direction
        self.colour = c
        self.boost = False  # is boost active
        self.start_boost = time.time()  # used to control boost length
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  # player rect object

    def __draw__(self):
        """
        method for drawing player
        """
        self.rect = pygame.Rect(self.x - 1, self.y - 1, 2, 2)  # redefines rect
        pygame.draw.rect(screen, self.colour, self.rect, 0)  # draws player onto screen

    def __move__(self):
        """
        method for moving the player
        """
        if not self.boost:  # player isn't currently boosting
            self.x += self.bearing[0]
            self.y += self.bearing[1]
        else:  # player is boosting
            self.x += self.bearing[0] * 2
            self.y += self.bearing[1] * 2

    def __boost__(self):
        """
        starts the player boost
        """
        self.boost = True
        self.start_boost = time.time()


def new_game():
    new_p1 = Player(50, height / 2, (2, 0), P1_COLOUR)
    new_p2 = Player(width - 50, height / 2, (-2, 0), P2_COLOUR)
    return new_p1, new_p2


width, height = 640, 640  # window dimensions
screen = pygame.display.set_mode((width, height))  # creates window
pygame.display.set_caption("Tron")  # sets window title

clock = pygame.time.Clock()  # used to regulate FPS
check_time = time.time()  # used to check collisions with rects

objects = list()
path = list()
p1 = Player(50, height / 2, (2, 0), P1_COLOUR)
p2 = Player(width - 50, height / 2, (-2, 0), P2_COLOUR)
objects.append(p1)
path.append((p1.rect, '1'))
objects.append(p2)
path.append((p2.rect, '2'))

done = False
new = False
while not done:
    for event in pygame.event.get():  # gets all event in last tick
        if event.type == pygame.QUIT:  # close button pressed
            done = True
        elif event.type == pygame.KEYDOWN:
            # === Player 1 === #
            if event.key == pygame.K_w:
                objects[0].bearing = (0, -2)
            elif event.key == pygame.K_s:
                objects[0].bearing = (0, 2)
            elif event.key == pygame.K_a:
                objects[0].bearing = (-2, 0)
            elif event.key == pygame.K_d:
                objects[0].bearing = (2, 0)
            elif event.key == pygame.K_TAB:
                objects[0].__boost__()
            # === Player 2 === #
            if event.key == pygame.K_UP:
                objects[1].bearing = (0, -2)
            elif event.key == pygame.K_DOWN:
                objects[1].bearing = (0, 2)
            elif event.key == pygame.K_LEFT:
                objects[1].bearing = (-2, 0)
            elif event.key == pygame.K_RIGHT:
                objects[1].bearing = (2, 0)
            elif event.key == pygame.K_RSHIFT:
                objects[1].__boost__()

    screen.fill(BLACK)  # clears the screen

    for o in objects:
        if time.time() - o.start_boost >= 0.5:
            o.boost = False

        if (o.rect, '1') in path or (o.rect, '2') in path \
           or o.x < 0 or o.x > width or o.y < 0 \
           or o.y > height:  # not yet traversed
            if (time.time() - check_time) >= 0.1:
                check_time = time.time()
                new = True
                new_p1, new_p2 = new_game()
                objects = [new_p1, new_p2]
                path = [(p1.rect, '1'), (p2.rect, '2')]
        else:
            path.append((o.rect, '1')) if o.colour == P1_COLOUR else path.append((o.rect, '2'))

        o.__draw__()
        o.__move__()

    for r in path:
        if new is True:
            path = []
            new = False
            break
        if r[1] == '1': pygame.draw.rect(screen, P1_COLOUR, r[0], 0)
        else: pygame.draw.rect(screen, P2_COLOUR, r[0], 0)

    pygame.display.flip()  # flips display
    clock.tick(60)  # regulates FPS

pygame.quit()
