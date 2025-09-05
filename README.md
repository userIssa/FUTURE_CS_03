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

Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

