from tkinter import *
import socket
import requests
import time
import datasaver
import _thread
from tkinter import messagebox
import ip_to_location_finder


labels = [
    'id',
    'Pc Name',
    'Interval',
    'API URL',
]
entries = []



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

        def save_data():
            data = [e[0].get() for e in entries]
            datasaver.saveData(data)
            messagebox.showinfo('Success', 'Installation Successful')
            save_btn.grid_forget()
            self.start()

            # r = requests.post(url, data={"ID": e1.get(), "IP" : self.get_ip()})
            # print(r.url, r.status_code, r.reason)
        #
        save_btn = Button(self, text="Start", command=save_data)
        save_btn.grid(row=len(labels)+1, column=2)

        data = datasaver.getData()
        if len(data) < len(labels):
            self.installation()
        else:
            self.hide_setup_fields()
            save_btn.grid_forget()
            self.start()


        #
        data = datasaver.getData()
        if len(data) == len(labels):
            self.hide_setup_fields()

    def client_exit(self):
        exit()

    def create_entry(self, label, row):
        l = Label(self, text=label)
        l.grid(row=row)
        e = Entry(self)
        e.grid(row=row, column = 1)
        return e, l

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

    def hide_setup_fields(self):
        for e in entries:
            e[0].grid_forget()
            e[1].grid_forget()

    def installation(self):
        # data = datasaver.getData()
        for index, e in enumerate(labels):
            entries.append(self.create_entry(e, index))

        # for index, e in enumerate(data):
        #     entries[index][0].insert(0, e)
        # since first entry is pc name, we get the pc name and put it in that entry
        entries[len(labels)-3][0].insert(0, socket.gethostname())

    def start(self):
        self.hide_setup_fields()
        data = datasaver.getData()
        interval = int(float(data[len(labels)-2])*60)
        _thread.start_new_thread(self.send_data_to_server, (interval,))

    def send_data_to_server(self, interval):
        self.show_ip_hostname(self.get_ip(), socket.gethostname())
        data = datasaver.getData()
        url = data[-1]
        while True:
            try:
                requests.post(url, data={
                    "id": data[0],
                    "hostname": data[1],
                    "loc": self.get_lat_long(),
                })
            except Exception as e:
                print("There was an error sending the data to server ", e)
            time.sleep(interval)

    def show_ip_hostname(self, ip, host_name):
        w = Label(self, text='IP: {}'.format(ip))
        w.pack()
        w = Label(self, text='Host Name: {}'.format(host_name))
        w.pack()

    def get_lat_long(self):
        r = requests.get(url='http://ipinfo.io/json')
        data = r.json()
        return data['loc']


root = Tk()
#size of the window
root.geometry("400x300")

app = Window(root)
root.mainloop()