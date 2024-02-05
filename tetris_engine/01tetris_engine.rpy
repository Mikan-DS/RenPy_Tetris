init python in tetris:

    from store import Action, Solid, Frame, Image, Text, persistent
    from random import choice, randint # renpy random is not work correctly

    #### CONSTANTS ####

    START_SPEED = 1

    COLOR_RANGE = (100, 240)

    # Sizes (default is for 1920x1080)

    BLOCK_SIZE = 54
    INFO_TEXT_SIZE = 80
    INFO_TEXT_COLOR = "#FFF"


    # Sprites

    background_frame = "images/tetris_frame.jpg"
    tetrino_brick = "images/tetris_brick.png"

    # Audio

    sfx_theme = "audio/theme.mp3"

    sfx_game_start = "audio/level_up.ogg"
    sfx_level_up = sfx_game_start #"audio/level_up.ogg"
    sfx_game_over = "audio/game_over.mp3"

    sfx_moving = "audio/moving.opus"
    sfx_rotate = sfx_moving #"audio/moving.opus"

    sfx_apply = "audio/apply.opus"
    sfx_line_clear = "audio/line_clear.ogg"


    #### Utilites & Other #####


    def pos2px(pos):
        """Block pos into px pos"""
        return pos*BLOCK_SIZE

    def pos2px_tuple(*posis):
        return tuple(pos2px(pos) for pos in posis)


    def move(src, dst):
        """Sum vector_1 & vector_2"""
        return src[0]+dst[0], src[1]+dst[1]


    def random_color():
        """Creates random RGB color"""
        return tuple(randint(COLOR_RANGE[0], COLOR_RANGE[1]) for i in range(3))

    def str2map(str_map, color):
        """Create tetrino map from string"""
        str_map = str_map.split("\n")

        map = []
        for y in str_map:
            map_y = []
            for x in y:
                map_y.append(color if x=="#" else None)
            map.append(map_y)
        return map


    # Movement Action

    class MoveTetrino(Action):
        def __init__(self, key):
            self.vector = {
                "K_LEFT": (-1, 0),
                "K_RIGHT": (1, 0),
                "K_DOWN": (0, 1)
            }[key]


        def __call__(self):

            pos = move(current_tetrino.pos, self.vector)

            if pos and not manager.board.is_collide(current_tetrino.bricks(), pos):
                renpy.play(sfx_moving)
                current_tetrino.pos = pos


    def RotateTetrino():

        collide = manager.board.is_collide(current_tetrino.rotated(), current_tetrino.pos)

        if not collide:
            renpy.play(sfx_rotate)
            current_tetrino.rotate()
        else:
            mod = correct = 0
            if collide[0] < 0:
                correct = -collide[0]+1
                mod = 1
            elif collide[0] >= manager.board.width:
                correct = manager.board.width-2-collide[0]
                mod = -1

            if mod:
                for i in range(mod, correct, mod):
                    collide = manager.board.is_collide(current_tetrino.rotated(), move(current_tetrino.pos, (i, 0)))

                    if not collide:
                        current_tetrino.pos = move(current_tetrino.pos, (i, 0))
                        renpy.play(sfx_rotate)
                        current_tetrino.rotate()
                        break


    # Useful displayables

    class TetrisBG(renpy.Displayable):
        """ Background of tetris window """

        def __init__(self, x, y):

            super(TetrisBG, self).__init__()

            self.x = x
            self.y = y
            self.size_x, self.size_y = pos2px_tuple(x, y)


        def render(self, width, height, st, at):

            render = renpy.Render(self.size_x, self.size_y)

            for x in range(self.x):
                for y in range(self.y):
                    brick = renpy.render(Image(tetrino_brick), BLOCK_SIZE, BLOCK_SIZE, st, at)
                    render.blit(brick, pos2px_tuple(x, y))

            return render

    class DynamicText(renpy.Displayable):
        """
        Text displayable that can be changes without restarting interaction.
        """

        def __init__(self, text="", size=80, color="FFF", *args, **kwargs):

            super(DynamicText, self).__init__()

            self.text = text

            self.size = size
            self.color = color
            self.args = args
            self.kwargs = kwargs


        def render(self, width, height, st, at):

            text = renpy.render(Text("{size="+str(self.size)+"}"+self.text+"{/size}", color=self.color, *self.args, **self.kwargs), width, height, st, at)

            render = renpy.Render(*text.get_size())

            render.blit(text, (0, 0))

            return render

        def update(self, text, *args, **kwargs):

            self.text = text
            self.args = args
            self.kwargs = kwargs

            renpy.redraw(self, 0)



    #### Tetrino builders ####

    # Tetrino makets

    def tetrino_O():

        color = random_color()

        return Tetrino(2, 2, (2, 1), color=color)

    def tetrino_S():

        color = random_color()

        variants = [
            " ##\n## \n   ",
            " # \n ##\n  #",
        ]

        return Tetrino(3, 3, (1, 1), variants=[str2map(variant, color) for variant in variants])


    def tetrino_Z():

        color = random_color()

        variants = [
            "## \n ##\n   ",
            "  #\n ##\n # ",
        ]

        return Tetrino(3, 3, (1, 1), variants=[str2map(variant, color) for variant in variants])

    def tetrino_T():

        color = random_color()

        variants = [
            " # \n###\n   ",
            " # \n ##\n # ",
            "   \n###\n # ",
            " # \n## \n # ",
        ]

        return Tetrino(3, 3, (1, 1), variants=[str2map(variant, color) for variant in variants])

    def tetrino_I():

        color = random_color()

        variants = [
            " #  \n #  \n #  \n #  ",
            "    \n    \n####\n    ",
        ]

        return Tetrino(4, 4, (0, 0), variants=[str2map(variant, color) for variant in variants])

    def tetrino_L():

        color = random_color()

        variants = [
            "#  \n#  \n## ",
            "###\n#  \n   ",
            " ##\n  #\n  #",
            "   \n  #\n###",
        ]

        return Tetrino(3, 3, (1, 1), variants=[str2map(variant, color) for variant in variants])

    def tetrino_J():

        color = random_color()

        variants = [
            "  #\n  #\n ##",
            "   \n#  \n###",
            "## \n#  \n#  ",
            "###\n  #\n   ",
        ]

        return Tetrino(3, 3, (1, 1), variants=[str2map(variant, color) for variant in variants])


    def random_tetrino():

        tetrino = choice([tetrino_O(), tetrino_S(), tetrino_Z(), tetrino_T(), tetrino_I(), tetrino_L(), tetrino_J()])
        tetrino.update_variant(randint(0, tetrino.max_variant))
        return tetrino

    def new_tetrino():

        global next_tetrino
        next_tetrino = random_tetrino()
        renpy.redraw(manager.next_tetrino, 0)


    class add_tetrino(Action):
        """debug action"""
        def __init__(self, board):
            self.board = board
        def __call__(self):
            global current_tetrino
            tetrino = Tetrino(2, 2, (self.board.width/2-1, -1), random_color())
            current_tetrino = tetrino


    #### Main classes #####

    class Tetrino(renpy.Displayable):

        def __init__(self, x, y, pos=(0, 0), color=None, variants=[]):

            super(Tetrino, self).__init__()

            self.pos = pos

            self.size = self.size_x, self.size_y = pos2px_tuple(x, y)
            self.width, self.height = x, y

            if variants:
                self.map = []
                self.map.extend(variants[0])
            else:
                self.map = [[color for i in range(x)] for i in range(y)]

            self.variants = variants
            self.variant = 0
            self.max_variant = len(variants)

        def render(self, width, height, st, at):

            render = renpy.Render(self.size_x, self.size_y)

            for (x, y), brick in self.bricks():

                brick = renpy.render(Solid(brick), BLOCK_SIZE, BLOCK_SIZE, st, at) # Draws brick
                render.blit(brick, pos2px_tuple(x, y))

                brick = renpy.render(Frame(tetrino_brick), BLOCK_SIZE, BLOCK_SIZE, st, at) # Draws frame on brick
                render.blit(brick, pos2px_tuple(x, y))

            return render

        @property
        def x(self):
            return self.pos[0]
        @property
        def y(self):
            return self.pos[1]


        def __getitem__(self, pos):
            x, y = pos
            try:
                return self.map[y][x]
            except:
                return None
        def __setitem__(self, pos, color):
            x, y = pos
            if x==abs(x) and y==abs(y):
                try:
                    self.map[y][x] = color
                except:
                    pass




        def bricks(self):
            for x in range(self.width):
                for y in range(self.height):
                    brick = self[x, y]

                    if brick:
                        yield (x, y), brick


        def rotated(self, var=None):
            """
            Same as self.bricks but it return data for next tetrino variant
            """
            variants = len(self.variants)
            if variants:
                variant = var or self.variant+1

                variant = variant if variant < variants else 0

                map = self.variants[variant]

                for x in range(self.width):
                    for y in range(self.height):
                        brick = map[y][x]
                        if brick:
                            yield (x, y), brick

        def rotate(self):
            self.update_variant(self.variant+1)

        def update_variant(self, variant):

            if self.variants:
                self.variant = variant

                if self.variant >= self.max_variant:
                    self.variant = 0

                self.map.clear()
                self.map.extend(self.variants[self.variant])

                renpy.redraw(self, 0)


    class GameBoard(renpy.Displayable):

        def __init__(self, x=15, y=20, uni=False):

            super(GameBoard, self).__init__()

            self.size = self.size_x, self.size_y = pos2px_tuple(x, y)
            self.width, self.height = x, y

            self.map = [Tetrino(x, 1) for i in range(y)]


            self.bg = TetrisBG(x, y) #
            self.uni = uni # if it's False -> this board is main

            self.on_remove = 0
            self.combo = 0


        def render(self, width, height, st, at):

            render = renpy.Render(self.size_x, self.size_y)

            bg = renpy.render(self.bg, width, height, st, at)

            render.blit(bg, (0, 0))

            if self.uni and next_tetrino: # Next tetrino shows here

                tetrino = renpy.render(next_tetrino, next_tetrino.size_x, next_tetrino.size_y, st, at)

                render.blit(tetrino, pos2px_tuple(*next_tetrino.pos))

                return render

            for y, tetrino in enumerate(self.map): # Draws board and applied tetrinos

                tetrino = renpy.render(tetrino, self.size_x, BLOCK_SIZE, st, at)

                render.blit(tetrino, (0, pos2px(y)))

            if lose: # Lose board effect draws here

                self[self.on_remove, self.combo] = random_color()
                renpy.redraw(self.map[self.combo], 0)

                if self.on_remove < self.width-1:
                    self.on_remove += 1
                else:
                    if self.combo < self.height-1:
                        self.on_remove = 0
                        self.combo+=1
                    else:
                        self.on_remove = self.combo = 0


                renpy.redraw(self, .5)

                return render

            global current_tetrino # If it get's here -> this is normal iteration

            if current_tetrino:

                tetrino = renpy.render(current_tetrino, current_tetrino.size_x, current_tetrino.size_y, st, at)

                render.blit(tetrino, pos2px_tuple(*current_tetrino.pos))

                if next_step<st: # Check for next game step
                    global next_step
                    next_step = st+speed

                    step = move(current_tetrino.pos, (0, 1))
                    if not self.is_collide(current_tetrino.bricks(), step):
                        current_tetrino.pos = step
                    else:
                        self.apply_tetrino(current_tetrino)
                        current_tetrino = None


            if pause: # If it return here -> displayable would not update by itself
                return render

            for y in reversed(self.map):
                if self.full_line(y): #Check for full lines
                    if self.on_remove >= self.width: # Line completly removed
                        for x in range(self.width):
                            y[x, 0] = None

                        self.on_remove = 0
                        self.combo+=1

                        self.map.remove(y) #FALLING
                        self.map.insert(0, Tetrino(self.width, 1))

                        renpy.redraw(self, .5)
                        return render

                    if not self.on_remove: # If it's just find out full line
                        renpy.play(sfx_line_clear)

                    y[self.on_remove, 0] = "000" # ANIMATION
                    self.on_remove += 1
                    renpy.redraw(y, 0)
                    renpy.redraw(self, .3)

                    return render

            else: # If there is no full lines left
                if self.combo: # If on last iteration lines has been removed
                    manager.award()
                if not current_tetrino: # If current tetrino does not exist - create it!

                    tetrino = next_tetrino or random_tetrino() # Takes from next_tetrino or create new
                    tetrino.pos = move(tetrino.pos, ((int(self.width/2-2), -3))) # update pos on initial position
                    new_tetrino() # Update next_tetrino variable


                    if self.is_collide(tetrino.bricks(), tetrino.pos): # If it's collide on initial pos -> game over
                        global lose, pause
                        lose = pause = True
                        renpy.music.play(sfx_game_over, "music", loop=True)
                        renpy.restart_interaction()
                    else:
                        current_tetrino = tetrino

                renpy.redraw(self, 0)

            return render

        def event(self, ev, x, y, st):

            if current_tetrino and not self.uni:

                self.collide_control(ev)


        def collide_control(self, ev):

            pos = None

            if renpy.map_event(ev, ["K_LEFT", "repeat_K_LEFT"]):
                pos = move(current_tetrino.pos, (-1, 0))

            elif renpy.map_event(ev, ["K_RIGHT", "repeat_K_RIGHT"]):
                pos = move(current_tetrino.pos, (1, 0))

            elif renpy.map_event(ev, ["K_DOWN", "repeat_K_DOWN"]):
                global next_step
                pos = move(current_tetrino.pos, (0, 1))
                next_step = 0

            elif renpy.map_event(ev, "K_UP"):

                collide = self.is_collide(current_tetrino.rotated(), current_tetrino.pos)

                if not collide:
                    renpy.play(sfx_rotate)
                    current_tetrino.rotate()
                else:
                    mod = correct = 0
                    if collide[0] < 0:
                        correct = -collide[0]+1
                        mod = 1
                    elif collide[0] >= self.width:
                        correct = self.width-2-collide[0]
                        mod = -1

                    if mod:
                        for i in range(mod, correct, mod):
                            collide = self.is_collide(current_tetrino.rotated(), move(current_tetrino.pos, (i, 0)))

                            if not collide:
                                current_tetrino.pos = move(current_tetrino.pos, (i, 0))
                                renpy.play(sfx_rotate)
                                current_tetrino.rotate()
                                break


            if pos and not self.is_collide(current_tetrino.bricks(), pos):
                renpy.play(sfx_moving)
                current_tetrino.pos = pos


        def is_collide(self, tetrino, tetrino_pos):
            for pos, brick in tetrino:

                x, y = move(pos, tetrino_pos)

                if not 0 <= x < self.width:
                    return (x, y)

                elif y >= self.height:
                    return (x, y)

                elif y < 0:
                    continue

                elif self[x, y]:
                    return (x, y)


        def apply_tetrino(self, tetrino):

            lines = set()

            for pos, brick in tetrino.bricks():

                x, y = move(pos, tetrino.pos)
                lines.add(y)

                self[x, y] = brick

            for y in lines:
                renpy.redraw(self.map[y], 0)

            renpy.play(sfx_apply)


        def full_line(self, y):

            for x in y.map[0]:
                if not x:
                    return False

            return True

        def __getitem__(self, pos):
            x, y = pos
            try:
                return self.map[y][x, 0]
            except:
                return None
        def __setitem__(self, pos, color):
            x, y = pos
            if x==abs(x) and y==abs(y):
                self.map[y][x, 0] = color


    class Game():
        """
        Main game handler
        """

        def __init__(self, x_size=15, y_size=20, info_text_size = None, info_text_color = None, initial_level=0):

            global manager, board_map, speed, next_step, pause, lose, score, level, goal

            info_text_size = info_text_size or INFO_TEXT_SIZE
            info_text_color = info_text_color or INFO_TEXT_COLOR


            if persistent.tetris_record is None:
                persistent.tetris_record = 0

            manager = self

            pause = True
            lose = False

            score = 0
            level = initial_level
            goal = 0

            self.board = GameBoard(x_size, y_size) # main game board
            self.next_tetrino = GameBoard(4, 4, uni=True)

            self.score = DynamicText(str(score), size=info_text_size, color=info_text_color)
            self.record = DynamicText(str(persistent.tetris_record), size=info_text_size, color=info_text_color)

            self.level = DynamicText(str(level), size=info_text_size, color=info_text_color)
            self.goal = DynamicText(str(goal)+"/"+str(20+level*5), size=info_text_size, color=info_text_color)

            board_map = self.board.map
            speed = START_SPEED*(4.0/(4+level))
            next_step = 0



            renpy.music.stop(channel=u'music')
            # if renpy.music.get_playing(channel=u'music') != sfx_theme: # It doesn't work :(
            renpy.music.play(sfx_theme, "music", loop=True)

            renpy.restart_interaction()


        def pause(self):

            global pause
            pause = not pause

            if not lose:
                if pause:
                    renpy.music.play(sfx_theme, "music", loop=True)
                else:
                    renpy.music.stop(channel=u'music')
                    if not current_tetrino:
                        renpy.play(sfx_game_start, "music")
                    renpy.redraw(self.board, 0)


            renpy.restart_interaction()


        def award(self):

            global score, goal, level, speed

            mod = {1:100, 2:300, 3:700, 4:1500}[self.board.combo] # f = lambda x: (f(x-1)*2 if x else 0)+100

            score += int(mod*((15+level)/15.0))

            goal += self.board.combo

            if goal >= 20+level*5:
                renpy.play(sfx_level_up)
                goal = goal-(20+level*5)
                level += 1
                speed = START_SPEED*(4.0/(4+level))

                self.level.update(str(level))


            if score > persistent.tetris_record:
                persistent.tetris_record = score
                self.record.update(str(persistent.tetris_record))


            self.goal.update(str(goal)+"/"+str(20+level*5))

            self.board.combo = 0
            self.score.update(str(score))



