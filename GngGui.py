import g2d
from GngGame import GngGame
class GngGui():
    def __init__(self, viewport_size=(400-2, 239-10)):
        self._x_view,self._y_view = 2,10
        self._w_view, self._h_view = 400,239
        self._initial_image_x = 2
        self._initial_image_y = 10
        self._end_image_x = 3585
        self._end_image_y = 239
        self._game = GngGame()
        self.viewport_size = viewport_size
        g2d.init_canvas(self.viewport_size, 2)
        g2d.main_loop(self.tick)
    
    def tick(self):
        g2d.clear_canvas()
        g2d.draw_image("./assets/sprites/ghosts-goblins-bg.png", (-self._initial_image_x,-self._initial_image_y),(self._x_view, self._y_view),(self._w_view,self._h_view) )
        for a in self._game.actors():
            if a.sprite() != None:
                x, y = a.pos()
                g2d.draw_image("./assets/sprites/ghosts-goblins.png", (x - self._x_view, y - self._y_view), a.sprite(), a.size())
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
        g2d.draw_text(f"Lives: {lives} Time: {time}", (250, 12), 24)

        if self._game.game_over():
            g2d.alert("Game over")
            g2d.close_canvas()
        elif self._game.game_won():
            g2d.alert("Game won")
            g2d.close_canvas()
        else:
            self._game.tick(g2d.current_keys())

