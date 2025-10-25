# Distributed File Replication Service 📁🔗

---

## 📘 Project Overview

The **Distributed File Replication Service** is a Python-based project that simulates a **distributed file system** with replication across multiple nodes.  

It allows clients to **upload files**, which are automatically replicated to **three separate nodes**, ensuring **availability, fault tolerance, and data reliability**. Clients can also **download files** from any node or the main data directory.  

This project demonstrates core **distributed systems concepts** such as replication, redundancy, and multi-client support.

---

## 🎯 SDG Alignment

This project aligns with the following **UN Sustainable Development Goals**:

| **SDG** | **Goal** | **How This Project Aligns** |
|:--------:|-----------|-----------------------------|
| **9** | *Industry, Innovation, and Infrastructure* | Builds resilient infrastructure using a distributed file system and demonstrates technological innovation through automated replication and fault tolerance. |
| **11** | *Sustainable Cities and Communities* | Supports reliable and distributed data storage, enabling smart and sustainable digital systems for city management, e-governance, or community services. |

---

## ⚙️ Setup and Installation

### 🧩 Prerequisites
- Python 3.8 or higher installed  
- Project folder contains `server/` and `client/` directories  

### 🚀 Setup

1. **Open the terminal:**
```bash
python server/server.py
You should see:
Server listening on 0.0.0.0:9000
```

▶️ Another Terminal
```bash
python client/client.py
```
Expected output:
```bash
Server response: UPLOAD_OK 3
The file will be replicated to:

📊 Sample Outputs
Upload Successful
Server response: UPLOAD_OK 3
Download Successful
```

📂 Project Structure
```bash
distributed-file-replication/
├── client/
│   └── client.py                
├── server/
│   ├── server.py                
│   ├── node1/                  
│   ├── node2/                 
│   └── node3/                  
├── data/                      
├── requirements.txt
```                
