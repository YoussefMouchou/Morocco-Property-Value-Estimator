"""
This module contains data about which cities support which property types
based on the available training data.
"""

# Cities that have villa data in the dataset
CITIES_WITH_VILLAS = {
    'casablanca': True,
    'rabat': True,
    'marrakech': True,
    'tanger': True,
    'fes': True,
    'agadir': True,
    'kenitra': False,
    'meknes': False,
    'tetouan': False,
    'sale': False,
    'oujda': False,
    'temara': False,
    'mohammedia': False,
    'el-jadida': False,
    'nador': False,
    'beni-mellal': False,
    'taza': False,
    'berkane': False,
    'khouribga': False,
    'safi': False
}

def city_supports_villas(city):
    """
    Check if a city has villa data in the dataset.
    
    Args:
        city (str): The name of the city to check
        
    Returns:
        bool: True if the city supports villas, False otherwise
    """
    city = city.lower()
    return CITIES_WITH_VILLAS.get(city, False)
