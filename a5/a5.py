# a5.py

# Chris Cyr, Justin Lee
# cyrc@uci.edu, justisl9@uci,edu
# 12436037, 39257953

# C:\Users\Christopher Cyr\Documents\School\First Year\Winter\ICS 32\a5\Chris.dsu

# server = "168.235.86.101"
# port = "3021"


import tkinter as tk
import ds_client as dsc
from tkinter import ttk, filedialog
from Profile import *
from NaClProfile import NaClProfile
from pathlib import Path
import nacl


class Body(tk.Frame):
    '''
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    '''
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._posts = [Post]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    
    def node_select(self, event):
        """
        Update the entry_editor with the full post entry when the corresponding node in the posts_tree
        is selected.
        """
        try:
            index = int(self.posts_tree.selection()[0])
            entry = self._posts[index].entry
            self.set_text_entry(entry)
        except Exception as ex:
            print(ex)
    
    
    def get_text_entry(self) -> str:
        """
        Returns the text that is currently displayed in the entry_editor widget.
        """
        return self.entry_editor.get(1.0, 'end').rstrip()

    
    def set_text_entry(self, text:str):
        """
        Sets the text to be displayed in the entry_editor widget.
        NOTE: This method is useful for clearing the widget, just pass an empty string.
        """
        self.entry_editor.delete(1.0, "end")
        self.entry_editor.insert(1.0, text)
    
    
    def set_posts(self, posts:list):
        """
        Populates the self._posts attribute with posts from the active DSU file.
        """
        newposts = []
        for i in posts: 
            newposts.append(i)
        for i in newposts: 
            self.insert_post(i)
            

    
    def insert_post(self, post: Post):
        """
        Inserts a single post to the post_tree widget.
        """
        self._posts.append(post)
        id = len(self._posts) - 1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, post)


    
    def reset_ui(self):
        """
        Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DSU file is loaded, for example.
        """
        self.set_text_entry("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    
    def _insert_post_tree(self, id, post: Post):
        """
        Inserts a post entry into the posts_tree widget.
        """
        entry = post.entry
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."
        
        self.posts_tree.insert('', id, id, text=entry)
    
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, save_callback=None, online_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using he get() function:
        # chk_value = self.is_online.get()
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    
    def online_click(self):
        """
        Calls the callback function specified in the online_callback class attribute, if
        available, when the chk_button widget has been clicked.
        """
        if self._online_callback is not None:
            self._online_callback(self.is_online.get())


    
    def save_click(self):
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._save_callback is not None:
            self._save_callback()

    
    def set_status(self, message):
        """
        Updates the text that is displayed in the footer_label widget
        """
        self.footer_label.configure(text=message)
    
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        save_button = tk.Button(master=self, text="Save Post", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        self.chk_button.configure(command=self.online_click)
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the NaClProfile class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = NaClProfile()
        self._is_online = False
        self._profile_filename = None

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    
    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name

        dsuserver = "168.235.86.101"
        username = "Chris"
        password = "password123"
        bio = ""

        self._current_profile.dsuserver = dsuserver
        self._current_profile.username = username
        self._current_profile.password = password
        self._current_profile.bio = bio
        self._current_profile._posts = []
        self._current_profile.generate_keypair()

        self.body.reset_ui()

        self._current_profile.save_profile(self._profile_filename)
    
    
    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        try:
            self._profile_filename = filename.name
            self._current_profile = NaClProfile()
            self._current_profile.load_profile(self._profile_filename)
            self._current_profile.import_keypair(self._current_profile.keypair)
            self.body.reset_ui()
            self.body.set_posts(self._current_profile.get_posts())
        except AttributeError:
            self.body.set_text_entry("Nothing happened.")

    
    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked.
        """
        self.root.destroy()

    
    def save_profile(self):
        """
        Saves the text currently in the entry_editor widget to the active DSU file.
        """
        try:
            post = Post(self.body.get_text_entry())
            self.body.insert_post(post)
            self._current_profile.add_post(post)
            self._current_profile.save_profile(self._profile_filename)
            if self._is_online is True:
                self.update()
                self.publish(post)
            self.body.set_text_entry("")
        except DsuProfileError:
            self.body.set_text_entry("ERROR: Invalid profile")
        except DsuFileError:
            self.body.set_text_entry("ERROR: Invalid file type!")
        except nacl.exceptions.TypeError:
            self.body.set_text_entry("ERROR: No profile open!")

        
    def publish(self, post: Post):
        # try:
        dsc.send(self._current_profile, post, 3021)
        self.footer.set_status("Successfully sent to server!")
        print("Successfully sent to server!")
        # except Exception as ex:
        #     self.footer.set_status(ex)
        #     print("ERROR:", ex)
    

    def online_changed(self, value:bool):
        """
        A callback function for responding to changes to the online chk_button.
        """
        if value:
            self.footer.set_status("Online")
            self._is_online = True
        else:
            self.footer.set_status("Offline")
            self._is_online = False
    
    
    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback=self.online_changed)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo by Chris Cyr and Justin Lee")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program.
    main.mainloop()