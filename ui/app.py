from tkinter import Tk, ttk
from ui.frames.research import ResearchFrame
from ui.frames.test import TestFrame

class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.title('Face Classifier')
        self.attributes('-zoomed', True)
        self.notebook = ttk.Notebook(self)
        self.test = TestFrame(self.notebook)
        self.research = ResearchFrame(self.notebook)
        self.notebook.add(self.test, text='Test')
        self.notebook.add(self.research, text='Research')
        self.notebook.pack(expand=1, fill='both')