# coding: utf-8

import curses
import time
from objects.character import Pacman, Ghost
from objects.game_box import GameBox
from objects.color import Color

COLOR = Color(curses)


# The only things configurable are the map (walls + food) and object postions
DATA = {
    'map_file': 'maps/map.txt',
    'map_chars': {
        'wall': '█',
        'door': '-',
        'space': ' ',
        'food': '·'
    },
    'character_positions': {
        'pacman': [18, 29],
        'ghosts': [[12, 25], [12, 29], [12, 33], [11, 29]]
    },
}


LIVES = 3
FOOD_SCORE = 10


class PacmanGame():
    def __init__(self):
        self.screen_obj = curses.initscr()
        curses.curs_set(0)
        curses.noecho()

        self.init_map()
        self.show_start_screen()


    def init_map(self):
        self.game_box = GameBox(
            self.screen_obj,
            DATA['map_file'],
            DATA['map_chars'],
            {
                'wall': COLOR.blue,
                'door': COLOR.blue,
                'space': COLOR.black,
                'food': COLOR.yellow
            }
        )


    def init_characters(self):
        positions = DATA['character_positions']
        ghost_pos = positions['ghosts']


        self.pacman = Pacman(
            self.game_box,
            # Part 2-1: Set Pacman's color to yellow, you can use the constant `COLOR.yellow`.
            # TODO: Set Pacmans's color to yellow!
            positions['pacman']
        )

        self.ghosts = {
            #　Part 2−２: Set Blinky's color to red, you can use the constant `COLOR.red`.
            'Blinky': Ghost(
                self.game_box,
                # TODO: Set Blinky's color to red!
                ghost_pos[0]
            ),

            # Part 2-3: Set Pinky's color to pink, you can use the constant `COLOR.pink`.
            'Pinky': Ghost(
                self.game_box,
                COLOR.pink,
                ghost_pos[1]
            ),

            # Part 2-4: Set Inky's color to cyan, you can use the constant `COLOR.cyan`.
            'Inky': Ghost(
                self.game_box,
                COLOR.cyan,
                ghost_pos[2]
            ),

            # Part 2-5: Set Clyde's color to orange, you can use the constant `COLOR.orange`.
            'Clyde': Ghost(
                self.game_box,
                COLOR.orange,
                ghost_pos[3]
            )
        }


    def start_new_game(self):
        self.lives = LIVES
        self.score = 0

        self.game_box.set_map_matrix()
        self.game_box.draw_map()
        self.game_box.update_score(self.score)
        self.game_box.update_lives(self.lives)

        self.food_count = self.game_box.food_count
        self.food_count -= 1    # Initial position over food

        self.init_characters()
        self.run_game_loop()


    def restart(self):
        self.reset_positions()
        self.standby()
        self.run_game_loop()


    def standby(self):
        time.sleep(1)

        self.pacman.respawn()
        for ghost in self.ghosts.values():
            ghost.respawn()

        self.blink_characters()


    def win(self):
        self.show_win_screen()


    def end(self):
        self.show_game_over_screen()


    def run_game_loop(self):
        game_loop_running = True
        key = curses.KEY_RIGHT

        while game_loop_running:
            next_key = self.game_box.map_box.getch()
            key = key if next_key == -1 else next_key
            self.prev_position = self.pacman.current_position

            # Ghosts move
            for ghost in self.ghosts.values():
                ghost.move_in_random_direction()

            # Check state
            if not self.pacman.stopped:
                if self.food_eaten():
                    self.food_count -= 1
                    self.increment_score('food')

                    if self.food_count <= 0:
                        game_loop_running = False
                        time.sleep(1)
                        self.win()

            if self.ghost_touched():
                game_loop_running = False
                for ghost in self.ghosts.values():
                    ghost.vanish()

                self.die()

                self.game_box.map_box.refresh()

                if self.lives >= 0:
                    self.restart()
                else:
                    self.end()

            # Pacman moves
            if key == curses.KEY_UP:
                self.pacman.move('UP')

            if key == curses.KEY_DOWN:
                self.pacman.move('DOWN')

            if key == curses.KEY_LEFT:
                self.pacman.move('LEFT')

            if key == curses.KEY_RIGHT:
                self.pacman.move('RIGHT')



    def die(self):
        self.lives -= 1
        self.game_box.update_lives(self.lives)
        self.pacman.die()


    def increment_score(self, score_type):
        score_values = {
            'food': FOOD_SCORE
        }
        self.score += score_values[score_type]
        self.game_box.update_score(self.score)


    def reset_positions(self):
        positions = DATA['character_positions']
        ghost_pos = positions['ghosts']

        self.pacman.set_position(positions['pacman'])

        for idx, ghost in enumerate(self.ghosts.values()):
            ghost.set_position(ghost_pos[idx])


    def blink_characters(self):
        show = False
        for i in range(4):
            time.sleep(0.5)
            self.pacman.toggle(show)
            for ghost in self.ghosts.values():
                ghost.toggle(show)
            self.game_box.map_box.refresh()
            
            show = not show


    def food_eaten(self):
        y, x = self.pacman.current_position
        return self.game_box.map_matrix[y][x] == DATA['map_chars']['food']


    def ghost_touched(self):
        for ghost in self.ghosts.values():
            if ghost.current_position in (self.pacman.current_position,
                                          self.prev_position):
                return True
        return False


    def show_start_screen(self):
        blink_line_index = 0
        mesg_line = '|                 Press any key to START                  |'
        blank_line = '|                                                         |'

        with open('screens/start.txt') as screen:
            line_index = 0
            for line in screen:
                if 'Press' in line:
                    blink_line_index = line_index
                self.game_box.map_box.addstr(
                    line_index,
                    0,
                    line,
                    COLOR.blue if '█' in line else COLOR.yellow
                )
                line_index += 1

        self.game_box.border_box.refresh()

        start_screen_running = True
        show_msg = False

        while start_screen_running:
            next_key = self.game_box.map_box.getch()
            self.game_box.map_box.addstr(
                blink_line_index,
                0,
                mesg_line if show_msg else blank_line,
                COLOR.yellow
            )
            show_msg = not show_msg
            if next_key != -1:
                start_screen_running = False
                self.start_new_game()
            time.sleep(0.5)


    def show_win_screen(self):
        self.show_end_screen('screens/win.txt', COLOR.yellow)


    def show_game_over_screen(self):
        self.show_end_screen('screens/game_over.txt', COLOR.orange)


    def show_end_screen(self, filename, color):
        with open(filename) as screen:
            line_index = 7
            for line in screen:
                if 'SCORE: 0000' in line:
                    line = line.replace('SCORE: 0000', 'SCORE: ' + str(self.score).zfill(4))
                self.game_box.map_box.addstr(line_index, 0, line, color)
                line_index += 1

        self.game_box.border_box.refresh()
        game_over_screen_running = True

        while game_over_screen_running:
            next_key = self.game_box.map_box.getch()
            if next_key != -1:
                game_over_screen_running = False

                if next_key == 27:
                    curses.endwin()
                    exit()
                else:
                    self.start_new_game()


