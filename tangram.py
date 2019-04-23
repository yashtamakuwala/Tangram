import re
import numpy as np
from collections import namedtuple

class Point():
       x = 0
       y = 0

class Piece():
    points = []
    color = ''

class Tangram:
    piecesList = [Piece]
    Coordinate = namedtuple('Coordinate','x y')
    piecesDict = {}

    def getPieces(self, paths):
        self.piecesDict.clear()
        for path in paths:
            p = Piece()
            pointsList = []

            texts = re.findall(r'"(.*?)"', path)
            pathLine = texts[0]
            color = texts[1]

            a = pathLine.split(' ')
            length = len(a)
            
            for i in range(1,length,3):
                pointsList.append((int(a[i]), int(a[i+1])))
            
            p.color = color
            p.points = pointsList
            self.piecesList.append(p)
            self.piecesDict[color] = pointsList
        
        return self.piecesDict


    def readFile(self, f):
        # with open(filename,'r') as f:
        s = f.readlines()
        paths = []

        for line in s:
            line = line.strip()
            if line.startswith('<path'):
                paths.append(line)

        return self.getPieces(paths)

    def are_valid(self, coloured_pieces):
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
                    det0 = det1 = self.checkOrientationFor2Points(pointsList[i], pointsList[i+1], pointsList[i+2]) 
                else:
                    det1 = self.checkOrientationFor2Points(pointsList[i], pointsList[i+1], pointsList[i+2])
                
                if det0 != det1 or det1 == 0:
                    return False
                det0 = det1
            
            # length is actualLength + 2
            pointsList = pointsList[:-2]    #reset pointslist to original
            # pointsList = pointsList * 2
            newLen = len(pointsList)

            if actualLength > 3: 
                for i in range(0, actualLength-2):
                    ptA = pointsList[i]
                    ptB = pointsList[i+1]
                    for j in range(i+2, actualLength + i - 2):
                        j = j % actualLength
                        ptC = pointsList[j]
                        ptD = pointsList[j+1]

                        det0, det1 = 0,0
                        # j = j % actualLength
                        # ptC = pointsList[j]
                        # ptD = pointsList[j+1]
                        det0 = self.checkOrientationFor2Points(ptA, ptB, ptC)
                        det1 = self.checkOrientationFor2Points(ptA, ptB, ptD)

                        if det0 != det1:
                            det0 = self.checkOrientationFor2Points(ptC, ptD, ptA)
                            det1 = self.checkOrientationFor2Points(ptC, ptD, ptB)

                            if det0 != det1:
                                return False
                        
                        else:
                            continue
        return True

    def checkOrientationFor2Points(self, ptA, ptB, ptC):
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
        

    def getAreaOfColoredPieces(self, pointsList):
        area = 0.0
        noOfPoints = len(pointsList)

        j = noOfPoints - 1
        for i in range(0, noOfPoints):
            pointTupleJ = pointsList[j]
            pointTupleI = pointsList[i]
            area += (pointTupleJ[0] + pointTupleI[0]) * (pointTupleJ[1] - pointTupleI[1])
            j = i

        return area/2.0

    def are_identical_sets_of_coloured_pieces(self, coloured_pieces_1, coloured_pieces_2):
        area1, area2 = 0.0, 0.0
        
        for a in coloured_pieces_1.values():
            area1 += self.getAreaOfColoredPieces(a)

        for a in coloured_pieces_1.values():
            area2 += self.getAreaOfColoredPieces(a)    

        if area1 != area2:
            return False
        
        return True

    def reflectionXaxis(self, pointsList):
        reflectedPoints = set()
        c = 0
        m = 1
        y = 0

        for pt in pointsList:
            x1, y1 = pt[0], pt[1]
            d = (x1 + (y1 - c)*m)/(1 + m^2)
            x2 = 2*d - x1
            y2 = 2*d*m - y1 + 2*c
            reflectedPoints.add((x2,y2))

        return reflectedPoints

    def reflectionYaxis(self, pointsList):
        reflectedPoints = set()
        # x = 0
        c = 0
        m = 0
        y = 1

        for pt in pointsList:
            x1, y1 = pt[0], pt[1]
            d = (x1 + (y1 - c)*m)/(1 + m^2)
            x2 = 2*d - x1
            y2 = 2*d*m - y1 + 2*c
            reflectedPoints.add((x2,y2))

        return reflectedPoints
        

    def getNormalisedPointsSet(self, pointsList):
        normalisedPoints = set()
        minX, minY = pointsList[0][0], pointsList[0][1]

        for point in pointsList:
            if point[0] < minX : minX = point[0]
            if point[1] < minY : minY = point[1]
            # minY = point[1] if point[1] < minY

        for point in pointsList:
                ptTuple = (point[0] - minX, point[1] - minY)
                normalisedPoints.add(ptTuple)

        return normalisedPoints

    def check(self, coloured_pieces_1, coloured_pieces_2):
        for key in coloured_pieces_1:
            pointsList = coloured_pieces_1[key]
            
            pointsSet = set(pointsList)

            if key not in coloured_pieces_2:
                return False

            targetPoints = set(coloured_pieces_2[key])
            
            # Q4        
            if pointsSet == targetPoints:
                continue
    

            normalisedPoints = self.getNormalisedPointsSet(normalisedPoints)
            if normalisedPoints == targetPoints:
                continue

            # Q1
            reflectedPoints = set()
            reflectedPoints = self.reflectionXaxis(pointsList)
            normalisedPoints = self.getNormalisedPointsSet(reflectedPoints)

            if normalisedPoints == targetPoints:
                continue
            
            # Q3
            reflectedPoints.clear()
            normalisedPoints.clear()

            reflectedPoints = self.reflectionYaxis(pointsList)
            normalisedPoints = self.getNormalisedPointsSet(reflectedPoints)

            if normalisedPoints == targetPoints:
                continue
            
            #Q2
            reflectedPoints.clear()
            reflectedPoints = self.reflectionXaxis(normalisedPoints)
            normalisedPoints = self.getNormalisedPointsSet(reflectedPoints)

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
            reflectedPoints = self.reflectionXaxis(mirroredPts)
            normalisedPoints = self.getNormalisedPointsSet(reflectedPoints)

            if normalisedPoints == targetPoints:
                continue

            # Q3
            reflectedPoints = self.reflectionYaxis(mirroredPts)
            normalisedPoints = self.getNormalisedPointsSet(reflectedPoints)

            if normalisedPoints == targetPoints:
                continue

            # Q2
            reflectedPoints = self.reflectionXaxis(reflectedPoints)
            normalisedPoints = self.getNormalisedPointsSet(reflectedPoints)

            if normalisedPoints != targetPoints:
                return False
        
        return True

t = Tangram()
file = open('pieces_A.xml')
# coloured_pieces_1 = []

def available_coloured_pieces(file):
    coloured_pieces = dict()
    coloured_pieces = t.readFile(file)
    return coloured_pieces

def are_valid(coloured_pieces):     
    return t.are_valid(coloured_pieces)


def are_identical_sets_of_coloured_pieces(coloured_pieces_1, coloured_pieces_2):
    return t.are_identical_sets_of_coloured_pieces(coloured_pieces_1, coloured_pieces_2)

coloured_pieces_1 = available_coloured_pieces(file)
# print('Piece is valid: ' + str(are_valid(coloured_pieces_1)))

file = open('shape_A_1.xml')
coloured_pieces_2 = available_coloured_pieces(file)
# print(are_identical_sets_of_coloured_pieces(coloured_pieces_1, coloured_pieces_2))

print(t.check(coloured_pieces_1, coloured_pieces_2))
