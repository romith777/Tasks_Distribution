# 🔧 Task Distributor: Distributed Secure Code Execution System

Task Distributor is a Python-based system that securely distributes and executes code files (Python, C++, Java) across multiple machines on a local network. It enables parallel execution, encrypted communication, and centralized result collection — all built using Python.

---

## 🚀 Features

- **Distributed Execution** – Sends tasks to multiple clients for concurrent execution
- **End-to-End Encryption** – Uses `cryptography` to securely transfer files
- **Parallel Processing** – Uses `threading` to manage multiple clients simultaneously
- **Multi-language Support** – Executes `.py`, `.cpp`, and `.java` files
- **Execution & Logging** – Collects execution results and logs them using `pandas`

---

## ⚙️ How It Works

1. **Task Distribution**  
   The server scans the `tasks/` folder and assigns code files to clients in a round-robin manner.

2. **Secure Communication**  
   Files are encrypted using Fernet encryption and decrypted by the client before execution.

3. **Code Execution**  
   Clients run:
   - `.py` files with Python  
   - `.cpp`/`.c` files with `g++`  
   - `.java` files with `javac` and `java`

4. **Result Collection**  
   Each client sends back output and status, which the server stores in a pandas DataFrame and saves in `received_output/`.

---

## 🧰 Tech Stack

**Developed In:**  
Python

**Supported Languages for Execution:**  
Python, C/C++, Java

**Core Technologies:**  
Socket Programming, Cryptography (Fernet), Multithreading, Subprocess Execution, Pandas

**Python Libraries Used:**  
- `socket`  
- `cryptography`  
- `threading`  
- `subprocess`  
- `pandas`  
- `os`, `sys`

---

## ✅ Requirements

- Python 3.x
- g++ (for compiling C/C++ files)
- JDK (for compiling and running Java files)
- Install Python dependencies:  
  ```bash
  pip install cryptography pandas

## 🔒 Security Note

This system uses symmetric encryption with Fernet (from `cryptography`) to ensure that code files are securely transmitted over the network. While suitable for local secure networks, production environments should use additional validation and authentication mechanisms.

---

## 📌 Future Improvements

- Add NLP-based static analysis to classify code behavior  
- Implement certificate-based authentication for clients  
- Include a GUI dashboard for real-time monitoring  
- Dockerize clients and server for easier deployment

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
