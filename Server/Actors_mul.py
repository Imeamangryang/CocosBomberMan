import random
import cocos.sprite
import cocos.actions as ac
import cocos.euclid as eu
import cocos.collision_model as cm
import cocos.particle_systems as ps
import numpy as np

from collections import defaultdict
from pyglet.image import load
from pyglet.window import key

import server
import Gamelayer_mul


class Actor(cocos.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Actor, self).__init__(image, position = (x, y))
        self.position = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(self.position, self.width * 0.5, self.height * 0.5)

    def move(self, offset):
        self.position += offset
        self.cshape.center += offset

    def update(self, elapsed):
        pass

    def collide(self, other):
        pass

class Player(Actor):
    KEYS_PRESSED = defaultdict(int)
    def __init__(self, x, y):
        super(Player, self).__init__('Player.png', x, y) # 나중에 이미지 추가
        self.speed = 100
        self.bomb_range = 2
        self.bomb_number = 1

    def collide(self, other):
        if isinstance(other, Explosion):
            self.kill()

    def get_position(self):
        return self.position

    def get_cshape(self):
        return self.cshape

class Player2(Actor):
    KEYS_PRESSED = defaultdict(int)
    def __init__(self, x, y):
        super(Player2, self).__init__('Player2.png', x, y) # 나중에 이미지 추가
        self.speed = 100
        self.bomb_range = 2
        self.bomb_number = 1

    def collide(self, other):
        if isinstance(other, Explosion):
            self.kill()

    def get_position(self):
        return self.position

    def get_cshape(self):
        return self.cshape

# 폭탄 개수 증가 아이템
class BombItem(Actor):
    def __init__(self, x, y):
        super(BombItem, self).__init__('item.png', x, y)
        self.position = eu.Vector2((x * 32) + 16, (y * 32) + 16)
        self.cshape = cm.AARectShape(self.position, self.width * 0.1, self.height * 0.1)
        self.posx = x
        self.posy = y

    def on_exit(self):
        super(BombItem, self).on_exit()
        Gamelayer_mul.GameLayer.disk[self.posy][self.posx] = None

# 폭탄 범위 증가 아이템
class Bombpowder(Actor):
    def __init__(self, x, y):
        super(Bombpowder, self).__init__('item2.png', x, y)
        self.position = eu.Vector2((x * 32) + 16, (y * 32) + 16)
        self.cshape = cm.AARectShape(self.position, self.width * 0.1, self.height * 0.1)
        self.posx = x
        self.posy = y

    def on_exit(self):
        super(Bombpowder, self).on_exit()
        Gamelayer_mul.GameLayer.disk[self.posy][self.posx] = None

# 이동 속도 증가 아이템
class Moveincrease(Actor):
    def __init__(self, x, y):
        super(Moveincrease, self).__init__('item3.png', x, y)
        self.position = eu.Vector2((x * 32) + 16, (y * 32) + 16)
        self.cshape = cm.AARectShape(self.position, self.width * 0.1, self.height * 0.1)
        self.posx = x
        self.posy = y

    def on_exit(self):
        super(Moveincrease, self).on_exit()
        Gamelayer_mul.GameLayer.disk[self.posy][self.posx] = None

# 파괴불가능한 블럭
class Block(Actor):
    def __init__(self, x, y):
        super(Block, self).__init__('Block.png', x, y)
        self.position = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(self.position, self.width * 0.3, self.height * 0.3)

class Break_block(Actor):
    def __init__(self, x, y):
        super(Break_block, self).__init__('Block2.png', x, y)
        self.position = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(self.position, self.width * 0.3, self.height * 0.3)

class Wall(Actor):
    def __init__(self, x, y):
        super(Wall, self).__init__('blank.png', x, y)
        self.position = eu.Vector2(x, y)
        self.cshape = cm.AARectShape(self.position, self.width * 0.3, self.height * 0.3)

