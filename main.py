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
from matplotlib import pylab as plt 
from PIL import Image
import sys

sys.path.append(".")
import MarchingSquares

def ShowPoints(image, points):
    plt.figure()
    plt.imshow(image, cmap='gray')
    plt.scatter(points[:,0], points[:,1])

def ShowEdges(image, points):
    plt.figure()
    plt.imshow(imgPIL, cmap='gray')
    for i in range(0,points.shape[0],2):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        plt.plot([x1,x2], [y1,y2], color='r')

if __name__ == "__main__":
    # Load map
    img = np.load("example.npy")

    # Turn to image
    imgPIL = Image.fromarray((img*255).astype('uint8'))

    # Calculate
    points = MarchingSquares.Extract(img)

    ShowPoints(imgPIL, points)
    ShowEdges(imgPIL, points)
    plt.show()
