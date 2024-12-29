import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.operations_writer as ow
import utils.operations_executer as oe 
import utils.sheetoperations as so
import nextcord
from nextcord import Embed

COLUMN_START = 2

ARCHIVE_INDEX = {
    "name": 0,
    "funds": 1,
    "population": 2,
    "capital": 3,
    "currency": 4,
    "languages": 5,
    "provinces": 6,
    "king": 7,
    "allies": 8,
    "enemies": 9,
    "manpower": 10,
    "devastation": 11,
    "year": 12,
    "userid": 13,
    "growth rate": 14,
    "population capacity": 15,
    "provincial player id": 16,
    "taxes collected?": 17
}

class Country:
    all_countries = []
    def __init__(self, name, userid):
        self.name = name
        self.column = latest_unused_column()
        self.userid = userid
        self.funds = 0
        self.population = 0
        self.capital = "N/A"
        self.currency = "N/A"
        self.languages = "N/A"
        self.provinces = "N/A"
        self.king = "N/A"
        self.allies = "N/A"
        self.enemies = "N/A"
        self.manpower = 0
        self.devastation = 0
        self.year = 1753
        self.archive = {
            "funds": 0,
            "population": 0,
            "capital": "N/A",
            "currency": "N/A",
            "languages": "N/A",
            "provinces": "N/A",
            "king": "N/A",
            "allies": "N/A",
            "enemies": "N/A",
            "manpower": 0,
            "devastation": 0,
            "year": 1753,
            "player id": userid,
            "growth rate": 0,
            "population capacity": 0,
            "provincial player id": "N/A",
            "taxes collected?": False
        }
        if not any(country.name == self.name for country in Country.all_countries):
            Country.all_countries.append(self)
        return None
    def __str__(self):
        return f"{self.name} has {self.funds} funds, and {self.population} people."
    def update_values(self, key, value):
        setattr(self, key, value)
        self.archive[key] = value
    def list_archive(self):
        l = []
        for key in self.archive:
            l.append(self.archive[key])
        return l
    def embedded(self):
        embed = Embed(title=f"{self.name}", description=f"**Funds:** {self.funds}\n**Population:** {self.population}\n**Capital:** {self.capital}\n**Currency:** {self.currency}\n**Languages:** {self.languages}\n**Provinces:** {self.provinces}\n**King:** {self.king}\n**Allies:** {self.allies}\n**Enemies:** {self.enemies}\n**Manpower:** {self.manpower}\n**Devastation:** {self.devastation}\n**Year:** {self.year}")
        return embed
    def assign(self, player):
        self.userid = player
        self.update_values("userid", player)
        return None
    def get_country_by_name(name):
        for country in Country.all_countries:
            if country.name == name:
                return country
        return False
    
    
def latest_unused_column():
    return so.unfilled_row("Countries", 1)

print(str(latest_unused_column()))

def initializeExistingCountries_asOBJ(): # This command won't use the operations system.()
    # Find the number of filled columns in row 1
    try:
        row_nbr = 1
        list = so.get_row(row_nbr, "Countries")   
        countries = []  
        for i in range(COLUMN_START, len(list) + 1): # start at column b
            countries.append(so.get_col(i, "Countries"))
        col = 2
        for country in countries:
            print(country)
            # Create a country with the data from the sheet
            name = country[0]
            new_country = Country(name, 0)
            new_country.column = col # assign it its column then update column to next
            col += 1
            new_country.archive["funds"] = country[1]
            new_country.archive["population"] = country[2]
            new_country.archive["capital"] = country[3]
            new_country.archive["currency"] = country[4]
            new_country.archive["languages"] = country[5]
            new_country.archive["provinces"] = country[6]
            new_country.archive["king"] = country[7]
            new_country.archive["allies"] = country[8]
            new_country.archive["enemies"] = country[9]
            new_country.archive["manpower"] = country[10]
            new_country.archive["devastation"] = country[11]
            new_country.archive["year"] = country[12]
            # Update the country attributes with the data from the archive
            for key in new_country.archive:
                setattr(new_country, key, new_country.archive[key]) 
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
def obj_checker(country_name):
    # check if the object exists in the list of countries
    for country in Country.all_countries:
        if country.name == country_name:
            return country
    return False

def get_attr_row(search_key: str):
    for key in ARCHIVE_INDEX:
        if search_key == key:
            return (ARCHIVE_INDEX[key] + 1)
    # otherwise
    raise KeyError(f"{search_key} is not a valid key.")
def get_country_by_id(id):
        for country in Country.all_countries:
            if country.userid == id:
                return country
        return False