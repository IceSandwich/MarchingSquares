'''
Copyright (C) 2021 IceSandwich
https://github.com/IceSandwich

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import numpy as np


# Linear interpolation between p1(float) and p2(float).
# Return the ratio(float). Range [0, 1].
def interp(p1, p2):
    return np.interp((p1+p2)*0.5, [p1, p2], [0, 1])



# Reference: https://en.wikipedia.org/wiki/Marching_squares
# For each square:      a      b
#                        ┌────┐
#                        │    │
#                        └────┘
#                       d      c
# The position of a: (x  , y  )
# The position of b: (x+1, y  )
# The position of c: (x+1, y+1)
# The position of d: (x  , y  )
LookupTable = [
    lambda a,b,c,d,x,y: [], #0
    lambda a,b,c,d,x,y: [[x+interp(d,c),y+1],[x,y+interp(a,d)]], #1
    lambda a,b,c,d,x,y: [[x+1,y+interp(b,c)],[x+interp(d,c),y+1]], #2
    lambda a,b,c,d,x,y: [[x+1,y+interp(b,c)],[x,y+interp(a,d)]], #3
    lambda a,b,c,d,x,y: [[x+interp(a,b),y],[x+1,y+interp(b,c)]], #4
    lambda a,b,c,d,x,y: [[x+interp(a,b),y],[x+interp(d,c),y+1],[x+1,y+interp(b,c)],[x,y+interp(a,d)]], #5
    lambda a,b,c,d,x,y: [[x+interp(a,b),y],[x+interp(d,c),y+1]], #6
    lambda a,b,c,d,x,y: [[x+interp(a,b),y],[x,y+interp(d,c)]], #7

    # The followings are same as above. Use `list.extend(list[::-1])` to add them.
    # lambda a,b,c,d,x,y: [[x+interp(a,d),y],[x,y+interp(d,c)]], #8
    # lambda a,b,c,d,x,y: [[x+interp(a,b),y],[x+interp(d,c),y+1]], #9
    # lambda a,b,c,d,x,y: [[x+interp(a,b),y],[x+1,y+interp(b,c)],[x+interp(d,c),y+1],[x,y+interp(a,d)]], #10
    # lambda a,b,c,d,x,y: [[x+interp(a,b),y],[x+1,y+interp(b,c)]], #11
    # lambda a,b,c,d,x,y: [[x+1,y+interp(b,c)],[x,y+interp(a,d)]], #12
    # lambda a,b,c,d,x,y: [[x+1,y+interp(b,c)],[x+interp(d,c),y+1]], #13
    # lambda a,b,c,d,x,y: [[x+interp(d,c),y+1],[x,y+interp(a,d)]], #14
    # lambda a,b,c,d,x,y: [], #15
]
LookupTable.extend(LookupTable[::-1])


"""
    Extract the contour using Marching Squares Algorithm.
    Input:
        data    np.2darray(F32C1)       the map(2-dimension)
        level   float                   the iso height
    Output:
        points  np.ndarray(Nx2)(float)  the points of contours, each point [x, y].
                                        odd index:  the first point of a line.
                                        even index: the second point of a line.
"""
def Extract(data, level=0.5):
    points=[]
    for y in range(data.shape[0]-1):
        for x in range(data.shape[1]-1):
            oi = data[y,x].item() # original
            rs = data[y,x+1].item() # right side
            bt = data[y+1,x].item() # bottom
            br = data[y+1,x+1].item() # bottom right
            idx = int(oi>level) << 3 | int(rs>level) << 2 | int(br>level) << 1 | int(bt>level)
            points.extend(LookupTable[idx](oi,rs,br,bt,x,y))
    return np.array(points)