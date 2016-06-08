def MakeJSON(arriconos):
    var = """{
    "files": "**/*.gif",
    "images": {
"""
    final = """
    }
}
    """
    for eicono in arriconos:
        var= var + '        "' + eicono[0][1:-1]+ """": {"category": "aaexodo"},""" + "\n"
#Eliminamos los dos ultimos caracteres (bajar de renglon y la coma). 
    var = var[:-2] + final
    return var


#Pixel=kk
