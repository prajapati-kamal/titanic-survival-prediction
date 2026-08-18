"""MAC Address Generator

Usage (CLI):
  python mac_address_generator.py --count 5 --separator ':'
"""
import random
import argparse

def random_mac(separator=':'):
    mac = [f"{random.randint(0,255):02x}" for _ in range(6)]
    return separator.join(mac)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate random MAC addresses')
    parser.add_argument('--count', type=int, default=1, help='Number of MAC addresses')
    parser.add_argument('--separator', type=str, default=':', help='Separator char (:, -, none)')
    args = parser.parse_args()
    for _ in range(args.count):
        s = args.separator
n        if s.lower() in ['none','']:
            s = ''
        print(random_mac(separator=s))
