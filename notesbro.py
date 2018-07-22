from tkinter import *
from tkinter import filedialog, ttk
import os
from fetchNotes import FetchNotes
import clipboard
import queue


class NotesBro(Frame):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.lbl1 = Label(self, text='Enter download URL\n(Make sure it '
                                     'is the first page of notes)', font=30)
        self.lbl1.grid(row=0, column=0, pady=30)

        self.txt1 = Entry(self, width=50, font=25)
        self.txt1.grid(row=1, column=0)
        self.txt1.insert(0, clipboard.paste())

        self.lbl2 = Label(self, text='Download Location', font=30)
        self.lbl2.grid(row=2, column=0, pady=20)

        global address
        address.set(os.getcwd()+'\\NotesBro')
        self.txt2 = Entry(self, textvariable=address, width=50, font=25)
        self.txt2.grid(row=3, column=0)

        self.btn1 = Button(self, text='...', command=self.choosedir)
        self.btn1.grid(row=3, column=1)

        print(self.txt1.get())
        self.thread1 = FetchNotes(self.txt1.get(), address)
        self.thread1.daemon = True  # Exits when the main thread exits
        self.btn2 = Button(self, text='Download', font=20,
                           command=self.thread1.start)
        self.btn2.grid(row=4, column=0, pady=25)

        self.progress = ttk.Progressbar(self, orient='horizontal',
                                        length=400, mode='determinate')
        self.progress.grid(row=5, columnspan=2)
        # self.thread1.return_queue().put(0)
        # self.set_progress(self.thread1)
        self.pack()

    def choosedir(self):
        file_path = filedialog.askdirectory()
        address.set(file_path + '/NotesBro')

    def set_progress(self, thread1):
        try:
            cur = thread1.return_queue().get(block=False)
            print('Setting progress')
            while not thread1.return_queue().empty():
                cur = thread1.return_queue().get(block=False)
                if cur is None:
                    break
                print(cur)
            self.progress['maximum'] = 100
            self.progress['value'] = cur

        except queue.Empty:
            self.after(100, self.set_progress(thread1))


root = Tk()
address = StringVar(root)
obj = NotesBro(root)
root.title('NotesBro')
root.geometry('520x400')
root.mainloop()
