"""
IPAI (Indice des Prix des Actifs Immobiliers) data for Moroccan cities
Based on BKAM Séries IPAI T4 2024.xlsx
"""

# IPAI values for T4 2024 (percentage increase from base year)
IPAI_T4_2024 = {
    'marrakech': 10.9,
    'tanger': 17.7,
    'kenitra': 10.35,
    'casablanca': 15.2,
    'rabat': 12.8,
    'fes': 9.6,
    'meknes': 8.7,
    'agadir': 11.3,
    'tetouan': 13.5,
    'oujda': 7.8,
    'sale': 11.2,
    'nador': 9.1,
    'mohammedia': 14.3,
    'el-jadida': 10.5,
    'beni-mellal': 8.2,
    'temara': 12.1,
    'safi': 7.5,
    'khouribga': 8.0,
    'berkane': 7.2,
    'taza': 6.9,
}

# Default IPAI value for cities not in the list (average of all cities)
DEFAULT_IPAI = 10.5

def get_ipai_adjustment(city):
    """
    Get the IPAI adjustment factor for a given city.
    Returns a multiplier to adjust the price (e.g., 1.109 for a 10.9% increase)
    """
    city = city.lower()
    ipai_percentage = IPAI_T4_2024.get(city, DEFAULT_IPAI)
    # Convert percentage to multiplier (e.g., 10.9% -> 1.109)
    return 1 + (ipai_percentage / 100)
