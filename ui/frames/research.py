from tkinter import (BOTH, BOTTOM, HORIZONTAL, LEFT, TOP, Button, Canvas,
                     Entry, Frame, Label, N, OptionMenu, Scrollbar, StringVar,
                     W, X)

from matplotlib import image
from core.config.config import METHODS, DATA_DIR
from core.scripts.research import parallel_research, research
from PIL import Image, ImageTk

class ResearchFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fst_frame = Frame(self)
        self.scnd_frame = Frame(self)

        self.const_label = Label(
            self.fst_frame,
            text='Step-by-step case',
            font='Times 15'
        )

        self.method_label = Label(self.fst_frame, text='Method: ')
        self.method = StringVar()
        self.method.set(METHODS[0])
        self.method_choose = OptionMenu(
            self.fst_frame,
            self.method,
            *METHODS
        )
        self.method_choose.configure(width=10)

        self.results = []
        self.run_button = Button(
            self.fst_frame,
            text = 'Go!',
            command=self.research
        )

        self.parallel_label = Label(
            self.fst_frame,
            text='Parallel case',
            font='Times 15'
        )
        self.hist_label = Label(self.fst_frame, text='Histogram: ')
        self.hist_entry = Entry(self.fst_frame,width=7)
        self.scale_label = Label(self.fst_frame, text='Scale: ')
        self.scale_entry = Entry(self.fst_frame,width=7)
        self.grad_label = Label(self.fst_frame, text='Gradient: ')
        self.grad_entry = Entry(self.fst_frame,width=7)
        self.dft_label = Label(self.fst_frame, text='DFT: ')
        self.dft_entry = Entry(self.fst_frame,width=7)
        self.dct_label = Label(self.fst_frame, text='DCT: ')
        self.dct_entry = Entry(self.fst_frame,width=7)

        self.parallel_run = Button(
            self.fst_frame,
            text='Go!',
            command=self.parallel_research
        )

        self.canvas = Canvas(self, width=1400,height=800)
        self.scroll_x = Scrollbar(
            self,
            orient=HORIZONTAL,
            command=self.canvas.xview
        )
        self.columnconfigure(0, weight=1)
        self.canvas.config(
            xscrollcommand=self.scroll_x.set,
            scrollregion=self.canvas.bbox('all')
        )
        self.canvas.create_window((0,0), window=self, anchor=N + W)

        self.fst_frame.pack(side=TOP, anchor=W)
        self.scnd_frame.pack(side=TOP, anchor=W)
        self.const_label.pack(side=TOP, padx=10, pady=7, anchor=W)
        self.method_label.pack(side=TOP, padx=10, pady=7, anchor=W)
        self.method_choose.pack(side=TOP, padx=10, pady=7, anchor=W)
        self.run_button.pack(side=TOP, padx=10, pady=7, anchor=W)

        self.parallel_label.pack(side=TOP, padx=10, pady=7, anchor=W)
        self.hist_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.hist_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.scale_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.scale_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.grad_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.grad_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dft_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dft_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dct_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dct_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.parallel_run.pack(side=TOP, padx=10, pady=7, anchor=W)

        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.canvas.pack(fill=BOTH,expand=True)

    def research(self) -> None:
        self.canvas.delete('all')
        best, _, _ = research(self.method.get())
        self.results = []

        pos_x, pos_y = 250, 250

        image = Image.open('./results/result.png')
        image = image.resize((350,350))
        image = ImageTk.PhotoImage(image)
        self.results.append(image)
        self.canvas.create_image(pos_x,pos_y,image=image)

        pos_x += 360
    
    def parallel_research(self) -> None:
        global image
        self.canvas.delete('all')
        self.results = []
        params = {}
        params['hist'] = int(self.hist_entry.get())
        params['scale'] = int(self.scale_entry.get())
        params['grad'] = int(self.grad_entry.get())
        params['dft'] = int(self.dft_entry.get())
        params['dct'] = int(self.dct_entry.get())

        _ = parallel_research(params)

        pos_x, pos_y = 250, 250

        image = Image.open('./results/parallel_res.png')
        image = image.resize((500,300))
        image = ImageTk.PhotoImage(image)
        self.results.append(image)
        self.canvas.create_image(pos_x,pos_y,image=image)
        




