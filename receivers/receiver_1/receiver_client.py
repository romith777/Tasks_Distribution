import socket
import subprocess
import os

PORT = 9999
TASKS_PATH = "received_tasks"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", PORT))
server.listen(1)
print(f"listening on port {PORT}... ")

client, address = server.accept()
print(f"Connection established with {address}")

done = 0

while not done:
    file_name = client.recv(1024).decode('utf-8')
    internalfile = False
    internalfile_name = ""

    file_b = b""
    while True:
        data = client.recv(1024)
        file_b += data
        if file_b.endswith(b"<FIN>"):
            break

    file_name = os.path.join(TASKS_PATH, file_name)
    with open(file_name, "wb") as f:
        f.write(file_b[:-5])

    #file_detection#

    output = ""
    status = ""

    if file_name.endswith(".cpp") or file_name.endswith(".c"):       
        try:
            exe_name = file_name.rsplit(".", 1)[0] + ".exe"
            compile = subprocess.run(["g++", file_name, "-o", exe_name], capture_output=True, text=True)
            run = subprocess.run([f"./{exe_name}"], capture_output=True, text=True)
            print(run)
            if run.returncode != 0:
                status = "error"
            else:
                status = "success"
        except:
            status = "error"
        output = run.stdout + run.stderr
        
    elif file_name.endswith(".java"):      
        try:
            exe_name = file_name.rsplit(".", 1)[0] + ".class"
            compile = subprocess.run(["javac", file_name], capture_output=True, text=True)
            run = subprocess.run(["java", file_name], capture_output=True, text=True)
            print(run)
            if run.returncode != 0:
                status = "error"
            else:
                status = "success"
        except:
            status = "error"
        output = run.stdout + run.stderr

    elif file_name.endswith(".py"):
        try:
            exe_name = file_name.rsplit(".", 1)[0] + ".py"
            run = subprocess.run(["python", file_name], capture_output=True, text=True)
            print(run)
            if run.returncode != 0:
                status = "error"
            else:
                status = "success"
        except:
            status = "error"
        output = run.stdout + run.stderr
    
    client.send(status.encode('utf-8'))
    client.send(output.encode('utf-8'))

    done1 = client.recv(1024).decode('utf-8')
    done = int(done1)

client.close()
server.close()

print("client connection closed")