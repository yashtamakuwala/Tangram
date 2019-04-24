import re
import numpy as np
from collections import namedtuple
from matplotlib import path
import random

class Point():
       x = 0
       y = 0

class Piece():
    points = []
    color = ''

# class Tangram:
piecesList = [Piece]
Coordinate = namedtuple('Coordinate','x y')
piecesDict = dict()

def getPieces( paths):
    piecesDict = dict()
    for path in paths:
        p = Piece()
        pointsList = []
        
        texts = re.findall(r'"(.*?)"', path)
        pathLine = texts[0]
        color = texts[1]

        a = re.sub('\s+', ' ', pathLine).strip().split(' ')
        length = len(a)
        
        for i in range(1,length,3):
            pointsList.append((int(a[i]), int(a[i+1])))
        
        p.color = color
        p.points = pointsList
        piecesList.append(p)
        piecesDict[color] = pointsList
    
    return  piecesDict


def readFile(f):
    # with open(filename,'r') as f:
    s = f.readlines()
    paths = []

    for line in s:
        line = line.strip()
        if line.startswith('<path'):
            paths.append(line)

    return getPieces(paths)

def are_valid(coloured_pieces):

    if not coloured_pieces:
        return False

    for key in coloured_pieces:
        pointsList = coloured_pieces[key]
        pointsSet = set(pointsList)

        if len(pointsList) != len(pointsSet):
            return False
        actualLength = len(pointsList)

        pointsList.append(pointsList[0])
        pointsList.append(pointsList[1])
        length = len(pointsList)
        
        det0, det1 = 0,0
        for i in range(0, length-2):
            
            if i == 0:
                det0 = det1 =  checkOrientationFor2Points(pointsList[i], pointsList[i+1], pointsList[i+2]) 
            else:
                det1 =  checkOrientationFor2Points(pointsList[i], pointsList[i+1], pointsList[i+2])
            
            if det0 != det1 or det1 == 0:
                return False
            det0 = det1
        
        # length is actualLength + 2
        pointsList = pointsList[:-2]    #reset pointslist to original
        # pointsList = pointsList * 2
        newLen = len(pointsList)

        if actualLength >= 3: 
            for i in range(0, actualLength-2):
                ptA = pointsList[i]
                ptB = pointsList[i+1]
                for j in range(i+2, actualLength + i - 2):
                    j = j % actualLength
                    ptC = pointsList[j]
                    ptD = pointsList[(j+1) % actualLength]

                    det0, det1 = 0,0
                    det0 =  checkOrientationFor2Points(ptA, ptB, ptC)
                    det1 =  checkOrientationFor2Points(ptA, ptB, ptD)

                    if det0 != det1:
                        det0 =  checkOrientationFor2Points(ptC, ptD, ptA)
                        det1 =  checkOrientationFor2Points(ptC, ptD, ptB)

                        if det0 != det1:
                            return False
                    
                    else:
                        continue
    return True

def checkOrientationFor2Points( ptA, ptB, ptC):
    xa, ya = ptA[0], ptA[1]
    xb, yb = ptB[0], ptB[1]
    xc, yc = ptC[0], ptC[1]

    det = (xb*yc) + (xa*yb) + (ya*xc) - (ya*xb) - (yb*xc) - (xa*yc)
    
    if det > 0:
        return 1
    elif det < 0:
        return -1
    else:
        return 0
    

def getAreaOfColoredPieces(pointsList):
    area = 0.0
    noOfPoints = len(pointsList)

    j = noOfPoints - 1
    for i in range(0, noOfPoints):
        pointTupleJ = pointsList[j]
        pointTupleI = pointsList[i]
        area += (pointTupleJ[0] + pointTupleI[0]) * (pointTupleJ[1] - pointTupleI[1])
        j = i

    return abs(area/2.0)

def are_identical_sets_of_coloured_pieces( coloured_pieces_1, coloured_pieces_2):
    area1, area2 = 0.0, 0.0
    
    for a in coloured_pieces_1.values():
        area1 +=  getAreaOfColoredPieces(a)

    for a in coloured_pieces_1.values():
        area2 +=  getAreaOfColoredPieces(a)    

    if area1 != area2:
        return False
    
    return check(coloured_pieces_1, coloured_pieces_2)

