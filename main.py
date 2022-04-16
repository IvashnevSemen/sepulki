import pygame
from pygame.locals import *
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, hp):
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


class Machine(pygame.sprite.Sprite):
    def __init__(self, mach_img, x, y):
        super().__init__(all_sprites)
        self.image = mach_img
        self.rect = pygame.Rect(x, y, mach_img.get_width(), mach_img.get_height())
        self.x = x
        self.y = y


class Cross(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y):
        super().__init__(all_sprites)
        self.image = sheet
        self.rect = pygame.Rect(x, y, sheet.get_width(), sheet.get_height())


class UpLine:
    def __init__(self, lives, boxes, score):
        self.lives = lives
        self.boxes = boxes
        self.score = score

    def update(self, l=0, b=0, s=0):
        global hp, score, b_count
        if l != 0:
            self.lives += l
        if b != 0:
            self.boxes += b
        if s != 0:
            self.score += s
        pygame.draw.rect(screen, 'white', (0, 0, width // 3, 100), 1)
        pygame.draw.rect(screen, 'white', (width // 3, 0, width // 3, 100), 1)
        pygame.draw.rect(screen, 'white', (width // 3 * 2, 0, width // 3, 100), 1)

        hp_text = font.render(f'Попытки: {self.lives}', True, (255, 0, 0))
        score_text = font.render(f'Счёт: {self.score}', True, (0, 255, 0))
        count_text = font.render(f'Собрано сепулек: {self.boxes}', True, (0, 255, 255))

        screen.blit(hp_text, (width // 6 - 40, 50))
        screen.blit(score_text, (width * 4 // 5 - 40, 50))
        screen.blit(count_text, (width // 2 - 80, 50))


def draw_cross():
    pass


size = width, height = 800, 600

m_width = 300
m_height = 100

tbl_width = 150
tbl_height = 100
tbl_x_pos = width // 2
tbl_y_pos = 100

all_sprites = pygame.sprite.Group()
cross_group = pygame.sprite.Group()
boxes = pygame.sprite.Group()

m1_x_pos = 500
m1_y_pos = height - m_height - 200
m2_y_pos = height - m_height - 100
m3_y_pos = height - m_height

dead_zone = (0, 200, width - m_width, height)

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Сепульки')

    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font(None, 30)

    FPS = 8
    vol = 0.05
    clock = pygame.time.Clock()

    # music
    pygame.mixer.music.load("was_wollen_wir_trinken.mp3")
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play(-1)

    cross = pygame.sprite.Sprite()
    cross.image = pygame.transform.scale(pygame.image.load('cross.png'), (40, 40))
    # draw table
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.transform.scale(pygame.image.load('table.png'), (tbl_width, tbl_height))
    table = Machine(sprite.image, tbl_x_pos - tbl_width // 2, tbl_y_pos)

    # draw machines
    sprite.image = pygame.transform.scale(pygame.image.load('machine.png'), (m_width, m_height))
    machine1 = Machine(sprite.image, m1_x_pos, m1_y_pos)
    machine2 = Machine(sprite.image, m1_x_pos, m2_y_pos)
    machine3 = Machine(sprite.image, m1_x_pos, m3_y_pos)

    # draw player
    sprite.image = pygame.image.load('worker.png')
    player = Player(sprite.image, 4, 4, width // 2, height // 2, 3)

    # draw box
    sprite.image = pygame.transform.scale(pygame.image.load('box.png'), (40, 40))
    # box = Box(sprite.image, m1_x_pos + m_width // 2 - 10, m1_y_pos + 20)

    up_line = UpLine(10, 0, 0)

    all_sprites.add(player)
    # boxes.add(box)

    flPause = False
    running = True
    t = 0
    while running:

        a = randint(1, 3)
        screen.fill("black")
        t += 1
        if t % 20 == 10 and not player.is_hold:
            box = Box(sprite.image, m1_x_pos + m_width // 2 - 10, m1_y_pos + 115 * a)
            all_sprites.add(box)
            boxes.add(box)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        key = pygame.key.get_pressed()
        if key[K_p]:
            flPause = not flPause
            if flPause:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        if key[K_a]:
            player.move(-10, 0)
            player.dir = 0
            player.update()
        elif key[K_d]:
            player.move(10, 0)
            player.dir = 2
            player.update()
        elif key[K_s]:
            player.move(0, 10)
            player.dir = 1
            player.update()
        elif key[K_w]:
            player.move(0, -10)
            player.dir = 3
            player.update()
        else:
            player.update()
        up_line.update()

        for item in boxes:
            if not player.is_hold:
                item.rect.x -= item.speed
            if pygame.sprite.collide_mask(player, item) and player.is_hold == False and key[K_SPACE]:
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
            if pygame.sprite.collide_mask(item, table) and key[K_SPACE]:
                item.kill()
                player.is_hold = False
                item.in_hand = False
                up_line.update(b=1, s=30)
            if (item.rect.x < dead_zone[0] + dead_zone[2] and item.rect.x + item.rect.w > dead_zone[0]) \
                    and not item.in_hand:
                cross_image = Cross(cross.image, item.rect.x, item.rect.y)
                cross_group.add(cross_image)
                cross_group.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)
                cross_image.kill()
                cross_image = Cross(cross.image, item.rect.x, item.rect.y)
                cross_group.add(cross_image)
                cross_group.draw(screen)
                pygame.display.flip()
                clock.tick(FPS)
                cross_image.kill()
                item.kill()
                up_line.update(l=-1)

        all_sprites.draw(screen)
        clock.tick(FPS)

        pygame.display.flip()
pygame.quit()
