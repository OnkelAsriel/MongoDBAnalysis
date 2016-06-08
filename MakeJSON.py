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
    #We need to delete the first and last character in eicono, which are ":".
        var= var + '        "' + eicono[0][1:-1]+ """": {"category": "aaexodo"},""" + "\n"
    #Deleting last two characters (carriage return and comma) to add the end of the file.
    var = var[:-2] + final
    return var


#Pixel=kk
