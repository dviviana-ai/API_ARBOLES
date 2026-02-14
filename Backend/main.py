#Hacer conexiones
import requests
#Administrar archivos Json
import json
#importar solo una parte de la biblioteca shapely.geometry (crear un shape)
from shapely.geometry import shape, mapping
#importar fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app= FastAPI()

#CORS: Habilitar peticiones desde clientes que no están en mi dominio

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
@app.get("/chapinero")
def consultar_chapinero():

# Cargar el archivo GeoJSON con los boundaries (debe subirse un poligono en formato Json para crear el área de busqueda)
    with open("chapinero.geojson", "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

# Obtener la geometría del primer feature (geometria del json)
    geometry = geojson_data["features"][0]["geometry"]
    polygon = shape(geometry)
    print(polygon)

# Extraer bounding box (xmin, ymin, xmax, ymax) (extrae las coordenadas para crear el bbox)
    xmin, ymin, xmax, ymax = polygon.bounds

# Construir la URL de la consulta al servicio ArcGIS REST
    url = "https://geoportal.jbb.gov.co/agc/rest/services/JBB/CensoArbol_v0/MapServer/0/query"

#Diccionario (Estructura de llave valor)
    params = {
        "where": "1=1",
        "geometry": f"{xmin},{ymin},{xmax},{ymax}",
        "geometryType": "esriGeometryEnvelope",
        "spatialRel": "esriSpatialRelIntersects",
        "inSR": 4326,
        "outSR":4326,
        "outFields": "*",
        "f": "json"
    }

    print

# Hacer la solicitud (get se utiliza para solicitar datos)
    response = requests.get(url, params=params)

    # Guardar el resultado si la solicitud fue exitosa (el with se utiliza como un gestor de condiciones)
    if response.status_code == 200:
        with open("censo_arboles.geojson", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Datos guardados en censo_arboles.json")
    else:
        print("Error al descargar los datos:", response.status_code)
