🔧 Task Distributor: Distributed Secure Code Execution System

This project securely distributes and executes code files across multiple machines on the same local network. It uses encrypted socket communication to protect data while enabling parallel execution and result collection from clients.

🚀 Features

📡 Distributed Execution: Offloads code files to multiple client systems for concurrent execution

🔐 End-to-End Encryption: Uses the cryptography library to ensure secure file transfer between server and clients

🔁 Parallel Processing: Utilizes Python's threading module for handling multiple clients at once

⚙️ Multi-language Support: Automatically compiles and runs Python, C/C++, and Java source files

📄 Task Logging: Records task statuses and output summaries using pandas

⚙️ How It Works

Task Distribution:

The server loads files from the tasks/ folder.

It distributes them evenly across all connected clients.

Secure Communication:

Files are encrypted using the cryptography library.

Clients decrypt and save them locally.

Code Execution:

Clients compile/run the code based on file extension:

.py → Python

.cpp/.c → C/C++

.java → Java

Result Collection:

Output and status are sent back to the server.

Server logs this using a pandas dataframe and stores outputs in received_output/.

🧰 Tech Stack

Languages: Python, C/C++, Java

Core Technologies:

Socket Programming

Cryptography (Fernet Encryption)

Multithreading

Subprocess Execution

Pandas for logging

Key Python Libraries:

socket

cryptography

threading

subprocess

pandas

os, sys

✅ Requirements

Python 3.7+

cryptography, pandas (install via pip)

g++ compiler (for C/C++)

Java (for .java file execution)

🔒 Security Note

This system uses symmetric encryption with Fernet (from cryptography) to ensure that code files are securely transmitted over the network. While suitable for local secure networks, production environments should use additional validation and authentication mechanisms.

📌 Future Improvements

Add NLP-based static analysis to classify code behavior

Implement certificate-based authentication for clients

Include a GUI dashboard for real-time monitoring

Dockerize clients and server for easier deployment

👨‍💻 Author

Romith Pagadala

📄 License

This project is licensed under the MIT License.

