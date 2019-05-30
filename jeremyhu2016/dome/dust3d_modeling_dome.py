#!/usr/bin/env python

# Run Dust3D with option: -remoteio to enable it
#   e.g.
#        $ open ./dust3d.app --args -remoteio
#        $ ./dust3d -remoteio
#        $ ./dust3d.AppImage -remoteio

import socket
import binascii
import uuid
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 53309
BUFFER_SIZE = 4096

RADIUS = 0.005

HEXAGON_COORDS = [
    (-0.0577, -0.10, 0),
     (0.0577, -0.10, 0),
    (0.11547,  0.0,  0),
     (0.0577,  0.10, 0),
    (-0.0577,  0.10, 0),
   (-0.11547,  0.0,  0)
]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

Z_OFFSET = 0.0
Z_STEP = 0.1

def scaleCoords(coords, scale):
    result = []
    for coord in coords:
        result.append((coord[0] * scale, coord[1] * scale, coord[2] * scale))
    return result

def zOffsetCoords(coords, offset):
    result = []
    for coord in coords:
        result.append((coord[0], coord[1], coord[2] + offset))
    return result

def genId():
    return "{" + str(uuid.uuid4()) + "}"

def addNode(nodeId, coord):
    s.send(binascii.hexlify("addnodewithid " + nodeId + " " + str(coord[0] + 0.5) + " " + str(coord[1] + 0.5) + " " + str(coord[2] + 1.00) + " " + str(RADIUS)) + "\0")
    time.sleep(1.5)
    return nodeId

def connectNodes(firstNodeId, secondNodeId):
    s.send(binascii.hexlify("addedge " + firstNodeId + " " + secondNodeId + "") + "\0")

def reset():
    s.send(binascii.hexlify("new") + "\0")

def addRing(coords):
    nodeIds = []
    for coord in coords:
        nodeId = genId()
        addNode(nodeId, coord)
        nodeIds.append(nodeId)
    for i in range(len(nodeIds)):
        connectNodes(nodeIds[i], nodeIds[(i + 1) % len(nodeIds)])
    return nodeIds

reset()

initialRingCoords = zOffsetCoords(scaleCoords(HEXAGON_COORDS, 0.8), Z_STEP)
addRing(initialRingCoords)
for coord in initialRingCoords:
    firstNodeId = addNode(genId(), coord)
    secondNodeId = addNode(genId(), (0, 0, 0))
    connectNodes(firstNodeId, secondNodeId)

secondRoundRingCoords = zOffsetCoords(scaleCoords(HEXAGON_COORDS, 1.6), Z_STEP * 2)
addRing(secondRoundRingCoords)
for i in range(len(initialRingCoords)):
    firstNodeId = addNode(genId(), initialRingCoords[i])
    secondNodeId = addNode(genId(), secondRoundRingCoords[i])
    connectNodes(firstNodeId, secondNodeId)

thirdRoundRingCoords = zOffsetCoords(scaleCoords(HEXAGON_COORDS, 2.4), Z_STEP * 3)
addRing(thirdRoundRingCoords)
for i in range(len(secondRoundRingCoords)):
    firstNodeId = addNode(genId(), secondRoundRingCoords[i])
    secondNodeId = addNode(genId(), thirdRoundRingCoords[i])
    connectNodes(firstNodeId, secondNodeId)

s.close()
