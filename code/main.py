from tkinter import *
from tkinter import ttk 
import tkinter.font as tf
import MultiListbox as table
from data import data

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Climbing Journal")
        width = 1200
        height = int(width * 2/3)
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        self.row = None

        # num of windows to open
        self.add_win = None
        self.edit_win = None

        self.date = StringVar()
        self.route_name = StringVar()
        self.grade = StringVar()
        self.place = StringVar()
        self.num_tries = StringVar()
        self.note = StringVar()
        self.os_var = BooleanVar()
        self.flash_var = BooleanVar()
        self.rp_var = BooleanVar()
        # Menu at top 
        self.top_menu = Menu(self.root)

        # file
        self.file = Menu(self.top_menu, tearoff=0)
        self.top_menu.add_cascade(label = "File", menu = self.file)
        self.file.add_command(label="Quit", command=self.root.quit)
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

        label_font = tf.Font(family="Arial", size=15)

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
        # table
        self.mlb = table.MultiListbox(
            self.journal_tab,
            (("Date", 20),
             ("Name", 20),
             ("Grade", 10))
        )
        
        for item in data:
            self.mlb.insert(END, (item.get("date"), item.get("route_name"), item.get("grade")))

        self.mlb.pack(fill=BOTH, side=LEFT, padx=5, pady=5)
        self.mlb.subscribe(lambda row: self.show(row))

        # details on the right
        self.detail_label_frame = LabelFrame(self.journal_tab, text="Details")
        self.detail_label_frame.pack(fill=BOTH, padx=10, pady=10, expand=True)

        self.detail_frame = Frame(self.detail_label_frame)
        self.detail_frame.pack(expand=True, fill=BOTH, padx=5, pady=5)

        self.detail_frame.columnconfigure(0, weight=0)  
        self.detail_frame.columnconfigure(1, weight=1)  
        self.detail_frame.columnconfigure(2, weight=2) 
        self.detail_frame.rowconfigure(6, weight=1)     

        # details content
        self.title_lbl = Label(self.detail_frame, text="Name", font=label_font)
        self.date_lbl = Label(self.detail_frame, text="Date", font=label_font)
        self.grade_lbl = Label(self.detail_frame, text="Grade", font=label_font)
        self.place_lbl = Label(self.detail_frame, text="Place", font=label_font)
        self.tries_lbl = Label(self.detail_frame, text="Tries", font=label_font)

        self.title_entry = Entry(self.detail_frame, width=18, textvariable=self.route_name)
        self.date_entry = Entry(self.detail_frame, width=18, textvariable=self.date)
        self.grade_entry = Entry(self.detail_frame, width=18, textvariable=self.grade)
        self.place_entry = Entry(self.detail_frame, width=18, textvariable=self.place)
        self.tries_entry = Entry(self.detail_frame, width=18, textvariable=self.num_tries)

        self.title_lbl.grid(row=0, column=0, sticky=W, padx=5, pady=2)
        self.title_entry.grid(row=0, column=1, sticky=EW, padx=5)

        self.date_lbl.grid(row=1, column=0, sticky=W, padx=5, pady=2)
        self.date_entry.grid(row=1, column=1, sticky=EW, padx=5)

        self.grade_lbl.grid(row=2, column=0, sticky=W, padx=5, pady=2)
        self.grade_entry.grid(row=2, column=1, sticky=EW, padx=5)

        self.place_lbl.grid(row=3, column=0, sticky=W, padx=5, pady=2)
        self.place_entry.grid(row=3, column=1, sticky=EW, padx=5)

        self.tries_lbl.grid(row=4, column=0, sticky=W, padx=5, pady=2)
        self.tries_entry.grid(row=4, column=1, sticky=EW, padx=5)


        self.os_cb = Checkbutton(self.detail_frame, text="OS", variable=self.os_var)
        self.flash_cb = Checkbutton(self.detail_frame, text="Flash", variable=self.flash_var)
        self.rp_cb = Checkbutton(self.detail_frame, text="RP", variable=self.rp_var)

        self.os_cb.grid(row=5, column=0, sticky=W, padx=5)
        self.flash_cb.grid(row=6, column=0, sticky=W, padx=5)
        self.rp_cb.grid(row=7, column=0, sticky=W, padx=5)

        # phot
        self.media_frame = Frame(self.detail_frame, relief=SOLID, bd=1)
        self.media_frame.grid(row=0, column=2, rowspan=6, padx=10, pady=5, sticky=NSEW)

        self.detail_frame.rowconfigure(0, weight=1)
        self.detail_frame.rowconfigure(1, weight=1)
        self.detail_frame.rowconfigure(2, weight=1)
        self.detail_frame.rowconfigure(3, weight=1)
        self.detail_frame.rowconfigure(4, weight=1)

        Label(self.media_frame, text="Photo / Video").place(relx=0.5, rely=0.5, anchor=CENTER)

        # notes
        self.notes_text = Text(self.detail_frame, height=8)
        self.notes_text.grid(row=8, column=0, columnspan=3, sticky=NSEW, padx=5, pady=5)

        self.detail_frame.columnconfigure(1, weight=1)

        # buttons (add, edit, delete)
        self.button_frame = Frame(self.journal_tab)
        self.button_frame.pack(fill=X)

        bw = 8
        bh = 1
        self.add_button = Button(self.button_frame, text="Add", width=bw, height=bh, command=self.new_add_window)
        self.edit_button = Button(self.button_frame, text="Edit", width=bw, height=bh, command=self.edit)
        self.delete_button = Button(self.button_frame, text="Delete", width=bw, height=bh, command=self.delete)
        self.add_button.pack(padx=5, pady = 5, side=LEFT, anchor=E, expand=True)
        self.edit_button.pack(padx=5, pady = 5, side=LEFT, anchor=E)
        self.delete_button.pack(padx=5, pady = 5, side=LEFT, anchor=W, expand=True)

        # stats tab
        ttk.Label(self.stats_tab, text="Stats tab").pack(fill=BOTH)

    
    def new_options_window(self):
        print("Opened new options window")

    def new_add_window(self):
        # reseting stuff
        self.row = None    
        self.date.set("")
        self.route_name.set("")
        self.grade.set("")
        self.place.set("")
        self.num_tries.set("")
        self.os_var.set(False)
        self.flash_var.set(False)
        self.rp_var.set(False)
        if self.notes:
            self.notes.delete("1.0", END)
        
        self.edit()
        
    def save(self):
        print("pressed save")
        record = {
            "date": self.date.get(),
            "route_name": self.route_name.get(),
            "grade": self.grade.get(),
            "place": self.place.get(),
            "num_tries": self.num_tries.get(),
            "os_var": self.os_var.get(),
            "flash_var": self.flash_var.get(),
            "rp_var": self.rp_var.get(),
            "note": self.notes.get("1.0", END).strip()
        }

        if self.row is None:
            data.append(record)
            self.mlb.insert(END, (record["date"], record["route_name"], record["grade"]))
        else:
            data[self.row] = record
            self.mlb.delete(self.row)
            self.mlb.insert(self.row, (record["date"], record["route_name"], record["grade"]))
        
        self.notes_text.delete("1.0", END)
        self.notes_text.insert(END, record.get("note"))
        
        self.edit_win.destroy()

    def show(self, row):
        self.row = row
        record = data[row]

        self.date.set(record.get("date"))
        self.route_name.set(record.get("route_name"))
        self.grade.set(record.get("grade"))
        self.place.set(record.get("place"))
        self.num_tries.set(record.get("num_tries"))

        self.os_var.set(record.get("os_var"))
        self.flash_var.set(record.get("flash_var"))
        self.rp_var.set(record.get("rp_var"))

        self.notes_text.delete("1.0", END)
        self.notes_text.insert(END, record.get("note"))

    def edit(self):
        print("pressed edit button")
        global edit_win
        
        if self.edit_win is None or not self.edit_win.winfo_exists():
            self.edit_win = Toplevel()
            w = 650
            h = int(w * (2/3))
            self.edit_win.geometry(f"{w}x{h}")
            self.edit_win.title("New Route")
            
            grades = ["5A","5A+","5B","5B+","5C","5C+",
                    "6A","6A+","6B","6B+","6C","6C+",
                    "7A","7A+","7B","7B+","7C","7C+",
                    "8A","8A+","8B","8B+","8C","8C+",
                    "9A","9A+","9B","9B+","9C"]
            
            self.main = Frame(self.edit_win)
            self.main.pack(fill=BOTH, expand=True)

            self.main.columnconfigure(0, weight=1)
            self.main.rowconfigure(0, weight=1)
            self.content = Frame(self.main)
            self.content.grid(row=0, column=0)

            self.form = Frame(self.content)
            self.form.grid(row=0, column=0, padx=20, pady=20, sticky=N)

            def add_row(row, label, widget):
                Label(self.form, text=label).grid(row=row, column=0, sticky=W, pady=4)
                widget.grid(row=row, column=1, sticky=W)

            add_row(0, "Date", Entry(self.form, textvariable=self.date, width=25))
            add_row(1, "Name", Entry(self.form, textvariable=self.route_name, width=25))
            add_row(2, "Grade", ttk.Combobox(self.form, textvariable=self.grade, values=grades, width=25))
            add_row(3, "Place", Entry(self.form, textvariable=self.place, width=25))
            add_row(4, "Tries", Spinbox(self.form, from_=1, to=100, textvariable=self.num_tries, width=5))
                        
            style_frame = Frame(self.form)
            Checkbutton(style_frame, text="OS", variable=self.os_var).pack(side=LEFT)
            Checkbutton(style_frame, text="Flash", variable=self.flash_var).pack(side=LEFT)
            Checkbutton(style_frame, text="RP", variable=self.rp_var).pack(side=LEFT)

            add_row(5, "Style", style_frame)

            Label(self.form, text="Notes").grid(row=6, column=0, sticky=NW)

            self.notes = Text(self.form, width=40, height=6)
            self.notes.grid(row=7, column=0, columnspan=2, pady=5)
            
            if self.row is not None:
                record = data[self.row]
                self.notes.insert("1.0", record.get("note"))

            self.photo = Frame(self.content, width=200, height=200)
            self.photo.grid(row=0, column=1, padx=30, pady=20)

            Button(self.photo, text="Upload Photo").place(relx=0.5, rely=0.5, anchor=CENTER)

            self.buttons = Frame(self.content)
            self.buttons.grid(row=1, column=0, columnspan=2, pady=20)

            Button(self.buttons, text="Save", width=12, command=self.save).pack(side=LEFT, padx=10)
            Button(self.buttons, text="Cancel", width=12, command=self.edit_win.destroy).pack(side=LEFT)
    
    
    def delete(self):
        if self.row is None:
            return
        
        del data[self.row]
        self.mlb.delete(self.row)
        
        # clearing after deleting
        self.row = None
        self.date.set("")
        self.route_name.set("")
        self.grade.set("")
        self.place.set("")
        self.num_tries.set("")
        self.os_var.set(False)
        self.flash_var.set(False)
        self.rp_var.set(False)

        self.notes_text.delete("1.0", END)

root = Tk()
app = App(root)
root.mainloop()