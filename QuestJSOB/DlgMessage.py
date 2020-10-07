import sys
sys.path.insert(0, '.')
sys.path.insert(0, '../')

from tkinter import *
import textwrap

from QuestJSOB.TkMacro import McText

class DlgMsg:
	''' A color-coded, parent-bethemed, set modal dialogs. '''

	@staticmethod
	def show_error(parent, title, message, msg_width=40):
		''' Show a dialog with a red (error) theme '''
		parent.bell()
		DlgMsg.show_message(parent, title, message, msg_width, color='red')

	@staticmethod
	def show_info(parent, title, message, msg_width=40, color='blue'):
		''' Show a dialog with a blue (info) theme '''
		DlgMsg.show_message(parent, title, message, msg_width, color='blue')

	@staticmethod
	def show_message(parent, title, message, msg_width=40, color=None):
		''' Show a dialog with the default theme '''
		loc = {
			'x': parent.winfo_x(),
			'y': parent.winfo_y(),
			'wide': parent.winfo_width(),
			'high': parent.winfo_height()
			}
		xpos = loc['x'] + (loc['wide']//4)
		ypos = loc['y'] + (loc['high']//4)

		dlg = None
		if color:
			dlg = Toplevel(master=parent, bg=color)
		else:
			dlg = Toplevel(master=parent)
		dlg.geometry(f"+{xpos}+{ypos}")
		dlg.title(title)

		lines = textwrap.wrap(message, width=msg_width)
		text = Text(dlg, width=msg_width + 2, height=len(lines)+2)
		McText.put(text, "\n".join(lines))
		McText.lock(text)
		text.pack()
		Button(dlg, text="Okay", command=dlg.destroy).pack()
		dlg.focus()
		dlg.grab_set() # modal
		parent.wait_window(dlg)
		dlg.destroy()





