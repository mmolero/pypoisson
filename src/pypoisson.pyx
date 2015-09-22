cimport numpy as np
import numpy as np
from libcpp.vector cimport vector
from libcpp.string cimport string
from libc.stdlib cimport malloc, free
from libcpp cimport bool


np.import_array()

cdef extern from "PoissonRecon_v6_13/src/PoissonReconLib.h":
    cdef int PoissonReconLibMain(int argc, char* argv[])
    cdef vector[double] double_data
    cdef vector[int] int_data
    cdef vector[double] mem_data

def poisson_reconstruction(points, normals, depth=8, full_depth=5, scale=1.10, samples_per_node=1.0, cg_depth=0.0,
                            enable_polygon_mesh=False, enable_density=False):

    return _poisson_reconstruction(np.ascontiguousarray(points), np.ascontiguousarray(normals),
                                   depth, full_depth, scale, samples_per_node, cg_depth,
                                   enable_polygon_mesh, enable_density)



cdef _poisson_reconstruction(double[:, ::1] points, double[:, ::1] normals,
                           int depth=8, int full_depth=5, double scale=1.10, double samples_per_node=1.0, double cg_depth=0.0,
                           bool enable_polygon_mesh=False, bool enable_density=False):

    cdef:
        char **c_argv
        string arg_depth = str(depth)
        string arg_full_depth = str(full_depth)
        string arg_scale = str(scale)
        string arg_samples_per_node = str(samples_per_node)
        string arg_cg_depth = str(cg_depth)


    int_data.clear()
    double_data.clear()
    mem_data.clear()

    point_nrows, point_ncols = np.shape(points)
    normal_nrows, normal_ncols = np.shape(normals)

    mem_data.resize(point_ncols * point_nrows + normal_ncols * normal_nrows)

    for i in range(point_nrows):
        for j in range(point_ncols):
            mem_data[j +  i*(point_ncols + normal_ncols)] = points[i,j]
            mem_data[j + point_ncols + i *(point_ncols + normal_ncols)] = normals[i,j]


    args = ["PoissonRecon", "--in", "none", "--out", "none", "--depth", arg_depth.c_str(),
                            "--fullDepth",    arg_full_depth.c_str(), "--scale",   arg_scale.c_str(),
                            "--samplesPerNode",  arg_samples_per_node.c_str(),
                            "--cgDepth", arg_cg_depth.c_str()]

    if enable_polygon_mesh:
        args += ["--polygonMesh"]
    if enable_density:
        args += ["--density"]

    c_argv = <char**> malloc(sizeof(char*) * len(args))
    for idx, s in enumerate(args):
        c_argv[idx] = s

    try:
        PoissonReconLibMain(len(args), c_argv)
    finally:
        free(c_argv)


    face_cols, vertex_cols = 3, 3
    face_rows = int_data.size() / face_cols
    vertex_rows = double_data.size() / vertex_cols

    cdef int *ptr_faces = &int_data[0]
    cdef double *ptr_vertices = &double_data[0]

    faces = np.zeros((face_rows*face_cols,), dtype=np.int32 )
    vertices = np.zeros((vertex_rows*vertex_cols,), dtype=np.float64)

    for i in range(face_rows*face_cols):
        faces[i] = ptr_faces[i]

    for i in range(vertex_rows*vertex_cols):
        vertices[i] = ptr_vertices[i]

    int_data.clear()
    double_data.clear()

    return faces.reshape(face_rows,face_cols), vertices.reshape(vertex_rows,vertex_cols)


