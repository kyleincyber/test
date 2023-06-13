import subprocess
import socket
import os

def resolve_ip_address(domain_name):
    # Resolve domain name to IP address
    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror:
        print(f"Error: Failed to resolve IP address for {domain_name}")
        return None

def run_nmap_basic(project_code, ip_address, output_dir):
    # Perform basic Nmap scan
    print(f"\nRunning basic Nmap scan on {ip_address}...")
    command = f"nmap {ip_address} -oA {output_dir}/{project_code}_nmap_basic"
    print(f"Command: {command}")  # Print the Nmap command being executed
    subprocess.run(command, shell=True)  # Execute the Nmap command
    print(f"Scan results saved to {output_dir}/{project_code}_nmap_basic files")

def run_nmap_full(project_code, ip_address, output_dir):
    # Perform full port scan using Nmap
    print(f"\nRunning full port scan using Nmap on {ip_address}...")
    command = f"nmap -p- {ip_address} -oA {output_dir}/{project_code}_nmap_full"
    print(f"Command: {command}")  # Print the Nmap command being executed
    subprocess.run(command, shell=True)  # Execute the Nmap command
    print(f"Scan results saved to {output_dir}/{project_code}_nmap_full files")

def run_dig(project_code, ip_address, output_dir):
    # Run dig command for DNS lookup
    print(f"\nRunning dig command on {ip_address}...")
    command = f"dig {ip_address} > {output_dir}/{project_code}_dig.txt"
    print(f"Command: {command}")  # Print the dig command being executed
    subprocess.run(command, shell=True)  # Execute the dig command
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

    print("\nSelect which scans to run:")
    print("1. Basic Nmap Scan")
    print("2. Full Port Scan")
    print("3. DNS Lookup")
    print("4. Run All")

    selected_scans = input("Enter the scan numbers separated by commas (e.g., 1,2): ")
    selected_scans = selected_scans.split(",")

    for target in targets:
        # Resolve domain name to IP address if a domain name is provided
        if not target.replace(".", "").isdigit():
            ip_address = resolve_ip_address(target)
            if ip_address is None:
                continue
        else:
            ip_address = target

        print(f"\nScanning target: {target} ({ip_address})")

        if '1' in selected_scans or '4' in selected_scans:
            run_nmap_basic(project_code, ip_address, output_dir)

        if '2' in selected_scans or '4' in selected_scans:
            run_nmap_full(project_code, ip_address, output_dir)

        if '3' in selected_scans or '4' in selected_scans:
            run_dig(project_code, ip_address, output_dir)
