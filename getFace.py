#!/usr/bin/env python3

from numpy import cross, linalg, isclose # Used only in is_collinear.
from stl import mesh # To get file data.

def find_parallel_facets(data,chosen_index):
    ''' Finds all facets in the mesh that are parallel with the chosen facet. 
        They would be coplanar under translation, but not rotation. The 
        [zero] index refers to the part of the data containing each facet's 
        normal vector, which determines what direction it is facing. '''
    parallel_facet_indicies = [index for index, facet in enumerate(data) 
                               if is_collinear(facet[0],data[chosen_index][0])]
    parallel_facet_indicies.remove(chosen_index)
    return parallel_facet_indicies


def is_collinear(v1, v2, atol=1e-08):
    ''' Determines whether vectors differ only in magnitude, or in direction 
        as well. Effectively normalizes the normal vector for the purposes of 
        this script. '''
    # Heavily based on almost_collinear() from the library 'vg'. https://vgpy.readthedocs.io/en/latest/_modules/vg/core.html#almost_collinear
    norm = linalg.norm(cross(v1, v2))
    return isclose(norm, 0.0, rtol=0, atol=atol)


def search_for_face(chosen_index, data, parallel_facet_indicies):
    ''' Looks for parallel facets that share two verticies with 
        face-established facets. Further detail of steps are commented 
        throughout. '''
    new_indicies = [chosen_index]
    recent_indicies = []
    face_indicies = []
    first_pass = True
    while new_indicies: # While there are facets apart of the face that haven't been checked for further neighbors...
        recent_indicies = new_indicies
        new_indicies = []

        for particular_recent_index, recent_facet in enumerate(data[recent_indicies]): # For each facet we are finding neighbors for...
            next_recent_facet = False
            neighbor_facet = False
            remove_from_parallel = []
            for index, facet in enumerate(data[parallel_facet_indicies]): # We search through the potential neighbors...
                if not parallel_facet_indicies:
                    break
                shared_vertex = False
                for recent_vertex in recent_facet[1]:       #
                    for vertex in facet[1]:                 # See if they share verticies.
                        if (vertex == recent_vertex).all(): #
                            if shared_vertex:                                      # If two are shared, add the facet to
                                new_indicies.append(parallel_facet_indicies[index])# the list of newly found facets, and
                                remove_from_parallel.insert(0, index)              # prevent it from being found again.
                                if neighbor_facet:
                                    if next_recent_facet:
                                        first_pass = False
                                    next_recent_facet = True
                                neighbor_facet = True
                            shared_vertex = True
                            break
                if next_recent_facet:
                    if not first_pass:
                        break
            if remove_from_parallel:
                for used_index in remove_from_parallel:
                    parallel_facet_indicies.pop(used_index)
            first_pass = False
        
        face_indicies = face_indicies + recent_indicies # Report the indicies of facets found in the face.
    return face_indicies


def get_whole_coplanar_face(chosen_index,filePATH):
    ''' Grabs file data from the file path, and executes the two main steps 
        of the script: finding all facets parallel (aka coplanar) to our 
        chosen facet, and finding neighboring facets within the set of 
        parallel ones. '''
    data = mesh.Mesh.from_file(filePATH).data
        
    parallel_facet_indicies = find_parallel_facets(data, chosen_index)
    
    face_indicies = search_for_face(chosen_index, data, parallel_facet_indicies)

    return face_indicies


def main():
    ''' Recieves a file path and index to facet of inquery. Runs a function 
        that finds the larger face containing our facet. '''
    while True: 
        filePATH = input("Enter path of STL file (defaults to 'dogbone.stl'):")
        if filePATH == "": filePATH = "dogbone.stl"
        maybe_blank = input("Enter index of facet to getFace of (leave blank to exit):")
        if maybe_blank == "": break
        chosen_index = int(maybe_blank)
        
        print(get_whole_coplanar_face(chosen_index, filePATH))


if __name__ == "__main__":
    main()
    