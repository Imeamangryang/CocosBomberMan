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

import server
import Mainmenu
import Actors_mul

cocos.audio.pygame.mixer.init()

class GameLayer(cocos.layer.Layer):
    NICK_NAME = ""
    PRESS_UP = 0
    PRESS_DOWN = 0
    PRESS_RIGHT = 0
    PRESS_LEFT = 0
    PRESS_SPACE = 0
    is_event_handler = True
    BOMBNUMBER = 0
    BOMBNUMBER2 = 0
    ITEM_X = []
    ITEM_Y = []
    ITEM = []
    disk = [[None for i in range(20)] for j in range(15)]

    #0 : Moveable, 1 : Wall, 2 : Non-breakable Block, 3 : Breakable Block
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

    def on_key_press(self, symbol, _):
        Actors_mul.Player.KEYS_PRESSED[symbol] = 1
        Actors_mul.Player2.KEYS_PRESSED[symbol] = 1
        if symbol == key.UP:
            print("UP Keyboard Press")
            msg = "up"
            server.client.sendall(msg.encode())
        elif symbol == key.DOWN:
            print("DOWN Keyboard Press")
            msg = "down"
            server.client.sendall(msg.encode())
        elif symbol == key.RIGHT:
            print("RIGHT Keyboard Press")
            msg = "right"
            server.client.sendall(msg.encode())
        elif symbol == key.LEFT:
            print("LEFT Keyboard Press")
            msg = "left"
            server.client.sendall(msg.encode())
        elif symbol == key.SPACE:
            print("SPACE Keyboard Press")
            msg = "space"
            server.client.sendall(msg.encode())

    def on_key_release(self, symbol, _):
        Actors_mul.Player.KEYS_PRESSED[symbol] = 0
        Actors_mul.Player2.KEYS_PRESSED[symbol] = 0
        if symbol == key.UP:
            print("UP Keyboard Release")
            msg = "N_up"
            server.client.sendall(msg.encode())
        elif symbol == key.DOWN:
            print("DOWN Keyboard Release")
            msg = "N_down"
            server.client.sendall(msg.encode())
        elif symbol == key.RIGHT:
            print("RIGHT Keyboard Release")
            msg = "N_right"
            server.client.sendall(msg.encode())
        elif symbol == key.LEFT:
            print("LEFT Keyboard Release")
            msg = "N_left"
            server.client.sendall(msg.encode())
        elif symbol == key.SPACE:
            print("SPACE Keyboard Release")
            msg = "N_space"
            server.client.sendall(msg.encode())

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

        for x in range (0, self.row):
            for y in range (0, self.column):
                if self.maptile[y][x] == 2:
                    self.block = Actors_mul.Block((x*32)+16, (y*32)+16)
                    self.add(self.block)
                elif self.maptile[y][x] == 1:
                    self.wall = Actors_mul.Wall((x*32)+16, (y*32)+16)
                    self.add(self.wall)
                elif self.maptile[y][x] == 3:
                    GameLayer.disk[y][x] = Actors_mul.Break_block((x*32)+16, (y*32)+16)
                    self.add(GameLayer.disk[y][x])

        self.life = True
        self.player = Actors_mul.Player(48, 48)
        self.add(self.player)
        self.life2 = True
        self.player2 = Actors_mul.Player2(592, 432)
        self.add(self.player2)
        self.collman = cm.CollisionManagerGrid(0, 640, 0, 480, self.player.width,  self.player.width)
        self.schedule(self.update)
        

    def update(self, dt):
        self.collman.clear()

        for _, node in self.children:
            self.collman.add(node)

        # 플레이어1 이동 부분
        pressed = Actors_mul.Player.KEYS_PRESSED
        movement_x = pressed[key.RIGHT] - pressed[key.LEFT]
        movement_y = pressed[key.UP] - pressed[key.DOWN]
        pos = self.player.position
        if movement_x != 0 or movement_y != 0:
            new_x = pos[0] + self.player.speed * dt * movement_x
            new_y = pos[1] + self.player.speed * dt * movement_y
            self.player.position = (new_x, new_y)
            self.player.cshape.center = self.player.position

        # 플레이어2 이동 부분
        movement_x2 = GameLayer.PRESS_RIGHT - GameLayer.PRESS_LEFT
        movement_y2 = GameLayer.PRESS_UP - GameLayer.PRESS_DOWN
        pos2 = self.player2.position
        pos_x2 = int(pos2[0] // 32)
        pos_y2 = int(pos2[1] // 32)
        if movement_x2 != 0 or movement_y2 != 0:
            new_x = pos2[0] + self.player2.speed * dt * movement_x2
            new_y = pos2[1] + self.player2.speed * dt * movement_y2
            self.player2.position = (new_x, new_y)
            self.player2.cshape.center = self.player2.position

        # 폭탄 설치
        space_pressed = pressed[key.SPACE] == 1
        bomb_x = (int(pos[0] // 32))
        bomb_y = (int(pos[1] // 32))
        if space_pressed and GameLayer.BOMBNUMBER < self.player.bomb_number and GameLayer.disk[bomb_y][bomb_x] is None:
            if GameLayer.disk[bomb_y][bomb_x] is None:
                GameLayer.disk[bomb_y][bomb_x] = Actors_mul.Bomb(self.player.bomb_range, bomb_x, bomb_y, self.maptile, self.player, self.gamelayer)
                self.add(GameLayer.disk[bomb_y][bomb_x])
                self.bomb_sound = cocos.audio.pygame.mixer.Sound('bomb.wav')
                self.bomb_sound.play()

        # 폭탄 설치
        space_pressed2 = GameLayer.PRESS_SPACE == 1
        bomb_x2 = (int(pos2[0] // 32))
        bomb_y2 = (int(pos2[1] // 32))
        if space_pressed2 and GameLayer.BOMBNUMBER2 < self.player2.bomb_number and GameLayer.disk[bomb_y2][bomb_x2] is None:
            if GameLayer.disk[bomb_y2][bomb_x2] is None:
                GameLayer.disk[bomb_y2][bomb_x2] = Actors_mul.Bomb2(self.player2.bomb_range, bomb_x2, bomb_y2, self.maptile, self.player2, self.gamelayer)
                self.add(GameLayer.disk[bomb_y2][bomb_x2])
                self.bomb_sound = cocos.audio.pygame.mixer.Sound('bomb.wav')
                self.bomb_sound.play()

        # 플레이어1 충돌 처리
        for other in self.collman.iter_colliding(self.player):
            print("플레이어 1 충돌물체 : %s" % type(other))
            #other.kill()
            # 플레이어가 폭발에 맞았을 때
            if isinstance(other, Actors_mul.Explosion):
                #print("die")
                if self.life is True:
                    self.player.kill()
                    self.gameover_sound = cocos.audio.pygame.mixer.Sound('gameover.wav')
                    self.gameover_sound.play()
                    self.life = False
                    self.unschedule(self.update)
                    self.win = self.hud.show_game_win(self.gamelayer, GameLayer.NICK_NAME)
                    self.add(self.win)
                    self.backgroundsound.stop()
            # 플레이어가 폭탄 증가 아이템을 습득했을 때
            elif isinstance(other, Actors_mul.BombItem):
                self.sound = cocos.audio.pygame.mixer.Sound('bombplus.wav')
                self.sound.play()
                other.kill()
                self.player.bomb_number += 1
            # 플레이어가 폭탄 범위 증가 아이템을 습득했을 때
            elif isinstance(other, Actors_mul.Bombpowder):
                self.sound = cocos.audio.pygame.mixer.Sound('bombpowder.wav')
                self.sound.play()
                other.kill()
                self.player.bomb_range += 1
            # 플레이어가 이동속도 증가 아이템을 습득했을 때
            elif isinstance(other, Actors_mul.Moveincrease):
                self.sound = cocos.audio.pygame.mixer.Sound('moveincre.wav')
                self.sound.play()
                other.kill()
                self.player.speed += 10
            elif isinstance(other, Actors_mul.Player2):
                pass
            # 이외의 충돌하면 안되는 것들
            else:
                self.player.position = (pos[0], pos[1])
                self.player.cshape.center = self.player.position

            # 플레이어1 충돌 처리
        for other in self.collman.iter_colliding(self.player2):
            print("플레이어 2 충돌물체 : %s" % type(other))
            #other.kill()
            # 플레이어가 폭발에 맞았을 때
            if isinstance(other, Actors_mul.Explosion):
                #print("die")
                if self.life2 is True:
                    self.player2.kill()
                    self.gameover_sound = cocos.audio.pygame.mixer.Sound('gameover.wav')
                    self.gameover_sound.play()
                    self.life2 = False
                    self.unschedule(self.update)
                    self.win2 = self.hud.show_game_win(self.gamelayer, "Developer")
                    self.add(self.win2)
                    self.backgroundsound.stop()
            # 플레이어가 폭탄 증가 아이템을 습득했을 때
            elif isinstance(other, Actors_mul.BombItem):
                self.sound = cocos.audio.pygame.mixer.Sound('bombplus.wav')
                self.sound.play()
                other.kill()
                self.player2.bomb_number += 1
            # 플레이어가 폭탄 범위 증가 아이템을 습득했을 때
            elif isinstance(other, Actors_mul.Bombpowder):
                self.sound = cocos.audio.pygame.mixer.Sound('bombpowder.wav')
                self.sound.play()
                other.kill()
                self.player2.bomb_range += 1
            # 플레이어가 이동속도 증가 아이템을 습득했을 때
            elif isinstance(other, Actors_mul.Moveincrease):
                self.sound = cocos.audio.pygame.mixer.Sound('moveincre.wav')
                self.sound.play()
                other.kill()
                self.player2.speed += 10
            elif isinstance(other, Actors_mul.Player):
                pass
            # 이외의 충돌하면 안되는 것들
            else:
                self.player2.position = (pos2[0], pos2[1])
                self.player2.cshape.center = self.player2.position

        if self.life is False and self.life2 is False:
            self.win.kill()
            self.win2.kill()
            self.hud.show_game_draw(self.gamelayer)

class HUD(cocos.layer.Layer):
    def __init__(self):
        super(HUD, self).__init__()
        w, h = director.get_window_size()

    def show_game_win(self, layer, player):
        w, h = director.get_window_size()
        game_win = cocos.text.Label('%s Win!' % player, font_size=50,
                                     anchor_x='center',
                                     anchor_y='center')
        game_win.position = w * 0.5, h * 0.5
        return game_win
        

    def show_game_draw(self, layer):
        w, h = director.get_window_size()
        game_win = cocos.text.Label('Ended in a Draw', font_size=50,
                                     anchor_x='center',
                                     anchor_y='center')
        game_win.position = w * 0.5, h * 0.5
        layer.add(game_win)
            
# 게임 시작 Scene
def new_game_multi():
    main_scene = cocos.scene.Scene()
    tmx_map = cocos.tiles.load('Map.tmx')
    bg = tmx_map['Map0']
    bg.set_view(0, 0, bg.px_width, bg.px_height)
    main_scene.add(bg, z = 0)
    hud = HUD()
    game_layer = GameLayer(hud)
    main_scene.add(game_layer, z = 1)
    return main_scene
