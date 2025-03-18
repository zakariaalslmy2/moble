import subprocess
import os
# أولاً، سنقوم بإنشاء برنامج لإنشاء قائمة كلمات المرور باستخدام crunch:
def create_password_list():
    try:
        # إنشاء قائمة كلمات المرور باستخدام crunch
        output_path = os.path.expanduser('passList.txt')
        cmd = f"crunch 4 7 abcde@#1234 -o {output_path}"
        subprocess.run(cmd, shell=True)
        print(f"تم إنشاء ملف كلمات المرور في: {output_path}")
        
        # عرض حجم الملف
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # تحويل إلى ميجابايت
        print(f"حجم الملف: {file_size:.2f} MB")
        
    except Exception as e:
        print(f"حدث خطأ: {e}")


# دالة لتنفيذ أوامر الشبكة الأساسية:
def network_commands():
    commands = {
        'ipconfig': 'عرض واجهات الشبكة وعناوين IP',
        'netstat -a': 'عرض جميع المنافذ المفتوحة',
        'netstat -tupln': 'عرض المنافذ المفتوحة مع البرامج المرتبطة',
    }
    
    for cmd, desc in commands.items():
        print(f"\nتنفيذ: {desc}")
        print("-" * 50)
        try:
            output = subprocess.check_output(cmd, shell=True).decode()
            print(output)
        except Exception as e:
            print(f"خطأ في تنفيذ {cmd}: {e}")
# دالة لفحص الثغرات باستخدام Nmap:
def nmap_scan(target):
    try:
        # فحص أساسي باستخدام Nmap
        print(f"\nجاري فحص {target} باستخدام Nmap...")
        cmd = f"nmap -sV -sC {target}"
        output = subprocess.check_output(cmd, shell=True).decode()
        print(output)
        
    except Exception as e:
        print(f"خطأ في تنفيذ Nmap: {e}")
# دالة لتنفيذ هجمات كسر كلمات المرور باستخدام Hydra:
def hydra_attack(target, users_file, passwords_file):
    try:
        # هجوم SSH باستخدام Hydra
        print(f"\nجاري تنفيذ هجوم Hydra على {target}...")
        cmd = f"hydra -L {users_file} -P {passwords_file} ssh://{target} -t 10 -V"
        output = subprocess.check_output(cmd, shell=True).decode()
        print(output)
        
    except Exception as e:
        print(f"خطأ في تنفيذ Hydra: {e}")
# الدالة الرئيسية التي تجمع كل الوظائف:
def main():
    print("=== برنامج فحص الثغرات الأمنية ===")
    
    # إنشاء قائمة كلمات المرور
    create_password_list()
    
    # تنفيذ أوامر الشبكة
    network_commands()
    
    # طلب عنوان IP الهدف من المستخدم
    target = input("\nأدخل عنوان IP الهدف: ")
    
    # فحص الثغرات باستخدام Nmap
    nmap_scan(target)
    
    # إعداد ملفات المستخدمين وكلمات المرور
    users_file = input("أدخل مسار ملف المستخدمين: ")
    passwords_file = input("أدخل مسار ملف كلمات المرور: ")
    
    # تنفيذ هجوم Hydra
    hydra_attack(target, users_file, passwords_file)

if __name__ == "__main__":
    main()


# # مسح الشبكة والمنافذ باستخدام بايثون:

# # مكتبة socket:

# # يمكنك استخدام هذه المكتبة لمسح المنافذ على جهاز معين والتحقق من كونها مفتوحة أم لا.

import socket

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((ip, port))
        print(f"Port {port} is open on {ip}")
        s.close()
    except:
        pass

ip = '192.168.1.1'  # ضع عنوان IP المراد مسحه
for port in range(1, 1025):
    scan_port(ip, port)




# # مكتبة scapy:

# # أداة قوية للتعامل مع حزم الشبكة، يمكنك استخدامها لمسح الشبكات ورصد الاتصالات.
    
# from scapy.all import ARP, Ether, srp

# def scan_network(ip_range):
#     arp = ARP(pdst=ip_range)
#     ether = Ether(dst="ff:ff:ff:ff:ff:ff")
#     packet = ether/arp
#     result = srp(packet, timeout=3, verbose=0)[0]

#     devices = []
#     for sent, received in result:
#         devices.append({'ip': received.psrc, 'mac': received.hwsrc})

#     for device in devices:
#         print(f"IP: {device['ip']}, MAC: {device['mac']}")

# scan_network("192.168.1.0/24")  # ضع نطاق الشبكة المناسب

# # اختبار قوة كلمات المرور (بشكل أخلاقي):

# # تحليل وتجربة كلمات المرور:

# # يمكنك كتابة سكربت يقوم بتحليل كلمات المرور المحتملة بناءً على معايير معينة، ولكن تذكر دائمًا أن هذا يجب أن يكون لأغراض تعليمية وبإذن صريح.

# # مثال لتحليل قوة كلمة المرور:

