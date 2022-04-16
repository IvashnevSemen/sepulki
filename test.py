sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load('data/gameover.png')
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)


x = -600

if x != 10:
    sprite.rect = x, 0
    all_sprites.draw(screen)
    all_sprites.update()
    x += 10