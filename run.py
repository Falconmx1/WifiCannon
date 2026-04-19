#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WifiCannon - Main Entry Point

import os
import sys
import platform

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def banner():
    banner_text = r"""
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║      ██     ██ ██ ███████ ██ ██████   █████          ║
    ║      ██     ██ ██ ██      ██ ██   ██ ██   ██         ║
    ║      ██  █  ██ ██ █████   ██ ██████  ██   ██         ║
    ║      ██ ███ ██ ██ ██      ██ ██   ██ ██   ██         ║
    ║       ███ ███  ██ ██      ██ ██   ██  █████          ║
    ║                                                      ║
    ║          ⚡ Cross-platform WiFi Attack Tool ⚡        ║
    ║         For authorized security testing only        ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner_text)

def show_menu():
    print("\n[ MAIN MENU ]")
    print("1. Scan for WiFi networks")
    print("2. Capture Handshake (WPA/WPA2)")
    print("3. PMKID Attack")
    print("4. Evil Twin Attack")
    print("5. WPS Brute Force")
    print("6. Deauth Attack")
    print("7. About & System Info")
    print("0. Exit")

def main():
    clear_screen()
    banner()
    print(f"\n[+] Platform detected: {platform.system()} {platform.release()}")
    print("[+] WifiCannon is ready. Use it responsibly.\n")
    
    while True:
        show_menu()
        try:
            choice = input("\n[?] Select an option: ")
            if choice == "0":
                print("[!] Exiting WifiCannon. Stay legal.")
                sys.exit(0)
            elif choice == "1":
                print("\n[+] Scanning networks (module not yet implemented)...")
                input("[?] Press Enter to continue...")
            elif choice == "2":
                print("\n[+] Capturing handshake (module not yet implemented)...")
                input("[?] Press Enter to continue...")
            elif choice == "3":
                print("\n[+] PMKID attack (module not yet implemented)...")
                input("[?] Press Enter to continue...")
            elif choice == "4":
                print("\n[+] Evil Twin attack (module not yet implemented)...")
                input("[?] Press Enter to continue...")
            elif choice == "5":
                print("\n[+] WPS brute force (module not yet implemented)...")
                input("[?] Press Enter to continue...")
            elif choice == "6":
                print("\n[+] Deauth attack (module not yet implemented)...")
                input("[?] Press Enter to continue...")
            elif choice == "7":
                print("\n[+] WifiCannon v0.1-alpha")
                print("    Developed by Falconmx1")
                print("    GitHub: https://github.com/Falconmx1/WifiCannon")
                print("    License: MIT")
                input("[?] Press Enter to continue...")
            else:
                print("[!] Invalid option. Try again.")
        except KeyboardInterrupt:
            print("\n[!] Interrupted. Exiting.")
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] Error: {e}")
            input("[?] Press Enter to continue...")
        clear_screen()
        banner()

if __name__ == "__main__":
    main()
