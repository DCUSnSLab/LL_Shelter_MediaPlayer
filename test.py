from time import sleep

import sysv_ipc

a = "0"
chek = int(a[0])
try:
    data = int(a[1:])
except:
    data = chek
print(chek, data)

adv_mq = sysv_ipc.MessageQueue(3820, sysv_ipc.IPC_CREAT)

while True:
    #adv_mq.send(str(data), True, type=1)
    data = adv_mq.receive(type=0)
    print(data[0])
    sleep(0.5)
