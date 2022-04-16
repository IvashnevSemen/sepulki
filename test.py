class Cross(pygame.sprite.Sprite):
    def __init__(self, sheet, x, y):
        super().__init__(all_sprites)
        self.image = sheet
        self.rect = pygame.Rect(x, y, sheet.get_width(), sheet.get_height())



cross_group = pygame.sprite.Group()


cross = pygame.sprite.Sprite()
cross.image = pygame.image.load('cross.png')


if (item.rect.x < dead_zone.rect.x + dead_zone.rect.w or item.rect.x + item.rect.w > dead_zone.rect.x) and not item.in_hand:
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