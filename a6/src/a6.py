# a6.py

# Chris Cyr, Justin Lee
# cyrc@uci.edu, justisl9@uci,edu
# 12436037, 39257953

# C:\Users\Christopher Cyr\Documents\School\First Year\Winter\ICS 32\a6\Chris.dsu

# server = "168.235.86.101"
# port = "3021"

from tkinter import ttk
from copy import copy
import tkinter as tk
import ds_messenger as dsm
import ds_protocol as dsp
import tkinter.filedialog, Profile


class Body(tk.Frame):
    '''
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    '''
    def __init__(self, root, profile: dsm.NaClProfile, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.profile = profile
        self._select_callback = select_callback
        self.current_recipient = dsm.DirectMessage("", 0, "Chris")

        self._posts = [dsm.DirectMessage]
        
        self._draw()
    
    
    def node_select(self, event):
        """
        Calls the callback function specified in the select_callback class attribute, if
        available, when the add_button has been clicked.
        """
        index = int(self.posts_tree.selection()[0])
        entry = str(self._posts[index].entry)
        self.entry_display.delete(1.0, "end")
        self.entry_display.insert(1.0, entry)
        self.current_recipient = self._posts[index]


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

    
    def insert_post(self, post: dsm.DirectMessage):
        """
        Inserts a single post to the post_tree widget.
        """
        self._posts.append(post)
        id = len(self._posts) - 1 #adjust id for 0-base of treeview widget

        title = post.get_recipient()
        
        if len(title) > 25: title = title[:24] + "..."
        
        self.posts_tree.insert('', id, id, text=title)

    
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
    

    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        self.posts_frame = tk.Frame(master=self, width=250, bg='orange')
        self.posts_frame.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)
        self.posts_tree = ttk.Treeview(self.posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=0, pady=0)

        self.entry_frame = tk.Frame(master=self, bg='orange')
        self.entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.editor_frame = tk.Frame(master=self.entry_frame, bg='orange')
        self.editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        self.scroll_frame = tk.Frame(master=self.entry_frame, bg='orange', width=10)
        self.scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, padx=5, pady=5)

        self.entry_display = tk.Text(self.editor_frame, width=0, height=23)
        self.entry_display.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        self.entry_editor = tk.Text(self.editor_frame, width=0, height=4)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True, padx=5, pady=5)

        self.entry_display_scrollbar = tk.Scrollbar(master=self.scroll_frame, command=self.entry_display.yview)
        self.entry_display['yscrollcommand'] = self.entry_display_scrollbar.set
        self.entry_display_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the footer portion of the root frame.
    """
    def __init__(self, root, send_callback=None, add_user_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._add_user_callback = add_user_callback
        
        self._draw()
    
    
    def add_click(self):
        """
        Calls the callback function specified in the add_user_callback class attribute, if
        available, when the add_button has been clicked.
        """
        if self._add_user_callback is not None: self._add_user_callback(self.add_entry.get())

    
    def send_click(self):
        """
        Calls the callback function specified in the send_callback class attribute, if
        available, when the send_button has been clicked.
        """
        if self._send_callback is not None: self._send_callback()
    
    
    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        send_button = tk.Button(master=self, text="Send Post", width=20)
        send_button.configure(command=self.send_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.add_entry = tk.Entry(master=self, width=18)
        self.add_entry.pack(fill=tk.Y, side=tk.LEFT, padx=5, pady=5)

        add_button = tk.Button(master=self, text="Add User", width=10)
        add_button.configure(command=self.add_click)
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame. Also manages all method calls for
    the NaClProfile class.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        self.profile = dsm.NaClProfile()
        self._profile_filename = ""

        self._draw()

    
    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        try:
            filename = tkinter.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
            self._profile_filename = filename.name

            dsuserver = "168.235.86.101"
            username = "Chris"
            password = "password123"
            bio = ""

            self.profile.dsuserver = dsuserver
            self.profile.username = username
            self.profile.password = password
            self.profile.bio = bio
            self.profile._posts = []

            self.body.reset_ui()

            self.profile.save_profile(self._profile_filename)
        except Exception as ex:
            print("ERROR:", ex)
    
    
    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        try:
            filename = tkinter.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])
            self._profile_filename = filename.name

            self.profile = dsm.NaClProfile()
            self.profile.load_profile(self._profile_filename)

            self.body.reset_ui()
            for post in self.profile._posts:
                self.body.insert_post(post)
            
            post = self.body.current_recipient
            self.update()
            messenger = dsm.DirectMessenger(self.profile.dsuserver, self.profile.username, self.profile.password)
            messenger.token, messenger.sock = dsp.join(messenger.port, messenger.dsuserver, messenger.username, messenger.password)
            responses = messenger.retrieve_new()
            for i in responses:
                if str(i['from']) == str(post.get_recipient()):
                    post.set_entry(str(post.get_entry()) + f'\n{i["from"]}: ' + str(i['message']))
        except Exception as ex:
            print("ERROR:", ex)

    
        # try:
        #     for i in response:
        #         entry = str(i['from']) + ': ' + str(i['message']) + '\n'
        #         self.body.entry_display.insert("end", entry)
        # except:
        #     raise dsm.NoRecipientError


    def save_profile(self):
        """
        Saves the text currently in the entry_editor widget to the active DSU file.
        Also sends it to the dsuserver
        """
        try:
            post = self.body.current_recipient
            self.update()
            messenger = dsm.DirectMessenger(self.profile.dsuserver, self.profile.username, self.profile.password)
            messenger.token, messenger.sock = dsp.join(messenger.port, messenger.dsuserver, messenger.username, messenger.password)
            message = self.body.get_text_entry()
            if message == "new" or message == "all":
                if message == "new":
                    responses = messenger.retrieve_new()
                    for i in responses:
                        if str(i['from']) == str(post.get_recipient()):
                            post.set_entry(str(post.get_entry()) + f'\n{i["from"]}: ' + str(i['message']))
                elif message == "all":
                    responses = messenger.retrieve_all()
                    for i in responses:
                        for j in self.profile.get_posts():
                            if str(i['from']) == str(j.get_recipient()):
                                j.set_entry(str(j.get_entry()) + f'\n{i["from"]}: ' + str(i['message']))
            else:
                response = messenger.send(message, post.get_recipient())
                post.set_entry(str(post.get_entry()) + f'\n{self.profile.username}: ' + str(message))

                self.body.entry_display.insert('end', f'\n{self.profile.username}: ')
                self.body.entry_display.insert('end', str(message))

                if response: print('Message successfully sent.')
                else: print("ERROR: Message not sent")
            
            self.profile.save_profile(self._profile_filename)
            self.update()
            self.body.entry_editor.delete(1.0, "end")
        except Profile.DsuProfileError:
            self.body.set_text_entry("ERROR: Invalid profile!")
        except Profile.DsuFileError:
            self.body.set_text_entry("ERROR: Invalid file type!")
        except dsm.NoRecipientError:
            self.body.set_text_entry("ERROR: No recipient selected!")
        except Exception as ex:
            print("ERROR:", ex)


    def add_user(self, recipient: str):
        '''
        Adds a new post with just the recipient
        '''
        post = dsm.DirectMessage(recipient=recipient)
        self.profile.add_post(post)
        self.body.insert_post(post)
        self.profile.save_profile(self._profile_filename)
        self.footer.add_entry.delete(0, "end")


    def close(self):
        """
        Safely exits the program.
        """
        self.root.destroy()


    def cyan(self):
        '''
        Sets the GUI color to cyan
        '''
        self.color_swap('cyan')

    
    def magenta(self):
        '''
        Sets the GUI color to magenta
        '''
        self.color_swap('magenta')


    def orange(self):
        '''
        Sets the GUI color to orange
        '''
        self.color_swap('orange')


    def red(self):
        '''
        Sets the GUI color to red
        '''
        self.color_swap('red')

    def green(self):
        '''
        Sets the GUI color to green
        '''
        self.color_swap('green')


    def color_swap(self, color):
        '''
        Changes the color of the Gui
        '''
        self.body.posts_frame.configure(bg=color)
        self.body.entry_frame.configure(bg=color)
        self.body.editor_frame.configure(bg=color)
        self.body.scroll_frame.configure(bg=color)
        self.body.configure(bg=color)
        self.footer.configure(bg=color)
        self.update()
        self.body.update()
        self.footer.update()


    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        
        self.body = Body(self.root, profile=self.profile)
        self.body.configure(bg='orange')
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        self.footer = Footer(self.root, send_callback=self.save_profile, add_user_callback=self.add_user)
        self.footer.configure(bg='orange')
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        menu_color = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_color, label='Color')
        menu_color.add_command(label='Cyan', command=self.cyan)
        menu_color.add_command(label='Magenta', command=self.magenta)
        menu_color.add_command(label='Orange', command=self.orange)
        menu_color.add_command(label='Red', command=self.red)
        menu_color.add_command(label='Green', command=self.green)




if __name__ == "__main__":
    main = tk.Tk()

    main.title("ICS 32 Direct Messenger by Chris Cyr and Justin Lee")

    main.geometry("1280x720")
    main.option_add('*tearOff', False)

    MainApp(main)

    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.mainloop()