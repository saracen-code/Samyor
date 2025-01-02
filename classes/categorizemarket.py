import nextcord
from nextcord.ext import commands
import json
import utils.sheetoperations as so
import utils.operations_writer as ow
import utils.operations_executer as oe 

class Categories:
    def __init__(self):
        self.category_mapping = {
            "G": "Grain",
            "D": "Dairy",
            "M": "Meat",
            "P": "Plants & Crops",
            "O": "Primary Goods",
            "T": "Transportation",
            "S": "Skin, Leather & Textile",
            "O": "Primary Goods (Lumber, Mining, Quarries)",
            "$": "Cash Crops",
            "O": "Wax, combustibles and lightning",
            "A": "Army and manpower",
            "J": "Jewels",
            "E": "Miscellaneous",
            "X": "Exotic Goods",
        }
    def categorize(self, ctx, year: int, marketname: str):
        global_year = so.get_valcell("2", "1", "Data")
        # Get all data from the sheet
        values_list = so.get_allval(f"{marketname} Market")
        for row in values_list:
            if row[0] == global_year:
                for i in range(1, len(row)):
                    if row[i] == "":
                        continue
                    

        