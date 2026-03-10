import geopandas as gpd
from sqlalchemy import create_engine
import rasterio 


# Database connection parameters
host = "localhost"
port = "5432"
dbname = "gme221laboratory3"
user = "postgres"
password = "zeroeyteen018"

# Create connection string
conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

# Create AQLAlchemy engine
engine = create_engine(conn_str)

# Minimal SQL queries (no spatial operations)
sql_roads = "SELECT gid,geom FROM public.roads"

roads = gpd.read_postgis(sql_roads, engine, geom_col="geom")
#IMPORTANT: attach CRS (GeoPandas often reads PostGIS geometry without CRS)
# Replace 3123 with the SRID from: SELECT ST_SRID(geom) FROM public.roads LIMIT 
1;
roads = roads.set_crs(epsg=3123, allow_override=True)

print(roads.head())
print(roads.crs)
print(roads.geometry.type.unique())

# continued from the previous code...
dem = rasterio.open("data/dem.tif")
print("DEM CRS:", dem.crs)
print("DEM Resolution:", dem.res)
print("DEM Bounds:", dem.bounds)
