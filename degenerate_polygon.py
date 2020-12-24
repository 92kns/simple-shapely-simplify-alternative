from shapely.geometry.polygon import (Polygon, geos_polygon_from_py)
import numpy as np
import math
import random

class DegeneratePolygon(Polygon):
    
    def __init__(self, shell=None, holes=None):
        """
        ::::THIS DOCSTRING COPIED FROM SHAPELY SRC CODE::::
        
        Parameters
        ----------
        shell : sequence
            A sequence of (x, y [,z]) numeric coordinate pairs or triples.
            Also can be a sequence of Point objects.
        holes : sequence
            A sequence of objects which satisfy the same requirements as the
            shell parameters above
        Example
        -------
        Create a square polygon with no holes
          >>> coords = ((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.))
          >>> polygon = Polygon(coords)
          >>> polygon.area
          1.0
        """
        # this is all we need!
        # just use Polygon classes init, which itself inherits
        # from BaseGeometry

        super().__init__(shell, holes)



    def _update_shapely_polygon(self,shell=None,holes = None):
        # copying factory of how it is done in shapely 1.7.1 src code, 
        # soon deprecated btw 
        ret = geos_polygon_from_py(shell = shell, holes = holes)
        if ret is not None:
            self._geom, self._ndim = ret
        pass
    
    # general angle calculation has no allegiance to this class
    @staticmethod
    def get_angles(vec_1,vec_2):
        dot = np.dot(vec_1, vec_2)
        det = np.cross(vec_1,vec_2)
        angle_in_rad = np.arctan2(det,dot)
        return np.degrees(angle_in_rad)
    
    def simplify_by_interior_angle(self, deg_tol = 1):
        """
        try to remove persistent coordinate points that remain after
        simplify, convex hul, etc with some trig
        params:
        
        deg_tol = the degree tolerance, in Angles, for which to elimnate points
                i.e. if deg_tol = 1, remove any point (x_n,y_n), whose angle 
                between vector <x_n+1-x_n,y_n+1-y_n> and <x_n-x_n-1,y_n-y_n-1> 
                is less than deg_tol. Default set to 1 for use case of eliminating
                degenerate points
                

        """

        ext_poly_coords = self.exterior.coords[:]
        vector_rep = np.diff(ext_poly_coords,axis = 0)
        angles_list = []
        for i in range(0,len(vector_rep) -1 ):
            angles_list.append(np.abs(self.get_angles(vector_rep[i],vector_rep[i+1])))


        thresh_vals_by_deg = np.where(np.array(angles_list) > deg_tol)
    #   gotta be a better way to do this. sandwich betweens first and last pts
        new_idx = [0] + (thresh_vals_by_deg[0] + 1).tolist() + [0]
        new_vertices = [ext_poly_coords[idx] for idx in new_idx]
        
        self._update_shapely_polygon(shell=new_vertices)




    
    def make_degenerate(self, pps = 5):
        """
        Params
        pps : integer of amount of random points to make per side i.e. edge between
            vertices
        return: modified polygon with new rand points
        """
        coords = self.exterior.coords[:]
        coords_arr = np.array(coords)
        vector_rep = np.diff(coords_arr,axis = 0)
        distances = np.linalg.norm(vector_rep,axis = 1)

        idx_dict = {"distance":0, 
                   "vector":1,
                   "coords":2}

        final_coords=[]
        dist_scaler = 10
        for e,d_v_c in enumerate(zip(distances,vector_rep,coords_arr)):
            d= d_v_c[idx_dict['distance']]
            v = d_v_c[idx_dict['vector']]
            c = d_v_c[idx_dict['coords']]

            u = v/d
            # side_pts = np.random.randint(1,d*10,(pps))/11 # dont want a chance of zero 
            side_pts = random.sample(range(1, math.floor(d*dist_scaler)), pps)

            # maintain proper sequence by sorting distance scalars and prepending starting pt of current vector
            side_pts.sort() 
            new_offset = [c + u*du/dist_scaler for du in side_pts]
            final_coords+= [c] + new_offset #+ list(coords[e+1])
            


        self._update_shapely_polygon(shell = final_coords)
            
        pass
