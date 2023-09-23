import cocos.menu
import cocos.scene
import cocos.layer
import cocos.audio
import cocos.actions as ac
import cocos.audio.pygame
import cocos.audio.pygame.mixer
from cocos.director import director
from cocos.scenes.transitions import FadeTRTransition

import pyglet.app

import server
from server import accept_client
from Gamelayer import new_game_single
from Gamelayer_mul import new_game_multi

class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Cocos BomberMan')
        cocos.audio.pygame.mixer.init()
        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = list()
        items.append(cocos.menu.MenuItem('Single Play', self.on_single_game))
        items.append(cocos.menu.MenuItem('Multi Play', self.on_multi_game))
        items.append(cocos.menu.MenuItem('Quit', pyglet.app.exit))
        self.sound = cocos.audio.pygame.mixer.Sound('Menubackgroundmusic.wav')
        self.sound.play(-1)
        

        self.create_menu(items, ac.ScaleTo(1.0, duration = 0.25), ac.ScaleTo(1.0, duration = 0.25))
        

    # 게임 시작 CallFunc
    def on_single_game(self):
        director.push(FadeTRTransition(new_game_single(), duration = 0.2))
        self.sound.stop()
    def on_multi_game(self):
        director.push(FadeTRTransition(new_game_multi(), duration = 0.2))
        self.sound.stop()
        accept_client()
        

# Menu 시작 Scene
def new_menu():
    scene = cocos.scene.Scene()
    color_layer = cocos.layer.ColorLayer(245, 245, 220, 255)
    scene.add(MainMenu(), z=1)
    scene.add(color_layer, z=0)
    return scene