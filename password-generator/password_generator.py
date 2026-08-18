"""Password Generator

Usage (CLI):
  python password_generator.py --length 16 --numbers --symbols --count 3

Generates `count` passwords of specified length using optional numbers and symbols.
"""
import secrets
import string
import argparse

def generate_password(length=12, use_numbers=True, use_symbols=True):
    alphabet = string.ascii_letters
    if use_numbers:
        alphabet += string.digits
    if use_symbols:
        alphabet += "!@#$%^&*()-_=+[]{};:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate secure random passwords')
    parser.add_argument('--length', type=int, default=12, help='Password length')
    parser.add_argument('--numbers', action='store_true', help='Include numbers')
    parser.add_argument('--symbols', action='store_true', help='Include symbols')
    parser.add_argument('--count', type=int, default=1, help='How many passwords to generate')
    args = parser.parse_args()

    for _ in range(args.count):
        print(generate_password(length=args.length, use_numbers=args.numbers, use_symbols=args.symbols))
