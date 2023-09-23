from Gamelayer_mul import new_game_multi
from cocos.director import director
from client import *

if __name__ == '__main__':
    Client()
    director.init(caption = 'Cocos BomberMan💣 Client')
    director.run(new_game_multi())
