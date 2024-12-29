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
    "ransom": 6,
    "domains": 7,
    "slot1": 8,
    "slot2": 9,
    "slot3": 10,
}

class Tax:
    all_taxes = []
    def __init__(self, country=Country):
        self.name = "N/A"
        self.land_tax = 15
        self.poll_tax = 15
        self.rents = 15
        self.customs = 15
        self.tribute = 15
        self.ransoms = 15
        self.central_demesne = 15
        self.projected_revenue = 750000
        self.country = "N/A"
        if not any(country.name == self.name for country in Country.all_countries):
            Country.all_countries.append(self)
        return None
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
    def increase_tax(self, tax, increase):
        self.update_tax(tax, self.__dict__[tax] + increase)
    def decrease_tax(self, tax, decrease):
        self.update_tax(tax, self.__dict__[tax] - decrease)


def initialize():
    for country in Country.all_countries:
        listing = so.get_col(country.column, "Revenue Param.")
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