import g2d
from GngGame import GngGame
import json
from model.SnowFlake import SnowFlake
from random import randint
class GngGui():
    def __init__(self, viewport_size=(400-2, 239-10)):
        self._x_view,self._y_view = 2,10
        self._w_view, self._h_view = 400,239
        self._initial_image_x = 2
        self._initial_image_y = 10
        self._end_image_x = 3585
        self._end_image_y = 239
        self.viewport_size = viewport_size
        

        self._prev_keys = set()
        self._key_buffer = ""
        self._snow = False
        self._max_snow_duration = 6*60
        self._snow_duration = self._max_snow_duration
        self._game = GngGame()


        with open("config.json") as f:
            data = json.load(f)
        #loading position of the number of the sprite
        self._numbers = [tuple(x) for x in data["numbers"]]
        self._time_text = tuple(data["time_text"])
        self._player1_text = tuple(data["player1_text"])
        self._top_score_text = tuple(data["top_score_text"])
        self._top_score = int(data["top_score"])

        
        g2d.init_canvas(self.viewport_size, 2)
        g2d.main_loop(self.tick)
    
    def tick(self):
        g2d.clear_canvas()
        keys = g2d.current_keys()
        #get the word just once since the tick goes too fast
        pressed_now = set(keys) - set(self._prev_keys)
        # catch if the player write "snow"
        for k in pressed_now:
            if len(k) == 1 and k.isalpha():
                self._key_buffer += k.lower()
                self._key_buffer = self._key_buffer[-4:]

        self._prev_keys = keys
        if self._key_buffer == "snow":
            #reset the buffer
            self._prev_keys = set()
            self._snow = True
            self._snow_duration = 0
        
        self._snow_duration = min(self._snow_duration+1, self._max_snow_duration)
        if self._snow and not(self._snow_duration == self._max_snow_duration):
            self.snowing()
        

        g2d.draw_image("./assets/sprites/ghosts-goblins-bg.png", (-self._initial_image_x,-self._initial_image_y),(self._x_view, self._y_view),(self._w_view,self._h_view) )
        for a in self._game.actors():
            if a.sprite() != None:
                x, y = a.pos()
                image = "./assets/sprites/ghosts-goblins.png"
                if isinstance(a, SnowFlake):
                    image = "./assets/sprites/snowflakes.png"
                    g2d.draw_image(image, (x - self._x_view, y - self._y_view), a.sprite(), a.size())
                else:
                    g2d.draw_image(image, (x - self._x_view, y - self._y_view), a.sprite(), a.size())
                g2d.draw_image("./assets/sprites/ghosts-goblins-babbinatale.png", (x - self._x_view, y - self._y_view), a.sprite(), a.size())
            else:
                pass
        
        #check collisions of the view
    
        if "ArrowUp" in g2d.current_keys():
            self._y_view = max(self._y_view - 5, self._initial_image_y)
        elif "ArrowDown" in g2d.current_keys():
            self._y_view = min(self._y_view + 5, self._initial_image_y)    
            
        elif "ArrowRight" in g2d.current_keys():
            self._x_view = min(self._x_view + 5, self._end_image_x - self._w_view-2)
        elif "ArrowLeft" in g2d.current_keys():
            self._x_view = max(self._x_view - 5, self._initial_image_x)

        lives, time = self._game.lives(), self._game.time() // 30
        # g2d.draw_text(f"Lives: {lives} Time: {time}", (250, 12), 24)
        g2d.draw_image("./assets/sprites/ghosts-goblins-babbinatale.png", (20, 3), self._player1_text[0], self._player1_text[1])
        for i,x in enumerate(self.score_to_font_img(self._game.score())):
            g2d.draw_image("./assets/sprites/ghosts-goblins-babbinatale.png", (20+i*8, 12), x[0], x[1])
        
        g2d.draw_image("./assets/sprites/ghosts-goblins-babbinatale.png", (100, 3), self._top_score_text[0], self._top_score_text[1])
        for i,x in enumerate(self.score_to_font_img(self._top_score)):
            g2d.draw_image("./assets/sprites/ghosts-goblins-babbinatale.png", (100+i*8, 12), x[0], x[1])

        g2d.draw_image("./assets/sprites/ghosts-goblins-babbinatale.png", (20, 25), self._time_text[0], self._time_text[1])
        for i,x in enumerate(self.number_to_font_img(time)):
            g2d.draw_image("./assets/sprites/ghosts-goblins-babbinatale.png", (20+i*8, 34), x[0], x[1])
        
        

        if self._game.game_over():
            self.save_top_score()
            g2d.alert("Game over")
            g2d.close_canvas()
        elif self._game.game_won():
            self.save_top_score()
            g2d.alert("Game won")
            g2d.close_canvas()
        else:
            self._game.tick(g2d.current_keys())
    
    def snowing(self):
        s = randint(0, 20)
        if s == 0:
            n = randint(0, 25)
            for i in range(n):
                x = randint(self._x_view, self._x_view+self._w_view)
                y = -20
                self._game.spawn(SnowFlake((x, y)))
    
    def save_top_score(self):
        with open("config.json", "r") as f:
            data = json.load(f)
            data["top_score"] = self._game.score() if self._game.score() > self._top_score else self._top_score
        with open("config.json", "w") as f:
            json.dump(data, f, indent=4, separators=(", ", ": "))

    def number_to_font_img(self, num: int) -> tuple:
        ### return the start position of the sprite and the size
        converted = []
        for v in str(num):
            tmp = []
            tmp.append(self._numbers[int(v)][0])
            tmp.append(self._numbers[int(v)][1])
            converted.append(tuple(tmp))
        return converted

    def score_to_font_img(self, num: int) -> tuple:
        num = min(9999, num)
        num = "0"*(4-len(str(num)))+str(num)
        return self.number_to_font_img(num)

