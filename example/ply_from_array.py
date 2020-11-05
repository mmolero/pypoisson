import numpy as np

__all__ = ["points_normals_from" ,"ply_from_array"]


def points_normals_from(filename):
    """
    Return the normals from a filename.

    Args:
        filename: (str): write your description
    """
    array = np.genfromtxt(filename)
    return array[:,0:3], array[:,3:6]

def ply_from_array(points, faces, output_file):
    """
    Write an array to a vtk file.

    Args:
        points: (array): write your description
        faces: (array): write your description
        output_file: (str): write your description
    """

    num_points = len(points)
    num_triangles = len(faces)

    header = """ply
format ascii 1.0
element vertex {0}
property float x
property float y
property float z
element face {1}
property list uchar int vertex_indices
end_header\n""".format(num_points, num_triangles)
    

    with open(output_file,'wb') as f:
        f.write(header.encode())
        for idx, item in enumerate(points):
            f.write("{0:0.6f} {1:0.6f} {2:0.6f}\n".format(item[0],item[1], item[2]).encode())

        for item in faces:
            number = len(item)
            row = "{0}".format(number)
            for elem in item:
                row += " {0} ".format(elem)
            row += "\n"
            f.write(row.encode())



