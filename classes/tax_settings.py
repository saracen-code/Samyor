import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import classes.country as clcountry
from classes.country import Country
import utils.sheetoperations as so

COLUMN_START = 2

TAX_INDEX = {
    "name": 0,
    "land_tax": 1,
    "poll_tax": 2,
    "rents": 3,
    "customs": 4,
    "tribute": 5,
    "ransoms": 6,
    "central_demesne": 7,
    "slot1": 8,
    "slot2": 9,
    "slot3": 10,
}

class Tax:
    all_taxes = []
    def __init__(self, country):
        self.name = "N/A"
        self.land_tax = 15
        self.poll_tax = 15
        self.rents = 15
        self.customs = 15
        self.tribute = 15
        self.ransoms = 15
        self.central_demesne = 15
        self.projected_revenue = 750000
        self.country = country
        self.column = country.column
        if not any(tax.country.name == self.country.name for tax in Tax.all_taxes):
            Tax.all_taxes.append(self)
        return None
    def get_key(self, key):
        if key == "land_tax":
            return self.land_tax
        elif key == "poll_tax":
            return self.poll_tax
        elif key == "rents":
            return self.rents
        elif key == "customs":
            return self.customs
        elif key == "tribute":
            return self.tribute
        elif key == "ransoms":
            return self.ransoms
        elif key == "central_demesne":
            return self.central_demesne
        else:
            raise ValueError("Invalid tax type.")
    def update_tax(self, tax, value):
        if tax == "land_tax":
            self.land_tax = value
        elif tax == "poll_tax":
            self.poll_tax = value
        elif tax == "rents":
            self.rents = value
        elif tax == "customs":
            self.customs = value
        elif tax == "tribute":
            self.tribute = value
        elif tax == "ransoms":
            self.ransoms = value
        elif tax == "central_demesne":
            self.central_demesne = value
        else:
            raise ValueError("Invalid tax type.")
    def update_spreadsheet(self, value, key):
        location = so.convert_to_A1(TAX_INDEX[key] + 1, self.column)
        print(location)
        print(value)
        so.update_cell(location, value, "Taxation")
    def increase_tax(self, key, increase):
        initial = self.get_key(key)
        total = int(initial) + int(increase)
        self.update_tax(key, total)
        self.update_spreadsheet(total, key)
    def decrease_tax(self, key, decrease):
        initial = self.get_key(key)
        total = int(initial) - int(decrease)
        self.update_tax(key, total)
        self.update_spreadsheet(total, key)


def initialize():
    for country in Country.all_countries:
        listing = so.get_col(country.column, "Taxation")
        print(listing)
        obj = Tax(country) # initialize taxable countries
        obj.name = listing[0]
        obj.land_tax = listing[1]
        obj.poll_tax = listing[2]
        obj.rents = listing[3]
        obj.customs = listing[4]
        obj.tribute = listing[5]
        obj.ransoms = listing[6]
        obj.central_demesne = listing[7]

def obj_checker(country):
    for obj in Tax.all_taxes:
        if obj.name == country:
            return obj
    return None