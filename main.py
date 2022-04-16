import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.x = x
        self.y = y
        self.dir = 0
        self.is_hold = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(columns):
            self.frames.append([])
            for i in range(rows):
                frame_location = (self.rect.w * j, self.rect.h * i)
                self.frames[j].append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.dir == 0:
            self.cur_frame = (self.cur_frame + 1) % 4
            self.image = self.frames[0][self.cur_frame]
        if self.dir == 1:
            self.cur_frame = (self.cur_frame + 1) % 4
            self.image = self.frames[1][self.cur_frame]
        if self.dir == 2:
            self.cur_frame = (self.cur_frame + 1) % 4
            self.image = self.frames[2][self.cur_frame]
        if self.dir == 3:
            self.cur_frame = (self.cur_frame + 1) % 4
            self.image = self.frames[3][self.cur_frame]

    def move(self, x, y):
        if self.x + self.rect.w + x <= width and self.x + x >= 0 \
                and self.y + self.rect.h + y <= height and self.y + y >= 0:
            self.x += x
            self.y += y
            self.rect = self.rect.move(x, y)


class Box(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y):
        super().__init__(all_sprites)
        self.image = sheet
        self.rect = pygame.Rect(x, y, sheet.get_width(), sheet.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.speed = 5
        self.visible = True
        self.in_hand = False

    def update(self):
        pass


class UpLine:
    def __init__(self, lives, boxes, score):
        self.lives = lives
        self.boxes = boxes
        self.score = score

    def update(self, l=0, b=0, s=0):
        if l != 0:
            self.lives += l
        if b != 0:
            self.boxes += b
        if s != 0:
            self.score += s


TABLE = (100, 100, 100, 100)

all_sprites = pygame.sprite.Group()
boxes = pygame.sprite.Group()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Сепульки')

    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    fps = 5
    clock = pygame.time.Clock()

    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load('worker.png')
    player = Player(sprite.image, 4, 4, 0, 0)

    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.transform.scale(pygame.image.load('box.png'), (40, 40))
    box = Box(sprite.image, 100, 100)

    all_sprites.add(player)
    boxes.add(box)

    running = True
    while running:
        screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            player.move(-10, 0)
            player.dir = 0
            player.update()
        elif key[K_RIGHT]:
            player.move(10, 0)
            player.dir = 2
            player.update()
        elif key[K_DOWN]:
            player.move(0, 10)
            player.dir = 1
            player.update()
        elif key[K_UP]:
            player.move(0, -10)
            player.dir = 3
            player.update()
        else:
            player.update()
        for item in boxes:
            if pygame.sprite.collide_mask(player, item) and player.is_hold == False:
                player.is_hold = True
                item.in_hand = True
            if item.in_hand:
                if player.dir == 0:
                    item.rect.x = player.rect.x - item.rect.w
                    item.rect.y = player.rect.y
                if player.dir == 1:
                    item.rect.x = player.rect.x
                    item.rect.y = player.rect.y + player.rect.h
                if player.dir == 2:
                    item.rect.x = player.rect.x + player.rect.w
                    item.rect.y = player.rect.y
                if player.dir == 3:
                    item.rect.x = player.rect.x
                    item.rect.y = player.rect.y - item.rect.h

        all_sprites.draw(screen)
        clock.tick(fps)

        pygame.display.flip()
pygame.quit()