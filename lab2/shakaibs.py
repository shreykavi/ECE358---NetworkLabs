import numpy
import math
import matplotlib.pyplot as plt

def generatePacketTime(beta):
	# u = numpy.random.uniform(0, 1)
	# x = -(1/lmbda)*math.log(1-u)
	# return x

    x = numpy.random.uniform(0, 1)
    x = - beta * math.log(1-x)
    return x

def generateQueue(SIMULATION_TIME, beta):
	collection = [generatePacketTime(beta)]

	while collection[-1] < SIMULATION_TIME:
		collection.append(collection[-1] + generatePacketTime(beta))
	return collection

def exponentialBackoff(numberOfCollisions, transmissionSpeed):
	R = numpy.random.uniform(0, math.pow(2, numberOfCollisions) - 1)
	return R*512/transmissionSpeed

# input the list of nodes
# returns the index of the node that will transmit next
def nextNode(nodes):
	# high number to start minArrival time
	minArrival = 10000000000000
	minIndex = 0
	for i, node in enumerate(nodes):
		queueLength = len(node['packetQueue'])
		if queueLength != 0:
			if minArrival > node['packetQueue'][0]:
				minArrival = node['packetQueue'][0]
				minIndex = i
	return minIndex

#calculate first collision time
def closestCollisionTime(nodes, transmittingNodeIndex, propDelayBetweenNodes, propSpeed):
	minIndex = transmittingNodeIndex
	minCollisionTime = 100000000000000
	transmittingNode = nodes[transmittingNodeIndex]

	for i, node in enumerate(nodes):
		if i == transmittingNodeIndex:
			continue

		distance = abs(i - transmittingNodeIndex)
		Tprop = distance*propDelayBetweenNodes
		# find closest distance
		if len(node['packetQueue']) > 0 and node['packetQueue'][0] <= (Tprop + transmittingNode['packetQueue'][0]):
			collisionTime = ((distance - (node['packetQueue'][0] - transmittingNode['packetQueue'][0])*propSpeed)/(2*propSpeed))+node['packetQueue'][0]
			if minCollisionTime > collisionTime:
				minCollisionTime = collisionTime
	return minCollisionTime

#exponential backoff to everything that has collided
def backOffCollidedNode(nodes, transmittingNodeIndex, propDelayBetweenNodes, propSpeed, lanSpeed, transmitCounter, firstCollisionTime):
	transmittingNode = nodes[transmittingNodeIndex]

	for i, node in enumerate(nodes):
		if i == transmittingNodeIndex:
			continue

		distance = abs(i - transmittingNodeIndex)
		Tprop = distance*propDelayBetweenNodes
		if len(node['packetQueue']) > 0 and node['packetQueue'][0] <= (Tprop + transmittingNode['packetQueue'][0]):
		#if node['packetQueue'][0] <= firstCollisionTime:
			transmitCounter += 1
			if node['numberOfCollisions'] > 10:
				node['numberOfCollisions'] = 0
				node['packetQueue'].pop(0)
				continue

			# calculate Twait for each node
			TwaitA = exponentialBackoff(node['numberOfCollisions'], lanSpeed)
			# TwaitB = exponentialBackoff(nodes[closestCollisionsIndex]['numberOfCollisions'], lanSpeed)
			
			for i, packet in enumerate(node['packetQueue']):
				if (packet < firstCollisionTime + TwaitA):
					node['packetQueue'][i] = firstCollisionTime + TwaitA
				else:
					break
	return transmitCounter

