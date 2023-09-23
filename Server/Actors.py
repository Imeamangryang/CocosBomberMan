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

import Gamelayer


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

class Enemy(Actor):
    def __init__(self, x, y):
        super(Enemy, self).__init__('enemy.png', x, y)
        self.posx = int(self.position[0] // 32)
        self.posy = int(self.position[1] // 32)
        self.cshape = cm.AARectShape(self.position, self.width * 0.3, self.height * 0.3)
        self.speed = 50
        self.movedistance = 0
        self.distance_list = []
        self.enemymove = False
        self.enemylife = True
        self.movetime = 0.0
        # 1: 위 2: 아래 3: 왼쪽 4: 오른쪽
        self.direction = random.randint(1, 4)
        self.move_able()
        self.schedule(self.make_move)

    def make_move(self, dt):
        # 위쪽으로 이동할 때 
        if self.direction == 1:
            # 이동 목표 위치에 도달 못했을 때
            if self.position[1] < self.movedistance:
                new_x = self.position[0]
                new_y = self.position[1] + self.speed * dt
                if new_y > self.movedistance:
                    self.move(new_x, self.movedistance)
                else:
                    self.move(new_x, new_y)
            # 도달 했을때
            else:
               # 약간의 딜레이를 가짐.
               if self.movetime < 1.0:
                   self.movetime += dt
               # 다시 이동 가능한 목표를 잡음.
               else:
                   self.move_able()
                   self.movetime = 0.0

        # 아래쪽으로 이동할 때
        if self.direction == 2:
            if self.position[1] > self.movedistance:
                new_x = self.position[0]
                new_y = self.position[1] - self.speed * dt
                if new_y < self.movedistance:
                    self.move(new_x, self.movedistance)
                else:
                    self.move(new_x, new_y)
            else:
               if self.movetime < 1.0:
                   self.movetime += dt
               else:
                   self.move_able()
                   self.movetime = 0.0

        # 왼쪽으로 이동할 때
        if self.direction == 3:
            if self.position[0] > self.movedistance:
                new_x = self.position[0] - self.speed * dt
                new_y = self.position[1]
                if new_x < self.movedistance:
                    self.move(self.movedistance, new_y)
                else:
                    self.move(new_x, new_y)
            else:
               if self.movetime < 1.0:
                   self.movetime += dt
               else:
                   self.move_able()
                   self.movetime = 0.0
        # 오른쪽으로 이동할 때 
        if self.direction == 4:
            if self.position[0] < self.movedistance:
                new_x = self.position[0] + self.speed * dt
                new_y = self.position[1] 
                if new_x > self.movedistance:
                    self.move(self.movedistance, new_y)
                else:
                    self.move(new_x, new_y)
            else:
               if self.movetime < 1.0:
                   self.movetime += dt
               else:
                   self.move_able()
                   self.movetime = 0.0

    # 적 이동 함수
    def move(self, posx, posy):
        self.position = (posx, posy)
        self.cshape.center = self.position

    def move_able(self):
        # 초기화
        self.distance_list.clear()
        # 현재 위치 업데이트
        self.posx = int(self.position[0] // 32)
        self.posy = int(self.position[1] // 32)
        posx = self.posx
        posy = self.posy

        # 유효한 이동 방향 찾기
        while self.enemymove == False:
            self.direction = random.randint(1, 4)
            if self.direction == 1 and Gamelayer.GameLayer.map_tile[posy + 1][posx] != 0:
                self.direction = random.randint(1, 4)
            elif self.direction == 2 and Gamelayer.GameLayer.map_tile[posy - 1][posx] != 0:
                self.direction = random.randint(1, 4)
            elif self.direction == 3 and Gamelayer.GameLayer.map_tile[posy][posx - 1] != 0:
                self.direction = random.randint(1, 4)
            elif self.direction == 4 and Gamelayer.GameLayer.map_tile[posy][posx + 1] != 0:
                self.direction = random.randint(1, 4)
            else:
                self.enemymove = True

        # 유효한 이동 블럭 위치 리스트에 저장
        if self.direction == 1:
            while Gamelayer.GameLayer.map_tile[posy + 1][posx] == 0:
                self.distance_list.append((posy + 1) * 32 + 16)
                posy += 1
        elif self.direction == 2:
            while Gamelayer.GameLayer.map_tile[posy - 1][posx] == 0:
                self.distance_list.append((posy - 1) * 32 + 16)
                posy -= 1
        elif self.direction == 3:
            while Gamelayer.GameLayer.map_tile[posy][posx - 1] == 0:
                self.distance_list.append((posx - 1) * 32 + 16)
                posx -= 1
        else:
            while Gamelayer.GameLayer.map_tile[posy][posx + 1] == 0:
                self.distance_list.append((posx + 1) * 32 + 16)
                posx += 1

        # 유효한 이동 위치 중에 하나 뽑기
        self.movedistance = random.choice(self.distance_list)
        self.enemymove = False


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
        Gamelayer.GameLayer.disk[self.posy][self.posx] = None

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
        Gamelayer.GameLayer.disk[self.posy][self.posx] = None

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
        Gamelayer.GameLayer.disk[self.posy][self.posx] = None

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
        Gamelayer.GameLayer.BOMBNUMBER += 1
        Gamelayer.GameLayer.map_tile[self.posy][self.posx] = 4
        
        
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
        Gamelayer.GameLayer.map_tile[self.posy][self.posx] = 0
        Gamelayer.GameLayer.disk[self.posy][self.posx] = None
        Gamelayer.GameLayer.BOMBNUMBER -= 1
        # 터진 범위내의 동작
        for sector, x, y in zip(self.sectors, self.xList, self.yList):
            # 빈곳일 때
            if sector == 0 and Gamelayer.GameLayer.disk[y][x] is None:
                self.explosion = Explosion(x, y)
                self.gamelayer.add(self.explosion)

            # 다른 폭탄이 감지됐을 때
            elif sector == 0 and Gamelayer.GameLayer.disk[y][x] is not None:
                if isinstance(Gamelayer.GameLayer.disk[y][x], Bomb):
                    Gamelayer.GameLayer.disk[y][x].kill()
                    Gamelayer.GameLayer.disk[y][x] = None
                    print("another Bomb!")
                else:
                    Gamelayer.GameLayer.disk[y][x].kill()
                    Gamelayer.GameLayer.disk[y][x] = None
                    self.explosion = Explosion(x, y)
                    self.gamelayer.add(self.explosion)
                    print("Item extinction!")

            # 파괴가능블럭이 있을 때
            if sector == 3 and Gamelayer.GameLayer.disk[y][x] is not None:
                Gamelayer.GameLayer.disk[y][x].kill() 
                Gamelayer.GameLayer.disk[y][x] = None
                Gamelayer.GameLayer.map_tile[y][x] = 0
                # 30%의 확률로 아이템 생성
                rand = random.random()
                if rand < 0.3:
                    rand2 = random.random()
                    if rand2 < 0.3:
                        Gamelayer.GameLayer.disk[y][x] = BombItem(x, y)
                        self.gamelayer.add(Gamelayer.GameLayer.disk[y][x])
                        print("create")
                    elif 0.3 <= rand2 < 0.6:
                        Gamelayer.GameLayer.disk[y][x] = Bombpowder(x, y)
                        self.gamelayer.add(Gamelayer.GameLayer.disk[y][x])
                        print("create2")
                    else:
                        Gamelayer.GameLayer.disk[y][x] = Moveincrease(x, y)
                        self.gamelayer.add(Gamelayer.GameLayer.disk[y][x])
                        print("create3")

class Explosion(Actor):
    def __init__(self, x, y):
        super(Explosion, self).__init__('explosion.png', x, y)
        self.position = eu.Vector2((x * 32) + 16, (y * 32) + 16)
        self.cshape = cm.AARectShape(self.position, self.width * 0.4, self.height * 0.4)
        self.posx = x
        self.posy = y        

        self.do(ac.ScaleTo(1.2, 0.25) + ac.ScaleTo(1, 0.25))
        self.do(ac.Delay(0.5) + ac.CallFunc(self.kill))

    