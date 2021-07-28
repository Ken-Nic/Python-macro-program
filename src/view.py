import sqlite3
import tkinter as tk
from tkinter import Button
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import filedialog
import data_access as data
from functools import partial
from sqlite3 import OperationalError
import os
import webbrowser
import time


class ViewGui(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.database = data.DatabaseAccess("macro_database.db")

        if self.database.check_db() is True:
            pass
        else:
            exit()

        # Title
        self.title("Macro App")
        hub = tk.Frame(self)
        hub.grid_columnconfigure(0,weight=1)
        hub.grid_rowconfigure(0, weight=1)
        hub.pack(side=tk.TOP,
                 fill=tk.BOTH,
                 expand=True)

        # Left Side container
        self.left_container = tk.Frame(hub, bg="gray")
        self.left_container.pack(side=tk.LEFT,
                                 fill="both")

        macro_group_label = tk.Label(self.left_container, text="Macro Groups")
        macro_group_label.pack(side=tk.TOP,
                               ipady=5,
                               fill="x")

        scroll_bar = Scrollbar(self.left_container)
        scroll_bar.pack(side=tk.RIGHT,
                        fill="y")

        self.marco_group_listbox = Listbox(self.left_container, yscrollcommand=scroll_bar.set)

        self.marco_group_listbox.pack(side=tk.TOP,
                                      fill="both",
                                      expand=True)

        scroll_bar.config(command=self.marco_group_listbox.yview())
        macro_group_add_button = Button(self.left_container,
                                       text="(Create New Group)",
                                       command=self.new_group)
        macro_group_add_button.pack(side=tk.TOP,
                                   fill="x")

        self.populate_groups(self.marco_group_listbox)

        # Right Side
        self.macro_label = tk.Label(hub, text=" ")
        self.macro_label.pack(side=tk.TOP,
                              fill="x",
                              ipady=5)

        self.right_container = tk.Frame(hub)
        self.right_container.pack(side=tk.RIGHT,
                             fill=tk.BOTH,
                             expand=True)

    def populate_groups(self,frame):
        for groups in self.database.get_groups():
            groups_id = groups[0]
            group_name = groups[1]
            bound_display_records = partial(self.populate_records, groups_id)
            new_button = tk.Button(frame,
                                   text=f"{group_name}",
                                   command=bound_display_records)
            new_button.pack(fill="x")

    def populate_records(self, id):
        for items in self.right_container.winfo_children():
            items.destroy()

        self.macro_label.config(text=f"{self.database.find_group_name(id)[0]}")

        # Apps
        app_frame = tk.Frame(self.right_container)
        app_frame.pack(side=tk.TOP,
                       fill="x",
                       padx=10,
                       pady=1)

        app_label = tk.Label(app_frame, text="Apps")
        app_label.pack(side=tk.LEFT)

        bound_add_apps = partial(self.add_new_app, id)
        app_add_button = tk.Button(app_frame,
                                   text="+",
                                   command=bound_add_apps)
        app_add_button.pack(side=tk.RIGHT)

        app_box = tk.Listbox(self.right_container)
        app_box.pack(side=tk.TOP,
                     fill="x",
                     padx=10)

        db_results = self.database.get_records_by_type('A',id)
        for apps in db_results:
            seating_frame = tk.Frame(app_box)

            new_app_name = tk.Label(seating_frame, text=f"{apps[1]}")
            new_app_name.pack(side=tk.LEFT)

            bound_app_trigger = partial(self.activate_address,apps[0],id,apps[3])
            new_app_trigger = tk.Button(seating_frame, text="P", command=bound_app_trigger)
            new_app_trigger.pack(side=tk.RIGHT)

            bound_edit_app = partial(self.edit_app, id, apps[0])
            new_app_edit = tk.Button(seating_frame,
                                     text="E",
                                     command=bound_edit_app)
            new_app_edit.pack(side=tk.RIGHT)

            bound_delete_app = partial(self.delete_record, id, apps[0])
            new_app_delete = tk.Button(seating_frame,
                                       text="X",
                                       command=bound_delete_app)
            new_app_delete.pack(side=tk.RIGHT)

            seating_frame.pack(side=tk.TOP, fill="x")

        # Links
        link_frame = tk.Frame(self.right_container)
        link_frame.pack(side=tk.TOP,
                       fill="x",
                       padx=10,
                       pady=1)

        link_label = tk.Label(link_frame, text="Links")
        link_label.pack(side=tk.LEFT)

        bound_add_links = partial(self.add_new_link, id)
        link_add_button = tk.Button(link_frame, text="+", command=bound_add_links)
        link_add_button.pack(side=tk.RIGHT)

        link_box = tk.Listbox(self.right_container)
        link_box.pack(side=tk.TOP,
                     fill="x",
                     padx=10)

        db_results = self.database.get_records_by_type('L', id)
        for links in db_results:
            seating_frame = tk.Frame(link_box)

            new_link_name = tk.Label(seating_frame, text=f"{links[1]}")
            new_link_name.pack(side=tk.LEFT)

            bound_link_trigger = partial(self.activate_address, links[0], id, links[3])
            new_link_trigger = tk.Button(seating_frame,text="P",command=bound_link_trigger)
            new_link_trigger.pack(side=tk.RIGHT)

            bound_edit_link = partial(self.edit_link, id, links[0])
            new_link_edit = tk.Button(seating_frame,
                                      text="E",
                                      command = bound_edit_link)
            new_link_edit.pack(side=tk.RIGHT)

            bound_delete_link = partial(self.delete_record, id, links[0])
            new_link_delete = tk.Button(seating_frame,
                                        text="X",
                                        command=bound_delete_link)
            new_link_delete.pack(side=tk.RIGHT)

            seating_frame.pack(side=tk.TOP, fill="x")

        # Settings
        setting_frame = tk.Frame(self.right_container)
        setting_label=tk.Label(setting_frame, text="Settings")
        setting_label.pack()

        bound_trigger = partial(self.edit_group,id)
        edit_group_name = tk.Button(setting_frame,
                                    text="Edit Group Name",
                                    command = bound_trigger)
        edit_group_name.pack()

        bound_trigger = partial(self.activate_group_address, id, 'A')
        trigger_all_apps = tk.Button(setting_frame,
                                     text="Trigger all applications",
                                     command=bound_trigger)
        trigger_all_apps.pack()

        bound_trigger = partial(self.activate_group_address, id, 'L')
        trigger_all_links = tk.Button(setting_frame,
                                      text="Trigger all links",
                                      command=bound_trigger)
        trigger_all_links.pack()

        bound_trigger = partial(self.delete_group,id)
        remove_group = tk.Button(setting_frame,
                                 text="Delete this group",
                                 command=bound_trigger)
        remove_group.pack()

        setting_frame.pack()

    def new_group(self):
        create_macro = tk.Toplevel()
        create_macro.grab_set()
        create_macro.title("Add macro")
        create_macro.minsize(250, 100)
        create_macro.maxsize(450, 300)
        name_label = tk.Label(create_macro, text="Name:")
        status_label = tk.Label(create_macro, text="")
        name_entry = tk.Entry(create_macro)
        name_label.pack()
        name_entry.pack()
        status_label.pack()

        def validate_button():
            if name_entry.get() != '' and name_entry.get() != '\n' and self.database.check_group_by_name(name_entry.get()) is not True:
                self.database.add_group(name_entry.get())
                self.refresh_groups()
                create_macro.destroy()
            else:
                status_label.config(text="Name is missing or group already exist")

        finalize_button = tk.Button(create_macro, text="Finish", command=validate_button)
        finalize_button.pack()

    def refresh_records(self, group_id):
        for items in self.right_container.winfo_children():
            items.destroy()

        if group_id > -1:
            self.populate_records(group_id)
        else:
            self.macro_label.config(text="")

    def refresh_groups(self):
        for items in self.marco_group_listbox.winfo_children():
            items.destroy()
        self.populate_groups(self.marco_group_listbox)

    def add_new_app(self, group_id):
        create_macro = tk.Toplevel()
        create_macro.grab_set()
        create_macro.title("New App")
        create_macro.minsize(250, 100)
        create_macro.maxsize(450, 300)

        name_label = tk.Label(create_macro, text="Name:")
        dir_label = tk.Label(create_macro, text="program path:")
        status_label = tk.Label(create_macro, text="")

        name_entry = tk.Entry(create_macro)

        def add_app_address(entry_text):
            filename = filedialog.askopenfilename(initialdir="/",
                                                  title="Select File",
                                                  filetypes=(("executables", "*exe"), ("all files", "*")))
            app_path = os.path.basename(filename)

            if app_path != '' and app_path != "\n":
                entry_text.set(filename)

        dir_frame = tk.Frame(create_macro)
        dir_address = tk.StringVar()
        bound_app_address = partial(add_app_address,dir_address)
        dir_entry = tk.Entry(dir_frame, textvariable=dir_address)
        dir_button = tk.Button(dir_frame, text=">",command=bound_app_address)

        name_label.pack()
        name_entry.pack()

        dir_label.pack()
        dir_frame.pack()
        dir_entry.pack(side=tk.LEFT)
        dir_button.pack(side=tk.RIGHT)

        status_label.pack()

        def validate_button():
            if name_entry.get() != '' and name_entry.get() != '\n' and \
                    self.database.check_record(group_id, dir_entry.get()) is not True:
                self.database.add_record(name_entry.get(), group_id, 'A', dir_entry.get())
                self.refresh_records(group_id)
                create_macro.destroy()
            else:
                status_label.config(text="Name or path for application is missing or already exist in this macro group")

        finalize_button = tk.Button(create_macro, text="Finish", command=validate_button)
        finalize_button.pack(ipadx=5)

    def add_new_link(self, group_id):
        new_top_window = tk.Toplevel()
        new_top_window.grab_set()
        new_top_window.title("New link")
        new_top_window.minsize(250, 100)
        new_top_window.maxsize(450, 300)

        name_label = tk.Label(new_top_window, text="Name:")
        dir_label = tk.Label(new_top_window, text="url path:")
        status_label = tk.Label(new_top_window, text="")
        name_entry = tk.Entry(new_top_window)
        dir_entry = tk.Entry(new_top_window)
        name_label.pack()
        name_entry.pack()
        dir_label.pack()
        dir_entry.pack()
        status_label.pack()

        def validate_button():
            if name_entry.get() != '' and name_entry.get() != '\n' and \
                    self.database.check_record(group_id, dir_entry.get()) is not True:
                self.database.add_record(name_entry.get(), group_id, 'L', dir_entry.get())
                self.refresh_records(group_id)
                new_top_window.destroy()
            else:
                status_label.config(text="Name or path for the link is missing or already exist in this macro group")

        finalize_button = tk.Button(new_top_window, text="Finish", command=validate_button)
        finalize_button.pack(ipadx=5)

    def edit_app(self, group_id, id):
        new_top_window = tk.Toplevel()
        new_top_window.grab_set()

        db_result = self.database.get_record(id,group_id)
        name = db_result[0][1]
        address = db_result[0][4]

        new_top_window.title(f"Editing {name}")
        new_top_window.minsize(350, 200)

        entry_name = tk.StringVar()
        entry_name.set(name)

        entry_address = tk.StringVar()
        entry_address.set(address)

        name_label = tk.Label(new_top_window, text="Name:")
        name_entry = tk.Entry(new_top_window,textvariable=entry_name)

        dir_label = tk.Label(new_top_window, text="program path:")
        dir_frame = tk.Frame(new_top_window)
        dir_entry = tk.Entry(dir_frame, textvariable=entry_address)
        dir_entry.pack(side=tk.LEFT)

        def add_app_address(entry_text):
            filename = filedialog.askopenfilename(initialdir="/",
                                                  title="Select File",
                                                  filetypes=(("executables", "*exe"), ("all files", "*")))
            app_path = os.path.basename(filename)

            if app_path != '' and app_path != "\n":
                entry_text.set(filename)

        bound_app_address = partial(add_app_address,entry_address)
        dir_entry_button = tk.Button(dir_frame, text="O",command=bound_app_address)
        dir_entry_button.pack(side=tk.RIGHT)

        status_label = tk.Label(new_top_window, text="")

        name_label.pack()
        name_entry.pack()
        dir_label.pack()
        dir_frame.pack()
        status_label.pack()

        def validate_button():
            if name_entry.get() != '' and name_entry.get() != '\n' and dir_entry.get() != '' and dir_entry.get() != '\n':
                self.database.edit_record_address(id, group_id,dir_entry.get())
                self.database.edit_record_name(id, group_id,name_entry.get())
                self.refresh_groups()
                new_top_window.destroy()
            else:
                status_label.config(text="Name or address already exist or is empty")
        finalize_button = tk.Button(new_top_window, text="Finish", command=validate_button)
        finalize_button.pack(ipadx=5)

    def edit_link(self, group_id, id):
        create_macro = tk.Toplevel()
        create_macro.grab_set()
        db_result = self.database.get_record(id, group_id)
        name = db_result[0][1]
        address = db_result[0][4]
        entry_name = tk.StringVar()
        entry_name.set(name)
        entry_address = tk.StringVar()
        entry_address.set(address)
        create_macro.title(f"Editing {name}")
        create_macro.minsize(350, 200)
        name_label = tk.Label(create_macro, text="Name:")
        dir_label = tk.Label(create_macro, text="program path:")
        status_label = tk.Label(create_macro, text="")
        name_entry = tk.Entry(create_macro,
                              textvariable=entry_name)
        dir_entry = tk.Entry(create_macro,
                             textvariable=entry_address)
        name_label.pack()
        name_entry.pack()
        dir_label.pack()
        dir_entry.pack()
        status_label.pack()

        def validate_button():
            if name_entry.get() != '' and name_entry.get() != '\n' and dir_entry.get() != '' and dir_entry.get() != '\n':
                self.database.edit_record_address(id, group_id, dir_entry.get())
                self.database.edit_record_name(id, group_id, name_entry.get())
                self.refresh_groups()
                create_macro.destroy()
            else:
                status_label.config(text="Name or address already exist or is empty")
        finalize_button = tk.Button(create_macro, text="Finish", command=validate_button)
        finalize_button.pack(ipadx=5)

    def edit_group(self, group_id):
        new_top_window = tk.Toplevel()
        new_top_window.grab_set()
        name = self.database.find_group_name(group_id)[0]
        new_top_window.title(f"{name}")
        new_top_window.minsize(250, 100)
        new_top_window.maxsize(450, 300)

        name_label = tk.Label(new_top_window, text="Name:")
        name_var = tk.StringVar()
        name_var.set(name)
        name_entry = tk.Entry(new_top_window,textvariable=name_var)
        name_label.pack()
        name_entry.pack()

        status_label = tk.Label(new_top_window, text="")
        status_label.pack()

        def validate_button():
            if name_entry.get() != '' and name_entry.get() != '\n' and self.database.check_group_by_name(name_entry.get()) is not True:
                self.database.edit_group_name(group_id,name_entry.get())
                self.refresh_groups()
                new_top_window.destroy()
            else:
                status_label.config(text="Group name already exist or is empty")

        finalize_button = tk.Button(new_top_window, text="Finish", command=validate_button)
        finalize_button.pack(ipadx=5)

    def delete_record(self,group_id, id):
        self.database.delete_record(id, group_id)
        self.refresh_records(group_id)

    def activate_address(self, id, group_id, type):
        if type == 'A':
            record = self.database.get_record(id,group_id)
            os.startfile(record[0][4])
        elif type == 'L':
            record = self.database.get_record(id, group_id)
            webbrowser.open(record[0][4])
        else:
            print(f"{type} has not been implemented")

    def activate_group_address(self, group_id, type):
        if type == 'A':
            records = self.database.get_records_by_type(type,group_id)
            for app in records:
                os.startfile(app[4])
        elif type == 'L':
            records = self.database.get_records_by_type(type, group_id)
            for link in records:
                webbrowser.open(link[4])
                time.sleep(2)
        else:
            pass

    def delete_group(self, id):
        self.database.delete_group(id)
        self.refresh_groups()
        self.refresh_records(-1)


view = ViewGui()
view.minsize(550, 350)
view.mainloop()
