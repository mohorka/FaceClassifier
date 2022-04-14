import random

from tkinter import (
    LEFT,
    TOP,
    Button,
    Canvas,
    Entry,
    Frame,
    Label,
    OptionMenu,
    StringVar,
    W
)
from core.config.config import METHODS, DATA_DIR
from core.scripts.recognition import recognition, parallel_recognition
from PIL import Image, ImageTk

class TestFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.const_frame = Frame(self)
        self.parall_frame = Frame(self)
        self._canvas = Frame(self)

        self.const_label = Label(
            self.const_frame,
            text='Step-by-step system',
            font='Times 15'
        )
        self.method_label = Label(
            self.const_frame,
            text = 'Method: '
        )
        self.method = StringVar()
        self.method.set(METHODS[0])
        self.method_choose = OptionMenu(
            self.const_frame,
            self.method,
            *METHODS
        )
        self.method_choose.configure(width=10)

        self.param_label = Label(
            self.const_frame,
            text='Parameter: '
        )
        self.p_entry = Entry(self.const_frame, width=7)

        self.train_percentage_label = Label(self.const_frame, text="Train, %: ")
        self.train_percentage_entry = Entry(self.const_frame, width=7)
        
        self.score_label = Label(self.const_frame, text="Accuracy:")
        self.score_result = Label(self.const_frame, text="")

        self.results = []
        self.templates = []

        self.run_button = Button(
            self.const_frame,
            text='Go!',
            command=self.const_test

        )
    
        self.parallel_label = Label(
            self.parall_frame,
            text='Parallel system',
            font='Times 15'
        )
        self.hist_label = Label(self.parall_frame, text="Histogram: ")
        self.hist_entry = Entry(self.parall_frame, width=7)
        
        self.scale_label = Label(self.parall_frame, text="Scale: ")
        self.scale_entry = Entry(self.parall_frame, width=7)

        self.gradient_label = Label(self.parall_frame, text="Gradient: ")
        self.gradient_entry = Entry(self.parall_frame, width=7)

        self.dft_label = Label(self.parall_frame, text="DFT: ")
        self.dft_entry = Entry(self.parall_frame, width=7)

        self.dct_label = Label(self.parall_frame, text="DCT: ")
        self.dct_entry = Entry(self.parall_frame, width=7)

        self.templ_num_label = Label(self.parall_frame, text="Amount of templates: ")
        self.templ_num_entry = Entry(self.parall_frame, width=7)

        self.parallel_button = Button(
            self.parall_frame,
            text='Go!',
            command=self.parallel_test
        )

        self.canvas = Canvas(self._canvas, width=1000,height=800)

        self.const_frame.pack(side=TOP,anchor=W)
        self.parall_frame.pack(side=TOP,anchor=W)
        self.canvas.pack(side=TOP,anchor=W)

        self.const_label.pack(side=TOP, padx=10, pady=7, anchor=W)
        self.method_label.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.method_choose.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.param_label.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.p_entry.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.train_percentage_label.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.train_percentage_entry.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.run_button.pack(side=LEFT, anchor=W, padx=10, pady=7)
        self.score_label.pack(side=LEFT, anchor=W, padx=10)
        self.score_result.pack(side=LEFT, anchor=W)

        self.parallel_label.pack(side=TOP, padx=10, pady=7, anchor=W)
        self.hist_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.hist_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.scale_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.scale_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.gradient_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.gradient_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dft_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dft_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dct_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.dct_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.templ_num_label.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.templ_num_entry.pack(side=LEFT, padx=10, pady=7, anchor=W)
        self.parallel_button.pack(side=TOP, padx=10, pady=7, anchor=W)

        self.canvas.pack(side=TOP)

    def const_test(self) -> None:
        score, images, templates = recognition(
            self.method.get(),
            int(self.p_entry.get()),
            float(self.train_percentage_entry.get())
        )
        self.score_result.config(text=score)

        templ_pos_x, templ_pos_y = 50, 50
        res_pos_x, res_pos_y = 300, 50
        random_idx = [random.randrange(len(images)) for _ in range(5)]

        for idx in random_idx:
            template = Image.fromarray(templates[idx].image)
            template.resize((50,50))
            template = ImageTk.PhotoImage(template)
            self.templates.append(templates)
            self.canvas.create_image(
                templ_pos_x,
                templ_pos_y,
                image=template)
            templ_pos_y += 80

            img = Image.fromarray(images[idx])
            img.resize((50,50))
            img = ImageTk.PhotoImage(img)
            self.results.append(img)
            self.canvas.create_image(res_pos_x,res_pos_y,image=img)
            res_pos_y += 80

    def parallel_test(self) -> None:
        params = {}
        params['hist'] = int(self.hist_entry.get())
        params['scale'] = int(self.scale_entry.get())
        params['grad'] = int(self.gradient_entry.get())
        params['dft'] = int(self.dft_entry.get())
        params['dct'] = int(self.dct_entry.get())
        amount = int(self.templ_num_entry.get())
        scores = parallel_recognition(
            params=params,
            size_of_train=amount
        )

        pos_x, pos_y = 250, 250

        image = Image.open('./results/parallel_res.png')
        image = image.resize((500,300))
        image = ImageTk.PhotoImage(image)
        self.canvas.create_image(pos_x,pos_y,image=image)


