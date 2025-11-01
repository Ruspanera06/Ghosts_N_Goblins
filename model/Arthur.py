from actor import Actor, Arena, Point
from random import choice, randint
from model.Torch import Torch
from model.Platform import Platform 
#animations sprites
#the tuple will contain ((start_x, start_y), (end_x, end_y)) of the png
IDLE_RIGHT_ARMOR = ((5, 42), (26, 73))
IDLE_LEFT_ARMOR = ((485, 42), (506, 74))
IDLE_RIGHT_NAKED = ((6, 76), (25, 106))
IDLE_LEFT_NAKED = ((486, 76), (505, 106))

JUMP_RIGHT_ARMOR = [
    ((143, 28), (176, 56)),
    ((179, 28), (207, 56))
]
JUMP_LEFT_ARMOR = [
    ((304, 28), (332, 56)),
    ((335, 28), (368, 56))
][::1]

JUMP_RIGHT_NAKED = [
    ((144, 61), (174, 88)),
    ((182, 61), (206, 88))
]
JUMP_LEFT_NAKED = [
    ((305, 61), (329, 88)),
    ((337, 61), (367, 88))
][::-1]


RUNNING_RIGHT_ARMOR = [
    ((39, 41),(63, 72)), 
    ((65, 41), (85, 74)), 
    ((88, 41), (107, 74)), 
    ((108, 41), (133, 72))
]
sprite_x = 511
RUNNING_LEFT_ARMOR = []
#mirroring RUNNING_RIGHT_ARMOR so it become RUNNING_LEF_ARMOR
for s in RUNNING_RIGHT_ARMOR:
    s_x = (s[1][0]-s[0][0])
    x = sprite_x - s[0][0] - s_x
    y = s[0][1]
    size_x = x + s_x
    size_y = s[1][1]
    RUNNING_LEFT_ARMOR.append(
        ((x, y), (size_x, size_y))
    )

RUNNING_RIGHT_NAKED = [
    ((36, 76), (62, 101)),
    ((66, 76),(84, 106)),
    ((90, 76),(106, 106)),
    ((109, 76), (134, 102))
]

RUNNING_LEFT_NAKED = []
#mirroring RUNNING_RIGHT_ARMOR so it become RUNNING_LEF_ARMOR
for s in RUNNING_RIGHT_NAKED:
    s_x = (s[1][0]-s[0][0])
    x = sprite_x - s[0][0] - s_x
    y = s[0][1]
    size_x = x + s_x
    size_y = s[1][1]
    RUNNING_LEFT_NAKED.append(
        ((x, y), (size_x, size_y))
    )



