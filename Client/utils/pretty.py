from colorama import init, Fore, Style
import time
import os

def console_welcome():
    init()
    
    banner = f"""{Fore.RED}
╔═══════════════════════════════════════════════════╗
║ ╔═╗╦  ╔═╗╦ ╦  ╦ ╦╔═╗╦ ╦╦═╗  ╔╦╗╦ ╦╔╗╔╔═╗╔═╗╔═╗╔╗╔ ║
║ ╠═╝║  ╠═╣╚╦╝  ╚╦╝║ ║║ ║╠╦╝   ║║║ ║║║║║ ╦║╣ ║ ║║║║ ║
║ ╩  ╩═╝╩ ╩ ╩    ╩ ╚═╝╚═╝╩╚═  ═╩╝╚═╝╝╚╝╚═╝╚═╝╚═╝╝╚╝ ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}"""
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.1)
    
    print(f"\n{Fore.YELLOW}Welcome brave adventurer to your destiny!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Prepare yourself for an epic journey...{Style.RESET_ALL}\n")
    
    print("Loading your adventure", end="")
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\n")

def console_login():
    """Handle user login with colored prompts and validation"""
    init()
    
    while True:
        print(f"\n{Fore.GREEN}╔════ LOGIN ════╗{Style.RESET_ALL}")
        username = input(f"{Fore.CYAN}Username: {Style.RESET_ALL}").strip()
        
        if not username:
            print(f"{Fore.RED}Username cannot be empty!{Style.RESET_ALL}")
            continue
            
        password = input(f"{Fore.CYAN}Password: {Style.RESET_ALL}").strip()
        
        if not password:
            print(f"{Fore.RED}Password cannot be empty!{Style.RESET_ALL}")
            continue

        print(f"\n{Fore.YELLOW}Validating credentials", end="")
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
            
        if len(username) >= 3 and len(password) >= 4:
            print(f"\n{Fore.GREEN}Login successful! Welcome {username}!{Style.RESET_ALL}\n")
            return username, password
        else:
            print(f"\n{Fore.RED}Invalid credentials! Username must be at least 3 characters and password at least 4 characters.{Style.RESET_ALL}")

def pretty_print(string: str, color: str = Fore.WHITE):
    print(f"{color}{string}{Style.RESET_ALL}")
