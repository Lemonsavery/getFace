# getFace
getFace.py is a tool for use with STL files, a file format used for storing 3D object models as a list of triangles (aka facets) in space. Given an STL file and the index of a chosen triangle within it, getFace finds all triangles in the face that the chosen triangle is a member of.

## Illutration of choosing a triangle, and of which triangles getFace returns.

![Illustration of Facet & Face](https://i.imgur.com/htRLA0c.png)

## Example of using getFace.

![Example of UsinggetFace](https://i.imgur.com/WDXkM4x.png)  
Two inputs are requested: file path, and facet index. 
dogbone.stl is a sample STL in this repository. A full path is only necessary if the desired STL file isn't in the same folder as getFace.py, otherwise only the file name is necessary.

## Requirements
Developed in Python3.  
getFace has dependencies for python libraries: numpy, stl.
