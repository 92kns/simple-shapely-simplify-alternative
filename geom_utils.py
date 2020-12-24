import shapely.geometry as sg
import shapely
import numpy as np
import random
import math
import pandas as pd

# collection of random funcs.
# makes pretty heavy use of shapely geometry methods

# pickling---------------------------------------------------
def update_poly_pickle(poly, return_df=False):
    try:
        df_poly = pd.read_pickle('./randpolys.pkl')
    except:
#         just make a new df
        print('making new poly df...')
        df_poly = make_poly_df()

#     get next loc
    df_idx_next = len(df_poly)
    df_poly.loc[df_idx_next] = poly.wkt
    df_poly = df_poly.drop_duplicates(ignore_index=True)

    df_poly.to_pickle('./randpolys.pkl')
    
    print('done')
    if return_df:
        return df_poly
    
def make_poly_df():
    poly_df = pd.DataFrame(columns=['poly_wkt'])
    poly_df.to_pickle('./randpolys.pkl')
    return poly_df

# visualization & polygon related---------------------------

def poly_as_mpt(polygon):
    coords = polygon.exterior.coords[:]
    as_pts = [sg.Point(x) for x in coords]
    as_mpt = sg.MultiPoint(as_pts)
    return as_mpt

def make_hex_poly(a, x, y):
    """
    hexagon centered on (x, y)
    :param a: length of the hexagon's edge
    :param x,y: desired centroid of hex
    :return: The shapely polygon representation of the hexagon
    """
    hex_coords = [(x + math.cos(math.radians(angle)) * a, y + math.sin(math.radians(angle)) * a) for angle in range(0, 360, 60)]
    return sg.Polygon(hex_coords)

def generate_random_polygon( n):

    # given n verticies, generate a random non-zero area, non-self intersecting poly

    x = np.random.randint(0,50,n)
    y = np.random.randint(0,50,n)
    centroid = [np.sum(x)/n, np.sum(y)/n]

    angles = np.arctan2(x-centroid[0], y-centroid[1])

    ##sorting the points by angle
    coords_by_theta = sorted([((xx,yy),theta) for xx,yy,theta in zip(x,y,angles)], key = lambda t: t[1])

    xy,angles = zip(*coords_by_theta)
#     append first point to end for complete linear ring sequence
#     xy.append(xy[0])
    xy = list(xy)
    xy.append(xy[0])
    return sg.Polygon(xy)


def buffer_poly_vtx(poly,buffer=1):
    pts = poly.exterior.coords[:]
    buffpts = [sg.Point(x).buffer(1) for x in pts]
    buffpts = sg.MultiPolygon(buffpts)
    poly_ext = poly.exterior
#     return geom collection
    try:
        return poly_ext.union(buffpts)    
    except Exception as e:
        print(e)
