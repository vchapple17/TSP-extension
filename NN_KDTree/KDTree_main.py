# Amended Dec 6, 2017
# Val Chapple
# To include c-extensions for optimization
# To include c-extensions for distance squared matrix development


# Original:
# Val Chapple
# Cody Dhein
# Date: Nov 22, 2017

import sys
import os.path
sys.path.append('./../twoOpt')

from operator import itemgetter
import heapq
import math
import timeit
import numpy as np

import _twoOpt

# KDTreeNN
#
# Build KDTree from city data points
# Use Tree to find solution
def kdTreeNN(text, outfilename):
    # Save data as 2D list [ [ id, x, y ],... ]
    points = [ [int(i[0]), int(i[1]), int(i[2])] for i in [j.split() for j in text ]]

    # Create kd-tree structure with points, 0 start depth, and 2D(x and y)
    root = kDTree( points, 0, 2)

    # Set Max number of Nearest Neighbors to Keep
    numNN = len(points) * .002
    if (numNN < 10):
        numNN = 10

    (totalDist, route, distSqdMatrix) = kDTreeSearchNN(root, len(points), numNN)

    # if (len(points) <= 400 ):
    #     (totalDist, route) = twoOptImprove(route , distSqdMatrix)

    # data = [ [r.city[0], r.city[1], r.city[2] ] for r in route]

    # Transpose data for parallel arrays
    data = np.array( [ [row[i] for row in [ [r.city[0], r.city[1], r.city[2] ] for r in route] ] for i in range(3) ], dtype=np.int32)

    # data = np.array([ [row[i] for row in points] for i in range(3) ], dtype=np.int32)

    (totalDist, route) = _twoOpt.twoOpt(data[0],data[1],data[2], len(points))

    # Save route
    outFile = open(outfilename, "w")
    outFile.write(str(totalDist) + "\n")
    for i in route:
        outFile.write(str(i) + "\n")
    return

# kDNode
# Class representation of the nodes of trees
# Accepts initialization values of:
#   city: contains id, x, and y. The x and y are the 2 dimensions
#   left and right: point to other kd-nodes
#   dim: represents the splitting axis (aka index to use on the city data)
class kDNode:
    def __init__(self, city, left, right, dim):
        self.city = city
        self.visited = False
        self.left = left
        self.right = right
        self.dim = dim      # 0 or 1
        self.nn = []

    def addNN( self, distSqd, node, maxNN ):
        if ( distSqd, node ) in self.nn:
            return
        if len(self.nn) < maxNN:
            self.nn.append( ( distSqd, node ) )
        else:
            self.nn.sort(key=itemgetter(0), reverse=True)
            if (self.nn[0][0] > distSqd):
                # Replace largest dist with dist
                self.nn[0] = ( distSqd, node )

    def getNNs( self ):
        return [ x for x in self.nn ]

    def __str__(self, level=1):
        ret = ""
        ret += "\t"*(level-1)+"-----"+repr(self.city[0])+"\n"
        if self.left != None:
            ret += self.left.__str__(level+1)
        if self.right != None:
            ret += self.right.__str__(level+1)
        return ret


# kDTree
# Creates kd-tree recursively with city data, depth into tree and dimensions (k)
# Returns a kDNode and its subtree
def kDTree( points, depth, k ):
    # Check that points has a list
    if len(points) < 1:
        return None

    # sort by axis chosen to find median:
    #   even for x= equation, and odd for y= equation
    points.sort(key=itemgetter(depth % k + 1))
    mid = len(points) / 2

    return kDNode(
        points[mid],
        kDTree(points[:mid], depth + 1, k),
        kDTree(points[mid+1:], depth + 1, k),
        depth % k + 1
    )

