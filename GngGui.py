import g2d
import GngGame
class GngGui():
    def __init__(self, viewport_size=(400, 239)):
        self._x_view,self._y_view = 2,10
        self._w_view, self._h_view = 400,239
        self._initial_image_x = 2
        self._initial_image_y = 10
        self._end_image_x = 3585
        self._end_image_y = 239
        self._game = GngGame()
        g2d.init_canvas(self._game.size())
        g2d.main_loop(self.tick)
    
    def tick(self):
        g2d.clear_canvas()
        for a in self._game.actors():
            if a.sprite() != None:
                g2d.draw_image("sprites.png", a.pos(), a.sprite(), a.size())

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

