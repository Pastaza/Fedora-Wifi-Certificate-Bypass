#!/usr/bin/env python3
"""
N4L Secure Access Wi-Fi Certificate Installer
For Asahi Linux (Fedora) with KDE Plasma

Uses native KDE dialogs (kdialog) for a seamless desktop experience.
No additional Python packages required.
"""

import subprocess
import sys
import os
import shutil

TITLE = "N4L Secure Access Installer"
CERT_DEST_DIR = "/etc/pki/ca-trust/source/anchors"


def run_kdialog(args):
    """Run a kdialog command and return the result."""
    try:
        return subprocess.run(["kdialog"] + args, capture_output=True, text=True)
    except FileNotFoundError:
        print("Error: kdialog not found. Install it with: sudo dnf install kdialog")
        sys.exit(1)


def show_info(message):
    run_kdialog(["--title", TITLE, "--msgbox", message])


def show_error(message):
    run_kdialog(["--title", TITLE, "--error", message])


def show_warning(message):
    run_kdialog(["--title", TITLE, "--sorry", message])


def select_certificate():
    """Open a native KDE file picker to select a certificate file."""
    result = run_kdialog([
        "--title", "Select your N4L Certificate",
        "--getopenfilename",
        os.path.expanduser("~"),
        "Certificate Files (*.crt *.pem *.cer)\nAll Files (*)",
    ])

    if result.returncode != 0 or not result.stdout.strip():
        return None

    return result.stdout.strip()


def install_certificate(cert_path):
    """Install the certificate to the Fedora system trust store via pkexec."""
    filename = os.path.basename(cert_path)
    dest_path = os.path.join(CERT_DEST_DIR, filename)

    command = [
        "pkexec", "sh", "-c",
        f'cp "{cert_path}" "{dest_path}" && chmod 644 "{dest_path}" && update-ca-trust',
    ]

    try:
        return subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        show_error(f"An unexpected error occurred:\n{e}")
        return None


def main():
    # Preflight checks
    if not shutil.which("kdialog"):
        print("Error: kdialog is not installed.")
        print("Install it with: sudo dnf install kdialog")
        sys.exit(1)

    if not shutil.which("pkexec"):
        show_error(
            "pkexec is not available.\n\n"
            "Install polkit with:\n"
            "sudo dnf install polkit"
        )
        sys.exit(1)

    # Step 1 — Select the certificate file
    cert_path = select_certificate()

    if not cert_path:
        sys.exit(0)  # User cancelled the file picker

    if not os.path.isfile(cert_path):
        show_error(f"Selected file does not exist:\n{cert_path}")
        sys.exit(1)

    # Step 2 — Confirm before installing
    filename = os.path.basename(cert_path)
    confirm = run_kdialog([
        "--title", TITLE,
        "--yesno",
        f"Install the following certificate to the system trust store?\n\n"
        f"File: {filename}\n"
        f"Destination: {CERT_DEST_DIR}/",
    ])

    if confirm.returncode != 0:
        sys.exit(0)  # User declined

    # Step 3 — Install with privilege escalation
    result = install_certificate(cert_path)

    if result is None:
        sys.exit(1)

    if result.returncode == 0:
        show_info(
            "Certificate installed successfully!\n\n"
            "Open your Wi-Fi settings in KDE, select the\n"
            "N4L Secure Access network, and choose your\n"
            "newly installed certificate from the CA list."
        )
    elif result.returncode == 126:
        show_warning("Authentication was cancelled.")
    else:
        show_error(f"Failed to install certificate.\n\nDetails:\n{result.stderr}")


if __name__ == "__main__":
    main()
