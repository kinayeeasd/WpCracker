##########################################
# -*- coding: utf-8 -*-  # Define the encoding of the script          #
# usr/bin/env/python  # Specify the interpreter for the script        #
# Err0r_HB  # Author information                                                #
# Cyb3r Drag0nz Team / ByteBlitz  # Team information                #
# Release Date: 03/12/2024 # Release date of the script          #
# Language: Python3  # Programming language used                    #
# Telegram: https:/t.me/DefacErr  # Contact information              #
# Pourpose: Combo maker  # Purpose of the script                       #
##########################################

"""
 *
 * Copyright (C) - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Err0r_HB <error_hb@protonmail.com>
 * Member and Co-Founder of Cyber Drag0nz / ByteBlitz Team
 *
 """
 
import os
import sys
import re
from pystyle import Colors, Colorate, Center

# Clearing the screen based on the operating system
if os.name == "nt":  # Checking if the OS is Windows
    os.system("cls")  # Clearing the screen for a fresh start
    os.system("color a") # Set the green color text output 
else:
    os.system("clear")  # Clearing the screen for Unix-based systems

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def extract_credentials(lines):
    credentials_set = set()
    for line in lines:
        line = line.strip()
        if line:
            # Regex to match URL with optional http/https scheme
            match = re.match(r'^(https?://)?([^:/]+)(:[0-9]+)?(:[^:]+:[^:]+)$', line)
            if match:
                # Extract the username:password part
                credentials = match.group(4)[1:]  # Remove the leading colon
                if 'http' not in credentials and 'www.' not in credentials:
                    credentials_set.add(credentials)
    return credentials_set

def write_output_file(credentials_set, output_file_path):
    with open(output_file_path, 'w') as file:
        for credential in credentials_set:
            file.write(credential + '\n')

def main(input_file_path=None, output_file_path=None):
    if not input_file_path:
        input_file_path = input("\033[1;93m\n[] Enter the path to the input file: ")
    if not output_file_path:
        output_file_path = input("\033[1;93m\n[] Enter the path to the output file: ")

    if not os.path.exists(input_file_path):
        print(f"`\n[] Error: The file {input_file_path} does not exist.")
        sys.exit(1)

    lines = read_input_file(input_file_path)
    credentials_set = extract_credentials(lines)
    write_output_file(credentials_set, output_file_path)
    print(f"\n\033[1;92m\n[] Credentials have been extracted and saved to {output_file_path}\n")

if __name__ == "__main__":
    banner = """
 ██████╗ ██████╗ ███╗   ███╗██████╗  ██████╗ 
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔═══██╗
██║     ██║   ██║██╔████╔██║██████╔╝██║   ██║
██║     ██║   ██║██║╚██╔╝██║██╔══██╗██║   ██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║██████╔╝╚██████╔╝
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝  ╚═════╝ """
    description = """
    This script performs the following tasks:
    ● Reads a list of URLs with credentials from a text file.
    ● Extracts the username and password from each URL.
    ● Ensures that the extracted credentials do not contain 'http', 'https', or 'www'.
    ● Saves the unique credentials to an output file without duplicates.
    ● Prompts the user for input and output file paths if not provided as arguments.
    """

    print(Colorate.Horizontal(Colors.red_to_yellow, Center.XCenter(banner)))
    print(Colorate.Horizontal(Colors.blue_to_green, Center.XCenter(description)))

    if len(sys.argv) == 3:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        main(input_file_path, output_file_path)
    else:
        main()