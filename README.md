# gme221laboratory3
TITLE AND OVERVIEW 
3D Computational Modeling; DEM-Vector Integration and GeoJSON Service Delivery 
Overview: The integration of DEM with vector data is crucial step in 3D Computational modeling.  This integration allows for the creation of accurate and detailed 3D representations of terrain, which are essential for various applications such as urban planning, land use and geological applocation 
# How to run analysis.py
Using different requirements and integrated with PostgreSQL/PostGIS database of the vector and DEM and some python script and code  needed to recall the data. 
# Outputs expected in output/
The information of vector and raster data appear in terminal and in the explorer under data folder 
# Commit milestones and reflections 
Many error was encountered,  particularly in the DEM/raster file such as installing rasterio, sqlalchemy and the binary 
# Required Commit-Hybrid IO Milestone Reflection 
 Why are roads retrieved from PostGIS instead of file?
  all spatial data is stored in one database. This makes it easier to manage, query, and share across projects
# Why is the DEM loaded directly from a raster file?
A DEM is a grid is not discrete geometries like points, lines, or polygons. Raster formats like GeoTIFF are designed to efficiently store and compress this kind of continuous surface data.
# How does hybrid IO reflect real-world GIS architecture? 
Hybrid I/O when you pull vector data like roads from spatial database such as PostGIS WHILE loading raster data like DEM directly call from file using scripts. 
# Is spatial analysis occuring at this stage? 
In this laboratory,  roads are being retrieved from PostGIS using gpd.read_postgis() while DEM being loaded from a raster file using rasterio.open()
These two different steps are about getting the data into memory and no spatial computation yet

# 3D Geometry Constructuin Milestone 
Why densification is necessary 
necessary it helps cities use land more efficiently,  reduce urban sprawl, support sustainable transportation and lower environmental impacts for the growing population.  
Why CRS alignment must happen before sampling 
It is simply aligned the spatial consistency particularly the coordinates
What it means that geometry now contains Z values 
The data is composed of 2dimension which is x and y,  z value is for 3D geometry composing of elevation, height and depth 

