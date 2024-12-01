from colorama import Fore
from utils.pretty import pretty_print
from getpass import getpass
from api_client import APIClient
import asyncio

async def login():
    pretty_print("╔═══════ RETURN TO YOUR QUEST ═══════╗", Fore.GREEN)
    async with APIClient() as client:
        while True:
            username = input("Brave adventurer, state your name: ").strip()
            password = getpass("Speak thy secret password: ").strip()
            
            if not all([username, password]):
                pretty_print("A hero must have both name and password!", Fore.RED)
                continue
                
            try:
                response = await client.login(username, password)
                if "user_id" in response:
                    pretty_print(f"Welcome back, mighty {username}!", Fore.GREEN)
                    return response["user_id"], username
                else:
                    pretty_print("Invalid credentials! Try again.", Fore.RED)
            except Exception as e:
                pretty_print(f"Login failed: {str(e)}", Fore.RED)

async def register():
    pretty_print("╔═══════ BEGIN YOUR EPIC JOURNEY ═══════╗", Fore.GREEN)
    async with APIClient() as client:
        while True:
            username = input("Declare your hero's name: ").strip()
            password = getpass("Create your mystical password: ").strip()
            email = input("Your magical contact scroll (email): ").strip()
            f_name = input("Your given name: ").strip()
            l_name = input("Your family name: ").strip()
            
            user_data = {
                "username": username,
                "password": password,
                "email": email,
                "f_name": f_name,
                "l_name": l_name
            }
            
            try:
                response = await client.register(user_data)
                if "user_id" in response:
                    pretty_print("Registration successful!", Fore.GREEN)
                    return response["user_id"], username
                else:
                    pretty_print("Registration failed! Try again.", Fore.RED)
            except Exception as e:
                pretty_print(f"Registration failed: {str(e)}", Fore.RED)

async def login_or_register():
    pretty_print("╔═══════ DESTINY AWAITS ═══════╗", Fore.GREEN)
    while True:
        choice = input("(1) Login \n(2) Register\n=> ").strip()
        
        if choice == "1":
            return await login()
        elif choice == "2":
            return await register()
        else:
            pretty_print("Invalid choice! Choose 1 or 2", Fore.RED)