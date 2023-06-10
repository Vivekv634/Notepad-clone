import datetime
import os
import pickle
from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import wikipedia
import requests

global a, find_entry, replace_entry, font_box, size_box, scrollbar_box, text_box, sentence_box, url_box

# importing recent_file.dat
with open('recent_file.dat', 'rb') as f:
    file_path = pickle.load(f)

with open('font.dat', 'rb') as f1:
    font = pickle.load(f1)

with open('size.dat', 'rb') as f2:
    size = pickle.load(f2)


class App:
    def __init__(self, master):
        global a
        self.master = master
        self.title = 'Untitled - ProBook'
        self.geometry = '1000x500+150+100'
        self.icon = 'notepad.ico'
        self.textarea = 'textarea'
        self.frame = 'frame'
        self.font = font
        self.size = size
        self.recent_file = file_path
        self.status = 'status'
        self.var = IntVar()
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.filemenu = 'filemenu'
        self.editmenu = 'editmenu'
        self.formatmenu = 'formatmenu'
        self.viewmenu = 'viewmenu'
        self.menubar = 'menubar'
        self.helpmenu = 'helpmenu'
        self.right_click = 'right_click'
        self.style = 'style'

    def start(self):
        # making structure
        self.master.title(f"{self.title}")
        self.master.geometry(f"{self.geometry}")
        # self.master.iconbitmap(f"{self.icon}")

        # making frame
        self.frame = Frame(self.master)
        self.frame.pack(expand=True, fill=BOTH)

        # making status bar
        self.status = Label(self.frame, anchor=E)
        self.status.pack(fill=X, side=BOTTOM)

        self.style = ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure("Vertical.TScrollbar", background="Gray15", bordercolor="Gray15", arrowcolor="black")
        self.style.configure("horizontal.TScrollbar", background="Gray15", bordercolor="Gray15", arrowcolor="black")

        ver_scrollbar = ttk.Scrollbar(self.frame, orient='vertical')
        ver_scrollbar.pack(side=RIGHT, fill=Y)

        hor_scrollbar = ttk.Scrollbar(self.frame, orient='horizontal')
        hor_scrollbar.pack(fill=X, side=BOTTOM)

        # making textarea
        self.textarea = Text(self.frame, font=f"{self.font} {self.size}", undo=True, bg='white', fg='black',
                             yscrollcommand=ver_scrollbar.set, xscrollcommand=hor_scrollbar.set, wrap=NONE)
        self.textarea.pack(expand=True, fill=BOTH, side=BOTTOM, anchor=NW)

        ver_scrollbar.config(command=self.textarea.yview)
        hor_scrollbar.config(command=self.textarea.xview)
        # making menu bar
        self.menubar = Menu(self.frame)

        # making file menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='New File\t\t\t\t\t\t\t\t\t\t\t', command=self.newfile)
        self.filemenu.add_command(label='Open File...', command=self.openfile)
        self.filemenu.add_command(label='Save File', command=self.savefile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Copy file content from online', command=self.copy_file_content_online)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.master.destroy, accelerator='Alt+F4')
        self.menubar.add_cascade(label='File', menu=self.filemenu)

        # making edit menu
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label='Undo\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', accelerator='Ctrl+Z',
                                  command=self.textarea.edit_undo)
        self.editmenu.add_command(label='Redo', command=self.textarea.edit_redo, accelerator='Ctrl+Y')
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Cut', command=self.cut, accelerator='Ctrl+X')
        self.editmenu.add_command(label='Copy', command=self.copy, accelerator='Ctrl+C')
        self.editmenu.add_command(label='Paste', command=self.paste, accelerator='Ctrl+V')
        self.editmenu.add_command(label='Delete', command=self.delete, accelerator='      Del')
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Copy active file path', command=self.copy_file_path)
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Search with Wikipedia & paste it', command=self.search_wikipedia)
        self.editmenu.add_command(label='Find', command=self.find_replace)
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Select All', command=self.select_all, accelerator='Ctrl+A')
        self.editmenu.add_command(label='Delete All', command=self.delete_all)
        self.editmenu.add_command(label='Time/Date', command=self.timendate)
        self.menubar.add_cascade(label='Edit', menu=self.editmenu)

        # making format menu
        self.formatmenu = Menu(self.menubar, tearoff=0)
        self.formatmenu.add_checkbutton(label='Word Wrap\t\t\t\t\t\t\t\t', variable=self.var1, onvalue=1, offvalue=0,
                                        command=self.word_wrap)
        self.formatmenu.add_command(label='Change Font type', command=self.font_type)
        self.formatmenu.add_command(label='Change Font size', command=self.font_size)
        self.menubar.add_cascade(label='Format', menu=self.formatmenu)

        # making view menu
        self.viewmenu = Menu(self.menubar, tearoff=0)
        self.viewmenu.add_checkbutton(label='Dark Mode\t\t\t\t\t\t\t\t\t\t\t\t', variable=self.var, onvalue=1,
                                      offvalue=0, command=self.dark_mode)
        self.viewmenu.add_command(label='Set Custom text Color', command=self.text_color)
        self.menubar.add_cascade(label='View', menu=self.viewmenu)

        # making help menu
        self.helpmenu = Menu(self.master, tearoff=0)
        self.helpmenu.add_command(label='Reset All Functions\t\t\t\t', command=self.reset_all)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        # making right click menu
        self.right_click = Menu(self.master, tearoff=0)
        self.right_click.add_command(label='Undo\t\t\t\t\t\t\t', command=self.textarea.edit_undo, accelerator='Ctrl+Z')
        self.right_click.add_command(label='Redo', command=self.textarea.edit_redo, accelerator='Ctrl+Y')
        self.right_click.add_separator()
        self.right_click.add_command(label='Cut', command=self.cut, accelerator='Ctrl+X')
        self.right_click.add_command(label='Copy', command=self.copy, accelerator='Ctrl+C')
        self.right_click.add_command(label='Paste', command=self.paste, accelerator='Ctrl+V')
        self.right_click.add_command(label='Delete', command=self.delete, accelerator='      Del')
        self.right_click.add_separator()
        # self.right_click.add_command(label='Search with Google', command=self.search)
        # self.right_click.add_separator()
        self.right_click.add_command(label='Select All', command=self.select_all, accelerator='Ctrl+A')
        self.textarea.bind('<Button-3>', self.do_popup)

        self.master.config(menu=self.menubar)

        self.line_column()

        file = open('recent_file.dat', 'rb')
        path = pickle.load(file)

        if path == '':
            pass
        else:
            with open(path) as a1:
                self.textarea.delete(1.0, END)
                self.textarea.insert(INSERT, a1.read())
                self.master.title(f"{os.path.abspath(path)} - ProBook")

    def newfile(self):
        self.master.title(f"{self.title}")
        self.textarea.delete(1.0, END)
        with open('recent_file.dat', 'wb') as file:
            self.recent_file = ''
            pickle.dump(self.recent_file, file)
        print('New File Open!')

    def openfile(self):
        recent_file = askopenfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'),
                                                                          ('All Files', '*.*')])
        if recent_file == '':
            pass
        else:
            with open(recent_file) as file:
                self.textarea.delete(1.0, END)
                self.textarea.insert(1.0, file.read())
                self.master.title(f"{os.path.abspath(self.recent_file)} - ProBook")

        with open('recent_file.dat', 'wb') as file1:
            file1.seek(0)
            pickle.dump(recent_file, file1)
        print('File Opened!')

    def savefile(self):
        if self.recent_file == '':
            file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"),
                                                ("Text Documents", "*.txt")])
            if file == "":
                self.recent_file = ''
            else:
                # Save as a new file
                file1 = open(file, "w")
                file1.write(self.textarea.get(1.0, END))
                file1.close()

                root.title(os.path.abspath(file) + " - ProBook")
                print("New File Saved")

                with open('recent_file.dat', 'wb') as file2:
                    file2.seek(0)
                    pickle.dump(file, file2)
        else:
            # Save the file
            file1 = open(self.recent_file, "w")
            file1.write(self.textarea.get(1.0, END))
            file1.close()

            with open('recent_file.dat', 'wb') as file2:
                file2.seek(0)
                pickle.dump(self.recent_file, file2)
            print('File Saved!')

    def copy_file_content_online(self):
        global url_box
        window = Toplevel(self.master)
        window.title('ProBook')
        window.geometry('300x120+150+150')
        window.iconbitmap('notepad.ico')
        label = Label(window, text='Enter URL:')
        label.place(x=20, y=20)
        url_box = Entry(window, width=30)
        url_box.place(x=80, y=20)
        okay_btn = Button(window, text='        OKAY        ', relief=RIDGE,
                          command=self.copy_file_content_online_command)
        okay_btn.place(x=50, y=60)
        cancel_btn = Button(window, text='      CANCEL      ', relief=RIDGE, command=window.destroy)
        cancel_btn.place(x=160, y=60)

        window.focus_set()

    def copy_file_content_online_command(self):
        try:
            url = requests.get(url_box.get())
            data = url.text
            self.textarea.insert(INSERT, data)
            print('Text Copied from Online file URL!')
        except Exception as e:
            print(e)

    def copy(self):
        self.textarea.clipboard_clear()
        text = self.textarea.get('sel.first', 'sel.last')
        self.textarea.clipboard_append(text)
        print('Text Copied!')

    def cut(self):
        self.textarea.clipboard_clear()
        text = self.textarea.get('sel.first', 'sel.last')
        self.textarea.clipboard_append(text)
        self.textarea.delete('sel.first', 'sel.last')
        print('Text Cut!')

    def paste(self):
        text = self.textarea.clipboard_get()
        self.textarea.insert(INSERT, text)
        print('Text Pasted!')

    def delete(self):
        self.textarea.delete('sel.first', 'sel.last')
        print('Text Deleted!')

    def select_all(self):
        self.textarea.tag_add(SEL, "1.0", END)
        self.textarea.mark_set(INSERT, "1.0")
        self.textarea.see(INSERT)
        print('All text selected!')

    def delete_all(self):
        self.textarea.delete(1.0, END)
        print('All text deleted!')

    def timendate(self):
        self.textarea.insert(INSERT, datetime.datetime.now())
        print('Current Time and Date inserted!')

    def search_wikipedia(self):
        global text_box, sentence_box
        window = Toplevel(self.master)
        window.iconbitmap('notepad.ico')
        window.geometry('300x150')
        window.resizable(False, False)
        window.title('Search with Wikipedia')

        text_label = Label(window, text='Text:')
        text_label.place(x=20, y=20)

        text_box = Entry(window)
        text_box.place(x=20, y=40)

        sentence_label = Label(window, text='Number of sentence:')
        sentence_label.place(x=20, y=70)

        sentence_box = Entry(window)
        sentence_box.place(x=20, y=90)

        search_btn = Button(window, text='Search & Find', relief=RIDGE, command=self.search)
        search_btn.place(x=170, y=50)
        window.focus_set()

    def search(self):
        global text_box, sentence_box
        lines = sentence_box
        text = wikipedia.summary(f'{text_box}', sentences=f'{lines}')
        self.textarea.insert(INSERT, text)
        print('Searching wikipedia for {}!'.format(text_box))

    def line_column(self):
        row, col = self.textarea.index(INSERT).split('.')
        self.status.config(text=f'Line:{row} | Column:{col}')
        self.master.after(100, self.line_column)

    def find_replace(self):
        global find_entry, replace_entry
        # making window setup
        window = Toplevel(self.master)
        window.geometry('300x150')
        window.resizable(False, False)
        window.iconbitmap('notepad.ico')
        window.title('Find & Replace')

        find_label = Label(window, text='Find:')
        find_label.place(x=20, y=20)

        find_entry = Entry(window)
        find_entry.place(x=50, y=20)

        find_btn = Button(window, text='      Find      ', relief=RIDGE, command=self.find)
        find_btn.place(x=205, y=15)

        replace_label = Label(window, text='Replace:')
        replace_label.place(x=0, y=60)

        replace_entry = Entry(window)
        replace_entry.place(x=50, y=60)

        replace_btn = Button(window, text='    Replace    ', relief=RIDGE, command=self.findNreplace)
        replace_btn.place(x=195, y=55)

        remove_highlight = Button(window, text='\tRemove Highlight\t', relief=RIDGE, command=self.remove_highlight)
        remove_highlight.place(x=40, y=100)

        window.focus_set()

    def find(self):
        self.textarea.tag_remove('found', '1.0', END)
        s = find_entry.get()

        if s:
            idx = '1.0'
            while 1:
                # searches for desired string from index 1
                idx = self.textarea.search(s, idx, nocase=1, stopindex=END)

                if not idx:
                    break

                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(s))

                # overwrite 'Found' at idx
                self.textarea.tag_add('found', idx, lastidx)
                idx = lastidx

            # mark located string as red

            self.textarea.tag_config('found', foreground='black', background='yellow')

        find_entry.focus_set()

    def remove_highlight(self):
        self.textarea.tag_remove('found', 1.0, END)
        print('Highlight removed!')

    def findNreplace(self):
        # remove tag 'found' from index 1 to END
        self.textarea.tag_remove('found', '1.0', END)

        # returns to widget currently in focus
        s = find_entry.get()
        r = replace_entry.get()

        if s and r:
            idx = '1.0'
            while 1:
                # searches for desired string from index 1
                idx = self.textarea.search(s, idx, nocase=1, stopindex=END)
                print(idx)
                if not idx:
                    break

                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(s))

                self.textarea.delete(idx, lastidx)
                self.textarea.insert(idx, r)

                lastidx = '% s+% dc' % (idx, len(r))

                # overwrite 'Found' at idx
                self.textarea.tag_add('found', idx, lastidx)
                idx = lastidx

            # mark located string as red
            self.textarea.tag_config('found', foreground='black', background='yellow')
        find_entry.focus_set()
        print('Text found and highlighted!')

    def copy_file_path(self):
        self.textarea.clipboard_clear()
        self.textarea.clipboard_append(self.recent_file)
        print('Current file path copied!')

    def font_type(self):
        global font_box
        window = Toplevel(self.master)
        window.geometry('270x250')
        window.title('Font')
        window.resizable(False, False)
        window.iconbitmap('notepad.ico')

        font_label = LabelFrame(window, text='Font:')
        font_label.place(x=20, y=20)

        font_box = Listbox(font_label)
        font_box.pack()

        apply = Button(window, text='     APPLY     ', command=self.apply, relief=RIDGE)
        apply.place(x=170, y=50)

        okay = Button(window, text='      OKAY      ', command=self.okay, relief=RIDGE)
        okay.place(x=170, y=100)

        okay = Button(window, text='   CANCEL    ', command=window.destroy, relief=RIDGE)
        okay.place(x=170, y=150)

        info = Label(window, text='First APPLY, then OKAY', font='Corbel 9')
        info.place(x=0, y=233)

        font_list = ['Consolas', 'Arial', 'Cambria', 'Calibri', 'Courier', 'Constantia', 'Corbel', 'Candara',
                     'Fixedsys', 'Gabriola', 'Georgia', 'Impact', 'Marlett', 'Ebrima', 'MingLiU_HKSCS-ExtB', 'Modern',
                     'NSimSun', 'PMingLiU-ExtB', 'Roman', 'Script', 'SimSun', 'Sylfaen', 'Symbol', 'System', 'Tahoma',
                     'Terminal', 'Webdings', 'Wingdings', 'Bahnschrift']
        font_list.sort()
        for i in font_list:
            font_box.insert(END, i)
        window.focus_set()

    @staticmethod
    def apply():
        file = open('font.dat', 'rb+')
        pickle.load(file)
        file.seek(0)
        new_font = font_box.selection_get()
        pickle.dump(new_font, file)
        file.close()

    def okay(self):
        file1 = open('size.dat', 'rb+')
        size1 = pickle.load(file1)
        file1.close()

        file2 = open('font.dat', 'rb')
        font1 = pickle.load(file2)
        file2.close()
        self.textarea.configure(font=f'{font1} {size1}')
        print('Font updated: {}'.format(font1))

    def font_size(self):
        global size_box
        size_list = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 55, 68, 72]

        window = Toplevel(self.master)
        window.title('Font Size')
        window.geometry('270x250')
        window.resizable(False, False)
        window.iconbitmap('notepad.ico')

        size_label = LabelFrame(window, text='Size:')
        size_label.place(x=20, y=20)

        size_box = Listbox(size_label)
        size_box.pack()

        for i in size_list:
            size_box.insert(END, i)

        apply = Button(window, text='     APPLY     ', command=self.size_apply, relief=RIDGE)
        apply.place(x=170, y=50)

        okay = Button(window, text='      OKAY      ', command=self.size_okay, relief=RIDGE)
        okay.place(x=170, y=100)

        okay = Button(window, text='   CANCEL    ', command=window.destroy, relief=RIDGE)
        okay.place(x=170, y=150)

        info = Label(window, text='First APPLY, then OKAY', font='Corbel 9')
        info.place(x=0, y=233)

        window.focus_set()

    @staticmethod
    def size_apply():
        f3 = open('size.dat', 'rb+')
        pickle.load(f3)
        new_size = size_box.selection_get()
        print(f'Font Size updated : {new_size}')
        f3.seek(0)
        pickle.dump(new_size, f3)
        f3.close()

    def size_okay(self):
        f4 = open('size.dat', 'rb+')
        file2 = pickle.load(f4)
        f5 = open('font.dat', 'rb+')
        file1 = pickle.load(f5)
        self.textarea.configure(font=f'{file1} {file2}')
        f4.close()
        f5.close()
        print('Font size updated: {}'.format(file2))

    def dark_mode(self):
        if self.var.get() == 1:
            self.textarea.configure(bg='Gray20', fg='White', insertbackground='Gray20')
            self.status.configure(bg='Gray30', fg='white')
            self.filemenu.configure(bg='Gray30', fg='white')
            self.editmenu.configure(bg='Gray30', fg='white')
            self.formatmenu.configure(bg='Gray30', fg='white')
            self.viewmenu.configure(bg='Gray30', fg='white')
            self.helpmenu.configure(bg='Gray30', fg='white')
            print('Dark Mode: ON')

        elif self.var.get() == 0:
            self.textarea.configure(bg='white', fg='Black', insertbackground='black')
            self.status.configure(bg='snow2', fg='black')
            self.filemenu.configure(bg='snow2', fg='black')
            self.editmenu.configure(bg='snow2', fg='black')
            self.formatmenu.configure(bg='snow2', fg='black')
            self.viewmenu.configure(bg='snow2', fg='black')
            self.helpmenu.configure(bg='snow2', fg='black')
            print('Dark Mode: OFF')
        else:
            pass

    def text_color(self):
        color = colorchooser.askcolor(title='Text Color')
        self.textarea.configure(fg=f"{color[1]}")
        print('Text Color changed: {}'.format(color[1]))

    def reset_all(self):
        self.master.title(f"{self.title}")
        self.master.geometry('1000x500+150+100')
        self.textarea.configure(bg='white', fg='Black', insertbackground='black', font='Calibri 14')
        self.status.configure(bg='snow2', fg='black')
        self.filemenu.configure(bg='snow2', fg='black')
        self.editmenu.configure(bg='snow2', fg='black')
        self.formatmenu.configure(bg='snow2', fg='black')
        self.viewmenu.configure(bg='snow2', fg='black')
        self.textarea.tag_remove('found', 1.0, END)

        file = open('recent_file.dat', 'rb+')
        pickle.load(file)
        file.seek(0)
        recent_file = ' '
        pickle.dump(recent_file, file)
        file.close()

        file1 = open('font.dat', 'rb+')
        pickle.load(file1)
        file1.seek(0)
        Font = 'Calibri'
        pickle.dump(Font, file1)
        file1.close()

        file2 = open('size.dat', 'rb+')
        pickle.load(file2)
        Size = '12'
        file2.seek(0)
        pickle.dump(Size, file2)
        file2.close()

        self.master.destroy()

    def word_wrap(self):
        if self.var1.get() == 1:
            self.textarea.configure(wrap=WORD)
            print('Word Wrap: ON')
        elif self.var1.get() == 0:
            self.textarea.configure(wrap=NONE)
            print('Word Wrap: OFF')
        else:
            pass

    def do_popup(self, event):
        try:
            self.right_click.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click.grab_release()


if __name__ == '__main__':
    root = Tk()
    App(root).start()
    root.mainloop()
