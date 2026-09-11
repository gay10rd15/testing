import argparse
import os
import re
import sys

import mac_imessage
import questionary
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "contacts.txt")


def load_contacts():
    contacts = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and ": " in line:
                    name, number = line.split(": ", 1)
                    contacts[name.strip()] = number.strip()
    return contacts


contacts = load_contacts()

parser = argparse.ArgumentParser()
parser.add_argument("target", nargs="?", help="Contact name or phone number")
parser.add_argument("-p", "--phone", help="Direct phone number to send to")
parser.add_argument("-c", "--contact", help="Send to contact by name")
args = parser.parse_args()


def get_phone_number(target):
    if re.search(r"\d", target):
        return "".join(filter(str.isdigit, target))
    if target in contacts:
        return "".join(filter(str.isdigit, contacts[target]))
    print(f"Contact '{target}' not found.")
    sys.exit(1)


# Determine phone number source
if args.phone:
    phone_number = get_phone_number(args.phone)
elif args.contact:
    phone_number = get_phone_number(args.contact)
elif args.target:
    phone_number = get_phone_number(args.target)
else:
    target = input("Enter contact name or phone number: ").strip()
    phone_number = get_phone_number(target)

if len(phone_number) > 10:
    print(f"Invalid number: {phone_number}")
    sys.exit(1)

while True:
    try:
        response = requests.get("https://catfact.ninja/fact")
        response.raise_for_status()
        fact = response.json()["fact"]
    except requests.exceptions.RequestException as e:
        print("Failed to fetch cat fact:", e)
        sys.exit(1)

    ui = questionary.confirm(f"is this an okay fact: {fact}").ask()
    if ui == True:
        try:
            mac_imessage.send(
                message=f"Here's a cat fact for you: {fact}",
                phone_number=phone_number,
                medium="imessage",
            )
            print("Sent successfully!")
        except Exception as e:  # noqa: BLE001
            print("Send failed:", e)
        break