# import re

# def check_password_strength(password):
#     length_error = len(password) < 8
#     digit_error = re.search(r"\d", password) is None
#     uppercase_error = re.search(r"[A-Z]", password) is None
#     lowercase_error = re.search(r"[a-z]", password) is None
#     symbol_error = re.search(r"[ @!#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

#     errors = [length_error, digit_error, uppercase_error, lowercase_error, symbol_error]

#     strength = 5 - sum(errors)

#     if strength == 5:
#         return "Strong Password"
#     elif 3 <= strength < 5:
#         return "Medium Strength Password"
#     else:
#         return "Weak Password"

# password = input("Enter a password to check its strength: ")
# print(check_password_strength(password))


# # الخطوات المقترحة لتنفيذ الواجب:

# # قراءة وفهم الأوامر والأدوات:

# # ابحث عن وثائق ومصادر تعليمية تشرح كيفية عمل ifconfig وnetstat وnmap وHydra وhashcat.

# # تنفيذ الأوامر على بيئة افتراضية:

# # جرب تنفيذ الأوامر على نظام Kali Linux مثبت على جهاز افتراضي.

# # قم بتدوين الملاحظات والنتائج التي تحصل عليها.

# # أتمتة المهام باستخدام بايثون:

# # اكتب سكربتات بايثون لأتمتة بعض العمليات مثل مسح المنافذ أو تحليل كلمات المرور.

# # تأكد من فهمك لكيفية عمل هذه السكربتات والهدف منها.


# import socket
# import subprocess
# import platform
# import threading
# import time
# import hashlib
# from datetime import datetime

# class NetworkScanner:
#     def __init__(self):
#         self.host = socket.gethostname()
#         self.local_ip = socket.gethostbyname(self.host)
        
#     def get_network_info(self):
#         """Similar to ifconfig/ipconfig"""
#         print("\n=== Network Interface Information ===")
#         print(f"Hostname: {self.host}")
#         print(f"Local IP: {self.local_ip}")
        
#         # Get all network interfaces
#         try:
#             if platform.system() == "Windows":
#                 output = subprocess.check_output("ipconfig", shell=True).decode()
#             else:
#                 output = subprocess.check_output("ifconfig", shell=True).decode()
#             print("\nNetwork Interfaces:")
#             print(output)
#         except:
#             print("Could not get network interface details")

#     def ping_host(self, target_ip):
#         """Simple ping implementation"""
#         try:
#             if platform.system() == "Windows":
#                 output = subprocess.check_output(f"ping -n 1 {target_ip}", shell=True).decode()
#             else:
#                 output = subprocess.check_output(f"ping -c 1 {target_ip}", shell=True).decode()
#             if "TTL=" in output or "ttl=" in output:
#                 return True
#             return False
#         except:
#             return False

#     def scan_ports(self, target_ip, port_range=(1, 1024)):
#         """Simple port scanner"""
#         open_ports = []
#         for port in range(port_range[0], port_range[1]):
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.settimeout(1)
#             result = sock.connect_ex((target_ip, port))
#             if result == 0:
#                 open_ports.append(port)
#             sock.close()
#         return open_ports

# class PasswordTester:
#     def __init__(self):
#         self.common_passwords = ["password", "123456", "admin", "test123"]
        
#     def generate_hash(self, password):
#         """Generate MD5 hash of password"""
#         return hashlib.md5(password.encode()).hexdigest()
    
#     def test_password_strength(self, password):
#         """Simple password strength checker"""
#         score = 0
#         if len(password) >= 8: score += 1
#         if any(c.islower() for c in password): score += 1
#         if any(c.isupper() for c in password): score += 1
#         if any(c.isdigit() for c in password): score += 1
#         if any(not c.isalnum() for c in password): score += 1
#         return score

# def main():
#     print("=== Network Security Lab Demo ===")
    
#     # Initialize scanner
#     scanner = NetworkScanner()
#     scanner.get_network_info()
    
#     # Scan local network
#     print("\n=== Scanning Local Network ===")
#     base_ip = ".".join(scanner.local_ip.split(".")[:-1]) + "."
#     for i in range(1, 5):  # Scan first 5 IPs
#         target = base_ip + str(i)
#         if scanner.ping_host(target):
#             print(f"Host {target} is up")
#             ports = scanner.scan_ports(target, (20, 25))  # Scan common ports
#             if ports:
#                 print(f"Open ports: {ports}")

#     # Password testing demo
#     print("\n=== Password Testing Demo ===")
#     pw_tester = PasswordTester()
#     test_passwords = ["password123", "P@ssw0rd!", "abc123", "StrongP@ss99"]
    
#     for password in test_passwords:
#         strength = pw_tester.test_password_strength(password)
#         print(f"\nPassword: {password}")
#         print(f"Strength score (0-5): {strength}")
#         print(f"Hash: {pw_tester.generate_hash(password)}")

# if __name__ == "__main__":
#     main()