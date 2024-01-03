import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, filedialog, messagebox
import re
from PIL import ImageTk, Image

###############################################################################################################
###############################################################################################################

# Applet Frame

###############################################################################################################
###############################################################################################################

class AppletFrame(tk.Frame):
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent, width="180", bg=app.theme["frame_background"])

        # Project Name Components
        self._projectNameLabel = CustomLabel(app, self, text="Project Name:")
        self._projectNameEntry = CustomEntry(app, self, width=20, initial_text='default')
        self._projectNameLabelSuffix = CustomLabel(app, self, text="_wdtitle.wdl")

        # Button Components
        self._addLineButton = CustomButton(app, self, text="Add Line", binding_function=parent.add_line)
        self._removeLineButton = CustomButton(app, self, text="Remove Line(s)", binding_function=parent.remove_lines)
        self._editButton = CustomButton(app, self, text="Edit Line", binding_function=parent.edit_line)
        self._saveButton = CustomButton(app, self, text="Save As", binding_function=parent.save_as)

        self._projectNameLabel.place(x=10, y=10, anchor='nw')
        self._projectNameEntry.place(x=90, y=10, anchor='nw')
        self._projectNameLabelSuffix.place(x=229, y=10, anchor='nw')

        self._addLineButton.place(x=10, y=50, anchor='nw')
        self._removeLineButton.place(x=110, y=50, anchor='nw')
        self._editButton.place(x=210, y=50, anchor='nw')
        self._saveButton.place(x=310, y=50, anchor='nw')

        # Treeview Component
        columns = ["Line #", "Description"]
        self._treeview = CustomTreeview(app, self,columns=columns, binding_function=lambda e: parent.current_item(e))
        self._treeview.column("1", width=110, anchor='c')
        self._treeview.column("2", width=255, anchor='c')
        self._treeview.place(x=10, y=100, anchor='nw')
        self._treeview.populate()

        # Vertical Scrollbar
        self._yscrollbar = CustomTreeviewScrollbarY(app, self, self._treeview)
        self._yscrollbar.place(x=380, y=100, height=226)
        self._treeview.add_vertical_scrollbar(self._yscrollbar)
    
    def clear(self):
        self._projectNameEntry.delete(0, 'end')
        self._treeview.populate()
    
    def update_file_name(self, filename):
        self._projectNameEntry.insert('0', filename)
    
    def get_file_name(self):
        return f"{self._projectNameEntry.get()}_wdtitle.wdl"


###############################################################################################################
###############################################################################################################

# Main Application

###############################################################################################################
###############################################################################################################

