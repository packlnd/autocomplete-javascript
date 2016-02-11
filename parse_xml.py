from xml.dom import minidom

def get_data(file):
    return minidom.parse(file).getElementsByTagName('row')
