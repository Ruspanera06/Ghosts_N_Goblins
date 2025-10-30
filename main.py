from random import choice, randrange, randint
from actor import Actor, Arena, Point
from model.Arthur import Arthur
from math import cos, sin, radians
from model.Zombie import Zombie
from model.Gravestone import Gravestone
from model.Platform import Platform

x_view,y_view = 2,10
w_view, h_view = 400,239
initial_image_x = 2
initial_image_y = 10
end_image_x = 3585
end_image_y = 239
def tick():
    global initial_image_x, initial_image_y, end_image_x, end_image_y
    g2d.clear_canvas()
    global x_view,y_view, w_view, h_view
    g2d.draw_image("./assets/sprites/ghosts-goblins-bg.png", (-initial_image_x,-initial_image_y),(x_view, y_view),(w_view,h_view) )

    #zombie spawning chance
    n = randrange(150)
    if n == 0:
        for x in arena.actors():
            if isinstance(x, Arthur) and len(arena.actors()) == 1:
                r = randint(20, 200)
                direction = choice([1, -1])
                z_pos = ((x.pos()[0] + (-1*direction*r)), arena.size()[1] - 69)
                arena.spawn(Zombie(z_pos, direction))
                break

    ######      drawing logic       #####
    for a in arena.actors():
        if a.sprite() != None:
            x, y = a.pos()
            g2d.draw_image("./assets/sprites/ghosts-goblins.png", (x - x_view, y - y_view), a.sprite(), a.size())
        else:
            pass  # g2d.draw_rect(a.pos(), a.size())

    arena.tick(g2d.current_keys())  # Game logic
    if "ArrowUp" in g2d.current_keys():
        y_view = max(y_view - 5, initial_image_y)
    elif "ArrowDown" in g2d.current_keys():
        y_view = min(y_view + 5, initial_image_y)    
        
    elif "ArrowRight" in g2d.current_keys():
        x_view = min(x_view + 5, end_image_x - w_view-2)
    elif "ArrowLeft" in g2d.current_keys():
        x_view = max(x_view - 5, initial_image_x)


def main():
    global w_view, h_view
    global g2d, arena
    import g2d  # game classes do not depend on g2d
    #-45
    arena = Arena((3585, h_view))
    arena.spawn(Arthur((100, 150)))
    # arena.spawn(Zombie((300, 165)))
    # arena.spawn(Zombie((300, 165)))
    g2d.init_canvas((w_view-2,h_view-10),2)
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()