class Application:
    def __init__(self):
        self._icon = None #os.path.abspath('img/wdl_builder.ico')

        # DIRECTORY SETUP
        self._srcDirectory = None
        if getattr(sys, 'frozen', False):
            self._srcDirectory = sys._MEIPASS
        else:
            self._srcDirectory = os.path.dirname(os.path.abspath(__file__))
        
        # APPLICATION COLORS
        self._frameBackground = '#ffffff'
        self._foreground = '#070707'

        self._label_font = ('Sans', '8') #, 'bold')
        self._label_background = '#ffffff'

        self._entry_font = ('Sans', '8') #, 'bold')
        self._entry_fg = '#000000'
        self._entry_bg = '#ffffff'
        self._entry_width = 10
        self._entry_justify = 'left'

        self._config = {
            "icon_path":self._icon,
            "src_dir":self._srcDirectory
        }

        self._theme = {
            "frame_background": self._frameBackground,
            "foreground": self._foreground,

            "label_font": self._label_font,
            "label_background": self._label_background,

            "entry_font": self._entry_font,
            "entry_fg": self._entry_fg,
            "entry_bg": self._entry_bg,
            "entry_width": self._entry_width,
            "entry_justify": self._entry_justify
        }

        self._defaults = {
            "lines": 20,
            "project_name": "default"
        }
        
        # List of Line Numbers (as strings), also serve as IDs for treeview
        self._line_ids = [f"Line {x+1}" for x in range(self._defaults["lines"])]

        # Dictionary of Line #s -> Line Descriptions
        self._lines = {f"Line {x+1}": "" for x in range(len(self._line_ids))}

        self._currentWindow = ApplicationWindow(self)

    @property
    def config(self):
        return self._config
    
    @property
    def theme(self):
        return self._theme
    
    @property
    def defaults(self):
        return self._defaults
    
    @property
    def srcDirectory(self):
        return self._srcDirectory
    
    @property
    def lines(self):
        return self._lines
    
    @property
    def line_ids(self):
        return self._line_ids
    
    def remove_line(self, line_id:str):
        '''
        Removes a line from the application with key line_id
        '''
        try:
            self._line_ids.remove(line_id)
            self._lines.pop(line_id)
        except Exception as e:
            return 0
    
    def add_line(self, line_id:str):
        '''
        Adds a line to the application with key line_id
        '''
        try:
            pattern = re.compile(r'^Line \d+$')
            if bool(pattern.match(line_id)) and line_id != "Line 0":
                self._line_ids.append(line_id)
                self._line_ids = sorted(self._line_ids, key=lambda x: int(x.split()[-1]))
                self._lines[line_id] = ""
                return 0
            return -1
        except Exception as e:
            return -1
    
    def edit_line(self, line_id:str, description:str):
        '''
        Edits a line's description.
        '''
        try:
            pattern = re.compile(r'^Line \d+$')
            if bool(pattern.match(line_id)) and line_id != "Line 0":
                self._lines[line_id] = description
                return 0
            return -1
        except Exception as e:
            return -1
    
    def clear_line(self, line_id:str):
        '''
        Clears a line's description
        '''
        self.edit_line(line_id, "")
    
    def clear_all_lines(self):
        '''
        Clears all the line descriptions
        '''
        for line_id in self._line_ids:
            self.edit_line(line_id, "")
    
    def new(self):
        '''
        Resets the application to default state.
        '''
        # List of Line Numbers (as strings), also serve as IDs for treeview
        self._line_ids = [f"Line {x+1}" for x in range(self._defaults["lines"])]
        # Dictionary of Line #s -> Line Descriptions
        self._lines = {f"Line {x+1}": "" for x in range(len(self._line_ids))}
    
    def import_lines(self, new_line_index, new_line_dict):
        self._line_ids = new_line_index
        self._lines = new_line_dict
    
    def generate_output(self):
        output_content = ""
        for line_id in self._line_ids:
            if self._lines[line_id] != "":
                output_content += f"{line_id.upper().replace(" ", "")}={self._lines[line_id]}\n"
        
        return output_content




        

    
    



###############################################################################################################
###############################################################################################################

#   Main Application Window

###############################################################################################################
###############################################################################################################

