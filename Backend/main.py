from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import requests
import json
import os
from shapely.geometry import shape

app = FastAPI()

# Permitir conexión con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/localidad/{nombre}")
def consultar_localidad(nombre: str):

    archivo = f"{nombre.lower()}.geojson"

    if not os.path.exists(archivo):
        return {"error": f"No existe el archivo {archivo}"}

    # Leer GeoJSON de la localidad
    with open(archivo, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # Obtener bounding box
    geometria = shape(geojson_data["features"][0]["geometry"])
    minx, miny, maxx, maxy = geometria.bounds

    # URL real del servicio de árboles de Bogotá
    url = "https://geoportal.jbb.gov.co/agc/rest/services/JBB/CensoArbol_v0/MapServer/0/query"

    params = {
        "where": "1=1",
        "geometry": f"{minx},{miny},{maxx},{maxy}",
        "geometryType": "esriGeometryEnvelope",
        "inSR": 4326,
        "outSR": 4326,
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "*",
        "returnGeometry": "true",
        "f": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {"error": "Error consultando ArcGIS"}

    data = response.json()

    # Descargar directamente como archivo
    return Response(
        content=json.dumps(data),
        media_type="application/geo+json",
        headers={
            "Content-Disposition": f"attachment; filename=arboles_{nombre}.geojson"
        }
    )
