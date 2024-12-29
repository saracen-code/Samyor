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
    def __init__(self, country=Country):
        self.land_tax = 15
        self.poll_tax = 15
        self.rents = 15
        self.customs = 15
        self.tribute = 15
        self.ransoms = 15
        self.central_demesne = 15
        self.projected_revenue = 750000
        self.country = "N/A"
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
        listing = so.get_column(country.column, "Revenue Param.")
        print(listing)
        self.country = country # initialize taxable countries
        for key in TAX_INDEX:
            print(key)
            self.land_tax = listing[1]
            print("For this object: ", self.land_tax)
            self.poll_tax = listing[2]
            self.rents = listing[3]
            self.customs = listing[4]
            self.tribute = listing[5]
            self.ransoms = listing[6]
            self.central_demesne = listing[7]