import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
class AliensInvasion:
    """管理游戏资源和行为的类"""
    """在init函数在调用pygame.init来初始化背景"""
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        """pygame.display.set_mode((1200,800))创建一个显示窗口 返回一个游戏的展示屏幕"""
        """窗口复制给self.screen 以便这个类的所有方法都能使用"""
        #全屏显示代码
        # self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height),
        #                                       pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Aliens Invasion") #设置标题
        #创建存储游戏统计信息的实例，并创建计分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        #创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        #self.bg_color = (230,230,230)
        self.ship = Ship(self)
        #创建一个子弹的编组
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #游戏启动后处于活跃状态
        self.game_active = False
        self.play_button = Button(self, "play")
    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._check_bullet_alien_collisions()
            self._update_aliens()
            print(len(self.bullets))
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """响应案件和鼠标事件"""
        """使用 pygame.event.get() 函数来访问 Pygame 检测到的事件。
                    这个函数返回一个列表，其中包含它在上一次调用后发生的所有事件。"""
        for event in pygame.event.get(): #用for循环迭代每一个事件
            if event.type == pygame.QUIT:
                sys.exit()
            #如果按下右键 就把飞船的位置向右移动一位
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        """在玩家单击play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            """重置游戏的统计信息"""
            self.stats.reset_stats()
            self.game_active = True
            #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #创建一个外星人舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        self.bullets.update()
        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 检查是否有子弹击中了外星人
        # 如果是 就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
        if not self.aliens:
            # 删除现有子弹并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
    def _update_screen(self):
        "更新屏幕上的图像，并切换到屏幕"
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #显示得分
        self.sb.show_score()
        #如果游戏处于非活动状态，就绘制play按钮
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip() #用新的代替旧的 表示移动

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建一个外星舰队"""
        alien = Alien(self)
        #外星人的间距为外星人的宽度
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._creat_alien(current_x, current_y)
                current_x += 2 * alien_width
            #添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2 * alien_height
    def _creat_alien(self, x_position,y_position):
        """创建一个外星人并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，更新外星舰队中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        """检查外星人和飞船之间的碰撞"""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _ship_hit(self):
        """响应外星人和飞船的碰撞"""
        if self.stats.ship_left > 0:
            #将ship_left减1
            self.stats.ship_left -= 1
            #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            #暂停
            sleep(1)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #like飞船被撞到一样处理
                self._ship_hit()
                break
if __name__ == '__main__':
    ai = AliensInvasion()
    ai.run_game()