import numpy as np

from pypoisson import poisson_reconstruction
from ply_from_array import points_normals_from, ply_from_array

filename = "horse_with_normals.xyz"
output_file = "horse_reconstruction.ply"

points, normals = points_normals_from(filename)
faces, vertices = poisson_reconstruction(points, normals, depth=10)

print faces, np.shape(faces)
print vertices, np.shape(vertices)

ply_from_array(vertices, faces, output_file=output_file)