def reflectionXaxis( pointsList):
    reflectedPoints = set()
    c = 0
    m = 1
    y = 0

    for pt in pointsList:
        x1, y1 = pt[0], pt[1]
        d = (x1 + (y1 - c)*m)/(1 + m**2)
        x2 = 2*d - x1
        y2 = 2*d*m - y1 + 2*c
        reflectedPoints.add((int(x2), int(y2)))

    return reflectedPoints

def reflectionYaxis( pointsList):
    reflectedPoints = set()
    # x = 0
    c = 0
    m = 0
    y = 1

    for pt in pointsList:
        x1, y1 = pt[0], pt[1]
        d = (x1 + (y1 - c)*m)/(1 + m**2)
        x2 = 2*d - x1
        y2 = 2*d*m - y1 + 2*c
        reflectedPoints.add((int(x2), int(y2)))

    return reflectedPoints
    

def getNormalisedPointsSet( pointsSet):
    normalisedPoints = set()
    pt = pointsSet.pop()
    minX, minY = pt[0], pt[1]
    pointsSet.add(pt)

    for point in pointsSet:
        if point[0] < minX : minX = point[0]
        if point[1] < minY : minY = point[1]
        # minY = point[1] if point[1] < minY

    for point in pointsSet:
            ptTuple = (int(point[0] - minX), int(point[1] - minY))
            normalisedPoints.add(ptTuple)

    return normalisedPoints

def check(coloured_pieces_1, coloured_pieces_2):
    for key in coloured_pieces_1:
        pointsList = coloured_pieces_1[key]
        
        pointsSet = set(pointsList)

        if key not in coloured_pieces_2:
            return False

        targetPoints = set(coloured_pieces_2[key])
        targetPoints = getNormalisedPointsSet(targetPoints)

        # Q4        
        if pointsSet == targetPoints:
            continue


        normalisedPoints =  getNormalisedPointsSet(pointsSet)
        if normalisedPoints == targetPoints:
            continue

        # Q1
        reflectedPoints = set()
        reflectedPoints =  reflectionXaxis(normalisedPoints)
        normalisedPoints =  getNormalisedPointsSet(reflectedPoints)

        if normalisedPoints == targetPoints:
            continue
        
        # Q3
        reflectedPoints.clear()
        normalisedPoints.clear()

        reflectedPoints =  reflectionYaxis(pointsList)
        normalisedPoints =  getNormalisedPointsSet(reflectedPoints)

        if normalisedPoints == targetPoints:
            continue
        
        #Q2
        reflectedPoints.clear()
        reflectedPoints =  reflectionXaxis(normalisedPoints)
        normalisedPoints =  getNormalisedPointsSet(reflectedPoints)

        if normalisedPoints == targetPoints:
            continue
        
        #mirroring
        # Q4
        mirroredPts = set()
        for point in pointsSet:
            ptTuple = (point[1], point[0])
            mirroredPts.add(ptTuple)
        
        if mirroredPts == targetPoints:
            continue
        
        # Q1
        reflectedPoints =  reflectionXaxis(mirroredPts)
        normalisedPoints =  getNormalisedPointsSet(reflectedPoints)

        if normalisedPoints == targetPoints:
            continue

        # Q3
        reflectedPoints =  reflectionYaxis(mirroredPts)
        normalisedPoints =  getNormalisedPointsSet(reflectedPoints)

        if normalisedPoints == targetPoints:
            continue

        # Q2
        reflectedPoints =  reflectionXaxis(reflectedPoints)
        normalisedPoints =  getNormalisedPointsSet(reflectedPoints)

        if normalisedPoints != targetPoints:
            return False
    
    return True

