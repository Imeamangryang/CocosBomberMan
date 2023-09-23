import sys
import socket
import threading
import Gamelayer_mul
import Actors_mul


#HOST = '192.168.45.27'
PORT = 65456
def Client():
    global client
    HOST = input("서버 주소를 입력해주세요 :")
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    nickname = input('Please Enter Your Name : ')
    client.sendall(nickname.encode())

    thr=threading.Thread(target=consoles,args=())
    thr.Daemon=True
    thr.start()


# 스레드에서 처리할 작업
def consoles():
    while True:
        try:
            msg=client.recv(1024)

            if not msg:
                break

            if (msg.decode()=='up'):
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_UP = 1
            elif (msg.decode()=='down'):
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_DOWN = 1
            elif (msg.decode()=='right'):
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_RIGHT = 1
            elif msg.decode()=='left':
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_LEFT = 1
            elif msg.decode()=='space':
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_SPACE = 1
            elif (msg.decode()=='N_up'):
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_UP = 0
            elif (msg.decode()=='N_down'):
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_DOWN = 0
            elif (msg.decode()=='N_right'):
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_RIGHT = 0
            elif msg.decode()=='N_left':
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_LEFT = 0
            elif msg.decode()=='N_space':
                print('Received from :',msg.decode())
                Gamelayer_mul.GameLayer.PRESS_SPACE = 0
            elif msg.decode()=='BombItem':
                print('Received from :',msg.decode())
                msg=client.recv(1024)
                print('Received from :',msg.decode())
                point = msg.decode().split(',')
                x = int(point[0])
                y = int(point[1])
                Gamelayer_mul.GameLayer.ITEM.append(1)
                Gamelayer_mul.GameLayer.ITEM_X.append(x)
                Gamelayer_mul.GameLayer.ITEM_Y.append(y)
            elif msg.decode()=='BombPowder':
                print('Received from :',msg.decode())
                msg=client.recv(1024)
                print('Received from :',msg.decode())
                point = msg.decode().split(',')
                x = int(point[0])
                y = int(point[1])
                Gamelayer_mul.GameLayer.ITEM.append(2)
                Gamelayer_mul.GameLayer.ITEM_X.append(x)
                Gamelayer_mul.GameLayer.ITEM_Y.append(y)
            elif msg.decode()=='Moveincrease':
                print('Received from :',msg.decode())
                msg=client.recv(1024)
                print('Received from :',msg.decode())
                point = msg.decode().split(',')
                x = int(point[0])
                y = int(point[1])
                Gamelayer_mul.GameLayer.ITEM.append(3)
                Gamelayer_mul.GameLayer.ITEM_X.append(x)
                Gamelayer_mul.GameLayer.ITEM_Y.append(y)
            else:
                print('Received from else:',msg.decode())
            
        except ConnectionResetError as e:
            break