# kDTreeSearchNN
# Accepts kd-tree root, number of cities in tree, and 2d distance squared matrix
# Determines a tour distance and route, using nearest unvisited neighbor greedy
def kDTreeSearchNN( tree, numCities, maxNN ):
    start = tree
    target = tree
    tree.visited = True
    route = [ tree ]
    totalDist = 0

    distSqdMatrix = [[ -1 for i in range(0,numCities)] for j in range(0,numCities)]

    # Find nearest city for entire loop
    while len(route) < numCities:
        #print(str(len(route)) + " " + str(numCities))
        heap = []
        bestDistSqd = float('inf')
        bestNode = None

        # Add to priority queue
        heapq.heappush( heap, (0 , tree ) )
        # Get target's nearest neighbors
        bestSumDists = float('inf')
        while len(heap) != 0:
            (d, node) = heapq.heappop( heap )
            if (d >= bestDistSqd):
                continue       # No node is closer, continue while loop
            if node == None:
                continue    # Skip node

            # Get distance squared value for comparison
            dist = distSqdMatrix[ node.city[0] ][ target.city[0] ]

            if dist == -1:
                dist = dist_sqd( node.city, target.city )
                distSqdMatrix[ target.city[0] ][ node.city[0] ] = dist
                distSqdMatrix[ node.city[0] ][ target.city[0] ] = dist
            target.addNN( dist , node, maxNN)

            if node.visited == False:
                if (dist < bestDistSqd ):
                    bestDistSqd = dist
                    bestNode = node

            # Add child nodes to priority queue, adjusting priority left/right
            if (target.city[node.dim] <= node.city[node.dim]):
                heapq.heappush(heap, (0, node.left ))
                heapq.heappush(heap, (dist, node.right ))  # sorting by dist?
            else:
                heapq.heappush(heap, (0, node.right ))
                heapq.heappush(heap, (dist, node.left ))

        # Add nearest neighbor to route, mark visited, update target
        if bestNode != None:
            bestNode.visited = True
            route.append(bestNode)
            target = bestNode
            totalDist += int(round(math.sqrt(bestDistSqd)))

    # Add distance from last target city to start city
    totalDist += int(round(math.sqrt(dist_sqd(target.city, start.city))))
    return (totalDist, route, distSqdMatrix)

# dist_sqd
# accepts a city list (id, x, y)
# Returns the distance squared between the two cities.
def dist_sqd( city1, city2 ):
    x_dist = city2[1] - city1[1]
    y_dist = city2[2] - city1[2]
    return x_dist*x_dist + y_dist*y_dist

# # twoOptSwap
# # accepts the full route (list of city id's) and indices for two nodes to swap
# # swaps the two nodes and flips the route to keep a circuit
# def twoOptSwap(route,i,j):
# 	new_route = route[:i]
# 	tmp = list(reversed(route[i:j+1]))
# 	new_route.extend(tmp)
# 	new_route.extend(route[j+1:])
# 	return new_route
#
# twoOptImprove
# accepts the tour list of city Id's and a 2d distance squared Matrix
# Performs a twoOpt improvement on the candidate solution
# def twoOptImprove(route,distances):
#     noSwap = route[0]
#     currentBest = calcLength(route,distances)
#     prevBest = currentBest + 1
#     n = 0
#     while currentBest < prevBest:
#         n += 1
#         #print(str(n))
#         prevBest = currentBest
#         for i in range(1,len(route)-2):
#             for j in range(i+1,len(route)-1):
#                 #print 'Try swap ' + str(route[i]) + ', ' + str(route[j])
#                 candidate = twoOptSwap(route,i,j)
#                 candidate_dist = calcLength(candidate,distances)
#                 if candidate_dist < currentBest:
#                     route = candidate
#                     currentBest = candidate_dist
#                     #break
#             # else:
# 			# 	continue
#             # break
#     currentBest = calcLength(route,distances)
#     return (currentBest,  route )

# calcLength(tour, distMatrix)
# accepts the tour list of city Id's and a 2d distance squared Matrix
# calculates total length of the given tour
# def calcLength(tour, dists):
#     length = 0
#
#     for i in range(len(tour)-1):
#         j = i+1
#         c1 = tour[i]
#         c2 = tour[j]
#         length += int(round(math.sqrt(dists[c1][c2])))
#     length += int(round(math.sqrt(dists[ tour[0] ][ tour[len(tour)-1] ] )))
#     return length
