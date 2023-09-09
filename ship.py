import pygame
class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.settins = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()

        #每艘新飞船都放在屏幕底部的中央
        #让飞船图像外接矩形底部中央位置等于屏幕底部中央位置
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        #移动过于慢了 给飞船添加一个属性 作为移动标志
        self.moving_right = False #注意飞船一开始不动
        self.moving_left= False

    def update(self):
        """根据移动标志来调整飞船的位置"""
        #飞船的右边缘小于屏幕的右边缘
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settins.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settins.ship_speed
        #根据self.x更新rect对象
        self.rect.x = self.x
    def blitme(self):
        """在指定的位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)