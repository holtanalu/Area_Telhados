import numpy as np


def area_pixel_metros(latA, lonA, latB, lonB, py, px):
    delLat = latA - latB
    delLon = lonA - lonB

    dely = (111.32*(10^3))/delLat
    delx = ((40075*(10^3))*np.cos(latA))/(360*delLon)

    y = dely/py
    x = delx/px

    area = y*x

    return area
