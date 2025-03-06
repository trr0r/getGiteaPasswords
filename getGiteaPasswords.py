#!/usr/bin/env python3

# Author: Álvaro Bernal (aka. trr0r)

import argparse, sys, signal, os, sqlite3, hashlib, multiprocessing
from colorama import Fore, Style
from pwn import *
from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify
from concurrent.futures import ProcessPoolExecutor
from argformat import StructuredFormatter

# Global Variables
yellow = Fore.YELLOW
white = Fore.WHITE
blue = Fore.BLUE
cyan = Fore.CYAN
magenta = Fore.MAGENTA
red = Fore.RED  # Red Text
green = Fore.GREEN  # Green Text
bold = Style.BRIGHT  # Bold Text
reset = Style.RESET_ALL  # Reset Styles

# Control with user make an CTRL + C
def ctrl_c(key, event):
    print(f"\n{red}[!] Exiting... \n{reset}")
    sys.exit(1)

# Capture CTRL + C
signal.signal(signal.SIGINT, ctrl_c)

# Function to get arguments
def get_args():
    # "\u2620\ufe0f SSH Log Poisoning with LFI → Automated Reverse Shell \u2620\ufe0f\n\nej: python3 autopoison.py -u http://172.17.0.2/vuln.php -pm file -t-ip 172.17.0.1 -h-ip 172.17.0.2"
    parser = argparse.ArgumentParser(description=f"☕ {green + bold}Retrieve Gitea hashes stored in SQLite3 database with {magenta + bold}pbkdf2{reset}{green + bold} format.{reset} ☕ \n \n\n\t{blue + bold}Format{reset} {magenta + bold}pbkdf2{reset} {blue}hashes into hashcat format{reset} {red + bold}(Fastest Method){reset}:\n\t\t{white}❯ python3{reset} {blue}getGiteaPasswords.py{reset} {green}-d gitea.db{reset}\n\n\t{blue + bold}Crack hashes directly within the script{reset} {red + bold}(Slowest Method){reset}:\n\t\t{white}❯ python3{reset} {blue}getGiteaPasswords.py{reset} {green}-d gitea.db{reset} {red}-w rockyou.txt{reset} {yellow}--crack{reset}", formatter_class=StructuredFormatter)

    parser.add_argument("-d", f"--database", required=True, dest="sqlite_db", help=f"{blue + bold}SQLite3 database file{reset}")
    parser.add_argument("-w", "--wordlist", required=False, dest="wordlist", help=f"{red + bold}Wordlist file{reset}")
    parser.add_argument("-c", "--crack", action="store_true", help=f"{yellow + bold}Add this option to crack hashes in the script{reset}")
    parser.add_argument("-o", "--output", required=False, dest="output_file", help=f"{green + bold}Output file{reset}", default="hashes.txt")

    args = parser.parse_args()

    if args.crack and not args.wordlist:
        parser.error(f"{red + bold}--wordlist / -w{reset} {red}argument is required when using {bold}--crack{reset}")

    if not args.crack and args.wordlist:
        parser.error(f"{red + bold}--crack / -c{reset} {red}argument is required when using {bold}--wordlist{reset}")

    # Return arguments
    return [args.sqlite_db, args.wordlist, args.crack, args.output_file]

# Function to check if a file exists
def check_files_exists(filename):

    if not os.path.isfile(filename):
        print(f"\n{red}[!] {bold}{filename}{reset}{red} file doesn't exist{reset}")
        sys.exit(1)

# Function to get credentials stored in database file
def get_credentials(sqlite_db):
    try:
        credentials = []
        conn = sqlite3.connect(sqlite_db)

        cur = conn.cursor()

        res = cur.execute("SELECT name, passwd, salt, passwd_hash_algo from user")

        for row in res:
            if "pbkdf2" in row[3]:
                iterations = row[3].split("$")[1]
                row = [row[0], row[1], row[2], iterations]
                credentials.append(row)
            else:
                print(f"\n{red}[!] Unknown Algorithm: {bold}{row[3]}{reset}\n")
                sys.exit(1)

        return credentials
    except Exception as e:
        print(f"\n{red}[!] An error occurred: {bold}{e}{reset}\n")
        sys.exit(1)

# Function to save credentials to file
def save_credentials_to_file(credentials, output_file):
    p = log.progress("Saving hashes")
    f = open(output_file, "a")
    for credential in credentials:
        user = credential[0]
        digest = base64.b64encode(bytes.fromhex(credential[1])).decode("utf-8")
        salt =  base64.b64encode(bytes.fromhex(credential[2])).decode("utf-8")
        hash = f"{user}:sha256:{credential[3]}:{salt}:{digest}\n"
        f.write(hash)
    p.success("All hashes have been saved correctly")
    f.close()

# Function to check if hash_file exists, and delete it if true
def check_hashes_if_exists(hash_file):
    global bold, reset

    if os.path.isfile(hash_file):
        os.remove(hash_file)

def check_password(password, hash):
    user, algo, iterations, salt, stored_hash = hash.strip().split(":")
    salt = unhexlify(salt)
    iterations = int(iterations)
    password = password.encode("utf-8")

    hash_attempt = hashlib.pbkdf2_hmac(algo, password, salt, iterations, dklen=50)

    return (hash_attempt.hex() == stored_hash, user)

def check_password_wrapper(args):
    password, hash_stored = args
    result = check_password(password, hash_stored)
    if result[0]:
        return (password, result[1])  # Return password and user
    return None

def crack_hashes(wordlist_filename, credentials):
    hashes = load_hashes(credentials)  # Load hashes into memory once
    num_workers = multiprocessing.cpu_count()  # Use available CPUs
    log.info("Cracking Hashes")

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        with open(wordlist_filename, "r", encoding="latin-1") as file:
            for password in file:
                password = password.strip()
                tasks = [(password, hash_stored) for hash_stored in hashes]

                # Use map() instead of multiple submit()
                for result in executor.map(check_password_wrapper, tasks):
                    if result:  # If we find a matching password
                        found_password, user = result
                        log.success(f"Password found: {green}{found_password}{reset} for user {green}{user}{reset}")
                        
                        executor.shutdown(wait=False, cancel_futures=True)  # Stop processes
                        return  # Exit function after finding a match

def load_hashes(credentials):
    return {f"{credential[0]}:sha256:{credential[3]}:{credential[2]}:{credential[1]}" for credential in credentials}

if __name__ == '__main__':
    # Save arguments to variables
    sqlite_db, wordlist, crack, output_file = get_args()

    # Check if SQLite3 database file exists
    check_files_exists(sqlite_db)

    if crack:
        # If crack option is selected, check if wordlist exists
        check_files_exists(wordlist)
    else:
        # Otherwise, check if hash_file already exists
        check_hashes_if_exists(output_file)

    # Store credentials in a file
    credentials = get_credentials(sqlite_db)

    if crack:
        # If crack option is selected, crack hashes in the script
        crack_hashes(wordlist, credentials)
    else:
        # Otherwise, save credentials to a file and provide advice
        save_credentials_to_file(credentials, output_file)
        log.info(f"To crack hashes you can: \n Run this command: {white + bold}❯ hashcat{reset} {green + bold}{output_file}{reset} <wordlist> --user{reset} {red + bold}(Fastest Method){reset}\n Or use: {green + bold}--crack{reset} option {red + bold}(Slowest Method){reset}")

