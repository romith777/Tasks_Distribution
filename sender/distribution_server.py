import socket
import os
import threading
import pandas as pd
from cryptography.fernet import Fernet

CLIENT_IP = "localhost"
CLIENT_PORTS = [9999,9998,9997]
TASKS_PATH = "tasks"
OUTPUT_PATH = "received_output"

ENCRYPTION_KEY = Fernet.generate_key()
ENCRYPTION_KEY = b"5FH3fAyb27cr3h9lvJYmApalid3X4-VS0-CuMVx4Prs="
cipher = Fernet(ENCRYPTION_KEY)

clients = []
Sent_tasks_status = []
client_names = []

for port in CLIENT_PORTS:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((CLIENT_IP, port))
        clients.append(client)
        print(f"Connected to {CLIENT_IP}:{port}")
    except ConnectionRefusedError:
        print(f"Connection to {CLIENT_IP}:{port} failed. Server may not be running.")
        exit(1)

for client in clients:
    client_names.append(client.getsockname())

sender_files = [os.path.join(TASKS_PATH, f) for f in os.listdir(TASKS_PATH) if os.path.isfile(os.path.join(TASKS_PATH, f))]

allfile_tran = False

no_of_clients = len(clients)
files_to_client = [[] for _ in range(no_of_clients)]
size = int(len(sender_files)/no_of_clients)

start_index = 0
end_index = size

if len(sender_files) > no_of_clients:
    for i in range(no_of_clients):
        if i == no_of_clients - 1:
            cf = sender_files[start_index:]
        else:
            cf = sender_files[start_index:end_index]
        files_to_client.append(cf)
        start_index = end_index
        end_index += size
    allfile_tran = True
else:
    files_to_client=sender_files

def RoundR_file_Dist():
    for index,file in enumerate(sender_files):
        files_to_client[(index)%(no_of_clients)].append(file)


def Client_output(client, c1f):
    done = "0"
    for file_name in c1f:
        received_task_status = {"name": "", "status": "", "client_address": ""}
        received_task_status["name"] = os.path.basename(file_name)
        if file_name == c1f[-1]:
            done = "1"
        print(f"Sending file: {file_name} to {client.getsockname()}")

        encrypted_file_name = cipher.encrypt(os.path.basename(file_name).encode('utf-8'))
        client.send(encrypted_file_name)

        with open(file_name,"rb") as f:
            data = f.read()

        encrypted_file_data = cipher.encrypt(data)

        with open(f"{file_name}.encrypted","wb") as f:
            f.write(encrypted_file_data)

        f =  open(f"{file_name}.encrypted", "rb")
        data = f.read(1024)
        client.sendall(data)
        f.close()
        client.send(b"<FIN>")
        os.remove(f"{file_name}.encrypted")

        output=""
        
        status = client.recv(1024)
        status = cipher.decrypt(status).decode('utf-8')
        output = client.recv(1024)
        output = cipher.decrypt(output).decode('utf-8')

        received_task_status["status"] = status
        received_task_status["client_address"] = (client.getsockname())
        Sent_tasks_status.append(received_task_status)
        
        #file_detection#

        if output != "":
            file_name = os.path.basename(file_name)
            file_name = file_name.rsplit(".", 1)[0]
            file_name = os.path.join(OUTPUT_PATH, file_name)
            with open(file_name,"w") as f:
                f.write(output)

        encrypted_done = cipher.encrypt(done.encode('utf-8'))
        client.send(encrypted_done)

    print(f"Finished sending files to {client.getsockname()}")
    

threads = []

RoundR_file_Dist()


for client, files in zip(clients, files_to_client):
    print(f"Starting thread for {client.getsockname()}")
    c = threading.Thread(target=Client_output, args=(client, files,))
    threads.append(c)
    print(f"Thread for {client.getsockname()} finished")

for thread in threads:
    thread.start()

for thread in threads:    
    thread.join()

for client in clients:
    client.close()

df = pd.DataFrame(Sent_tasks_status)

df = df.rename(columns={'name': 'file_name'})
df = df[['file_name', 'status', 'client_address']]
print(df)
