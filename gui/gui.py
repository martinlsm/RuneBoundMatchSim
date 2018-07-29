from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


def create_token_img(file_front, file_back):
	large_img = Image.open(file_front)
	small_img = Image.open(file_back)
	paste_loc = (large_img.size[0] - small_img.size[0], large_img.size[1] - small_img.size[1])
	large_img.paste(small_img, box=(paste_loc), mask=small_img)
	large_img = ImageTk.PhotoImage(large_img)
	return large_img


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

	frame_stats = Frame(root)
	frame_stats.pack()
	frame_stats.configure(background='burlywood')

	ttk.Label(frame_stats, text='HP: 6/11').grid(row=0, column=0, sticky=W)
	ttk.Label(frame_stats, text='Initiative: 2').grid(row=0, column=1, sticky=W)

	ttk.Label(frame_stats, text='Body: 0').grid(row=1, column=0, sticky=W)
	ttk.Label(frame_stats, text='Mind: 3').grid(row=1, column=1, sticky=W)
	ttk.Label(frame_stats, text='Spirit: 2').grid(row=1, column=2, sticky=W)

	frame_tokens = Frame(root)
	frame_tokens.pack()
	frame_tokens.configure(background='burlywood')
	photo_both = create_token_img('gui/token-img/skull-token.png', 'gui/token-img/shield-token-small-gold.png')

	for i in range(10):
		ttk.Label(frame_tokens, image=photo_both).grid(row=int(i/2), column=i%2)

	for i in range(5):
		ttk.Button(frame_tokens, text='{}: Ability'.format(i)).grid(row=i, column=3)

	frame_low = Frame(root)
	frame_low.pack()
	frame_low.configure(background='burlywood')
	ttk.Button(frame_low, text='Attack').grid(row=0, column=0)
	ttk.Button(frame_low, text='Pass').grid(row=0, column=1)
	ttk.Button(frame_low, text='Retreat').grid(row=0, column=2)
	ttk.Button(frame_low, text='Double').grid(row=1, column=0)
	ttk.Button(frame_low, text='Agility').grid(row=1, column=1)
	status_btn = ttk.Button(frame_low, text='Status').grid(row=1, column=2)

	root.mainloop()
