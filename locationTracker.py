from tkinter import *
import socket
import requests


url = ""

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master
        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Location Tracker")

        # # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        #
        # # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        #
        # # create the file object)
        file = Menu(menu)
        #
        # # adds a command to the menu option, calling it exit, and the
        # # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)
        #
        # # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # Label(self, text='Enter URL').grid(row=0)
        # e1 = Entry(self)
        # e1.grid(row=0, column=1)

        e1 = self.create_entry("ID", 0)
        e2 = self.create_entry("URL", 1)

        def print_data():
            url = e2.get()
            r = requests.post(url, data={"ID": e1.get(), "IP" : self.get_ip()})
            print(r.url, r.status_code, r.reason)

        Button(self, text="Save", command=print_data).grid(row=4)

    def client_exit(self):
        exit()

    def create_entry(self, label, row):
        Label(self, text=label).grid(row=row)
        e = Entry(self)
        e.grid(row=row, column = 1)
        return e

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

root = Tk()
#size of the window
root.geometry("400x300")

app = Window(root)
root.mainloop()