class Bomb(Actor):
    def __init__(self, r, x, y, map, player, gamelayer):
        super(Bomb, self).__init__('Bomb.png', x, y)
        self.position = eu.Vector2((x * 32) + 16, (y * 32) + 16)
        self.range = r
        self.player = player
        self.gamelayer = gamelayer
        self.posx = x
        self.posy = y
        self.sectors = list()
        self.xList = list()
        self.yList = list()
        self.reload = 0.0
        self.time = 0
        self.period = 3.5
        self.get_range(map)
        self.bomb_knows = False
        self.do(ac.ScaleTo(2, 0.5) + ac.ScaleTo(1, 0.5) + ac.ScaleTo(1.5, 0.5) + ac.Blink(7, 2))
        self.schedule(self.update)
        Gamelayer_mul.GameLayer.BOMBNUMBER += 1
        Gamelayer_mul.GameLayer.map_tile[self.posy][self.posx] = 4
        
        
    def update(self, dt):
        # 폭탄이 처음 플레이어가 설치했을 때에는 콜리젼 반응 X
        if self.bomb_knows == False:
            pos = self.player.get_position()
            if abs(self.position[0] - pos[0]) >= 32 or abs(self.position[1] - pos[1]) >= 32:
                self.cshape = cm.AARectShape(self.position, self.width * 0.2, self.height * 0.2)
                self.bomb_knows = True

        # 3.5초뒤에 폭발
        self.time += dt
        if self.time >= 3.5:
            self.kill()

    # 폭발 범위 리스트 저장
    def get_range(self, map):
        self.sectors.append(map[self.posy][self.posx])
        self.xList.append(self.posx)
        self.yList.append(self.posy)
        # 4방향 탐지
        for x in range(1, self.range):
            if map[self.posy + x][self.posx] == 0:
                self.sectors.append(map[self.posy + x][self.posx])
                self.xList.append(self.posx)
                self.yList.append(self.posy + x)
            elif map[self.posy + x][self.posx] == 3:
                self.sectors.append(map[self.posy + x][self.posx])
                self.xList.append(self.posx)
                self.yList.append(self.posy + x)
                break
            else:
                break
        for x in range(1, self.range):
            if map[self.posy - x][self.posx] == 0:
                self.sectors.append(map[self.posy - x][self.posx])
                self.xList.append(self.posx)
                self.yList.append(self.posy - x)
            elif map[self.posy - x][self.posx] == 3:
                self.sectors.append(map[self.posy - x][self.posx])
                self.xList.append(self.posx)
                self.yList.append(self.posy - x)
                break
            else:
                break
        for x in range(1, self.range):
            if map[self.posy][self.posx + x] == 0:
                self.sectors.append(map[self.posy][self.posx + x])
                self.xList.append(self.posx + x)
                self.yList.append(self.posy)
            elif map[self.posy][self.posx + x] == 3:
                self.sectors.append(map[self.posy][self.posx + x])
                self.xList.append(self.posx + x)
                self.yList.append(self.posy)
                break
            else:
                break
        for x in range(1, self.range):
            if map[self.posy][self.posx - x] == 0:
                self.sectors.append(map[self.posy][self.posx - x])
                self.xList.append(self.posx - x)
                self.yList.append(self.posy)
            elif map[self.posy][self.posx - x] == 3:
                self.sectors.append(map[self.posy][self.posx - x])
                self.xList.append(self.posx - x)
                self.yList.append(self.posy)
                break
            else:
                break


    def on_exit(self):
        super(Bomb, self).on_exit()
        #터질때의 동작
        self.sound = cocos.audio.pygame.mixer.Sound('explosion.wav')
        self.sound.play()
        Gamelayer_mul.GameLayer.map_tile[self.posy][self.posx] = 0
        Gamelayer_mul.GameLayer.disk[self.posy][self.posx] = None
        Gamelayer_mul.GameLayer.BOMBNUMBER -= 1
        # 터진 범위내의 동작
        for sector, x, y in zip(self.sectors, self.xList, self.yList):
            # 빈곳일 때
            if sector == 0 and Gamelayer_mul.GameLayer.disk[y][x] is None:
                self.explosion = Explosion(x, y)
                self.gamelayer.add(self.explosion)

            # 다른 폭탄이 감지됐을 때
            elif sector == 0 and Gamelayer_mul.GameLayer.disk[y][x] is not None:
                if isinstance(Gamelayer_mul.GameLayer.disk[y][x], Bomb):
                    Gamelayer_mul.GameLayer.disk[y][x].kill()
                    Gamelayer_mul.GameLayer.disk[y][x] = None
                    print("Bomb!")
                elif isinstance(Gamelayer_mul.GameLayer.disk[y][x], Bomb2):
                    Gamelayer_mul.GameLayer.disk[y][x].kill()
                    Gamelayer_mul.GameLayer.disk[y][x] = None
                    print("another Bomb!")
                else:
                    Gamelayer_mul.GameLayer.disk[y][x].kill()
                    Gamelayer_mul.GameLayer.disk[y][x] = None
                    self.explosion = Explosion(x, y)
                    self.gamelayer.add(self.explosion)
                    print("Item extinction!")

            # 파괴가능블럭이 있을 때
            if sector == 3 and Gamelayer_mul.GameLayer.disk[y][x] is not None:
                Gamelayer_mul.GameLayer.disk[y][x].kill() 
                Gamelayer_mul.GameLayer.disk[y][x] = None
                Gamelayer_mul.GameLayer.map_tile[y][x] = 0
                rand = random.random()
                if rand < 0.3:
                    rand2 = random.random()
                    if rand2 < 0.3:
                        Gamelayer_mul.GameLayer.disk[y][x] = BombItem(x, y)
                        self.gamelayer.add(Gamelayer_mul.GameLayer.disk[y][x])
                        print("create")
                        msg = "BombItem"
                        server.client.send(msg.encode())
                        msg = str(x) + "," + str(y)
                        server.client.send(msg.encode())
                    elif 0.3 <= rand2 < 0.6:
                        Gamelayer_mul.GameLayer.disk[y][x] = Bombpowder(x, y)
                        self.gamelayer.add(Gamelayer_mul.GameLayer.disk[y][x])
                        print("create2")
                        msg = "BombPowder"
                        server.client.send(msg.encode())
                        msg = str(x) + "," + str(y)
                        server.client.send(msg.encode())
                    else:
                        Gamelayer_mul.GameLayer.disk[y][x] = Moveincrease(x, y)
                        self.gamelayer.add(Gamelayer_mul.GameLayer.disk[y][x])
                        print("create3")
                        msg = "Moveincrease"
                        server.client.send(msg.encode())
                        msg = str(x) + "," + str(y)
                        server.client.send(msg.encode())

