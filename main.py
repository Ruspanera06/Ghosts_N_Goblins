from random import choice, randrange, randint
from actor import Actor, Arena, Point
from Arthur import Arthur
from math import cos, sin, radians


x_view,y_view = 300,200
w_view, h_view = 400,400
def tick():
    g2d.clear_canvas()
    global x_view,y_view, w_view, h_view
    g2d.draw_image("https://fondinfo.github.io/sprites/ghosts-goblins-bg.png", (0,0),(x_view, y_view),(w_view,h_view) )
    for a in arena.actors():
        if a.sprite() != None:
            x, y = a.pos()
            g2d.draw_image("sprites.png", (x - x_view, y - y_view), a.sprite(), a.size())
        else:
            pass  # g2d.draw_rect(a.pos(), a.size())

    arena.tick(g2d.current_keys())  # Game logic
    if "ArrowUp" in g2d.current_keys():
        y_view = max(y_view-5, 0)
    elif "ArrowDown" in g2d.current_keys():
        y_view = min(y_view + 5, h_view)    
        
    elif "ArrowRight" in g2d.current_keys():
        x_view = min(x_view + 5, w_view)
    elif "ArrowLeft" in g2d.current_keys():
        x_view = max(x_view - 5, 0)


def main():
    global g2d, arena
    import g2d  # game classes do not depend on g2d

    arena = Arena((480, 360))
    arena.spawn(Arthur((230, 170)))

    g2d.init_canvas((w_view,h_view),2)
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()