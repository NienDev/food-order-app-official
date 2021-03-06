import requests
import socket
import os
import time
import json
import pickle
from io import BytesIO
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import tkinter.font as font

HOST = "127.0.0.1"
PORT = 65432
FORMAT = "utf8"
 
    
    
def download_food_image(Food_Info):
    #create folder
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'food_imgs')
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)
       
       for idx, info in enumerate(Food_Info):
       
        # print(pic_url)
        with open('./food_imgs/pic' + str(idx) + '.jpg', 'wb') as handle:
            response = requests.get(info['url'], stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)       

def createFolder():
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'Assets')
   
    
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    
    time_to_wait = 10
    time_counter = 0
    while not os.path.exists(final_directory):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:break

    print("finish creating folder named: ASSETS")

def recvAssetsFromServer(client):
    msg = client.recv(1024).decode(FORMAT)
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'Assets')
    if os.path.exists(final_directory):
        msg = "DONE"
        client.sendall(msg.encode(FORMAT))
        return
        
    if (msg == "FOLDER"):
        createFolder()
        client.sendall(msg.encode(FORMAT))
        
    
    tmp = client.recv(1024).decode(FORMAT)
    for i in range(int(tmp)):
        size_img = int(client.recv(8).decode(FORMAT))
        # print(size_img)
        img_name = "./Assets/img" + str(i) + ".jpg" 
        f = open(img_name, "wb")
        print(img_name, "is downloading")
        data = client.recv(size_img)
        print(img_name, "downloaded successfully")
        f.write(data)
        f.close()
        
        msg = "done"
        msg = client.sendall(msg.encode(FORMAT))

