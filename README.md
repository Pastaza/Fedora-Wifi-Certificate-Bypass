# N4L Secure Access Wi-Fi Installer for Linux

A lightweight, native Python application that helps Linux users easily install their unique N4L Secure Access certificates. It provides a simple graphical flow using native KDE dialogs and securely installs certificates to the system trust store, automatically handling privilege escalation via `pkexec`.

## Features
- **KDE Native**: Uses `kdialog` for file selection and prompts — looks and feels like part of your desktop.
- **System Native**: Escalates privileges using Linux's native Polkit (`pkexec`) to prompt for your password securely.
- **Zero Dependencies**: Only needs Python 3 (pre-installed) and `kdialog` (pre-installed on KDE Plasma). No `pip install` required.
- **Easy Sharing**: It's a single Python file, making it easy to distribute to your classmates or friends on Linux.

## Target Platform
- **Asahi Linux** (Fedora Remix) with **KDE Plasma**
- Should also work on any Fedora-based distro with KDE Plasma

## Requirements
Python 3 and `kdialog` are pre-installed on Fedora KDE Plasma. No extra packages should be needed.

If for some reason `kdialog` is missing:
```bash
sudo dnf install kdialog
```

## Usage
1. Make the script executable (if it isn't already):
```bash
chmod +x n4l_installer.py
```
2. Run the application:
```bash
./n4l_installer.py
```
3. A native KDE file picker will open — select your `.crt`, `.pem`, or `.cer` file.
4. Confirm the installation. You will be prompted for your password to install the certificate to the system trust store.

## Post-Installation
Once the certificate is successfully installed, open your Wi-Fi settings in **KDE System Settings → Network → Wi-Fi**, select the N4L Secure Access Wi-Fi network, and choose your newly installed certificate from the **CA Certificate** dropdown list.