import bpy, sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import hy
import hy.lex
import hy.importer

import threading
import socket

HOST = "localhost"
PORT = 1952

def handle_incoming_code(sock):
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = sock.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        code = conn.recv(4096).decode('utf-8')
        print('Got: ' + code)
        # print('Tokenized: ' + hy.lex.tokenize(code))
        hy.importer.hy_eval(hy.lex.tokenize(code), {}, "<hy repl>")

class ToolsPanel(bpy.types.Panel):
    bl_label = "Hy Language"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
 
    def draw(self, context):
        self.layout.operator("hy.start_repl")

class OBJECT_OT_HyStartRepl(bpy.types.Operator):
    bl_idname = "hy.start_repl"
    bl_label = "Start Hy REPL"
 
    def execute(self, context):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket created')

        #Bind socket to local host and port
        try:
            self.socket.bind((HOST, PORT))
            self.socket.listen(5)
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])

        self.thread = threading.Thread(target=handle_incoming_code, args=(self.socket,))
        self.thread.start()
        print("Started REPL!")
        return{'FINISHED'}
        
class OBJECT_OT_HyStopRepl(bpy.types.Operator):
    bl_idname = "hy.stop_repl"
    bl_label = "Stop Hy REPL"
 
    def execute(self, context):
        self.socket.close()
        print("Can't really stop REPL!")
        return{'FINISHED'}

def register():
    bpy.utils.register_module(__name__)