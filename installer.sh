#!/bin/bash

# Update & Upgrade Sistem
echo "Updating and upgrading system..."
sudo apt update && sudo apt upgrade -y

# Install Nginx
echo "Installing Nginx..."
sudo apt install -y nginx
sudo systemctl enable --now nginx

# Konfigurasi Firewall
echo "Configuring firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw allow 1935/tcp
sudo ufw allow 5000
echo "y" | sudo ufw enable

# Pindah ke Direktori Web
WEB_DIR="/var/www/html/badutpanel"
if [ ! -d "$WEB_DIR" ]; then
    echo "Cloning repository..."
    sudo git clone https://github.com/orlin24/badutpanel.git "$WEB_DIR"
else
    echo "Repository already exists, pulling latest changes..."
    cd "$WEB_DIR" && sudo git pull
fi

# Beri Izin Akses ke Folder
echo "Setting folder permissions..."
sudo chmod -R 777 "$WEB_DIR"

# Set Zona Waktu
echo "Setting timezone to Asia/Jakarta..."
sudo timedatectl set-timezone Asia/Jakarta

# Install Dependencies
echo "Installing dependencies..."
sudo apt install -y python3.10-venv ffmpeg

# Buat Virtual Environment dan Install Packages
cd "$WEB_DIR"
echo "Creating virtual environment and installing Python packages..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask_cors Flask Flask-Admin flask-login Flask-SQLAlchemy Flask-Migrate Flask-Dotenv Flask-Limiter python-dotenv

echo "Starting application..."
python3 app.py