class ApplicationWindow(tk.Tk):
    def __init__(self, application):
        self._app: Application = application
        self._current_selection = []

        tk.Tk.__init__(self)
        self.winfo_toplevel().title("WDL Builder")
        #self.iconbitmap(application.config['icon_path'])

        menubar = ApplicationMenu(self)
        self._appletFrame = AppletFrame(self, application)
        self.columnconfigure(0, minsize=100, weight=1)
        self.columnconfigure(1, minsize=100, weight=1)
        self.columnconfigure(2, minsize=100, weight=1)
        self.columnconfigure(3, minsize=100, weight=1)
        self.rowconfigure(0, minsize=100, weight=1)
        self.rowconfigure(1, minsize=100, weight=1)
        self.rowconfigure(2, minsize=250, weight=1)

        self._appletFrame.grid(row=0, column=0, columnspan=4, rowspan=3, sticky="NEWS")

        self.winfo_toplevel().geometry("400x350+50+50")
        self.mainloop()

    def kill(self):
        self.winfo_toplevel().destroy()
    
    @property
    def app(self):
        return self._app
    
    def current_item(self, event):
        '''
        Event function to keep track of currently selected rows
        '''
        tree = event.widget
        self._current_selection = [tree.item(item)["text"] for item in tree.selection()]
    
    def open(self):
        '''
        Opens the file dialog and asks user to open an existing WDL file.
        '''
        try:
            lines = []
            filename = ""
            with filedialog.askopenfile('r',defaultextension="wdl",title="Choose WDL file...") as fd:
                if os.path.splitext(os.path.basename(fd.name))[1] != '.wdl':
                    fd.close()
                    return -1
                
                if not os.path.splitext(os.path.basename(fd.name))[0].lower().endswith('_wdtitle'):
                    fd.close()
                    return -1
                
                lines = fd.readlines()
                filename = os.path.splitext(os.path.basename(fd.name))[0].lower().replace('_wdtitle', '')
            
                fd.close()
        except TypeError:
            return -1
        
        try:
            line_dict = {}
            line_index = []
            for line in lines:
                line_key, line_description = line.split('=')
                line_key = line_key.replace("LINE", "")
                line_key = "Line " + line_key

                line_index.append(line_key)
                
                line_description = line_description.strip()
                line_dict[line_key] = line_description
            
            self._app.import_lines(line_index, line_dict)
            self._appletFrame.clear()
            self._appletFrame.update_file_name(filename)
            self._current_selection = []
        
        except ValueError:
            return -1

    def save_as(self):
        content = self._app.generate_output()
        if content == "":
            return -1

        initial_file_name = self._appletFrame.get_file_name()
        if initial_file_name == "_wdtitle.wdl":
            initial_file_name = "default" + initial_file_name

        file_path = None
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".wdl", confirmoverwrite=True, filetypes=[("WDL Files", "*.wdl")], initialfile=f"{initial_file_name}")
        except TypeError:
            return -1
        
        try:
            if file_path:
                with open(file_path, 'w') as fd:
                    fd.write(content)
                    fd.close()
                return 0
            return -1
        except Exception:
            return -1
    
    def clear(self):
        self._app.clear_all_lines()
        self._appletFrame.clear()
        self._current_selection = []
    
    def new(self):
        self._app.new()
        self._appletFrame.clear()
        self._current_selection = []
    
    def add_line(self):
        user_input = simpledialog.askinteger("Enter", "Enter line number to add:")
        line_id = "Line " + str(user_input)
        if line_id in self._app.line_ids:
            return 0
        
        self._app.add_line(line_id)
        self._appletFrame.clear()
        self._current_selection = []
    
    def add_lines(self):
        user_input = simpledialog.askstring("Enter", "Enter line numbers separated by commas:")
        
        def unique_integers(string):
            try:
                integers = [int(num) for num in string.split(',')]
                return len(integers) == len(set(integers))
            except ValueError:
                return False
            except AttributeError:
                return False
        
        if unique_integers(user_input):
            for i in [int(num) for num in user_input.split(',')]:
                line_id = "Line " + str(i)
                if line_id in self._app.line_ids:
                    continue
                self._app.add_line(line_id)
                self._appletFrame.clear()

            self._current_selection = []
        
    def remove_lines(self):
        if len(self._current_selection) == 0:
            return -1
        
        result = ""
        if len(self._current_selection) == 1:
            result = messagebox.askquestion("Remove Line",f"Are you sure you want to delete {self._current_selection[0]}?")
        else:
            result = messagebox.askquestion("Remove Lines",f"Are you sure you want to delete these lines?")

        if result == 'no':
            return -1
        
        for selection in self._current_selection:
            self._app.remove_line(selection)
            self._appletFrame.clear()
        
        self._current_selection = []

        return 0
    
    def edit_line(self):
        if len(self._current_selection) != 1:
            return -1

        description = simpledialog.askstring("Enter", f"Enter description for {self._current_selection[0]}:")

        def does_not_contain_special_characters(input_string):
            pattern = re.compile(r'[@#.*?~\[\]-]')
            match = pattern.search(input_string)
            return match is None
        
        if description is not None and does_not_contain_special_characters(description):
            self._app.edit_line(self._current_selection[0], description)
            self._appletFrame.clear()
            self._current_selection = []
            return 0
        
        return -1
        


        


        
        

###############################################################################################################
###############################################################################################################

#   Main Menu Bar

###############################################################################################################
###############################################################################################################