PacmanGame()
white_check_mark
eyes
raised_hands





3:39
character.py
3:39
import abc
import random
import time
from .character_progression import CharProgression


class Character():
    def __init__(self, game_box, color, initial_position=None):
        self.game_box = game_box

        # Part 1-1  In `character.py` please prepare the Character class so that it can recieve a `color` attribute when instanced.
        # TODO: Implement color

        self.pass_over = False
        self.stopped = False

        self.init_progressions()

        if initial_position:
            self.set_position(initial_position)


    @abc.abstractmethod
    def init_progressions(self):
        self.progressions = {}
        return


    def appear(self):
        self.draw_char(self.current_progression.get_char(), False)


    def vanish(self):
        self.draw_char(' ', False)


    def toggle(self, show=True):
        if show:
            self.appear()
        else:
            self.vanish()


    def move(self, direction):
        new_position = self.game_box.get_new_position(self.current_position, direction)

        if new_position != self.current_position:
            self.stopped = False
            self.update_progression(direction)
            self.set_position(new_position)
        else:
            self.stopped = True


    def set_position(self, coordinates):
        if hasattr(self, 'current_position'):
            if not self.pass_over:
                self.draw_char(' ')
            else:
                self.draw_char(' ', True, True)

        self.current_position = coordinates
        self.draw_char(self.current_progression.get_char(), False)


    def update_progression(self, direction):
        self.current_progression = self.progressions.get(direction)
        self.current_progression.update()


    def draw_char(self, char, update=True, redraw=False):
        y, x = self.current_position

        color = self.color

        if redraw:
            char = self.game_box.map_matrix[y][x]
            color = self.game_box.color_matrix[y][x]

        self.game_box.map_box.addstr(
            y,
            x,
            char,
            color
        )

        if update:
            self.game_box.map_matrix[y][x] = char




class Pacman(Character):
    def init_progressions(self):
        self.progressions = {
            'UP': CharProgression('UP', ['v', 'V', '|', '|', 'V', 'v']),
            'DOWN': CharProgression('DOWN', ['^']),
            'LEFT': CharProgression('LEFT', ['}', ')', '>', '-', '-', '>', ')', '}']),
            'RIGHT': CharProgression('RIGHT', ['{', '(', '<', '-', '-', '<', '(', '{'])
        }

        self.current_progression = self.progressions.get('RIGHT')


    # Part 3: Implement Pacman death animation
    def die(self):
        self.appear()
        # 1. Loop through the array `['O', 'o', '.', "'", '*', ' ']` to perform the character changes that act as our animations.
        # 2. Pause on every iteration of the loop for `0.2` seconds using `time.sleep()`
        # 3. Use the `self.draw_char()` method to draw the character in the animation sequence, the second parameter is `False`.
        # 4. Finally, refresh the game_box/main screen with `self.game_box.map_box.refresh()`.

        self.vanish()


    def respawn(self):
        self.appear()




class Ghost(Character):
    SPEED_DAMPER_LEVEL = 1

    def __init__(self, *args, **kwargs):
        super(Ghost, self).__init__(*args, **kwargs)
        # Part 1-2: In `character.py`, for Ghosts please set override the default value of false for the `pass_over` attribute to `True`
        self.pass_over = True
        self.wait_flag = 0


    def init_progressions(self):
        self.progressions = {
            'UP': CharProgression('UP', ['M']),
            'DOWN': CharProgression('DOWN', ['M']),
            'LEFT': CharProgression('LEFT', ['M']),
            'RIGHT': CharProgression('RIGHT', ['M'])
        }

        self.current_progression = self.progressions.get('RIGHT')


    def move_in_random_direction(self, bias=None):
        if self.wait_flag < self.SPEED_DAMPER_LEVEL:
            self.wait_flag += 1
            return

        self.wait_flag = 0

        box = self.game_box

        current_direction = self.current_progression.name
        forward_directions = box.get_all_forward_directions(current_direction)
        possible_directions = []

        for d in forward_directions:
            if box.get_new_position(self.current_position, d) != self.current_position:
                possible_directions.append(d)

        if possible_directions:
            self.move(random.choice(possible_directions))
        else:
            self.move(box.get_opposite_direction(current_direction))


    def respawn(self):
        self.appear()
