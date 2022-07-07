import socket
import os
import pickle
import json
import threading

HOST = "127.0.0.1"
PORT = 65432
FORMAT = "utf8"

def sendFile(conn):
    msg = "FOLDER"
    conn.sendall(msg.encode(FORMAT))
    msg = conn.recv(1024).decode(FORMAT)
    if (msg == "DONE"): return
    
    imgs = ["./imgs/thumbnail_banhmi.jpg", "./imgs/thumbnail_bo.jpg", "./imgs/thumbnail_bundau.jpg", "./imgs/thumbnail_banhdau.jpg", "./imgs/thumbnail_comcari.jpg", "./imgs/thumbnail_comga.jpg", "./imgs/thumbnail_dimsum.jpg", "./imgs/thumbnail_goicuon.jpg", "./imgs/thumbnail_mochi.jpg", "./imgs/thumbnail_saladucga.jpg", "./imgs/banhmi.jpg", "./imgs/bo.jpg", "./imgs/bundau.jpg", "./imgs/banhdau.jpg", "./imgs/comcari.jpg", "./imgs/comga.jpg", "./imgs/dimsum.jpg", "./imgs/goicuon.jpg", "./imgs/mochi.jpg", "./imgs/saladucga.jpg", "./imgs/cart.png", "./imgs/icon.ico", "./imgs/logo.png", "./imgs/thank_you.jpg", "./imgs/main_page.png"]
    n = str(len(imgs))
    conn.sendall(n.encode(FORMAT))
    for img in imgs:
        f = open(img, "rb")
        size_img = os.path.getsize(img)
        conn.sendall(str(size_img).encode(FORMAT))
        # print(size_img)
        data = f.read(size_img)
        print("sending", img, "to client")
        conn.sendall(data)
        print("finish sending", img, "to client")
        f.close()
        
        conn.recv(1024)

def deleteOrder(orderData, newOrder):
    for idx, order in enumerate(orderData):
        if (order['ID_Client'] == newOrder['ID_Client']):
            orderData.pop(idx)
           
def sendClientInfo(orderData, addr, amount_dic):
    for idx, order in enumerate(orderData):
        print(order['ID_Client'], addr)
        found = False
        if (str(order['ID_Client']) == str(addr)):
                found = True
                oldorder = order
                deleteOrder(orderData, oldorder)
                with open('orderData.json', 'w') as f:
                    json.dump(orderData, f, indent=2)
                for food in oldorder['Food_List']:
                    amount_dic[int(food['Id']) + 1] += int(food['Quantity'])
                
                break
    if (found == True):
        conn.sendall("FOUND".encode(FORMAT))
    else:
        conn.sendall("DONE".encode(FORMAT))
    amount_dic = pickle.dumps(amount_dic)
    conn.sendall(amount_dic)
    conn.recv(1024)
    
def handleClient(conn, addr):
    amount_dic = [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print("client", addr, "has joined")

    msg = conn.recv(1024).decode(FORMAT)
    conn.sendall(msg.encode(FORMAT))
    if (msg == "FOOD"):
        #send FOOD LIST
        with open('foodData.json') as f:
            data = json.load(f)
        # print(data)
        food_list = pickle.dumps(data['food'])
        conn.sendall(food_list)
    conn.recv(1024) #client finish receiving food_list
    sendFile(conn)

    with open('orderData.json') as f:
        orderData = json.load(f)
    
    addr = conn.recv(4096).decode(FORMAT)
    if (addr != "DONE"):
        sendClientInfo(orderData, addr, amount_dic)

    msg = None
    msg = conn.recv(4096)
    conn.sendall(msg)
    # conn.sendall(msg)
    finish_msg = conn.recv(4096).decode(FORMAT)
    conn.sendall(finish_msg.encode(FORMAT))
    while (finish_msg != "FINISH"):
        # newOrder = conn.recv(4096)
        # if ((msg != "FINISH") and (msg.decode(FORMAT) == "FINISH")):
            # break
        with open('orderData.json') as f:
            orderData = json.load(f)

        newOrder = msg
        newOrder = pickle.loads(newOrder)
        # before append new order, find whether this client have ordered before, if yes delete that order and append this new order
        deleteOrder(orderData, newOrder)
        
        orderData.append(newOrder)
        msg = "DONE"
        conn.sendall(msg.encode(FORMAT))
        
        with open('orderData.json', 'w') as f:
            json.dump(orderData, f, indent=2)
        
        print(orderData)
        msg = conn.recv(4096) #waiting for the next order
        conn.sendall(msg)
        finish_msg = conn.recv(4096).decode(FORMAT)
    
    conn.close()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("SERVER SIDE")

server.bind((HOST, PORT))
server.listen()

nclient = 0
while (nclient < 3):
    # try:
    conn, addr = server.accept()
    thr = threading.Thread(target=handleClient, args=(conn, addr))
    thr.daemon = True
    thr.start()

    # except:
        # print("error")
    
    nclient += 1
    
input()

