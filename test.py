def move(self, x, y):
    if self.x + self.width + x <= width and self.x + x >= 0 \
            and self.y + self.height + y <= height and self.y + y >= 0:
        self.x += x
        self.y += y