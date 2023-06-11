# Imports
import customtkinter as ctk
import requests
import threading
import time
from customtkinter import CTkFont

# Variables
server_connection_interval = 5  
nodemcu_connected = False
server_connected = False
 
# Functions
# GUI -> Server
def gui_startup_request(): 
    url = "http://192.168.100.4:5000/gui-startup"
    try:
        response = requests.post(url)
        if response.status_code != 200:
            print("Failed to send startup request")
        
        print("Request for server connection sent by client")
        server_to_gui_state(response.text)
    except requests.ConnectionError:
        print("Server status: Down || Refused.")

# Server <- GUI
def server_to_gui_state(server_response):
    global server_connected
    print("Server response:", server_response)
    if server_response == "GUI started!":
        server_connected = True
        gui_connection_checkbox.select()
    
# GUI (3) -> Server (2) <- NodeMCU (1)
def nodemcu_startup_request(): 
    url = "http://192.168.100.4:5000/nodemcu-server-gui"
    try:
        response = requests.post(url)
        if response.status_code != 200:
            print("Failed to send startup request")
        
        print("Request for NodeMCU connection sent by client")
        nodemcu_to_gui_state(response.text)
    except requests.ConnectionError:
        print("NodeMCU status: Down || Refused.")

# GUI (3) <- Server (2) <- NodeMCU (1)
def nodemcu_to_gui_state(server_response):
    global nodemcu_connected
    print("Server response:", server_response)
    if server_response == "NodeMCU connected!":
        nodemcu_connected = True
        node_connection_checkbox.select()

# Server connection checker 
def check_server_connection():
    url = "http://192.168.100.4:5000/server-connection-state-check"
    while True:
        try:
            response = requests.post(url)
            if response.status_code != 200:
                print("Failed to send startup request")
            
            server_state = server_state_checker(response.text)

            if server_state == "Both connected!":
                gui_connection_checkbox.select()
                node_connection_checkbox.select()
            elif server_state == "Only NodeMCU connected":
                gui_connection_checkbox.deselect()
                node_connection_checkbox.select()

        except requests.ConnectionError:
            gui_connection_checkbox.deselect()
            node_connection_checkbox.deselect()
            print("Server status: Down || Refused.")
        time.sleep(server_connection_interval)

def server_state_checker(server_response):
    gui_startup_request()
    nodemcu_startup_request()
    print("Server and NodeMCU connection:", server_response)
    if server_response != "Both connected!":
        return "Either the server or the NodeMCU is down."
    
    return "Both connected!"
     
# Open door requests
def open_door():
    url = "http://192.168.100.44/open-door"
    try:
        response = requests.post(url)
        if response.status_code != 200:
            print("Failed to send startup request")
        else:
            handle_open_door_request(response.text)
            print("Request for open door sent by client")
    except requests.ConnectionError:
        print("Server status: Down || Refused.")

def handle_open_door_request(server_response):
    print("Server response:", server_response)
    if server_response == "Open door request sent!":
        open_button.configure(state="disabled")
        time.sleep(2)
        open_button.configure(state="normal")

# Main window stuff
main_window = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
main_window.title("Door-Lock")

screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
window_width = 240
window_height = 190
x = screen_width - window_width - 20
y = screen_height - window_height - 40
main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
main_window.resizable(False, False)

# Widget stuff
main_frame = ctk.CTkFrame(master=main_window)
main_frame.pack(padx=20, pady=15, fill="both", expand=True)
checkbox_font = ctk.CTkFont(family="Arial", size=10, weight="normal")
node_connection_checkbox = ctk.CTkCheckBox(master=main_frame, state="disabled", text="ESP8266", font=checkbox_font)
node_connection_checkbox.pack(padx=10, pady=10)
gui_connection_checkbox = ctk.CTkCheckBox(master=main_frame, state="disabled", text="Flask Server", font=checkbox_font)
gui_connection_checkbox.pack(padx=10, pady=10)
button_font = ctk.CTkFont(family="Arial", size=12, weight="bold")
open_button = ctk.CTkButton(master=main_frame, text="Open door", font=button_font, command=open_door)
open_button.pack(padx=15, pady=15)

# Main window loop
if __name__ == '__main__':
    threading.Thread(target=check_server_connection, daemon=True).start()
    main_window.mainloop()