init:

    # Default constans
    # They are saving if renpy do statement

    default tetris.manager = None

    default tetris.score = 0
    default tetris.level = 0
    default tetris.goal = 0

    default tetris.board_map = []

    default tetris.current_tetrino = None
    default tetris.next_tetrino = None

    default tetris.speed = 1
    default tetris.next_step = 0


    default tetris.pause = True
    default tetris.lose = False


    transform MoveButton(d=90):

        # НЕ ХОЧУ ДЕЛАТЬ НОВЫЕ КНОПКИ

        rotate d

        on idle:
            zoom 1.0
        on hover:
            zoom 0.97


    screen default_tetris_game(): # Default screen

        default game = tetris.Game()

        add Solid("CCC")

        frame:
            background Frame(tetris.background_frame, 3, 3, 3, 3, tile=True)
            xalign .5 yalign .5
            add game.board

        frame:
            background Frame(tetris.background_frame, 3, 3, 3, 3, tile=True)
            xalign .1 yalign .1
            add game.next_tetrino

        vbox:

            xalign .95 yalign .1

            text "SCORE" size 80 xalign .5
            add game.score xalign .5

            text "HI-SCORE" size 80 xalign .5
            add game.record xalign .5

            null height 250

            text "LEVEL" size 80 xalign .5
            add game.level xalign .5

            text "GOAL" size 80 xalign .5
            add game.goal xalign .5


        vbox:

            xalign .05
            yalign .9

            frame:
                xmaximum 400 ymaximum 400
                background None

                imagebutton idle "images/control.png" keyboard_focus False xalign .5 yalign 0 action tetris.RotateTetrino at MoveButton(0)
                imagebutton idle "images/control.png" keyboard_focus False xalign 0 yalign .5 action tetris.MoveTetrino("K_LEFT") at MoveButton(-90)
                imagebutton idle "images/control.png" keyboard_focus False xalign .5 yalign 1.0 action tetris.MoveTetrino("K_DOWN") at MoveButton(180)
                imagebutton idle "images/control.png" keyboard_focus False xalign 1.0 yalign .5 action tetris.MoveTetrino("K_RIGHT") at MoveButton(90)

            textbutton "PAUSE|SPACE" text_size 50 keyboard_focus False background Solid("111") hover_background Solid("499") xalign .5 action game.pause


        if tetris.lose:
            button action game.__init__ keysym "K_SPACE"
            text "GAME OVER" size 160 text_align .5 color "F55" xalign .5 yalign .5

        elif tetris.pause:
            button action game.pause keysym "K_SPACE"
            text "НАЖМИТЕ ДЛЯ ИГРЫ!" size 160 text_align .5 color "599" xalign .5 yalign .5
        else:
            key "K_SPACE" action game.pause




label TETRIS(autosave=True):

    show screen default_tetris_game

    if autosave:
        jump .auto_tetris
    else:
        jump .tetris


label .auto_tetris:

    # In this mode it'll saves every 1 second, but may broke

    pause 1
    jump .auto_tetris

label .tetris:

    # Safe mode

    pause
    jump .tetris
