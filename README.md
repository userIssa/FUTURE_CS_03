# FUTURE_CS_03
# 🔐 Secure File Sharing System  

A simple yet secure **file sharing system** built with **Flask** and **AES encryption**.  
Users can:  
- Upload files (automatically encrypted using AES-256).  
- Download either the **encrypted** version or the **decrypted original**.  

This project simulates real-world secure file transfer in environments like healthcare, corporate, and legal industries where **data security is critical**.  

---

## ✨ Features  
- ✔ Secure file **upload & encryption** (AES-256, CBC mode)  
- ✔ Download **encrypted** files for secure storage or sharing  
- ✔ Download **decrypted** files to restore the original content  
- ✔ Simple, clean **Bootstrap interface**  
- ✔ No decrypted files are stored on the server — they are streamed to the user directly  

---

## 📂 Project Structure
secure_file_share/
│── app.py # Flask app (routes & logic)
│── encryption.py # AES encryption & decryption functions
│── uploads/ # Stores encrypted files
│── templates/
│ └── index.html # Web UI

---

## 🚀 Getting Started  

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/secure-file-share.git
cd secure-file-share
```

### 2️⃣ Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

### 3️⃣ Install dependencies
```bash
pip install flask pycryptodome
```

### 4️⃣ Run the app
```bash
python app.py
```
### 5️⃣ Open in browser
Go to: http://127.0.0.1:5000

---

## 🔑 Security Overview
- Encryption Algorithm: AES-256 in CBC mode
- Key Handling: A single static key (for demo purposes)
- In production, keys should be managed with a Key Management System (KMS) or environment variables
- IV Handling: Each file uses a random IV, stored alongside the ciphertext
- Decryption: Performed in memory and streamed back to the client

---

## 🛠 Tools Used
Flask
 – Web framework
PyCryptodome
 – AES encryption
Bootstrap 5
 – Frontend styling

 ---

 ## 📹 Deliverables
 - GitHub repository with clean, commented code
 - Walkthrough video showing file upload, encryption, and download
 - Security overview document (this README’s Security Overview section)

--- 

## ⚠️ Disclaimer
This project is for educational purposes only.
For production use, implement:
- Strong key management (e.g., AWS KMS, HashiCorp Vault)
- Authentication & access control
- HTTPS for secure transport