class ApplicationMenu(tk.Menu):
    def __init__(self, parent):
        self._menubar = tk.Menu(parent)
        parent.config(menu=self._menubar)

        # File Menu Items
        self._fileMenu = tk.Menu(self._menubar, tearoff=0)
        self._fileMenu.add_command(label="New", command=parent.new)
        self._fileMenu.add_separator()
        self._fileMenu.add_command(label="Open...", command=parent.open)
        self._fileMenu.add_command(label="Save As...", command=parent.save_as)
        self._fileMenu.add_separator()
        self._fileMenu.add_command(label="Clear Descriptions", command=parent.clear)
        self._fileMenu.add_command(label="Close", command=parent.kill)

        self._menubar.add_cascade(label="File", menu = self._fileMenu)

        # Edit Menu Items
        self._editMenu = tk.Menu(self._menubar, tearoff=0)
        self._editMenu.add_command(label="Add Line...", command=parent.add_line)
        self._editMenu.add_command(label="Add Lines...", command=parent.add_lines)
        self._editMenu.add_command(label="Modify Selected Line...", command=parent.edit_line)
        self._editMenu.add_command(label="Remove Selected Line(s)...", command=parent.remove_lines)

        self._menubar.add_cascade(label="Edit", menu=self._editMenu)



###############################################################################################################
###############################################################################################################

#   Custom Entry

###############################################################################################################
###############################################################################################################

class CustomEntry(ttk.Entry):
    def __init__(self, app:Application, parent, width=0, initial_text=""):
        if width == 0:
            width = app.theme["entry_width"]
        
        ttk.Entry.__init__(self, parent)

        self.configure(font=app.theme["entry_font"])
        self.configure(width=width)
        self.configure(justify=app.theme["entry_justify"])

        self.insert(0, initial_text)

###############################################################################################################
###############################################################################################################

#   Custom Label

###############################################################################################################
###############################################################################################################

class CustomLabel(ttk.Label):
    def __init__(self, app:Application, parent, text=""):
        if text == "":
            text = "placeholder"
        
        ttk.Label.__init__(self, parent)

        self.configure(text=text)
        self.configure(background=app.theme['label_background'])
        self.configure(font=app.theme['label_font'])

###############################################################################################################
###############################################################################################################

#   Custom Button

###############################################################################################################
###############################################################################################################

class CustomButton(ttk.Button):
    def __init__(self, app:Application, parent, text="", binding_type="", binding_function=None):
        if text == "":
            text = "placeholder"
        
        if binding_function is not None and binding_type == "":
            ttk.Button.__init__(self, parent, command=binding_function)
        else:
            ttk.Button.__init__(self, parent)

        self.configure(text=text)

###############################################################################################################
###############################################################################################################

#   Custom Treeview

###############################################################################################################
###############################################################################################################

class CustomTreeview(ttk.Treeview):
    def __init__(self, app:Application, parent, columns=[], binding_function=None):
        self._app = app

        if len(columns) == 0:
            raise ValueError("Can't build treeview without columns")
        
        ttk.Treeview.__init__(self, parent)
        
        if binding_function is not None:
            self.bind("<<TreeviewSelect>>", binding_function)

        self.configure(height=10)

        # Configure and add column IDs to treeview
        column_ids = []
        for c_id in range(0, len(columns)):
            column_ids.append(str(c_id+1))
        self["columns"] = tuple(column_ids)
        
        # Configure headings to show, delete the #0 index column
        self['show'] = 'headings'

        # Add headings
        for c_id in range(0, len(column_ids)):
            self.heading(str(c_id+1), text=columns[c_id])

    def add_vertical_scrollbar(self, scrollbar:ttk.Scrollbar):
        self.configure(yscrollcommand=scrollbar.set_scrollbar())

    def populate(self):
        self.delete(*self.get_children())

        for i in range(0, len(self._app.line_ids)):
            text = self._app.line_ids[i]
            value = self._app.lines[text]
            self.insert("", 'end', text=text, values=(text, value))

###############################################################################################################
###############################################################################################################

#   Custom Treeview Vertical Scrollbar

###############################################################################################################
###############################################################################################################

class CustomTreeviewScrollbarY(ttk.Scrollbar):
    def __init__(self, app:Application, parent, treeview:ttk.Treeview):
        ttk.Scrollbar.__init__(self, parent, orient='vertical', command=treeview.yview)
    
    def set_scrollbar(self):
        return self.set
    


if __name__ == "__main__":
    app = Application()