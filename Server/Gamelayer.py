from cocos.director import director
from cocos.scenes.transitions import SplitColsTransition, FadeTransition

import cocos.layer
import cocos.scene
import cocos.text
import cocos.actions as ac
import cocos.collision_model as cm
import cocos.tiles
import cocos.euclid as eu
import cocos.audio.pygame
import cocos.audio.pygame.mixer

from pyglet.window import key
from cocos import mapcolliders

import numpy as np

import Mainmenu
import Actors

cocos.audio.pygame.mixer.init()

class GameLayer(cocos.layer.Layer):
    is_event_handler = True
    BOMBNUMBER = 0
    disk = [[None for i in range(20)] for j in range(15)] # 폭탄이 놓였는지 확인하는 용도

    #0 : Moveable, 1 : Wall, 2 : Non-breakable Block, 3 : Breakable Block 4: Bomb
    map_tile = np.array([ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 1],
                          [1, 0, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 0, 1],
                          [1, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 1],
                          [1, 3, 2, 3, 3, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 3, 3, 2, 3, 1],
                          [1, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 1],
                          [1, 3, 2, 3, 3, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 3, 3, 2, 3, 1],
                          [1, 3, 0, 3, 3, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 3, 3, 0, 3, 1],
                          [1, 3, 2, 3, 3, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 3, 3, 2, 3, 1],
                          [1, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 1],
                          [1, 3, 2, 3, 3, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 3, 3, 2, 3, 1],
                          [1, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                          [1, 0, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 0, 1],
                          [1, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ])

    #map_tile = np.array([ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #                      [1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1],
    #                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #                      [1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1],
    #                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #                      [1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1],
    #                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #                      [1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1],
    #                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #                      [1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1],
    #                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #                      [1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 1],
    #                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ])

    # 키보드 이벤트
    def on_key_press(self, key, _):
        Actors.Player.KEYS_PRESSED[key] = 1

    def on_key_release(self, key, _):
        Actors.Player.KEYS_PRESSED[key] = 0

    def __init__(self, hud):
        super(GameLayer, self).__init__()
        self.backgroundsound = cocos.audio.pygame.mixer.Sound('gamebackground.wav')
        self.backgroundsound.play(-1)
        self.hud = hud
        self.row = 20
        self.column = 15
        self.gamelayer = self

        # 0 : Moveable, 1 : Wall, 2 : Non-breakable Block, 3 : Breakable Block
        self.maptile = GameLayer.map_tile

        self.disk = [[None for i in range(self.row)] for j in range(self.column)]

        # 맵 타일에 따라 맵 생성
        for x in range (0, self.row):
            for y in range (0, self.column):
                if self.maptile[y][x] == 2:
                    self.block = Actors.Block((x*32)+16, (y*32)+16)
                    self.add(self.block)
                elif self.maptile[y][x] == 1:
                    self.wall = Actors.Wall((x*32)+16, (y*32)+16)
                    self.add(self.wall)
                elif self.maptile[y][x] == 3:
                    GameLayer.disk[y][x] = Actors.Break_block((x*32)+16, (y*32)+16)
                    self.add(GameLayer.disk[y][x])

        # 플레이어와 적 추가
        self.life = True
        self.enemyexistence = False
        self.player = Actors.Player(48, 48)
        self.add(self.player)
        self.enemy = Actors.Enemy(592, 432)
        self.add(self.enemy)
        self.enemy2 = Actors.Enemy(48, 432)
        self.add(self.enemy2)
        self.enemy3 = Actors.Enemy(592, 48)
        self.add(self.enemy3)
        self.enemy4 = Actors.Enemy(336, 240)
        self.add(self.enemy4)
        self.collman = cm.CollisionManagerGrid(0, 640, 0, 480, self.player.width,  self.player.width)
        self.schedule(self.update)
        

    def update(self, dt):
        self.collman.clear()
        self.enemyexistence = False

        for _, node in self.children:
            self.collman.add(node)
            # 적이 있는지 확인
            if isinstance(node, Actors.Enemy) and self.enemyexistence is False:
                self.enemyexistence = True

        # 맵 내의 적이 모두 제거되었을 경우 게임 끝
        if self.enemyexistence is False:
            self.unschedule(self.update)
            self.hud.show_game_win(self.gamelayer)

        # 플레이어 이동 부분
        pressed = Actors.Player.KEYS_PRESSED
        movement_x = pressed[key.RIGHT] - pressed[key.LEFT]
        movement_y = pressed[key.UP] - pressed[key.DOWN]
        pos = self.player.position
        if movement_x != 0 or movement_y != 0:
            new_x = pos[0] + self.player.speed * dt * movement_x
            new_y = pos[1] + self.player.speed * dt * movement_y
            self.player.position = (new_x, new_y)
            self.player.cshape.center = self.player.position

        # 폭탄 설치
        space_pressed = pressed[key.SPACE] == 1
        bomb_x = (int(pos[0] // 32))
        bomb_y = (int(pos[1] // 32))
        if space_pressed and GameLayer.BOMBNUMBER < self.player.bomb_number and GameLayer.disk[bomb_y][bomb_x] is None:
            if GameLayer.disk[bomb_y][bomb_x] is None:
                GameLayer.disk[bomb_y][bomb_x] = Actors.Bomb(self.player.bomb_range, bomb_x, bomb_y, self.maptile, self.player, self.gamelayer)
                self.add(GameLayer.disk[bomb_y][bomb_x])
                self.bomb_sound = cocos.audio.pygame.mixer.Sound('bomb.wav')
                self.bomb_sound.play()

        # 플레이어 충돌 처리
        for other in self.collman.iter_colliding(self.player):
            print("충돌물체 : %s" % type(other))
            #other.kill()
            # 플레이어가 폭발에 맞았을 때
            if isinstance(other, Actors.Explosion):
                #print("die")
                if self.life is True:
                    self.player.kill()
                    self.gameover_sound = cocos.audio.pygame.mixer.Sound('gameover.wav')
                    self.gameover_sound.play()
                    self.life = False
                    self.unschedule(self.update)
                    self.hud.show_game_over(self.gamelayer)
                    self.backgroundsound.stop()
            # 플레이어가 폭탄 증가 아이템을 습득했을 때
            if isinstance(other, Actors.BombItem):
                self.sound = cocos.audio.pygame.mixer.Sound('bombplus.wav')
                self.sound.play()
                other.kill()
                self.player.bomb_number += 1
            # 플레이어가 폭탄 범위 증가 아이템을 습득했을 때
            if isinstance(other, Actors.Bombpowder):
                self.sound = cocos.audio.pygame.mixer.Sound('bombpowder.wav')
                self.sound.play()
                other.kill()
                self.player.bomb_range += 1
            # 플레이어가 이동속도 증가 아이템을 습득했을 때
            if isinstance(other, Actors.Moveincrease):
                self.sound = cocos.audio.pygame.mixer.Sound('moveincre.wav')
                self.sound.play()
                other.kill()
                self.player.speed += 10
            # 플레이어가 적군과 충돌했을 때
            if isinstance(other, Actors.Enemy):
                if self.life is True:
                    self.player.kill()
                    self.gameover_sound = cocos.audio.pygame.mixer.Sound('gameover.wav')
                    self.gameover_sound.play()
                    self.life = False

            # 이외의 충돌하면 안되는 것들
            self.player.position = (pos[0], pos[1])
            self.player.cshape.center = self.player.position

        # enemy 처리
        for other in self.collman.iter_colliding(self.enemy):
            if isinstance(other, Actors.Explosion):
                if self.enemy.enemylife is True:
                    self.enemy.kill()
                    self.gameover_sound = cocos.audio.pygame.mixer.Sound('gameover.wav')
                    self.gameover_sound.play()
                    self.enemy.enemylife = False
        for other in self.collman.iter_colliding(self.enemy2):
            if isinstance(other, Actors.Explosion):
                if self.enemy2.enemylife is True:
                    self.enemy2.kill()
                    self.gameover_sound = cocos.audio.pygame.mixer.Sound('gameover.wav')
                    self.gameover_sound.play()
                    self.enemy2.enemylife = False
        for other in self.collman.iter_colliding(self.enemy3):
            if isinstance(other, Actors.Explosion):
                if self.enemy3.enemylife is True:
                    self.enemy3.kill()
                    self.gameover_sound = cocos.audio.pygame.mixer.Sound('gameover.wav')
                    self.gameover_sound.play()
                    self.enemy3.enemylife = False
        for other in self.collman.iter_colliding(self.enemy4):
            if isinstance(other, Actors.Explosion):
                if self.enemy4.enemylife is True:
                    self.enemy4.kill()
                    self.gameover_sound = cocos.audio.pygame.mixer.Sound('gameover.wav')
                    self.gameover_sound.play()
                    self.enemy4.enemylife = False


class HUD(cocos.layer.Layer):
    def __init__(self):
        super(HUD, self).__init__()
        w, h = director.get_window_size()

    def show_game_over(self, layer):
        w, h = director.get_window_size()
        game_over = cocos.text.Label('Game Over', font_size=50,
                                     anchor_x='center',
                                     anchor_y='center')
        game_over.position = w * 0.5, h * 0.5
        layer.add(game_over)

    def show_game_win(self, layer):
        w, h = director.get_window_size()
        game_win = cocos.text.Label('Game Win!', font_size=50,
                                     anchor_x='center',
                                     anchor_y='center')
        game_win.position = w * 0.5, h * 0.5
        layer.add(game_win)
            
# 게임 시작 Scene
def new_game_single():
    main_scene = cocos.scene.Scene()
    tmx_map = cocos.tiles.load('Map.tmx')
    bg = tmx_map['Map0']
    bg.set_view(0, 0, bg.px_width, bg.px_height)
    main_scene.add(bg, z = 0)
    hud = HUD()
    game_layer = GameLayer(hud)
    main_scene.add(game_layer, z = 1)
    return main_scene