def     show_menu(logo, btn, client, img_labels):
        global root
        global Food_Info
        global amount_dic
        global totalmoney
        global IS_VALID
        
        def checkID():
            def checkIDValid(ee):
                number1 = str(ee.get())
                if (number1 == ""):
                        credit_window.destroy()  
                        number1 = "DONE"
                        client.sendall(number1.encode(FORMAT))
                        return
                        
                client.sendall(number1.encode(FORMAT))
                found = client.recv(1024).decode(FORMAT)
                #check whether client has ordered or not
                global amount_dic
                amount_dic = client.recv(4096)
                amount_dic = pickle.loads(amount_dic)
                print(amount_dic)
                client.sendall("DONE".encode(FORMAT))
                if (found == "FOUND"):
                    show_receipt()
                ee.delete(0, END)
                credit_window.destroy()  
                
            credit_window =  Toplevel(root)
            credit_window.title = "ORDER ID"
            credit_window.config(bg="#CEE5D0")  
            f = font.Font(family="Cooper Black", size=16)
            label = Label(credit_window, text="Your Order ID\nYou can leave it blank if you have not order anything", bg="#CEE5D0")
            label['font']=f
            ee = Entry(credit_window, justify=CENTER, width=25)
            label.pack()
            ee.pack()
            credit_btn = Button(credit_window, text="Confirm", command=lambda: checkIDValid(ee), relief="flat",fg="white",bg="#94B49F")
            credit_btn['font']=f
            credit_btn.pack()
        #turn off the show_welcome window
        
        logo.forget()
        btn.forget()
    
        checkID()
        
        frame = LabelFrame(root)
        frame.pack(padx=20,pady=20,fill=BOTH,expand=1)
        #show menu
            #create main frame
        main_frame =Frame(frame)
        main_frame.pack(fill=BOTH, expand=1)
            #create  a canvas
            
        # global my_canvas
        my_canvas = Canvas(main_frame)
        my_canvas.configure(bg='#CEE5D0')
        
        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1*(event.delta//120)), "units")
        
        def _bound_to_mousewheel(event):
            my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbound_to_mousewheel(event):
            my_canvas.unbind_all("<MouseWheel>")
        
        my_canvas.bind('<Enter>', _bound_to_mousewheel)
        my_canvas.bind('<Leave>', _unbound_to_mousewheel)

        
        # def _on_mousewheel(event):
            # my_canvas.yview_scroll(-1*(event.delta//120), "units") 
        
        # my_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
            
            #add a scrollbar to canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        
            #configure the canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))   
            
            #create another frame in canvas
        second_frame = Frame(my_canvas)
        second_frame.configure(bg='#CEE5D0')
        
            #add that new frame to a window in the canvas
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        
        
        frame1 = LabelFrame(second_frame)
        frame1.grid(row=0, column=0, padx=10, pady=10)
        frame2 = LabelFrame(second_frame)
        frame2.grid(row=0, column=1, padx=10, pady=10)
        frame3 = LabelFrame(second_frame)
        frame3.grid(row=1, column=0, padx=10, pady=10)
        frame4 = LabelFrame(second_frame)
        frame4.grid(row=1, column=1, padx=10, pady=10)
        frame5 = LabelFrame(second_frame)
        frame5.grid(row=2, column=0, padx=10, pady=10)
        frame6 = LabelFrame(second_frame)
        frame6.grid(row=2, column=1, padx=10, pady=10)
        frame7 = LabelFrame(second_frame)
        frame7.grid(row=3, column=0, padx=10, pady=10)
        frame8 = LabelFrame(second_frame)
        frame8.grid(row=3, column=1, padx=10, pady=10)
        frame9 = LabelFrame(second_frame)
        frame9.grid(row=4, column=0, padx=10, pady=10)
        frame10 = LabelFrame(second_frame)
        frame10.grid(row=4, column=1, padx=10, pady=10)
        def show_receipt():
            global totalmoney
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            app_width = 600
            app_height = 600
            x = (screen_width - app_width)/2   
            y = (screen_height - app_height)/2
            
            pop = Toplevel(root)
            pop.title = "Receipt"
            pop.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
            pop.config( bg="#94B49F")
            
            f = font.Font(family="Cooper Black", size=20)
            main_label = Label(pop, text="Your Bill",  bg="#94B49F", fg="white")
            main_label['font']=f
            main_label.pack()
            
            food_frame = Frame(pop, bg="#CEE5D0")
            food_frame.pack(fill=BOTH,expand=1)
            
            #show menu
                #create main frame
            main_frame =Frame(food_frame)
            main_frame.pack(fill=BOTH, expand=1)
                #create  a canvas
            my_canvas = Canvas(main_frame)
            my_canvas.config(bg="#CEE5D0")
            def _on_mousewheel(event):
                my_canvas.yview_scroll(int(-1*(event.delta//120)), "units")
            
            def _bound_to_mousewheel(event):
                my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

            def _unbound_to_mousewheel(event):
                my_canvas.unbind_all("<MouseWheel>")
            
            my_canvas.bind('<Enter>', _bound_to_mousewheel)
            my_canvas.bind('<Leave>', _unbound_to_mousewheel)
            
            my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
                
                #add a scrollbar to canvas
            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=RIGHT, fill=Y)
            
                #configure the canvas
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))   
                
                #create another frame in canvas
            second_frame = Frame(my_canvas, bg="#CEE5D0")
                
                #add that new frame to a window in the canvas
            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
                
            # food 1 
            def remove_order1():
                totalmoney[0] -= amount_dic[1] * int(Food_Info[0]['price'])
                amount_dic[1] = 0
                print(amount_dic)
                food_thumbnail_label1.grid_remove()
                text_label.grid_remove()
                amount_label.grid_remove()
                undo_btn.grid_remove()
                order_frame1.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[1] != 0):
                order_frame1 = LabelFrame(second_frame)
                order_frame1.pack(padx=20, pady=20)
                
                food_thumbnail1 = Image.open("./Assets/img0.jpg")
                food_thumbnail1 = ImageTk.PhotoImage(food_thumbnail1)
                food_thumbnail_label1 = Label(order_frame1, image=food_thumbnail1)
                food_thumbnail_label1.image = food_thumbnail1
                food_thumbnail_label1['image']=food_thumbnail1
                food_thumbnail_label1.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label = Label(order_frame1, text=Food_Info[0]['name'], justify=LEFT, font='Roboto 16 bold')
                text_label['font']=f
                text_label.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                amount_label = Label(order_frame1, text="Amount: " +  str(amount_dic[1]) + "\nPrice: $" + Food_Info[0]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label['font']=f
                amount_label.grid(row=1, column=1, pady=20,sticky="nw")
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn = Button(order_frame1, text="UNDO", command=remove_order1, relief="flat", bg="#ECB390")
                undo_btn['font'] = f
                undo_btn.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
                
            #food 2
            def remove_order2():
                totalmoney[0] -= amount_dic[2] * int(Food_Info[1]['price'])
                amount_dic[2] = 0
                print(amount_dic)
                food_thumbnail_label2.grid_remove()
                text_label2.grid_remove()
                amount_label2.grid_remove()
                undo_btn2.grid_remove()
                order_frame2.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[2] != 0):
                order_frame2 = LabelFrame(second_frame)
                order_frame2.pack(padx=20, pady=20)
                
                food_thumbnail2 = Image.open("./Assets/img1.jpg")
                food_thumbnail2 = ImageTk.PhotoImage(food_thumbnail2)
                food_thumbnail_label2 = Label(order_frame2, image=food_thumbnail2)
                food_thumbnail_label2.image = food_thumbnail2
                food_thumbnail_label2['image']=food_thumbnail2
                food_thumbnail_label2.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label2 = Label(order_frame2, text=Food_Info[1]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label2['font']=f
                text_label2.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label2 = Label(order_frame2, text="Amount: " +  str(amount_dic[2]) + "\nPrice: $" + Food_Info[1]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label2['font']=f
                amount_label2.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn2 = Button(order_frame2, text="UNDO", command=remove_order2, relief="flat", bg="#ECB390")
                undo_btn2['font']=f
                undo_btn2.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            #food 3
            def remove_order3():
                totalmoney[0] -= amount_dic[3] * int(Food_Info[2]['price'])
                amount_dic[3] = 0
                print(amount_dic)
                food_thumbnail_label3.grid_remove()
                text_label3.grid_remove()
                amount_label3.grid_remove()
                undo_btn3.grid_remove()
                order_frame3.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[3] != 0):
                order_frame3 = LabelFrame(second_frame)
                order_frame3.pack(padx=20, pady=20)
                
                food_thumbnail3 = Image.open("./Assets/img2.jpg")
                food_thumbnail3 = ImageTk.PhotoImage(food_thumbnail3)
                food_thumbnail_label3 = Label(order_frame3, image=food_thumbnail3)
                food_thumbnail_label3.image = food_thumbnail3
                food_thumbnail_label3['image']=food_thumbnail3
                food_thumbnail_label3.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label3 = Label(order_frame3, text=Food_Info[2]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label3['font']=f
                text_label3.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label3 = Label(order_frame3, text="Amount: " +  str(amount_dic[3]) + "\nPrice: $" + Food_Info[2]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label3['font']=f
                amount_label3.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn3 = Button(order_frame3, text="UNDO", command=remove_order3, relief="flat", bg="#ECB390")
                undo_btn3['font']=f
                undo_btn3.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            #food 4
            def remove_order4():
                totalmoney[0] -= amount_dic[4] * int(Food_Info[3]['price'])
                amount_dic[4] = 0
                print(amount_dic)
                food_thumbnail_label4.grid_remove()
                text_label4.grid_remove()
                amount_label4.grid_remove()
                undo_btn4.grid_remove()
                order_frame4.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[4] != 0):
                order_frame4 = LabelFrame(second_frame)
                order_frame4.pack(padx=20, pady=20)
                
                food_thumbnail4 = Image.open("./Assets/img3.jpg")
                food_thumbnail4 = ImageTk.PhotoImage(food_thumbnail4)
                food_thumbnail_label4 = Label(order_frame4, image=food_thumbnail4)
                food_thumbnail_label4.image = food_thumbnail4
                food_thumbnail_label4['image']=food_thumbnail4
                food_thumbnail_label4.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label4 = Label(order_frame4, text=Food_Info[3]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label4['font']=f
                text_label4.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label4 = Label(order_frame4, text="Amount: " +  str(amount_dic[4]) + "\nPrice: $" + Food_Info[3]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label4['font']=f
                amount_label4.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn4 = Button(order_frame4, text="UNDO", command=remove_order4, relief="flat", bg="#ECB390")
                undo_btn4['font']=f
                undo_btn4.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            #food 5
            def remove_order5():
                totalmoney[0] -= amount_dic[5] * int(Food_Info[4]['price'])
                amount_dic[5] = 0
                print(amount_dic)
                food_thumbnail_label5.grid_remove()
                text_label5.grid_remove()
                amount_label5.grid_remove()
                undo_btn5.grid_remove()
                order_frame5.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[5] != 0):
                order_frame5 = LabelFrame(second_frame)
                order_frame5.pack(padx=20, pady=20)
                
                food_thumbnail5 = Image.open("./Assets/img4.jpg")
                food_thumbnail5 = ImageTk.PhotoImage(food_thumbnail5)
                food_thumbnail_label5 = Label(order_frame5, image=food_thumbnail5)
                food_thumbnail_label5.image = food_thumbnail5
                food_thumbnail_label5['image']=food_thumbnail5
                food_thumbnail_label5.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label5 = Label(order_frame5, text=Food_Info[4]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label5['font']=f
                text_label5.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label5 = Label(order_frame5, text="Amount: " +  str(amount_dic[5]) + "\nPrice: $" + Food_Info[4]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label5['font']=f
                amount_label5.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn5 = Button(order_frame5, text="UNDO", command=remove_order5,relief="flat", bg="#ECB390")
                undo_btn5['font']=f
                undo_btn5.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            #food 6
            def remove_order6():
                totalmoney[0] -= amount_dic[6] * int(Food_Info[5]['price'])
                amount_dic[6] = 0
                print(amount_dic)
                food_thumbnail_label6.grid_remove()
                text_label6.grid_remove()
                amount_label6.grid_remove()
                undo_btn6.grid_remove()
                order_frame6.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[6] != 0):
                order_frame6 = LabelFrame(second_frame)
                order_frame6.pack(padx=20, pady=20)
                
                food_thumbnail6 = Image.open("./Assets/img5.jpg")
                food_thumbnail6 = ImageTk.PhotoImage(food_thumbnail6)
                food_thumbnail_label6 = Label(order_frame6, image=food_thumbnail6)
                food_thumbnail_label6.image = food_thumbnail6
                food_thumbnail_label6['image']=food_thumbnail6
                food_thumbnail_label6.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label6 = Label(order_frame6, text=Food_Info[5]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label6['font']=f
                text_label6.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label6 = Label(order_frame6, text="Amount: " +  str(amount_dic[6]) + "\nPrice: $" + Food_Info[5]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label6['font']=f
                amount_label6.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn6 = Button(order_frame6, text="UNDO", command=remove_order6,relief="flat", bg="#ECB390")
                undo_btn6['font']=f
                undo_btn6.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            #food 7
            def remove_order7():
                totalmoney[0] -= amount_dic[7] * int(Food_Info[6]['price'])
                amount_dic[7] = 0
                print(amount_dic)
                food_thumbnail_label7.grid_remove()
                text_label7.grid_remove()
                amount_label7.grid_remove()
                undo_btn7.grid_remove()
                order_frame7.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[7] != 0):
                order_frame7 = LabelFrame(second_frame)
                order_frame7.pack(padx=20, pady=20)
                
                food_thumbnail7 = Image.open("./Assets/img6.jpg")
                food_thumbnail7 = ImageTk.PhotoImage(food_thumbnail7)
                food_thumbnail_label7 = Label(order_frame7, image=food_thumbnail7)
                food_thumbnail_label7.image = food_thumbnail7
                food_thumbnail_label7['image']=food_thumbnail7
                food_thumbnail_label7.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label7 = Label(order_frame7, text=Food_Info[6]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label7['font']=f
                text_label7.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label7 = Label(order_frame7, text="Amount: " +  str(amount_dic[7]) + "\nPrice: $" + Food_Info[6]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label7['font']=f
                amount_label7.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn7 = Button(order_frame7, text="UNDO", command=remove_order7, relief="flat", bg="#ECB390")
                undo_btn7['font']=f
                undo_btn7.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            
            #food 8
            def remove_order8():
                totalmoney[0] -= amount_dic[8] * int(Food_Info[7]['price'])
                amount_dic[8] = 0
                print(amount_dic)
                food_thumbnail_label8.grid_remove()
                text_label8.grid_remove()
                amount_label8.grid_remove()
                undo_btn8.grid_remove()
                order_frame8.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[8] != 0):
                order_frame8 = LabelFrame(second_frame)
                order_frame8.pack(padx=20, pady=20)
                
                food_thumbnail8 = Image.open("./Assets/img7.jpg")
                food_thumbnail8 = ImageTk.PhotoImage(food_thumbnail8)
                food_thumbnail_label8 = Label(order_frame8, image=food_thumbnail8)
                food_thumbnail_label8.image = food_thumbnail8
                food_thumbnail_label8['image']=food_thumbnail8
                food_thumbnail_label8.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label8 = Label(order_frame8, text=Food_Info[7]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label8['font']=f
                text_label8.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label8 = Label(order_frame8, text="Amount: " +  str(amount_dic[8]) + "\nPrice: $" + Food_Info[7]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label8['font']=f
                amount_label8.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn8 = Button(order_frame8, text="UNDO", command=remove_order8,  relief="flat", bg="#ECB390")
                undo_btn8['font']=f
                undo_btn8.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            
            #food 9
            def remove_order9():
                totalmoney[0] -= amount_dic[9] * int(Food_Info[8]['price'])
                amount_dic[9] = 0
                print(amount_dic)
                food_thumbnail_label9.grid_remove()
                text_label9.grid_remove()
                amount_label9.grid_remove()
                undo_btn9.grid_remove()
                order_frame9.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[9] != 0):
                order_frame9 = LabelFrame(second_frame)
                order_frame9.pack(padx=20, pady=20)
                
                food_thumbnail9 = Image.open("./Assets/img8.jpg")
                food_thumbnail9 = ImageTk.PhotoImage(food_thumbnail9)
                food_thumbnail_label9 = Label(order_frame9, image=food_thumbnail9)
                food_thumbnail_label9.image = food_thumbnail9
                food_thumbnail_label9['image']=food_thumbnail9
                food_thumbnail_label9.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label9 = Label(order_frame9, text=Food_Info[8]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label9['font']=f
                text_label9.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label9 = Label(order_frame9, text="Amount: " +  str(amount_dic[9]) + "\nPrice: $" + Food_Info[8]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label9['font']=f
                amount_label9.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn9 = Button(order_frame9, text="UNDO", command=remove_order9,relief="flat", bg="#ECB390")
                undo_btn9['font']=f
                undo_btn9.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            #food 10
            def remove_order10():
                totalmoney[0] -= amount_dic[10] * int(Food_Info[9]['price'])
                amount_dic[10] = 0
                print(amount_dic)
                food_thumbnail_label10.grid_remove()
                text_label10.grid_remove()
                amount_label10.grid_remove()
                undo_btn10.grid_remove()
                order_frame10.forget()
                
                totalmoney_label.config(text="Total Money: $" + str(totalmoney[0]))
                totalmoney_label.pack()
            
            if (amount_dic[10] != 0):
                order_frame10 = LabelFrame(second_frame)
                order_frame10.pack(padx=20, pady=20)
                
                food_thumbnail10 = Image.open("./Assets/img9.jpg")
                food_thumbnail10 = ImageTk.PhotoImage(food_thumbnail10)
                food_thumbnail_label10 = Label(order_frame10, image=food_thumbnail10)
                food_thumbnail_label10.image = food_thumbnail10
                food_thumbnail_label10['image']=food_thumbnail10
                food_thumbnail_label10.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
                
                text_label10 = Label(order_frame10, text=Food_Info[9]['name'], justify=LEFT, font='Roboto 16 bold')
                f = font.Font(family="Bahnschrift SemiLight", size=18)
                text_label10['font']=f
                text_label10.grid(row=0, column=1, columnspan=2, pady=20, sticky="sw")
                
                amount_label10 = Label(order_frame10, text="Amount: " +  str(amount_dic[10]) + "\nPrice: $" + Food_Info[9]['price'], justify=LEFT)
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                amount_label10['font']=f
                amount_label10.grid(row=1, column=1, pady=20,sticky="nw")
                
                f = font.Font(family="Arial Rounded MT Bold", size=14)
                undo_btn10 = Button(order_frame10, text="UNDO", command=remove_order10, relief="flat", bg="#ECB390")
                undo_btn10['font']=f
                undo_btn10.grid(row=0, column=3, rowspan=2,sticky="ne", padx=(20,0))
            
            #total money section
            totalmoney[0] = 0
            print(amount_dic)
            for i in range(10):
                totalmoney[0] += amount_dic[i+1] * int(Food_Info[i]['price'])
            
            f = font.Font(family="Cooper Black", size=14)
            totalmoney_label = Label(pop, text="Total Money: $" + str(totalmoney[0]), bg="#94B49F", fg="white")
            totalmoney_label['font']=f
            totalmoney_label.pack(side=LEFT, fill = BOTH, expand = True)
            
            def update_data_to_server():
                # amount_dic: the amount of food i
                # Food_Info: 
               
                #send object to server
                
                id_client = client.getsockname()[1]
                detail_order = []
                total = 0
                for i in range(10):
                    if (amount_dic[i+1] == 0): continue
                    order = {
                        "Id": i,
                        "Food_name": Food_Info[i]['name'],
                        "Quantity": amount_dic[i+1],
                        "Price": Food_Info[i]['price'],  
                        "Total": amount_dic[i+1] * int(Food_Info[i]['price'])
                    }
                    total += amount_dic[i+1] * int(Food_Info[i]['price']) 
                    detail_order.append(order)
                
                order = {
                    "ID_Client": id_client,
                    "Food_List": detail_order,
                    "Total": total
                }
                
                order = pickle.dumps(order)
                client.sendall(order)
                client.recv(4096)
                client.sendall("Still waiting".encode(FORMAT))
                client.recv(4096)
                #fixing
                client.recv(4096)
                
            # def show_client_id():
                # thanks_window = Toplevel(root)
                # thanks_window.title = "ORDER ID"
                # thanks_window.config(bg="#94B49F")
                # f = font.Font(family="Cooper Black", size=16)
                # label = Label(thanks_window, text="Your order ID: " + str(client.getsockname()[1]),bg="#94B49F", fg="#fff")
                # label['font']=f
                # label.pack(padx=20,pady=10);
                
            def show_thank_window():
                # show_client_id()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                app_width = 400
                app_height = 400
                x = (screen_width - app_width)/2   
                y = (screen_height - app_height)/2
                
                thanks_window = Toplevel(root)
                thanks_window.title = "Finish ordering"
                thanks_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
                thanks_window.config(bg="#94B49F")
                
                img = Image.open("./Assets/img23.jpg")
                img.thumbnail((400,400))
                img.save("./Assets/thankyou.jpg")
                img = Image.open("./Assets/thankyou.jpg")
                img = ImageTk.PhotoImage(img)

                f = font.Font(family="Cooper Black", size=16)
                label = Label(thanks_window, text="Your order ID: " + str(client.getsockname()[1]),bg="#94B49F", fg="#fff")
                label['font']=f
                label.pack(padx=20,pady=10);
                label_img = Label(thanks_window)
                label_img.image = img
                label_img['image']=img
                label_img.pack()
                
                # take off all the widget of show receipt and show menu
                pop.destroy()
                pop.update()
                # frame.forget()
                for widget in frame.winfo_children():
                    widget.destroy()
                frame.destroy()
                # show_welcome()
                time.sleep(5)
                update_data_to_server()
                root.destroy()
                
            def show_invalid():
                thanks_window = Toplevel(root)
                thanks_window.title = "INVALID"
                thanks_window.config(bg="#D92027")
                
                f = font.Font(family="Cooper Black", size=18)
                label = Label(thanks_window, text="Your number is INVALID", bg="#D92027", fg="#fff")
                label['font']=f
                label.pack(padx=20, pady=10)
            
                
            def paid():
                def checkCreditNumber(e):
                    number = str(e.get())
                    if (len(number) == 10) and (number.isdigit()):
                        IS_VALID[0] = True
                        credit_window.destroy()
                        show_thank_window()
                        STATE[0] = True
                    else:
                        show_invalid()
            
                if (cash.get() == 1):
                    show_thank_window()
                else:
                    credit_window =  Toplevel(root)
                    credit_window.title = "Pay by credit card"
                    credit_window.geometry("200x200")
                    credit_window.config(bg="#CEE5D0")
                    e = Entry(credit_window, text="your card NUMBER",justify="center",width=15)
                    e.pack()
                    
                    f = font.Font(family="Cooper Black", size=16)
                    credit_btn = Button(credit_window, text="Confirm", command=lambda: checkCreditNumber(e), relief="flat", bg="#94B49F", fg="white")
                    credit_btn['font'] = f
                    credit_btn.pack()
                
            cash = IntVar()
            credit = IntVar()
            f = font.Font(family="Cooper Black", size=12)
            paid_cash = Radiobutton(pop, text="Paid by cash", variable=cash, value=1)
            paid_credit = Radiobutton(pop, text="Paid by credit card", variable=cash, value=2)
            paid_cash['font']=f
            paid_credit['font']=f
            paid_cash.pack(side=LEFT)
            paid_credit.pack(side=LEFT)
            
            confirm_btn = Button(pop, text="Confirm", command=paid,bg="#94B49F", fg="white")
            confirm_btn['font']=f
            confirm_btn.pack()
            
        img_cart = Image.open("./Assets/img20.jpg")
        img_cart = ImageTk.PhotoImage(img_cart)
        btn_show_receipt = Button(second_frame, command=show_receipt)
        btn_show_receipt.image = img_cart
        btn_show_receipt['image']=img_cart
        btn_show_receipt.grid(row=5, column=0, columnspan=4, padx=20, pady=20)
        
        def show_image():
            
            row1=0
            col1=0
     
            #image 1
            def show_food_description1():
                def back_to_show_image():
                    name_label1.grid_remove()
                    description_label1.grid_remove()
                    btn1.grid_remove()
                    amount1.grid_remove()
                    order_btn1.grid_remove()
                    wrap_frame1.grid_remove()
                
                def order1():
                    amount_dic[1] += int(amount1.get())
                    print(amount_dic)
                    back_to_show_image()
                
                wrap_frame1 = Frame(frame1)
                wrap_frame1.grid(row=0,column=1)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn1 = Button(wrap_frame1, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn1['font'] = f
                btn1.grid(row=0, column=1, sticky="e")
                
             
        
                food_name1 = Food_Info[0]['name']
                food_description1 = Food_Info[0]['description']
                
                f = font.Font(family="Agency FB", size=18)
                name_label1 = Label(wrap_frame1, text=food_name1,wraplength=200)
             
                description_label1 = Label(wrap_frame1, wraplength=200 ,text=food_description1, justify=LEFT) 
                description_label1['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price1 = Label(wrap_frame1, text="Price: $" + Food_Info[0]['price'], justify=LEFT)
                price1['font'] = f
                # name_label1.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label1.grid(row=2, column=0, pady=0, padx=(40,0))
                price1.grid(row=3, column=0, pady=0, sticky="w", padx=(40,0))
                
                def clicked(e):
                    amount1.config(state=NORMAL)
                    amount1.delete(0, END)
                
                amount1 = Entry(wrap_frame1, width=10, borderwidth=4)
                amount1.insert(0, "Quantity")
                amount1.config(state=DISABLED)
                amount1.bind("<Button-1>", clicked)
                amount1.grid(row=4,column=0, pady=20, sticky="w", padx=(40,0))
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn1 = Button(wrap_frame1, text="Order", command=order1, relief="flat", bg="#94B49F", fg="white")
                order_btn1['font'] = f
                order_btn1.grid(row=4, column=1, padx=10)
            
            #image 2
            def show_food_description2():
                def back_to_show_image2():
                    name_label2.grid_remove()
                    description_label2.grid_remove()
                    btn2.grid_remove()
                    amount2.grid_remove()
                    order_btn2.grid_remove()
                    wrap_frame2.grid_remove()
                    # show_image()
            
                # btn_img2.grid_remove()
                def order2():
                    amount_dic[2] += int(amount2.get())
                    print(amount_dic)
                    back_to_show_image2()
                
                wrap_frame2 = Frame(frame2)
                wrap_frame2.grid(row=0,column=2)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn2 = Button(wrap_frame2, command=back_to_show_image2, text="x", relief="flat", bg="#ECB390")
                btn2['font'] = f
                btn2.grid(row=0, column=1, sticky="e")
                
                food_name2 = Food_Info[1]['name']
                food_description2 = Food_Info[1]['description']
                
                f = font.Font(family="Agency FB", size=18)
                name_label2 = Label(wrap_frame2, text=food_name2, wraplength=200)
                description_label2 = Label(wrap_frame2, wraplength=180 ,text=food_description2, justify=LEFT) 
                description_label2['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price2 = Label(wrap_frame2, text="Price: $" + Food_Info[1]['price'], justify=LEFT)
                price2['font'] = f
                # name_label2.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label2.grid(row=2, column=0,  pady=0, padx=(40,0))
                price2.grid(row=3, column=0, pady=0, sticky="w", padx=(40,0))
                
                def clicked(e):
                    amount2.config(state=NORMAL)
                    amount2.delete(0, END)
                
                amount2 = Entry(wrap_frame2, width=10, borderwidth=4)
                amount2.insert(0, "Quantity")
                amount2.config(state=DISABLED)
                amount2.bind("<Button-1>", clicked)
                amount2.grid(row=4,column=0, pady=20, sticky="w", padx=(40, 0))
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn2 = Button(wrap_frame2, text="Order", command=order2, relief="flat", bg="#94B49F", fg="white")
                order_btn2['font'] = f
                order_btn2.grid(row=4, column=1, padx=10)
            
            #image 3
            def show_food_description3():
                def back_to_show_image():
                    name_label3.grid_remove()
                    description_label3.grid_remove()
                    btn3.grid_remove()
                    amount3.grid_remove()
                    order_btn3.grid_remove()
                    wrap_frame3.grid_remove()
                
                def order3():
                    amount_dic[3] += int(amount3.get())
                    print(amount_dic)
                    back_to_show_image()
                    
                wrap_frame3 = Frame(frame3)
                wrap_frame3.grid(row=0,column=2)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn3 = Button(wrap_frame3, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn3['font'] = f
                btn3.grid(row=0, column=1, padx=0, pady=0, sticky="ne")
                
             
        
                food_name3 = Food_Info[2]['name']
                food_description3 = Food_Info[2]['description']
                f = font.Font(family="Agency FB", size=18)
                name_label3 = Label(wrap_frame3, text=food_name3,wraplength=200)
                description_label3 = Label(wrap_frame3, wraplength=160 ,text=food_description3, justify=LEFT) 
                description_label3['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price3 = Label(wrap_frame3, text="Price: $" + Food_Info[2]['price'], justify=LEFT)
                price3['font'] = f
                # name_label3.grid(row=1, column=0, pady=(0,20), padx=20)
                description_label3.grid(row=2, column=0,  pady=0, padx=(40,0))
                price3.grid(row=3, column=0, pady=0, sticky="w", padx=(40,0))
                
                def clicked(e):
                    amount3.config(state=NORMAL)
                    amount3.delete(0, END)
                
                amount3 = Entry(wrap_frame3, width=10, borderwidth=4)
                amount3.insert(0, "Quantity")
                amount3.config(state=DISABLED)
                amount3.bind("<Button-1>", clicked)
                amount3.grid(row=4,column=0, pady=20, sticky="w", padx=(40, 0))
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn3 = Button(wrap_frame3, text="Order", command=order3,relief="flat", bg="#94B49F", fg="white")
                order_btn3['font'] = f
                order_btn3.grid(row=4, column=1, padx=10)
            
            #image 4
            def show_food_description4():
                def back_to_show_image():
                    name_label4.grid_remove()
                    description_label4.grid_remove()
                    btn4.grid_remove()
                    amount4.grid_remove()
                    order_btn4.grid_remove()
                    wrap_frame4.grid_remove()
                
                def order4():
                    amount_dic[4] += int(amount4.get())
                    print(amount_dic)
                    back_to_show_image()
                
                wrap_frame4 = Frame(frame4)
                wrap_frame4.grid(row=0,column=2)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn4 = Button(wrap_frame4, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn4['font'] = f
                btn4.grid(row=0, column=1, sticky="e")
                
             
        
                food_name4 = Food_Info[3]['name']
                food_description4 = Food_Info[3]['description']
                f = font.Font(family="Agency FB", size=18)
                name_label4 = Label(wrap_frame4, text=food_name4,wraplength=200)
                description_label4 = Label(wrap_frame4, wraplength=160 ,text=food_description4, justify=LEFT) 
                description_label4['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price4 = Label(wrap_frame4, text="Price: $" + Food_Info[3]['price'], justify=LEFT)
                price4['font'] = f
                # name_label4.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label4.grid(row=2, column=0,  pady=0, padx=(40,0))
                price4.grid(row=3, column=0, pady=0, sticky="w", padx=(40,0))
                
                def clicked(e):
                    amount4.config(state=NORMAL)
                    amount4.delete(0, END)
                
                amount4 = Entry(wrap_frame4, width=10, borderwidth=4)
                amount4.insert(0, "Quantity")
                amount4.config(state=DISABLED)
                amount4.bind("<Button-1>", clicked)
                amount4.grid(row=4,column=0, pady=20, sticky="w", padx=(40, 0))
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn4 = Button(wrap_frame4, text="Order", command=order4,relief="flat", bg="#94B49F", fg="white")
                order_btn4['font'] = f
                order_btn4.grid(row=4, column=1, padx=10)
            
            #image 5
            def show_food_description5():
                def back_to_show_image():
                    name_label5.grid_remove()
                    description_label5.grid_remove()
                    btn5.grid_remove()
                    amount5.grid_remove()
                    order_btn5.grid_remove()
                    wrap_frame5.grid_remove()
                
                def order5():
                    amount_dic[5] += int(amount5.get())
                    print(amount_dic)
                    back_to_show_image()
                
                wrap_frame5 = Frame(frame5)
                wrap_frame5.grid(row=0,column=2)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn5 = Button(wrap_frame5, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn5['font'] = f
                btn5.grid(row=0, column=1, sticky="e")
                
             
        
                food_name5 = Food_Info[4]['name']
                food_description5 = Food_Info[4]['description']
                f = font.Font(family="Agency FB", size=18)
                name_label5 = Label(wrap_frame5, text=food_name5,wraplength=200)
                description_label5 = Label(wrap_frame5, wraplength=220 ,text=food_description5, justify=LEFT) 
                description_label5['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price5 = Label(wrap_frame5, text="Price: $" + Food_Info[4]['price'], justify=LEFT)
                price5['font'] = f
                # name_label5.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label5.grid(row=2, column=0,  pady=0, padx=(40,0))
                price5.grid(row=3, column=0, pady=0, sticky="w", padx=(40,0))
                
                def clicked(e):
                    amount5.config(state=NORMAL)
                    amount5.delete(0, END)
                
                amount5 = Entry(wrap_frame5, width=10, borderwidth=4)
                amount5.insert(0, "Quantity")
                amount5.config(state=DISABLED)
                amount5.bind("<Button-1>", clicked)
                amount5.grid(row=4,column=0, pady=20, sticky="w", padx=(40, 0))
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn5 = Button(wrap_frame5, text="Order", command=order5,relief="flat", bg="#94B49F", fg="white")
                order_btn5['font'] = f
                order_btn5.grid(row=4, column=1, padx=10)
            
            #image 6
            def show_food_description6():
                def back_to_show_image():
                    name_label6.grid_remove()
                    description_label6.grid_remove()
                    btn6.grid_remove()
                    amount6.grid_remove()
                    order_btn6.grid_remove()
                    wrap_frame6.grid_remove()
                
                def order6():
                    amount_dic[6] += int(amount6.get())
                    print(amount_dic)
                    back_to_show_image()
                
                wrap_frame6 = Frame(frame6)
                wrap_frame6.grid(row=0,column=2)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn6 = Button(wrap_frame6, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn6['font'] = f
                btn6.grid(row=0, column=1, sticky="e")
                
             
        
                food_name6 = Food_Info[5]['name']
                food_description6 = Food_Info[5]['description']
                f = font.Font(family="Agency FB", size=18)
                name_label6 = Label(wrap_frame6, text=food_name6,wraplength=250)
                description_label6 = Label(wrap_frame6, wraplength=260 ,text=food_description6, justify=LEFT) 
                description_label6['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price6 = Label(wrap_frame6, text="Price: $" + Food_Info[5]['price'], justify=LEFT)
                price6['font'] = f
                # name_label6.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label6.grid(row=2, column=0,  pady=0, padx=(40,0))
                price6.grid(row=3, column=0, pady=0, sticky="w", padx=(40,0))
                
                def clicked(e):
                    amount6.config(state=NORMAL)
                    amount6.delete(0, END)
                
                amount6 = Entry(wrap_frame6, width=10, borderwidth=4)
                amount6.insert(0, "Quantity")
                amount6.config(state=DISABLED)
                amount6.bind("<Button-1>", clicked)
                amount6.grid(row=4,column=0, pady=20, sticky="w", padx=(40, 0))
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn6 = Button(wrap_frame6, text="Order", command=order6,relief="flat", bg="#94B49F", fg="white")
                order_btn6['font'] = f
                order_btn6.grid(row=4, column=1, padx=10)
            
            #image 7
            def show_food_description7():
                def back_to_show_image():
                    name_label7.grid_remove()
                    description_label7.grid_remove()
                    btn7.grid_remove()
                    amount7.grid_remove()
                    order_btn7.grid_remove()
                    wrap_frame7.grid_remove()
                
                def order7():
                    amount_dic[7] += int(amount7.get())
                    print(amount_dic)
                    back_to_show_image()
                
                wrap_frame7 = Frame(frame7)
                wrap_frame7.grid(row=0,column=2)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn7 = Button(wrap_frame7, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn7['font'] = f
                btn7.grid(row=0, column=1, sticky="e")
                
             
        
                food_name7 = Food_Info[6]['name']
                food_description7 = Food_Info[6]['description']
                f = font.Font(family="Agency FB", size=18)
                name_label7 = Label(wrap_frame7, text=food_name7,wraplength=200)
                description_label7 = Label(wrap_frame7, wraplength=200 ,text=food_description7, justify=LEFT) 
                description_label7['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price7 = Label(wrap_frame7, text="Price: $" + Food_Info[6]['price'], justify=LEFT)
                price7['font'] = f
                # name_label7.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label7.grid(row=2, column=0,  pady=0, padx=(40,0))
                price7.grid(row=3, column=0, pady=0, sticky="w",padx=(40,0))
                
                def clicked(e):
                    amount7.config(state=NORMAL)
                    amount7.delete(0, END)
                
                amount7 = Entry(wrap_frame7, width=10, borderwidth=4)
                amount7.insert(0, "Quantity")
                amount7.config(state=DISABLED)
                amount7.bind("<Button-1>", clicked)
                amount7.grid(row=4,column=0,  pady=20, sticky="w", padx=(40, 0))
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn7 = Button(wrap_frame7, text="Order", command=order7,relief="flat", bg="#94B49F", fg="white")
                order_btn7['font'] = f
                order_btn7.grid(row=4, column=1, padx=10)
            
            #image 8
            def show_food_description8():
                def back_to_show_image():
                    name_label8.grid_remove()
                    description_label8.grid_remove()
                    btn8.grid_remove()
                    amount8.grid_remove()
                    order_btn8.grid_remove()
                    wrap_frame8.grid_remove()
                
                def order8():
                    amount_dic[8] += int(amount8.get())
                    print(amount_dic)
                    back_to_show_image()
                
                wrap_frame8 = Frame(frame8)
                wrap_frame8.grid(row=0,column=2)
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn8 = Button(wrap_frame8, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn8['font'] = f
                btn8.grid(row=0, column=1,sticky="e")
                
             
        
                food_name8 = Food_Info[7]['name']
                food_description8 = Food_Info[7]['description']
                f = font.Font(family="Agency FB", size=18)
                name_label8 = Label(wrap_frame8, text=food_name8, font='Roboto 16 bold',wraplength=200)
                description_label8 = Label(wrap_frame8, wraplength=200 ,text=food_description8, justify=LEFT) 
                description_label8['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price8 = Label(wrap_frame8, text="Price: $" + Food_Info[7]['price'], justify=LEFT)
                price8['font'] = f
                # name_label8.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label8.grid(row=2, column=0,  pady=0, padx=(40,0))
                price8.grid(row=3, column=0, pady=0, sticky="w",padx=(40,0))
                
                def clicked(e):
                    amount8.config(state=NORMAL)
                    amount8.delete(0, END)
                
                amount8 = Entry(wrap_frame8, width=10, borderwidth=4)
                amount8.insert(0, "Quantity")
                
                amount8.grid(row=4,column=0, pady=20,sticky="w",padx=(40, 0))
                amount8.config(state=DISABLED)
                amount8.bind("<Button-1>", clicked)
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn8 = Button(wrap_frame8, text="Order", command=order8,relief="flat", bg="#94B49F", fg="white")
                order_btn8['font'] = f
                order_btn8.grid(row=4, column=1, padx=10)
            
            #image 9
            def show_food_description9():
                def back_to_show_image():
                    name_label9.grid_remove()
                    description_label9.grid_remove()
                    btn9.grid_remove()
                    amount9.grid_remove()
                    order_btn9.grid_remove()
                    wrap_frame9.grid_remove()
                
                def order9():
                    amount_dic[9] += int(amount9.get())
                    print(amount_dic)
                    back_to_show_image()
                
                wrap_frame9 = Frame(frame9)
                wrap_frame9.grid(row=0,column=2)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn9 = Button(wrap_frame9, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn9['font'] = f
                btn9.grid(row=0, column=1, sticky="e")
                
             
        
                food_name9 = Food_Info[8]['name']
                food_description9 = Food_Info[8]['description']
                f = font.Font(family="Agency FB", size=18)
                name_label9 = Label(wrap_frame9, text=food_name9, font='Roboto 16 bold',wraplength=200)
                description_label9 = Label(wrap_frame9, wraplength=300 ,text=food_description9, justify=LEFT)
                description_label9['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")                
                price9 = Label(wrap_frame9, text="Price: $" + Food_Info[8]['price'], justify=LEFT)
                price9['font'] = f
                
                # name_label9.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label9.grid(row=2, column=0,  pady=0, padx=(40,0))
                price9.grid(row=3, column=0, pady=0, sticky="w", padx=(40,0))
                
                def clicked(e):
                    amount9.config(state=NORMAL)
                    amount9.delete(0, END)
                
                amount9= Entry(wrap_frame9, width=10, borderwidth=4)
                amount9.insert(0, "Quantity")
                amount9.config(state=DISABLED)
                amount9.bind("<Button-1>", clicked)
                amount9.grid(row=4,column=0, pady=20,padx=(40, 0), sticky="w")
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn9 = Button(wrap_frame9, text="Order", command=order9,relief="flat", bg="#94B49F", fg="white")
                order_btn9['font'] = f
                order_btn9.grid(row=4, column=1, padx=10)
            
            #image 10
            def show_food_description10():
                def back_to_show_image():
                    name_label10.grid_remove()
                    description_label10.grid_remove()
                    btn10.grid_remove()
                    amount10.grid_remove()
                    order_btn10.grid_remove()
                    wrap_frame10.grid_remove()
                
                def order10():
                    amount_dic[10] += int(amount10.get())
                    print(amount_dic)
                    back_to_show_image()
                
                wrap_frame10 = Frame(frame10)
                wrap_frame10.grid(row=0,column=2)
                
                f = font.Font(family="Arial Rounded MT Bold", size=20)
                btn10 = Button(wrap_frame10, command=back_to_show_image, text="x", relief="flat", bg="#ECB390")
                btn10['font'] = f
                btn10.grid(row=0, column=1, sticky="e")
                
             
        
                food_name10 = Food_Info[9]['name']
                food_description10 = Food_Info[9]['description']
                f = font.Font(family="Agency FB", size=18)
                name_label10 = Label(wrap_frame10, text=food_name10, font='Roboto 16 bold',wraplength=200)
                description_label10 = Label(wrap_frame10, wraplength=200 ,text=food_description10, justify=LEFT) 
                description_label10['font'] = f
                f = font.Font(family="Imprint MT Shadow", size=16, weight="bold")
                price10 = Label(wrap_frame10, text="Price: $" + Food_Info[9]['price'], justify=LEFT)
                price10['font'] = f
                # name_label10.grid(row=1, column=0, pady=(0, 20), padx=20)
                description_label10.grid(row=2, column=0,  pady=0, padx=(40,0))
                price10.grid(row=3, column=0, pady=0, sticky="w",padx=(40,0))
                
                def clicked(e):
                    amount10.config(state=NORMAL)
                    amount10.delete(0, END)
                
                amount10= Entry(wrap_frame10, width=10, borderwidth=4)
                amount10.insert(0, "Quantity")
                amount10.config(state=DISABLED)
                amount10.bind("<Button-1>", clicked)
                amount10.grid(row=4,column=0, pady=20, sticky="w", padx=(40, 0))
                
                f = font.Font(family="Cooper Black", size=20)
                order_btn10 = Button(wrap_frame10, text="Order", command=order10,relief="flat", bg="#94B49F", fg="white")
                order_btn10['font'] = f
                order_btn10.grid(row=4, column=1, padx=10)
            
            img1 = Image.open("./Assets/img10.jpg")
            img1 = ImageTk.PhotoImage(img1)
            
            btn_img1 = Button(frame1, command=lambda: show_food_description1(), relief=FLAT)
            btn_img1.image = img1
            btn_img1['image']=img1
            btn_img1.grid(row=0, column=0)
            
            
            img2 = Image.open("./Assets/img11.jpg")
            img2 = ImageTk.PhotoImage(img2)
            
            btn_img2 = Button(frame2, command=lambda: show_food_description2(), relief=FLAT)
            btn_img2.image = img2
            btn_img2['image']=img2
            btn_img2.grid(row=0, column=1)
            
          
            img3 = Image.open("./Assets/img12.jpg")
            img3 = ImageTk.PhotoImage(img3)
            
            btn_img3 = Button(frame3, command=lambda: show_food_description3(), relief=FLAT)
            btn_img3.image = img3
            btn_img3['image']=img3
            btn_img3.grid(row=0, column=0)
            
         
            img4 = Image.open("./Assets/img13.jpg")
            img4 = ImageTk.PhotoImage(img4)
             
            btn_img4 = Button(frame4, command=lambda: show_food_description4(), relief=FLAT)
            btn_img4.image = img4
            btn_img4['image']=img4
            btn_img4.grid(row=0, column=0)
            
            
            img5 = Image.open("./Assets/img14.jpg")
            img5 = ImageTk.PhotoImage(img5)
            
            btn_img5 = Button(frame5, command=lambda: show_food_description5(), relief=FLAT)
            btn_img5.image = img5
            btn_img5['image']=img5
            btn_img5.grid(row=0, column=0)
            
            
            img6 = Image.open("./Assets/img15.jpg")
            img6 = ImageTk.PhotoImage(img6)
            
            btn_img6 = Button(frame6, command=lambda: show_food_description6(), relief=FLAT)
            btn_img6.image = img6
            btn_img6['image']=img6
            btn_img6.grid(row=0, column=1)
            
          
            img7 = Image.open("./Assets/img16.jpg")
            img7 = ImageTk.PhotoImage(img7)
            
            btn_img7 = Button(frame7, command=lambda: show_food_description7(), relief=FLAT)
            btn_img7.image = img7
            btn_img7['image']=img7
            btn_img7.grid(row=0, column=0)
            
         
            img8 = Image.open("./Assets/img17.jpg")
            img8= ImageTk.PhotoImage(img8)
             
            btn_img8 = Button(frame8, command=lambda: show_food_description8(), relief=FLAT)
            btn_img8.image = img8
            btn_img8['image']=img8
            btn_img8.grid(row=0, column=0)
            
            img9 = Image.open("./Assets/img18.jpg")
            img9 = ImageTk.PhotoImage(img9)
            
            btn_img9 = Button(frame9, command=lambda: show_food_description9(), relief=FLAT)
            btn_img9.image = img9
            btn_img9['image']=img9
            btn_img9.grid(row=0, column=0)
            
         
            img10 = Image.open("./Assets/img19.jpg")
            img10= ImageTk.PhotoImage(img10)
             
            btn_img10 = Button(frame10, command=lambda: show_food_description10(), relief=FLAT)
            btn_img10.image = img10
            btn_img10['image']=img10
            btn_img10.grid(row=0, column=0)
        show_image()
                

def show_welcome():
    global root

    # FRAME.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    LOGO_IMG.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # WELCOME_LABEL.pack(pady=(20,40))
    
    BTN_MENU.place(x=830, y=450)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
#glocal variables
FOOD_LISTS = []
LIST_IMG_LABELS = []   
amount_dic = []
totalmoney = []
totalmoney.append(int(0))
for i in range(21):
    amount_dic.append(int(0))
print(amount_dic)
STATE = []
STATE.append(False) # false is pay by cash, true is pay by credit
IS_VALID = []
IS_VALID.append(False)

client.connect((HOST, PORT))
msg = "FOOD"
client.sendall(msg.encode(FORMAT))
client.recv(1024)
#receive food info from server
Food_Info = client.recv(4096)
client.sendall(msg.encode(FORMAT))
Food_Info = pickle.loads(Food_Info)
FOOD_LISTS.append(Food_Info)

# download_food_image(Food_Info)
recvAssetsFromServer(client)

root = Tk()
root.option_add( "*font", "Roboto") #set default font
root.title("FOOD ORDER APP")
root.iconbitmap("./Assets/img21.jpg")
root.geometry("1360x700+0+0")
root.configure(bg='#01001f')
root.option_add("*Label*Background", "white")
root.option_add("*LabelFrame*Background", "white")
root.option_add("*Frame*Background", "white")
root.option_add("*Entry*Background", "white")

#widgets
# FRAME = LabelFrame(root, padx=20, pady=20)
LOGO = ImageTk.PhotoImage(Image.open("./Assets/img24.jpg"))
LOGO_IMG = Label(root, image=LOGO, borderwidth=0)
# WELCOME_LABEL = Label(FRAME, text="Welcome to NNP Restaurant", font=("Roboto", 20, "bold"))
f = font.Font(family="Cooper Black", size=14)
BTN_MENU = Button(root, text="Show Food Menu", padx=20,pady=10, command=lambda: show_menu(LOGO_IMG, BTN_MENU, client, IMG_LABELS), bg="#4e17a6", relief="flat",fg="#fff")
BTN_MENU['font']=f
IMG_LABELS = []


# img = ImageTk.PhotoImage(Image.open())
# label = Label(FRAME, image=img)
# IMG_LABELS.append(label)
# IMG_LABELS[0].pack()

# welcome

show_welcome()



root.mainloop()
msg = "FINISH"
client.sendall(msg.encode(FORMAT))
client.recv(4096)
client.sendall(msg.encode(FORMAT))
# print(STATE)

client.close()
# except:
    # print("error")
    






