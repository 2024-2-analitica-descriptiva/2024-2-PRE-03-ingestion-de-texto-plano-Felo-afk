"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re, pandas as pd

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requerimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    def formatter(head):
        """Formatea los títulos a minúsculas y reemplaza espacios por guiones bajos."""
        return head.lower().replace(" ", "_")

    # Leer el archivo y obtener las líneas
    with open("files/input/clusters_report.txt", "r") as file:
        lineas = file.readlines()

    # Procesar headers
    tit_1 = re.sub(r"\s{2,}", "-", lineas[0]).strip().split("-")
    tit_2 = re.sub(r"\s{2,}", "-", lineas[1]).strip().split("-")
    tit_1.pop() 
    tit_2.pop(0) 
    
    headers = [
        tit_1[0],  # cluster
        f"{tit_1[1]} {tit_2[0]}",  
        f"{tit_1[2]} {tit_2[1]}",
        tit_1[3], 
    ]
    headers = [formatter(h) for h in headers]


    # Leer el archivo como DataFrame con pandas
    data = pd.read_fwf(
        "files/input/clusters_report.txt",
        widths=[9, 16, 16, 80], 
        header=None,
        names=headers,
        skip_blank_lines=False,
        converters={headers[2]: lambda x: x.rstrip(" %").replace(",", ".")},
    ).iloc[4:] 


    # Procesar columna de palabras clave
    claves = data[headers[3]]
    data = data[data[headers[0]].notna()].drop(columns=[headers[3]])
    data = data.astype({
        headers[0]: int,
        headers[1]: int,
        headers[2]: float,
    })


    # Concatenar las palabras clave por cluster
    keywords = []
    temp_text = ""
    for linea in claves:        
        if isinstance(linea, str): 
            if linea.endswith("."): 
                linea = linea[:-1]
            linea = re.sub(r'\s+', ' ', linea).strip()
            temp_text += linea + " "
        elif temp_text: 
            keywords.append(", ".join(re.split(r'\s*,\s*', temp_text.strip())))
            temp_text = ""
    if temp_text:
        keywords.append(", ".join(re.split(r'\s*,\s*', temp_text.strip())))

    data[headers[3]] = keywords

    return data