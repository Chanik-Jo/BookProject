import socket,sys,struct,time
import threading,multiprocessing

from PyQt5.QtWidgets import QTableWidgetItem

HOST,PORT = "localhost",7889


clientSock =""

def utf8len(s):#utf-8 형태의 바이트 갯수를 반환합니다.
    return len(s.encode('utf-8'))



def recvMsg(clientSock,window):
    print("recvmsg thread on")
    # 병렬프로그래밍 때문에 차질을 빛고 있다.
    # 멀티 프로세스를 하면 이게 끝날때까지 기다렸다가 main메소드도 종료해야하는데 메인메소드가 먼저 혼자 종료하고,
    # 멀티스레드를 하면 GIL이 걸려서 읽기도 쓰기도 못하는 골떄는 상황으로 들어간다.
    # GIL 공통변수를 쓰면 자동으로 락걸리는걸 회피하기위해 아예 매개변수로 넘겨줬다.  내부적으론
    # "복사"가 되었으려나?????

    sizeReceive = clientSock.recv(40)
    sizeReceive=int.from_bytes(sizeReceive,"little")
    print("recv msg size ",sizeReceive)# 겨우 숫자가 올바르게 돌아왔다.  이거 알아내는데 3시간 날렸네.

    msgReceive =clientSock.recv(sizeReceive)#제대로 다 왔는데 이걸 \t 같은 특문을 어찌 번역해야 하냐.....
    msgReceive = msgReceive.decode('utf-8')# 이러니까 된다!!
    print("received Real Message \n",msgReceive)#결국 메모리를 타이트하게 알뜰살뜰하게 쓰면서 송수신이 성공했다.
    #문제는 그것을 리스트로 변환해주는 것이다.
    print("msgREceive type ",type(msgReceive))
    msgReceive = msgReceive.rstrip('\n')#remove last \n 할 의도였는데 .
    print("msg receive\n",msgReceive)
    lineSpiltedData = msgReceive.split('\n')#모든 \n이 사라지고 거기를 기준으로 갈라졌다
    print("line spilted data type ",type(lineSpiltedData))
    print("linespilted data\n",lineSpiltedData)
    for i in range(len(lineSpiltedData)):
        tempLine= lineSpiltedData[i].rstrip('\t')#내가 sp엘-아이t 인데 sp아이-엘t로 보고 1시간 가까이 삽질중이었다.
        tempLine= tempLine.split('\t')#내가 sp엘-아이t 인데 sp아이-엘t로 보고 1시간 가까이 삽질중이었다.

        #print("tempLine  ",tempLine)
        lineSpiltedData[i] = tempLine
        #print("lineSpiltedData[i]  ",lineSpiltedData[i])


    print("\n\n\n\nline spilted data last calculation\n\n\n",lineSpiltedData) #드디어 드디어 성공하였다성공하였다!!!!!


    table =window.userListTable
    table.setRowCount(0)#이게 정상적으로(다 비우기)가 되
    # 는걸로 보면 레퍼런스는 잘
    #넘어간걸로 추정
    table.setColumnWidth(0, table.width() * 1 / 10)
    table.setColumnWidth(1, table.width() * 7 / 10)
    table.setColumnWidth(2, table.width() * 2 / 10)

    table.setColumnCount(len(lineSpiltedData[0]))

    for i in range(len(lineSpiltedData)):
        table.insertRow(table.rowCount())
        for j in range(len(lineSpiltedData[0])):
            value =lineSpiltedData[i][j]
            print("value",value)
            table.setItem(i, j, QTableWidgetItem(value))










def sendMsg(msg,clientSock):

    print("type of msg is ",type(msg))# 현시점에서는 string
    msg = msg+"\0"#이거 하면 남아도는 인코딩오류 char배열 쓰레기값들을 다 잡아낼수 있을까.
    msgSize=sys.getsizeof(msg)
    print("Message size is ",msgSize)
    try:
        #http://daplus.net/python-python-3%EC%97%90%EC%84%9C-int%EB%A5%BC-%EB%B0%94%EC%9D%B4%ED%8A%B8%EB%A1%9C-%EB%B3%80%ED%99%98/
        clientSock.send(struct.pack("I",msgSize)) #일단 버퍼 사이즈는 정상전송에 성공하였다.
    except Exception as e:
        print("exception1 is ",e)


    #print(struct.pack("I", msg))
    try:
        clientSock.send(bytes(msg,encoding="utf-8"))
    except Exception as e:
        print("exception2 is e ",e)

    #어짜피 string은 정상적으로 전송되니, 궃이 json을 사용하는것은 포기하였다.

    #recvMsg(clientSock)

def retrieveDBDatafromServer(window,m = "select * from custom_table"):


    #m ="INSERT INTO custom_table (name, age) VALUES ('jo2', '13')"
    #global clientSock if는 global 안써도 구역(스코프)가 구분안됨
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSock.connect((HOST,PORT))
    #sendMsg(m,clientSock)
    threads = []

    t1 = threading.Thread(target=sendMsg,args=(m,clientSock))
    t1.start()
    threads.append(t1)

    t2 = threading.Thread(target=recvMsg,args=(clientSock,window))
    t2.start()
    threads.append(t2)

    for thread in threads:
        thread.join()