class Arthur(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._dx, self._dy = 0, 0
        self._jump = False
        self.max_jump = 40
        self._djump = 15
        self._speed = 3
        self._health = 1
        self._attack_speed = 10
        self._attack_frame = self._attack_speed
        
        #animation stats
        self._sprite_start, self._sprite_end = IDLE_RIGHT_ARMOR
        self._frame = 0
        self._duration_frame = 3
        self._direction = 0 
        self._jump_anim = False
        self._i_jump = None
        
        

    def move(self, arena: Arena):
            G = 2
            aw, ah = arena.size()
            keys = arena.current_keys()

            # ==========================================================
            # 1. GESTIONE INPUT E ATTACCO (Il tuo codice, invariato)
            # ==========================================================

            self._dx = 0
            if "a" in keys:
                self._dx -= self._speed
                self._direction = 1
            elif "d" in keys:
                self._direction = 0
                self._dx += self._speed
            
            if "f" in keys:
                if self._attack_frame == self._attack_speed:
                    self.throw_Torch(arena)
                    self._attack_frame = 0
            
            self._attack_frame = min(self._attack_frame+1, self._attack_speed)

            # ==========================================================
            # 2. GESTIONE FISICA E COLLISIONI (Logica di Mario)
            #    (Questa parte SOSTITUISCE la tua vecchia fisica)
            # ==========================================================

            # Partiamo dal presupposto di essere in aria
            self._is_grounded = False

            # 2.1 Controllo Pavimento (Se vuoi mantenere un pavimento di "base" oltre alle piattaforme)
            floor_y = ah - 45  # Il tuo "pavimento" originale
            if self._y + self._h >= floor_y and self._dy >= 0:
                self._y = floor_y - self._h
                self._dy = 0
                self._is_grounded = True
                self._jump_anim = False # Siamo atterrati

            # 2.2 Controllo Piattaforme (La logica a 4 lati di Mario)
            for other in arena.collisions():
                if isinstance(other, Platform):
                    plat_x, plat_y = other.pos()
                    plat_w, plat_h = other.size()

                    # 1. Atterraggio ⤓ (Stiamo cadendo e siamo sopra la piattaforma)
                    if self._y < plat_y and self._dy >= 0:
                        self._y = plat_y - self._h  # Atterrato
                        self._dy = 0
                        self._is_grounded = True
                        self._jump_anim = False # Siamo atterrati
                    
                    # 2. Testa sbattuta ⤒ (Stiamo salendo e siamo sotto la piattaforma)
                    elif self._y + self._h > plat_y + plat_h and self._dy <= 0:
                        self._y = plat_y + plat_h + 1
                        self._dy = 0
                    
                    # 3. Scontro a sinistra ⇥ (Andiamo a dx e colpiamo il lato sx)
                    elif self._x < plat_x and self._dx >= 0:
                        self._x = plat_x - self._w
                        self._dx = 0 # Blocca movimento orizzontale
                    
                    # 4. Scontro a destra ⇤ (Andiamo a sx e colpiamo il lato dx)
                    elif self._x + self._w > plat_x + plat_w and self._dx <= 0:
                        self._x = plat_x + plat_w
                        self._dx = 0 # Blocca movimento orizzontale

            # 2.3 Gestione Salto (Controlla il tasto ORA che sappiamo se siamo a terra)
            if ("Spacebar" in keys or "w" in keys) and self._is_grounded:
                self._dy = -self._djump  # Salta! (Usa la tua variabile _djump)
                self._jump_anim = True
                self._i_jump = None
                
            # ==========================================================
            # 3. APPLICA FISICA E MOVIMENTO FINALE
            # ==========================================================
            
            # Applica gravità
            self._dy += G 
            
            # Applica movimento
            self._x += self._dx
            self._y += self._dy

            # Clamp ai bordi dell'arena (Il tuo clamp per X, ma per Y solo in alto)
            self._x = min(max(self._x, 5), aw - self._w)
            self._y = max(self._y, 5) # Clamp solo per il "cielo"
                                    # Il fondo è gestito da 'floor_y' e dalle piattaforme


            # ==========================================================
            # 4. ANIMATION ZONE (Il tuo codice, invariato)
            # ==========================================================
            
            if self._frame >= 120:
                self._frame = 0
            else:
                self._frame += 1

            #________________JUMP FRAME LOGIC________________
            if self._jump_anim : # (Ho rinominato il tuo `self._jump` in `self._jump_anim`
                                #  perché ha senso, ma puoi ri-cambiarlo se preferisci)
                if self._i_jump == None:
                    self._i_jump = randint(0,1)
                if self._direction == 1 and self._health == 2:
                    self._sprite_start, self._sprite_end = JUMP_LEFT_ARMOR[self._i_jump]
                # ... (TUTTA LA TUA LOGICA DI ANIMAZIONE RESTA QUI, IDENTICA) ...
                elif self._direction == 0 and self._health == 2:
                    self._sprite_start, self._sprite_end = JUMP_RIGHT_ARMOR[self._i_jump]
                elif self._direction == 1 and self._health == 1:
                    self._sprite_start, self._sprite_end = JUMP_LEFT_NAKED[self._i_jump]
                else:
                    self._sprite_start, self._sprite_end = JUMP_RIGHT_NAKED[self._i_jump]
            
            #________________IDLE FRAME LOGIC________________
            elif self._dx == 0:
                self._frame = 0
                if self._direction == 1 and self._health == 2:
                    self._sprite_start, self._sprite_end = IDLE_LEFT_ARMOR
                # ... (TUTTA LA TUA LOGICA DI ANIMAZIONE RESTA QUI, IDENTICA) ...
                elif self._direction == 0 and self._health == 2:
                    self._sprite_start, self._sprite_end = IDLE_RIGHT_ARMOR
                elif self._direction == 1 and self._health == 1:
                    self._sprite_start, self._sprite_end = IDLE_LEFT_NAKED
                else:
                    self._sprite_start, self._sprite_end = IDLE_RIGHT_NAKED

            #________________RUNNING FRAME LOGIC________________
            else:
                if self._direction == 1 and self._health == 2:
                    animation = RUNNING_LEFT_ARMOR.copy()
                # ... (TUTTA LA TUA LOGICA DI ANIMAZIONE RESTA QUI, IDENTICA) ...
                elif self._direction == 1 and self._health == 1:  
                    animation = RUNNING_LEFT_NAKED.copy()
                elif self._direction == 0 and self._health == 2:
                    animation = RUNNING_RIGHT_ARMOR.copy()
                else:
                    animation = RUNNING_RIGHT_NAKED.copy()

                index = (self._frame//self._duration_frame)%(len(animation))
                self._sprite_start, self._sprite_end = animation[index]
            
    def throw_Torch(self, arena: Arena):
        y = self.pos()[1] + 2
        x = self.pos()[0] if self._direction == 1 else self.pos()[0] + self.size()[0]
        # if self._direction == 1:
        #     x = self.pos()[0]
        # else:
        #     x = self.pos()[0] + self.size()[0]
        direction = 0
        if self._direction == 1:
            direction = -1
        else:
            direction = 1
        arena.spawn(Torch((x, y), direction))

    def hit(self, arena: Arena):
        arena.kill(self)

    def pos(self) -> Point:
        return self._x, self._y

    def size(self) -> Point:
        iw, ih = self._sprite_start
        ew, eh = self._sprite_end
        dw = ew-iw
        dh = eh-ih
        return dw, dh

    def sprite(self) -> Point:
        return self._sprite_start