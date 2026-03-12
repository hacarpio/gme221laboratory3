import geopandas as gpd
import rasterio
import numpy as np
from sqlalchemy import create_engine
from shapely.geometry import LineString, MultiLineString
import os 

# 1. Database connection
host, port, dbname = "localhost", "5432", "gme221laboratory3"
user, password = "postgres", "zeroeyteen018"
conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(conn_str)

# 2. Load Roads (SRID 3123)
sql_roads = "SELECT gid, geom FROM public.roads"
roads = gpd.read_postgis(sql_roads, engine, geom_col="geom")
roads = roads.set_crs(epsg=3123, allow_override=True)

# 3. Load DEM and prepare for sampling
dem = rasterio.open("data/dem.tif")
band1 = dem.read(1)  # Read into memory for speed
nodata = dem.nodata

# 4. Helper Functions
def explode_to_lines(geom):
    if geom is None: return []
    if geom.geom_type == "LineString": return [geom]
    if geom.geom_type == "MultiLineString": return list(geom.geoms)
    return []

def densify_line(line, step):
    if line.length == 0: return []
    distances = [d for d in range(0, int(line.length), int(step))]
    pts = [line.interpolate(d) for d in distances]
    pts.append(line.interpolate(line.length)) 
    return pts

def sample_dem_z(x, y):
    """Samples elevation from the raster at x, y coordinates."""
    try:
        row, col = dem.index(x, y)
        # Verify coordinates are within raster bounds
        if row < 0 or col < 0 or row >= band1.shape[0] or col >= band1.shape[1]:
            return None
        z = band1[row, col]
        if (nodata is not None and z == nodata) or np.isnan(z):
            return None
        return float(z)
    except Exception:
        return None

# 5. Main Processing Loop
SAMPLE_STEP = 10 
roads_3d = []

for geom in roads.geometry:
    parts = explode_to_lines(geom)
    if not parts:
        roads_3d.append(None)
        continue
    
    # Process the first part (LineString) of the geometry
    line = parts[0]
    pts = densify_line(line, SAMPLE_STEP)
    
    coords_3d = []
    for pt in pts:
        z = sample_dem_z(pt.x, pt.y)
        if z is not None:
            coords_3d.append((pt.x, pt.y, z))
    
    # Create 3D LineString if we have at least 2 valid points
    if len(coords_3d) >= 2:
        roads_3d.append(LineString(coords_3d))
    else:
        roads_3d.append(None)

# 6. Finalize GeoDataFrame
roads["geom_3d"] = roads_3d
print("3D lines created:", roads["geom_3d"].notna().sum(), "/", len(roads))

valid_3d = roads["geom_3d"].dropna()
print("3D geometries created:", len(valid_3d), "/", len(roads))
# Verify Z exists (third coord)
first = valid_3d.iloc[0]
print("First 3D coord sample:", list(first.coords)[0])

os.makedirs("output", exist_ok=True)
# keep only ONE geometry column for export
roads_3d_gdf = roads.dropna(subset=["geom_3d"]).copy()
roads_3d_gdf = roads_3d_gdf.drop(columns=["geom"], errors="ignore") # drop the 

# original geometry column to avoid confusion

roads_3d_gdf = roads_3d_gdf.set_geometry("geom_3d")
roads_3d_gdf.to_file("output/roads_3d.geojson", driver="GeoJSON")
print("Saved: output/roads_3d.geojson")

