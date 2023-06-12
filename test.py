import subprocess
import socket
import os

def resolve_ip_address(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror:
        print(f"Error: Failed to resolve IP address for {domain_name}")
        return None

def run_nmap_basic(project_code, ip_address, output_dir):
    print(f"Running basic Nmap scan on {ip_address}...")
    command = f"nmap {ip_address} -oA {output_dir}/{project_code}_nmap_basic"
    subprocess.run(command, shell=True)
    print(f"Scan results saved to {output_dir}/{project_code}_nmap_basic files")

def run_nmap_full(project_code, ip_address, output_dir):
    print(f"Running full port scan using Nmap on {ip_address}...")
    command = f"nmap -p- {ip_address} -oA {output_dir}/{project_code}_nmap_full"
    subprocess.run(command, shell=True)
    print(f"Scan results saved to {output_dir}/{project_code}_nmap_full files")

def run_dig(project_code, ip_address, output_dir):
    print(f"Running dig command on {ip_address}...")
    command = f"dig {ip_address} > {output_dir}/{project_code}_dig.txt"
    subprocess.run(command, shell=True)
    print(f"Dig results saved to {output_dir}/{project_code}_dig.txt")

# Main program
if __name__ == "__main__":
    project_code = input("Enter the project code: ")

    file_path = "targets.txt"
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist. Please create the 'targets.txt' file.")
        exit(1)

    output_dir = project_code
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory created: {output_dir}")

    with open(file_path, 'r') as file:
        targets = [line.strip() for line in file]

    if len(targets) == 0:
        print(f"Error: File '{file_path}' is empty. Please add IP addresses or domain names.")
        exit(1)

    for target in targets:
        # Resolve domain name to IP address if a domain name is provided
        if not target.replace(".", "").isdigit():
            ip_address = resolve_ip_address(target)
            if ip_address is None:
                continue
        else:
            ip_address = target

        print(f"\nScanning target: {target} ({ip_address})")
        run_nmap_basic(project_code, ip_address, output_dir)
        run_nmap_full(project_code, ip_address, output_dir)
        run_dig(project_code, ip_address, output_dir)
