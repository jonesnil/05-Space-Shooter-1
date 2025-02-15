import sys, logging, os, random, math, open_color, arcade

#https://opengameart.org/sites/default/files/AlienSpaceShipInvasion_0.zip 
#https://opengameart.org/sites/default/files/space_ships.zip
#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {3}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Space shooter" 

NUM_ENEMIES = 5
STARTING_LOCATION = (200,100)
BULLET_DAMAGE = 20
ENEMY_HP = 100
HIT_SCORE = 20
KILL_SCORE = 100

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage, image):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__(image, 2)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/TM_7.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes an alien spaceship enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/alien_spaceship_invasion_11.png", 0.7,)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.blue_4)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0

    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            y = 120 * (i+1) + 40
            x = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)
                    

    def update(self, delta_time): 
        self.bullet_list.update()
        for e in self.enemy_list:
            hit = arcade.check_for_collision_with_list(e, self.bullet_list)
            for h in hit:
                e.hp=e.hp-h.damage
                h.kill()
                if e.hp<=0:
                    self.score += KILL_SCORE
                    
                    e.kill()
            pass
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse, The player shoots bullets with the mouse.
        '''
        self.player.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 45
            bullet = Bullet((x,y),(10,0),BULLET_DAMAGE,"assets/sword1.png")
            self.bullet_list.append(bullet)
            x = self.player.center_x
            y = self.player.center_y - 45
            bullet = Bullet((x,y),(10,0),BULLET_DAMAGE,"assets/sword1.png")
            self.bullet_list.append(bullet)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(10,0),BULLET_DAMAGE,"assets/Fireball2.png")
            self.bullet_list.append(bullet)
            x = self.player.center_x
            y = self.player.center_y
            bullet = Bullet((x,y),(10,0),BULLET_DAMAGE,"assets/Fireball2.png")
            self.bullet_list.append(bullet)
def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()