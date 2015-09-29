from pypoisson import poisson_reconstruction
from ply_from_array import points_normals_from, ply_from_array

filename = "horse_with_normals.xyz"
output_file = "horse_reconstruction.ply"

#Helper Function to read the xyz-normals point cloud file
points, normals = points_normals_from(filename)

faces, vertices = poisson_reconstruction(points, normals, depth=10)

#Helper function to save mesh to PLY Format
ply_from_array(vertices, faces, output_file=output_file)
