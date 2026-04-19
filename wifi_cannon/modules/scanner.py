#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WifiCannon - WiFi Scanner Module

import subprocess
import re
import time
import os
import platform

class WiFiScanner:
    def __init__(self):
        self.interface = None
        self.is_linux = platform.system() == "Linux"
        
    def get_wifi_interfaces(self):
        """Detecta interfaces WiFi disponibles"""
        interfaces = []
        try:
            if self.is_linux:
                # Linux: usar iwconfig
                result = subprocess.run(['iwconfig'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'IEEE 802.11' in line:
                        iface = line.split()[0]
                        interfaces.append(iface)
            else:
                # Windows: usar netsh
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Nombre' in line or 'Name' in line:
                        iface = line.split(':')[-1].strip()
                        interfaces.append(iface)
        except Exception as e:
            print(f"[!] Error detecting interfaces: {e}")
        return interfaces
    
    def enable_monitor_mode(self, interface):
        """Activa modo monitor (solo Linux)"""
        if not self.is_linux:
            print("[!] Monitor mode only available on Linux")
            return False
        
        try:
            print(f"[+] Killing conflicting processes...")
            subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], check=False)
            
            print(f"[+] Enabling monitor mode on {interface}...")
            result = subprocess.run(['sudo', 'airmon-ng', 'start', interface], 
                                  capture_output=True, text=True)
            
            # Detectar nueva interfaz (ej: wlan0mon)
            for line in result.stdout.split('\n'):
                if 'monitor mode enabled' in line.lower():
                    # Extraer nombre de la interfaz monitor
                    parts = line.split()
                    for part in parts:
                        if 'mon' in part or 'wlan' in part:
                            self.interface = part
                            break
            
            if not self.interface:
                self.interface = f"{interface}mon"
            
            print(f"[+] Monitor mode enabled: {self.interface}")
            return True
            
        except Exception as e:
            print(f"[!] Error enabling monitor mode: {e}")
            return False
    
    def scan_networks(self, interface, duration=15):
        """Escanea redes WiFi cercanas"""
        print(f"[+] Scanning networks on {interface} for {duration} seconds...")
        
        # Crear archivo temporal para la salida
        temp_file = f"/tmp/wificannon_scan_{int(time.time())}"
        
        try:
            if self.is_linux:
                # Usar airodump-ng en Linux
                cmd = ['sudo', 'airodump-ng', '--write', temp_file, '--output-format', 'csv', interface]
                process = subprocess.Popen(cmd, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                time.sleep(duration)
                process.terminate()
                time.sleep(2)
                
                # Parsear el CSV generado
                networks = self._parse_airodump_csv(f"{temp_file}-01.csv")
                
                # Limpiar archivos temporales
                subprocess.run(['rm', '-f', f"{temp_file}*"], check=False)
                
            else:
                # Windows: usar netsh (modo monitor limitado)
                networks = self._netsh_scan()
            
            return networks
            
        except Exception as e:
            print(f"[!] Scan error: {e}")
            return []
    
    def _parse_airodump_csv(self, csv_file):
        """Parsea el CSV generado por airodump-ng"""
        networks = []
        try:
            with open(csv_file, 'r') as f:
                lines = f.readlines()
            
            in_ap_section = False
            for line in lines:
                if 'BSSID' in line and 'PWR' in line:
                    in_ap_section = True
                    continue
                
                if in_ap_section and line.strip() and not line.startswith(','):
                    parts = line.strip().split(',')
                    if len(parts) >= 8:
                        bssid = parts[0].strip()
                        if bssid and ':' in bssid and bssid != 'BSSID':
                            network = {
                                'bssid': bssid,
                                'channel': parts[3].strip(),
                                'signal': parts[5].strip(),
                                'encryption': parts[6].strip(),
                                'essid': parts[13].strip() if len(parts) > 13 else 'Hidden'
                            }
                            networks.append(network)
        except Exception as e:
            print(f"[!] Error parsing scan results: {e}")
        
        return networks
    
    def _netsh_scan(self):
        """Escaneo básico en Windows"""
        networks = []
        try:
            print("[+] Running netsh scan (Windows mode)...")
            subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], 
                         capture_output=True, text=True)
            
            # Parseo básico de netsh (simplificado)
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'], 
                                  capture_output=True, text=True)
            
            current_ssid = None
            for line in result.stdout.split('\n'):
                if 'SSID' in line and ':' in line:
                    current_ssid = line.split(':')[-1].strip()
                elif 'BSSID' in line and ':' in line and current_ssid:
                    bssid = line.split(':')[-1].strip()
                    networks.append({
                        'bssid': bssid,
                        'channel': 'N/A',
                        'signal': 'N/A',
                        'encryption': 'WPA/WPA2',
                        'essid': current_ssid
                    })
        except Exception as e:
            print(f"[!] Netsh scan error: {e}")
        
        return networks
    
    def display_networks(self, networks):
        """Muestra las redes en formato bonito"""
        if not networks:
            print("[!] No networks found")
            return
        
        print(f"\n[+] Found {len(networks)} networks:\n")
        print(f"{'No.':<4} {'BSSID':<20} {'Channel':<8} {'Signal':<8} {'Encryption':<15} {'ESSID':<20}")
        print("-" * 85)
        
        for idx, net in enumerate(networks, 1):
            print(f"{idx:<4} {net['bssid']:<20} {net['channel']:<8} {net['signal']:<8} {net['encryption']:<15} {net['essid']:<20}")
        
        return networks

def run():
    """Función principal del módulo scanner"""
    print("\n[🔍 WifiCannon - WiFi Scanner Module]\n")
    
    scanner = WiFiScanner()
    
    # Detectar interfaces
    interfaces = scanner.get_wifi_interfaces()
    if not interfaces:
        print("[!] No WiFi interfaces found")
        return
    
    print(f"[+] Available interfaces: {', '.join(interfaces)}")
    
    if scanner.is_linux:
        # En Linux, preguntar si usar modo monitor
        use_monitor = input("[?] Enable monitor mode for deeper scan? (y/n): ").lower()
        if use_monitor == 'y':
            iface = input(f"[?] Select interface ({interfaces[0]}): ") or interfaces[0]
            if scanner.enable_monitor_mode(iface):
                networks = scanner.scan_networks(scanner.interface, 20)
            else:
                print("[!] Using managed mode scan (limited)")
                networks = scanner.scan_networks(iface, 15)
        else:
            iface = input(f"[?] Select interface ({interfaces[0]}): ") or interfaces[0]
            networks = scanner.scan_networks(iface, 15)
    else:
        # Windows: escaneo básico
        networks = scanner.scan_networks(None, 0)
    
    scanner.display_networks(networks)
    
    if networks:
        save = input("\n[?] Save results to file? (y/n): ").lower()
        if save == 'y':
            filename = f"wificannon_scan_{int(time.time())}.txt"
            with open(filename, 'w') as f:
                for net in networks:
                    f.write(f"{net['bssid']} | {net['essid']} | Ch:{net['channel']} | {net['signal']} | {net['encryption']}\n")
            print(f"[+] Results saved to {filename}")
    
    input("\n[?] Press Enter to continue...")

if __name__ == "__main__":
    run()
