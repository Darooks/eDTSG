import xml.etree.ElementTree as ET
from Vehicle import Vehicle


def sumo_upload(file):
    outputFile = open(file, 'r')
    tree = ET.parse(outputFile)
    root = tree.getroot()

    TIME_STEPS = {}

    for timeStep in root:
        time = float(timeStep.attrib['time'])
        VEHICLES = {}

        if len(timeStep.findall('vehicle')) == 0:
            break

        for vehicle in timeStep.findall('vehicle'):
            id = vehicle.attrib['id']
            new_vehicle = Vehicle(id,
                                  vehicle.attrib['x'],
                                  vehicle.attrib['y'],
                                  vehicle.attrib['speed'],
                                  vehicle.attrib['lane'].partition('#')[0],  # delete '#' and everything after
                                  in_accident=False,
                                  angle=vehicle.attrib['angle'])

            VEHICLES[id] = new_vehicle

        TIME_STEPS[time] = VEHICLES

    return TIME_STEPS