def is_solution(tangram, shape):
    
    # if not are_valid(tangram):
    #     return False

    #check area
    areaTangram, areaShape = 0.0, 0.0

    for key in tangram:
        areaTangram += getAreaOfColoredPieces(tangram[key])
    
    for key in shape:
        areaShape += getAreaOfColoredPieces(shape[key])

    if areaTangram != areaShape:
        return False

    pieces, target = dict(), dict()
    if len(tangram.keys()) > 1 :
        pieces, target = tangram, shape
    else:
        pieces, target = shape, tangram


    # check if point inside polygon
    allTargetValues = target.values()
    targetPoints = list()

    for value in allTargetValues:
        targetPoints = value
    
    increasedPoints1 = increaseSizeOfPolygon(targetPoints, 0.1, 0.0)
    increasedPoints2 = increaseSizeOfPolygon(targetPoints, 0.0, 0.1)
    increasedPoints3 = increaseSizeOfPolygon(targetPoints, 0.0, -0.1)
    increasedPoints4 = increaseSizeOfPolygon(targetPoints, -0.1, 0.0)
    polyPath = path.Path(increasedPoints1)

    for key in pieces:
        ptsList = pieces[key]

        inOutArray = polyPath.contains_points(ptsList)
        
        polyPath = path.Path(increasedPoints2)
        inOutArray2 = polyPath.contains_points(ptsList)
            # for i in range(0,len(inOutArray)):
            #     if inOutArray2[i]:
            #         ptsList.pop(i)

            
        polyPath = path.Path(increasedPoints3)
        inOutArray3 = polyPath.contains_points(ptsList)
        
                
                # if len(ptsList) > 0:
        polyPath = path.Path(increasedPoints4)
        inOutArray4 = polyPath.contains_points(ptsList)
                    # for i in range(0,len(inOutArray)):
                    #     if inOutArray4[i]:
                    #         ptsList.pop(i)

        a1 = np.array(inOutArray)
        a2 = np.array(inOutArray2)
        a3 = np.array(inOutArray3)
        a4 = np.array(inOutArray4)

        z = a1 | a2 | a3 | a4

        if not z.all :
            return False

    # for key in pieces:
    #     for pt in pieces[key]:
            
    #         inOutArray = polyPath.contains_points([pt])

    #         if pt in targetPoints:
    #             continue


    #         # Check collinearlity of points, range of x and y coordinate and determinant of 3 points
    #         if not inOutArray[0]:
    #             return False

    #         # if not point_inside_polygon(pt[0], pt[1], targetPoints):
    #         #     return False


    # pieces not intersecting with shape
    if doPiecesIntersectTarget(pieces, targetPoints):
        return False

    return True

def increaseSizeOfPolygon(targetPoints, xinc, yinc):
    increasedPoints = list()
    for ptTuple in targetPoints:
        x = float(ptTuple[0]) + xinc
        y = float(ptTuple[1]) + yinc
        increasedPoints.append((x,y))
    return increasedPoints

def doPiecesIntersectTarget(pieces, targetPoints):
    tgPtLength = len(targetPoints)
    for key in pieces:
        ptList = pieces[key]
        length = len(ptList)

        for i in range(0,length+1):
            ptA = ptList[i%length]
            ptB = ptList[(i+1)%length]

            for j in range(i + 2, tgPtLength+1):
                j = j % tgPtLength
                ptC = targetPoints[j]
                ptD = targetPoints[(j+1)%tgPtLength]
                
                det0, det1 = 0,0
                det0 =  checkOrientationFor2Points(ptA, ptB, ptC)
                det1 =  checkOrientationFor2Points(ptA, ptB, ptD)

                if det0 != det1:
                    det0 =  checkOrientationFor2Points(ptC, ptD, ptA)
                    det1 =  checkOrientationFor2Points(ptC, ptD, ptB)

                    if det0 != det1:
                        return True
                
                else:
                    continue
    return False


def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def available_coloured_pieces(file):
    coloured_pieces = dict()
    coloured_pieces = readFile(file)
    return coloured_pieces


# file = open('shape_A_1.xml')
# shape = available_coloured_pieces(file)
# file = open('tangram_A_1_a.xml')
# tangram = available_coloured_pieces(file)
# print(is_solution(tangram, shape))