# Counter of transmitted packets
# Collision counter of each node but reset once sucessul transmission
# Count the number of total attempts to transmit
def initiatePersistentSimulation(numNodes, avgPacketArrivalRate, lanSpeed, packetLength, nodeDistance, propSpeed, SIMULATION_TIME):
	
	# Calculated constants
	transmissionDelay = packetLength/lanSpeed
	propDelayBetweenNodes = nodeDistance/propSpeed
	numberOfNodesInQueue = SIMULATION_TIME*avgPacketArrivalRate
	transmitCounter = 0
	successCounter = 0

	# Store each node in dictionary
	nodes = [
		{
		'packetQueue' : None,
		'numberOfCollisions': 0
		}
	]
	nodes[0]['packetQueue'] = generateQueue(SIMULATION_TIME, 1/avgPacketArrivalRate)

	for i in range(1, numNodes):
		nodes.append(
			{
			'packetQueue' : None,
			'numberOfCollisions': 0
			})
		nodes[i]['packetQueue'] = generateQueue(SIMULATION_TIME, 1/avgPacketArrivalRate)

	# Node currently transmitting
	transmittingNodeIndex = nextNode(nodes)
	transmittingNode = nodes[transmittingNodeIndex]
	
	firstCollisionTime = closestCollisionTime(nodes, transmittingNodeIndex, propDelayBetweenNodes, propSpeed)

	while len(transmittingNode['packetQueue']) > 0 and transmittingNode['packetQueue'][0] < SIMULATION_TIME:
		#check if there is a collision update the arrival times accordingly
		if firstCollisionTime == 100000000000000:
			transmitCounter += 1
			successCounter += 1;
			for i, node in enumerate(nodes):
				#skip the current transmitting node
				if i == transmittingNodeIndex:
					continue

				distance = abs(i - transmittingNodeIndex)
				Tprop = distance*propDelayBetweenNodes

				#check: TB1 + TProp < TC1 < TB1 + TProp + Ttransmission_delay
				for i, packet in enumerate(node['packetQueue']):
					if (Tprop + transmittingNode['packetQueue'][0]) <= node['packetQueue'][i] and node['packetQueue'][i] <= (Tprop + transmittingNode['packetQueue'][0] + transmissionDelay):
						node['packetQueue'][i] = Tprop + transmittingNode['packetQueue'][0] + transmissionDelay
					else:
						break
			#drop successfully transmitted packets and clear number of collisions for the node
			transmittingNode['packetQueue'].pop(0)
			transmittingNode['numberOfCollisions'] = 0
		else:
			#increment transmitCounter 2 times for the packets transmitted by colliding nodes
			transmitCounter += 1
			transmittingNode['numberOfCollisions'] += 1

			# calculate Twait for each node
			transmitCounter = backOffCollidedNode(nodes, transmittingNodeIndex, propDelayBetweenNodes, propSpeed, lanSpeed, transmitCounter, firstCollisionTime)

			if transmittingNode['numberOfCollisions'] > 10:
				transmittingNode['numberOfCollisions'] = 0
				transmittingNode['packetQueue'].pop(0)
				break

			TwaitA = exponentialBackoff(transmittingNode['numberOfCollisions'], lanSpeed)
			
			for i, packet in enumerate(transmittingNode['packetQueue']):
				if (packet < firstCollisionTime+TwaitA):
					transmittingNode['packetQueue'][i] = firstCollisionTime + TwaitA
				else:
					break

		# calculate the next transmitting nodes
		transmittingNodeIndex = nextNode(nodes)
		transmittingNode = nodes[transmittingNodeIndex]
		firstCollisionTime = closestCollisionTime(nodes, transmittingNodeIndex, propDelayBetweenNodes, propSpeed)

	return successCounter/transmitCounter
# simulation
def simulation():
	lanSpeed = 1000000
	packetLength = 1500
	propSpeed = 200000000
	nodeDistance = 10
	SIMULATION_TIME = 1000

	efficiency7 = []
	efficiency10 = []
	efficiency20 = []

	for N in range(20,120,20):
		efficiency7.append(initiatePersistentSimulation(N, 5, lanSpeed, packetLength, nodeDistance, propSpeed, SIMULATION_TIME))
		efficiency10.append(initiatePersistentSimulation(N, 12, lanSpeed, packetLength, nodeDistance, propSpeed, SIMULATION_TIME))
		#efficiency20.append(initiatePersistentSimulation(N, 20, lanSpeed, packetLength, nodeDistance, propSpeed, SIMULATION_TIME))

	plt.plot([20,40,60,80,100],efficiency7,label="Arrival rate = 5")
	plt.plot([20,40,60,80,100],efficiency10,label="Arrival rate = 12")
	#plt.plot([20,40,60,80,100],efficiency20,label="Arrival rate = 20")
	plt.legend()
	plt.ylabel('Efficiency')
	plt.xlabel('Number of nodes')
	plt.show()

simulation()
