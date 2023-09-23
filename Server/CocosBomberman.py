from cocos.director import director
from Mainmenu import new_menu

if __name__ == '__main__':
    director.init(caption = 'Cocos BomberMan💣')
    director.run(new_menu())