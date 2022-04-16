if pygame.sprite.collide_mask(item, table):
    item.kill()
    player.is_hold = False
    item.in_hand = False
    up_line.update(b=1, s=30)