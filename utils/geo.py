"""Country centroid coordinates used by the dashboard.

This module centralises a mapping between common country names (as they
appear in the CSV) and an approximate latitude / longitude centroid.
"""

COUNTRY_COORDS = {
    'France': (46.2276, 2.2137),
    'Germany': (51.1657, 10.4515),
    'Greece': (39.0742, 21.8243),
    'Lithuania': (55.1694, 23.8813),
    'Switzerland': (46.8182, 8.2275),
    'Slovenia': (46.1512, 14.9955),
    'Czech Republic': (49.8175, 15.4730),
    'Czechia': (49.8175, 15.4730),
    'The Netherlands': (52.1326, 5.2913),
    'Netherlands': (52.1326, 5.2913),
    'Hungary': (47.1625, 19.5033),
    'Poland': (51.9194, 19.1451),
    'Spain': (40.4637, -3.7492),
    'Italy': (41.8719, 12.5674),
    'Portugal': (39.3999, -8.2245),
    'Belgium': (50.5039, 4.4699),
    'Austria': (47.5162, 14.5501),
    'Sweden': (60.1282, 18.6435),
    'Norway': (60.4720, 8.4689),
    'Finland': (61.9241, 25.7482),
    'Denmark': (56.2639, 9.5018),
    'Ireland': (53.4129, -8.2439),
    'Croatia': (45.1000, 15.2000),
    'Romania': (45.9432, 24.9668),
    'Bulgaria': (42.7339, 25.4858),
    'Slovakia': (48.6690, 19.6990),
    'Estonia': (58.5953, 25.0136),
    'Latvia': (56.8796, 24.6032),
    'Luxembourg': (49.8153, 6.1296),
    'Serbia': (44.0165, 21.0059),
    'Belgique': (50.5039, 4.4699),
}


def get_coord(country_name):
    """Return (lat, lon) for a country name, or (None, None) if unknown.
    """
    if country_name is None:
        return None, None
    # direct lookup
    coord = COUNTRY_COORDS.get(country_name)
    if coord:
        return coord
    return None, None
