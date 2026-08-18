"""Mall Inventory Manager

Simple inventory manager with CSV export.
"""
import csv
import argparse
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Product:
    sku: str
    name: str
    qty: int
    price: float

class Inventory:
    def __init__(self):
        self.products = []
    def add(self, p: Product):
        self.products.append(p)
    def remove(self, sku: str):
        self.products = [p for p in self.products if p.sku != sku]
    def list(self):
        return self.products
    def export_csv(self, path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['sku','name','qty','price'])
            writer.writeheader()
            for p in self.products:
                writer.writerow(asdict(p))

if __name__ == '__main__':
    inv = Inventory()
    # sample usage
    inv.add(Product('SKU001','T-Shirt',50,199.0))
    inv.add(Product('SKU002','Sneakers',20,2999.0))
    print('Current inventory:')
    for p in inv.list():
        print(f"{p.sku} | {p.name} | qty:{p.qty} | price:{p.price}")
    inv.export_csv('inventory_export.csv')
    print('Exported inventory_export.csv')
