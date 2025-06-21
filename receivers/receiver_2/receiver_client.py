import socket
import subprocess
import os
from cryptography.fernet import Fernet

PORT = 9998
TASKS_PATH = "received_tasks"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", PORT))
server.listen(1)
print(f"listening on port {PORT}... ")

client, address = server.accept()
print(f"Connection established with {address}")

ENCRYPTION_KEY = Fernet.generate_key()
ENCRYPTION_KEY = b"5FH3fAyb27cr3h9lvJYmApalid3X4-VS0-CuMVx4Prs="
cipher = Fernet(ENCRYPTION_KEY)


done = 0

while not done:
    file_name = client.recv(1024)
    file_name = cipher.decrypt(file_name).decode('utf-8')
    file_name = os.path.join(TASKS_PATH, file_name)

    file_b = b""
    while True:
        data = client.recv(1024)
        file_b += data
        if file_b.endswith(b"<FIN>"):
            break
    file_b = file_b[:-5]

    with open(f"{file_name}.encrypted", "wb") as f:
        f.write(file_b)

    with open(f"{file_name}.encrypted", "rb") as f:
        encrypted_data = f.read()

    decrypted = cipher.decrypt(encrypted_data)

    with open(file_name, "wb") as f:
        f.write(decrypted)
    
    #file_detection#

    output = ""
    status = ""

    classfile = False
    java_class_name = ""
    exefile = False
    exe_name = ""

    if file_name.endswith(".cpp") or file_name.endswith(".c"):       
        try:
            exe_name = file_name.rsplit(".", 1)[0] + ".exe"
            compile = subprocess.run(["g++", file_name, "-o", exe_name], capture_output=True, text=True)
            run = subprocess.run([f"./{exe_name}"], capture_output=True, text=True)
            exefile = True
            # print(run)
        except:
            status = "error"
        output = run.stdout + run.stderr
        
    elif file_name.endswith(".java"):      
        try:
            java_class_name = file_name.rsplit(".", 1)[0] + ".class"
            compile = subprocess.run(["javac", file_name], capture_output=True, text=True)
            run = subprocess.run(["java", file_name], capture_output=True, text=True)
            classfile = True
            # print(run)
        except:
            status = "error"
        output = run.stdout + run.stderr

    elif file_name.endswith(".py"):
        try:
            exe_name = file_name.rsplit(".", 1)[0] + ".py"
            run = subprocess.run(["python", file_name], capture_output=True, text=True)
            # print(run)
        except:
            status = "error"
        output = run.stdout + run.stderr
    if run.returncode != 0:
        status = "error"
    else:
        status = "success"

    print(f"{os.path.basename(file_name)} processed")

    encrypted_status = cipher.encrypt(status.encode('utf-8'))
    client.send(encrypted_status)
    encrypted_output = cipher.encrypt(output.encode('utf-8'))
    client.send(encrypted_output)

    done1 = client.recv(1024)
    done1 = cipher.decrypt(done1).decode('utf-8')
    done = int(done1)
    os.remove(f"{file_name}.encrypted")
    os.remove(file_name)
    if os.path.exists(java_class_name) :
        os.remove(java_class_name)
    if os.path.exists(exe_name):
        os.remove(exe_name)

client.close()
server.close()

print("client connection closed")