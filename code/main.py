from tkinter import *
from tkinter import ttk 

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Climbing Journal")
        width = 1200
        height = int(width * 2/3)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        # Menu at top 
        self.top_menu = Menu(self.root)

        # file
        self.file = Menu(self.top_menu, tearoff=0)
        self.top_menu.add_cascade(label = "File", menu = self.file)
        self.file.add_command(label="Quit", command=None)
        self.root.config(menu = self.top_menu)

        # options
        self.options = Menu(self.top_menu, tearoff=0)
        self.top_menu.add_command(label="Options", command=self.new_options_window) # opens new options window
        self.root.config(menu = self.top_menu)
    

        # style
        self.tab_style = ttk.Style()
        w = 45
        h = 10
        # makes tabs bigger
        self.tab_style.theme_create("TabStyle", settings={"TNotebook.Tab": {"configure": {"padding": [w, h] },}})
        self.tab_style.theme_use("TabStyle")

        # notebook tab (Journal, stats)
        # create tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(pady=10)
        self.journal_tab = ttk.Frame(self.tabs)
        self.stats_tab = ttk.Frame(self.tabs)

        self.journal_tab.pack(fill=BOTH, expand=1)
        self.stats_tab.pack(fill=BOTH, expand=1)

        self.tabs.add(self.journal_tab, text="Journal")
        self.tabs.add(self.stats_tab, text="Statistics")
        self.tabs.pack(expand=True, fill=BOTH)

        # journal tab
        ttk.Label(self.journal_tab, text="Journal tab").pack(fill=BOTH)

        # stats tab
        ttk.Label(self.stats_tab, text="Stats tab").pack(fill=BOTH)


    def new_options_window(self):
        print("Opened new options window")


root = Tk()
app = App(root)
root.mainloop()