class Bomb2(Actor):
    def __init__(self, r, x, y, map, player, gamelayer):
        super(Bomb2, self).__init__('Bomb2.png', x, y)
        self.position = eu.Vector2((x * 32) + 16, (y * 32) + 16)
        self.range = r
        self.player = player
        self.gamelayer = gamelayer
        self.posx = x
        self.posy = y
        self.sectors = list()
        self.xList = list()
        self.yList = list()
        self.reload = 0.0
        self.time = 0
        self.period = 3.5
        self.get_range(map)
        self.bomb_knows = False
        self.do(ac.ScaleTo(2, 0.5) + ac.ScaleTo(1, 0.5) + ac.ScaleTo(1.5, 0.5) + ac.Blink(7, 2))
        self.schedule(self.update)
        Gamelayer_mul.GameLayer.BOMBNUMBER2 += 1
        Gamelayer_mul.GameLayer.map_tile[self.posy][self.posx] = 4
        
        
    def update(self, dt):
        # 폭탄이 처음 플레이어가 설치했을 때에는 콜리젼 반응 X
        if self.bomb_knows == False:
            pos = self.player.get_position()
            if abs(self.position[0] - pos[0]) >= 32 or abs(self.position[1] - pos[1]) >= 32:
                self.cshape = cm.AARectShape(self.position, self.width * 0.2, self.height * 0.2)
                self.bomb_knows = True

        # 3.5초뒤에 폭발
        self.time += dt
        if self.time >= 3.5:
            self.kill()

    # 폭발 범위 리스트 저장
    def get_range(self, map):
        self.sectors.append(map[self.posy][self.posx])
        self.xList.append(self.posx)
        self.yList.append(self.posy)
        # 4방향 탐지
        for x in range(1, self.range):
            if map[self.posy + x][self.posx] == 0:
                self.sectors.append(map[self.posy + x][self.posx])
                self.xList.append(self.posx)
                self.yList.append(self.posy + x)
            elif map[self.posy + x][self.posx] == 3:
                self.sectors.append(map[self.posy + x][self.posx])
                self.xList.append(self.posx)
                self.yList.append(self.posy + x)
                break
            else:
                break
        for x in range(1, self.range):
            if map[self.posy - x][self.posx] == 0:
                self.sectors.append(map[self.posy - x][self.posx])
                self.xList.append(self.posx)
                self.yList.append(self.posy - x)
            elif map[self.posy - x][self.posx] == 3:
                self.sectors.append(map[self.posy - x][self.posx])
                self.xList.append(self.posx)
                self.yList.append(self.posy - x)
                break
            else:
                break
        for x in range(1, self.range):
            if map[self.posy][self.posx + x] == 0:
                self.sectors.append(map[self.posy][self.posx + x])
                self.xList.append(self.posx + x)
                self.yList.append(self.posy)
            elif map[self.posy][self.posx + x] == 3:
                self.sectors.append(map[self.posy][self.posx + x])
                self.xList.append(self.posx + x)
                self.yList.append(self.posy)
                break
            else:
                break
        for x in range(1, self.range):
            if map[self.posy][self.posx - x] == 0:
                self.sectors.append(map[self.posy][self.posx - x])
                self.xList.append(self.posx - x)
                self.yList.append(self.posy)
            elif map[self.posy][self.posx - x] == 3:
                self.sectors.append(map[self.posy][self.posx - x])
                self.xList.append(self.posx - x)
                self.yList.append(self.posy)
                break
            else:
                break


    def on_exit(self):
        super(Bomb2, self).on_exit()
        #터질때의 동작
        self.sound = cocos.audio.pygame.mixer.Sound('explosion.wav')
        self.sound.play()
        Gamelayer_mul.GameLayer.map_tile[self.posy][self.posx] = 0
        Gamelayer_mul.GameLayer.disk[self.posy][self.posx] = None
        Gamelayer_mul.GameLayer.BOMBNUMBER2 -= 1
        # 터진 범위내의 동작
        for sector, x, y in zip(self.sectors, self.xList, self.yList):
            # 빈곳일 때
            if sector == 0 and Gamelayer_mul.GameLayer.disk[y][x] is None:
                self.explosion = Explosion(x, y)
                self.gamelayer.add(self.explosion)

            # 다른 폭탄이 감지됐을 때
            elif sector == 0 and Gamelayer_mul.GameLayer.disk[y][x] is not None:
                if isinstance(Gamelayer_mul.GameLayer.disk[y][x], Bomb):
                    Gamelayer_mul.GameLayer.disk[y][x].kill()
                    Gamelayer_mul.GameLayer.disk[y][x] = None
                    print("Bomb!")
                elif isinstance(Gamelayer_mul.GameLayer.disk[y][x], Bomb2):
                    Gamelayer_mul.GameLayer.disk[y][x].kill()
                    Gamelayer_mul.GameLayer.disk[y][x] = None
                    print("another Bomb!")
                else:
                    Gamelayer_mul.GameLayer.disk[y][x].kill()
                    Gamelayer_mul.GameLayer.disk[y][x] = None
                    self.explosion = Explosion(x, y)
                    self.gamelayer.add(self.explosion)
                    print("Item extinction!")

            # 파괴가능블럭이 있을 때
            if sector == 3 and Gamelayer_mul.GameLayer.disk[y][x] is not None:
                Gamelayer_mul.GameLayer.disk[y][x].kill() 
                Gamelayer_mul.GameLayer.disk[y][x] = None
                Gamelayer_mul.GameLayer.map_tile[y][x] = 0
        for item, x, y in zip(Gamelayer_mul.GameLayer.ITEM, Gamelayer_mul.GameLayer.ITEM_X, Gamelayer_mul.GameLayer.ITEM_Y):
            if item == 1:
                Gamelayer_mul.GameLayer.disk[y][x] = BombItem(x, y)
                self.gamelayer.add(Gamelayer_mul.GameLayer.disk[y][x])
            elif item == 2:
                Gamelayer_mul.GameLayer.disk[y][x] = Bombpowder(x, y)
                self.gamelayer.add(Gamelayer_mul.GameLayer.disk[y][x])
            elif item == 3:
                Gamelayer_mul.GameLayer.disk[y][x] = Moveincrease(x, y)
                self.gamelayer.add(Gamelayer_mul.GameLayer.disk[y][x])
        Gamelayer_mul.GameLayer.ITEM.clear()
        Gamelayer_mul.GameLayer.ITEM_X.clear()
        Gamelayer_mul.GameLayer.ITEM_Y.clear()

class Explosion(Actor):
    def __init__(self, x, y):
        super(Explosion, self).__init__('explosion.png', x, y)
        self.position = eu.Vector2((x * 32) + 16, (y * 32) + 16)
        self.cshape = cm.AARectShape(self.position, self.width * 0.4, self.height * 0.4)
        self.posx = x
        self.posy = y        

        self.do(ac.ScaleTo(1.2, 0.25) + ac.ScaleTo(1, 0.25))
        self.do(ac.Delay(0.5) + ac.CallFunc(self.kill))

    