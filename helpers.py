import numpy as np
import wradlib

# Some additional functions and objects
radars = {

    "asd": {
        'name' : 'ASR Dresden',
        'wmo': 10487,
        'lon': 13.76347,
        'lat': 51.12404,
        'alt': 261},

    "boo": {
        'name' : 'Boostedt',
        'wmo': 10132,
        'lon': 10.04687,
        'lat': 54.00438,
        'alt': 124.56},

    "drs": {
        'name' : 'Dresden',
        'wmo': 10488,
        'lon': 13.76865,
        'lat': 51.12465,
        'alt': 263.36},

    "eis": {
        'name' : 'Eisberg',
        'wmo': 10780,
        'lon': 12.40278,
        'lat': 49.54066,
        'alt': 798.79},

    "emd": {
        'name' : 'Emden',
        'wmo': 10204,
        'lon': 7.02377,
        'lat': 53.33872,
        'alt': 58},
 
    "ess": {
        'name' : 'Essen',
        'wmo': 10410,
        'lon': 6.96712,
        'lat': 51.40563,
        'alt': 185.10},

    "fbg": {
        'name' : 'Feldberg',
        'wmo': 10908,
        'lon': 8.00361,
        'lat': 47.87361,
        'alt': 1516.10},

    "fld": {
        'name' : 'Flechtdorf',
        'wmo': 10440 ,
        'lon': 8.802,
        'lat': 51.3112,
        'alt': 627.88},

    "han": {
        'name' : 'Hannover',
        'wmo': 10339,
        'lon': 9.69452,
        'lat': 52.46008,
        'alt': 97.66},

    "neu": {
        'name' : 'Neuhaus',
        'wmo': 10557,
        'lon': 11.13504,
        'lat': 50.50012,
        'alt': 878.04},

    "nhb": {
        'name' : 'Neuheilenbach',
        'wmo': 10605,
        'lon': 6.54853,
        'lat': 50.10965,
        'alt': 585.84},

    "oft": {
        'name' : 'Offenthal',
        'wmo': 10629,
        'lon': 8.71293,
        'lat': 49.9847,
        'alt': 245.80},

    "pro": {
        'name' : 'Proetzel',
        'wmo': 10392,
        'lon': 13.85821,
        'lat': 52.64867,
        'alt': 193.92},

    "ros": {
        'name' : 'Rostock',
        'wmo': 10169,
        'lon': 12.05808,
        'lat': 54.17566,
        'alt': 37},

    "mem": {
        'name' : 'Memmingen',
        'wmo': 10950,
        'lon': 10.21924,
        'lat': 48.04214,
        'alt': 724.40},

    "isn": {
        'name' : 'Isen',
        'wmo': 10873,
        'lon': 12.10177,
        'lat': 48.1747,
        'alt': 677.77},

    "tur": {
        'name' : 'Tuerkheim',
        'wmo': 10832,
        'lon': 9.78278,
        'lat': 48.58528,
        'alt': 767.62},

    "umm": {
        'name' : 'Ummendorf',
        'wmo': 10356,
        'lon': 11.17609,
        'lat': 52.16009,
        'alt': 183},

    "bln": {
        'name' : 'Berlin-Tempelhof',
        'wmo': 10384,
        'lon': 13.388056,
        'lat': 52.478611,
        'alt': 183},

    }

# scanning pattern
specs_dx = {'r':np.arange(500, 128500, 1000),
            'az': np.arange(0.5, 360.5, 1.)}

# in seconds
tdeltas = {"SF":86400, "RW":3600, "RY":300, "DX":300}


def dbz2depth(dbz):
    """
    """
    # to Z
    data = wradlib.trafo.idecibel(dbz)
    # to R
    data = wradlib.zr.z_to_r(data, a=200., b=1.6)
    # to depth
    return wradlib.trafo.r_to_depth(data, tdeltas["DX"])
