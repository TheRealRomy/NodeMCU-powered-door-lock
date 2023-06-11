from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

gui_started = False
nodemcu_connected = False

@app.route('/gui-startup', methods=['POST'])
def handle_gui_startup():
    global gui_started
    gui_started = True
    return "GUI started!"

@app.route('/nodemcu-startup', methods=['POST'])
def handle_nodemcu_startup():
    global nodemcu_connected 
    nodemcu_connected = True
    return "NodeMCU connected!"

@app.route('/nodemcu-server-gui', methods=['POST'])
def handle_node_to_gui():
    if nodemcu_connected != True:
        return "Not connected."
    else:
        return "NodeMCU still connected!"
    
@app.route('/server-connection-state-check', methods=['POST'])
def handle_server_connection_state():
    global gui_started
    global nodemcu_connected
    if nodemcu_connected == True and gui_started == True:
        return "Both connected!"
    elif nodemcu_connected == True and gui_started == False:
        return "Only NodeMCU connected."
    else:
        return "Server and NodeMCU is down."

if __name__ == '__main__':
    app.run(host='192.168.100.4', port=5000)
