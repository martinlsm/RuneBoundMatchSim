import os

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import tokens

filename_tokens = { tokens.AGILITY : 'agility',
                    tokens.BLANK : 'blank',
                    tokens.DMG_MAGIC : 'magic',
                    tokens.DMG_PHYS : 'physical',
                    tokens.DMG_SKULL : 'skull',
                    tokens.DOUBLE : 'double',
                    tokens.SHIELD : 'shield',
                    tokens.SURGE : 'surge'}


class TokenDisplay:

    def __init__(self, parent, token_type_front, token_type_back, index, golden_front=False, golden_back=False):
        self.canvas = Canvas(parent, width=72, height=72, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.configure(background='burlywood')
        self.canvas.grid(row=int(index/2), column=index%2)
        self.canvas.bind('<Button-1>', self.on_click)
        self.index = index

        token_type_front = filename_tokens[token_type_front]
        token_type_back = filename_tokens[token_type_back]
        folder_path = 'gui/token-img'
        front_big = os.path.join(folder_path, self.get_token_filename(token_type_front, golden_front, True))
        front_small = os.path.join(folder_path, self.get_token_filename(token_type_front, golden_front, False))
        back_big = os.path.join(folder_path, self.get_token_filename(token_type_back, golden_back, True))
        back_small = os.path.join(folder_path, self.get_token_filename(token_type_back, golden_back, False))

        self.images = (self.create_token_img(front_big, back_small), self.create_token_img(back_big, front_small))
        self.active_side = 0

    def draw(self):
        self.canvas.delete(ALL)
        self.canvas.create_image((8, 8), image=self.images[self.active_side], anchor=NW)

    def flip(self):
        self.active_side = (1 + self.active_side) % 2

    def on_click(self, event):
        # Check if click is within the circle shape
        tkn_radius = 56 / 2
        x_center = y_center = 72 / 2
        if tkn_radius**2 >= (event.x - x_center)**2 + (event.y - y_center)**2:
            self.flip()
            self.draw()
            combat_log.write('[Token] {} flipped.'.format(self.index), tags=[('tag_player', 1, 6)])

    def get_token_filename(self, token_type, is_golden, is_large):
        filename = ''.join([filename_tokens[token_type], '-token'])
        if not is_large:
            filename = ''.join([filename, '-small'])
        if is_golden:
            filename = ''.join([filename, '-gold'])
        return ''.join([filename, '.png'])

    def create_token_img(self, file_front, file_back):
        large_img = Image.open(file_front)
        small_img = Image.open(file_back)
        paste_loc = (large_img.size[0] - small_img.size[0], large_img.size[1] - small_img.size[1])
        large_img.paste(small_img, box=(paste_loc), mask=small_img)
        large_img = ImageTk.PhotoImage(large_img)
        return large_img


class GridOfTokens:

    def __init__(self):
        self.token_displays = []

    def add_token_display(self, token_display):
        self.token_displays.append(token_display)

    def draw_all(self):
        for tkn in self.token_displays:
            tkn.draw()


class AbilityButton:

    def __init__(self, root, index):
        self.btn = ttk.Button(root, text='{}: Ability'.format(index), command=self.on_click)
        self.btn.grid(row=index, column=3)
        self.index = index

    def on_click(self):
        combat_log.write('[Ability] {} activated!'.format(self.index), tags=[('tag_ability', 1, 8)])


class PlayerPane:

    def __init__(self, root, player_index):
        side = LEFT if player_index == 1 else RIGHT
        self.root = Frame(root)
        self.root.pack(side=side)
        self.root.configure(background='burlywood')

        self.frame_stats = Frame(self.root)
        self.frame_stats.pack()
        self.frame_stats.configure(background='burlywood')

        ttk.Label(self.frame_stats, text='HP: 6/11').grid(row=0, column=0, sticky=W)
        ttk.Label(self.frame_stats, text='Initiative: 2').grid(row=0, column=1, sticky=W)

        ttk.Label(self.frame_stats, text='Body: 0').grid(row=1, column=0, sticky=W)
        ttk.Label(self.frame_stats, text='Mind: 3').grid(row=1, column=1, sticky=W)
        ttk.Label(self.frame_stats, text='Spirit: 2').grid(row=1, column=2, sticky=W)

        self.frame_tokens = Frame(self.root)
        self.frame_tokens.pack()
        self.frame_tokens.configure(background='burlywood')

        self.tkn_grid = GridOfTokens()
        for i in range(10):
            tkn_disp = TokenDisplay(self.frame_tokens, tokens.SURGE, tokens.SHIELD, i, golden_front=True)
            self.tkn_grid.add_token_display(tkn_disp)
        self.tkn_grid.draw_all()

        for i in range(5):
            AbilityButton(self.frame_tokens, i)

        self.frame_low = Frame(self.root)
        self.frame_low.pack()
        self.frame_low.configure(background='burlywood')
        ttk.Button(self.frame_low, text='Attack').grid(row=0, column=0)
        ttk.Button(self.frame_low, text='Pass').grid(row=0, column=1)
        ttk.Button(self.frame_low, text='Retreat').grid(row=0, column=2)
        ttk.Button(self.frame_low, text='Double').grid(row=1, column=0)
        ttk.Button(self.frame_low, text='Agility').grid(row=1, column=1)
        ttk.Button(self.frame_low, text='Status').grid(row=1, column=2)


class CombatLog:

    def __init__(self, root):

        self.text = Text(root, width=40, height=30)
        self.text.pack()
        self.text.config()
        self.text.config(background='dark slate gray', foreground='LightCyan3', font='Courier 12', state=DISABLED)

        self.current_line = 1
        self.text.tag_config('tag_ability', foreground='cyan')
        self.text.tag_config('tag_enemy', foreground='red')
        self.text.tag_config('tag_player', foreground='yellow')

    def write(self, string, newline=True, tags=[]):
        """
        Appends text to the combat log.
        :param string: The text to be written.
        :param newline: True if the log should insert a newline character after the line, otherwise False.
        :param tags: A list of tuples with three elements with the format (tag name, line index 1, line index 2)
        """
        self.text.config(state=NORMAL)
        self.text.insert('end', string + ('\n' if newline else ''))
        for tag in tags:
            self.text.tag_add(tag[0], '{}.{}'.format(self.current_line, tag[1]), '{}.{}'.format(self.current_line, tag[2]))
        self.text.see('end')
        self.text.config(state=DISABLED)
        self.current_line += 1

def apply_style():
    style = ttk.Style()
    style.configure('TLabel',
                background='burlywood',
                foreground='dark slate gray',
                font='Times 14 bold italic',
                padding=10)

    style.configure('TButton',
                background='dark slate gray',
                foreground='gold2',
                font='Times 14 bold italic',
                padding=10)


if __name__ == '__main__':
    root = Tk()
    root.title('Runebound Match Simulator')
    root.configure(background='burlywood')

    apply_style()
    PlayerPane(root, 1)
    PlayerPane(root, 2)
    combat_log = CombatLog(root)

    root.mainloop()
