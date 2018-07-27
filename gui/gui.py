from tkinter import *
from tkinter import ttk


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
	frame_stats.pack(side=TOP)
	frame_stats.configure(background='burlywood')

	ttk.Label(frame_stats, text='HP: 6/11').grid(row=0, column=0, sticky=W)
	ttk.Label(frame_stats, text='Initiative: 2').grid(row=0, column=1, sticky=W)

	ttk.Label(frame_stats, text='Body: 0').grid(row=1, column=0, sticky=W)
	ttk.Label(frame_stats, text='Mind: 3').grid(row=1, column=1, sticky=W)
	ttk.Label(frame_stats, text='Spirit: 2').grid(row=1, column=2, sticky=W)

	frame_tokens = Frame(root)
	frame_tokens.pack(side=LEFT)
	frame_tokens.configure(background='burlywood')
	photo = PhotoImage(file='gui/shield-token.png')
	for i in range(10):
		ttk.Label(frame_tokens, image=photo).grid(row=int(i/2), column=i%2, sticky=W)

	for i in range(5):
		ttk.Button(frame_tokens, text='{}: Ability'.format(i)).grid(row=i, column=3)

	root.mainloop()
