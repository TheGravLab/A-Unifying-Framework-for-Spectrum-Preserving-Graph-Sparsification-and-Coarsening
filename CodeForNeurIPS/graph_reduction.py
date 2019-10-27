import numpy as np
from GLGraph import GLGraph


##########################################
### Parameters for reduction 
##########################################

reductionTarget = 'edges'		# 'edges' or 'nodes': 	Target item to reduce.
actionSwitch = 'both'			# 'both' or 'delete': 	Choosing 'delete' does not allow contraction.
numSamplesS = 'all'				# integer or 'all': 	Number of edges to sample. Choosing 'all' samples the entire graph when q=1, and a maximal matching when q>1.
qOverS = 1.0/8					# fraction (0<=x<=1): 	Perturbed edges per sampled edges. Setting to 0 gives q=1 per round using the single-edge method.
minProbPerActionD = 1.0/4		# fraction (0<x<1): 	Minimum expected (target items removed)/(num actions taken).
								# 						We tend to set around d=1/4, but go to town and experiment if you want.

minTargetItems = 1024			# integer or 'all':		End the reduction when the number of target items is below this number. If 'all', then reduce until one cannot.

plotError = False				# bool: 				Decide whether or not to compute the hyperbolic alignment of the output of the original eigenvectors.
iHaveIGraph = False				# bool:					Do you have iGraph for Python, and is it working correctly?
								#						Also, if your pycairo is working, we have a graph plotter in our GLGraph, currently commented out.


##########################################
### Import Jazz Musicians data.
### Format is a list of node pairs, where nodes are integers in [0,n-1]. 
##########################################

edges = np.load('./Jazz_Edges.npy')						# Import Jazz Musicians data.  Format is a list of node pairs, where nodes are integers in [0,n-1].


##########################################
### Do the reduction.
##########################################

print("Starting")
flatten = lambda l: [item for sublist in l for item in sublist]				# Because I couldn't find a general 'flatten' in Python.
if iHaveIGraph:
	from igraph import *		#import iGraph if you have it.

if minTargetItems=='none':
	if reductionTarget=='nodes':
		minTargetItems = 2
	elif reductionTarget=='edges' and actionSwitch=='both':
		minTargetItems = 1
	elif reductionTarget=='edges' and actionSwitch=='delete':
		minTargetItems = len(set(flatten(edges)))
connected = False				# In case the graph becomes disconnected, try again.
while not connected:			# In case the graph becomes disconnected, try again.
	print("Initializing GLGraph")
	g = GLGraph(edges,edgeWeights='none',nodeWeights='none',plotError=plotError,layout='random')
	edgeNumList = []			# List of edges in the reduced graphs if target is 'edges'.
	nodeNumList = []			# List of nodes in the reduced graphs if target is 'nodes'.
	eigenAlignList = []			# List of hyperbolic distance of eigenvector output if plotError is True.
	edgeNumList.append(len(g.edgeList))
	nodeNumList.append(len(g.nodeList))
	if plotError: eigenAlignList.append(g.get_eigenvector_alignment()[1:])
	iteration = 0
	while True:
		iteration += 1
		if np.mod(iteration,1)==0:						# Say where we are in the reduction.
			print("Iteration ", iteration,", ",len(g.edgeList),"/",len(g.edgeListIn)," edges, ",len(g.nodeList),"/",len(g.nodeListIn)," nodes")
		if qOverS>0:			# If q is determined by a fraction of s, use reduce_graph_multi_edge, as the edges should form a matching.
			g.reduce_graph_multi_edge(numSamples=numSamplesS,qFraction=qOverS,pMin=minProbPerActionD,\
									reductionType=actionSwitch,reductionTarget=reductionTarget,maxReweightFactor=0)
		else:					# If q is fixed at 1 (ie, qOverS==0), use reduce_graph_single_edge, as we do not care if the edges form a matching.
			g.reduce_graph_single_edge(minSamples=numSamplesS,pMin=minProbPerActionD,\
									reductionType=actionSwitch,reductionTarget=reductionTarget,maxReweightFactor=0)
		if reductionTarget=='nodes':					# If targeting nodes, save data whenever the number of nodes is reduced.
			if len(g.nodeList)<nodeNumList[-1]:
				edgeNumList.append(len(g.edgeList))
				nodeNumList.append(len(g.nodeList))
				if plotError: eigenAlignList.append(g.get_eigenvector_alignment()[1:])
		if reductionTarget=='edges':					# If targeting edges, save data whenever the number of edges is reduced.
			if len(g.edgeList)<edgeNumList[-1]:
				edgeNumList.append(len(g.edgeList))
				nodeNumList.append(len(g.nodeList))
				if plotError: eigenAlignList.append(g.get_eigenvector_alignment()[1:])
		if actionSwitch=='both':						# If we can merge nodes, go until there are only two left.
			if len(g.nodeList)<3 or (reductionTarget=='edges' and len(g.edgeList)<minTargetItems) \
								or (reductionTarget=='nodes' and len(g.nodeList)<minTargetItems): break
		if actionSwitch=='delete':						# If we cannot merge nodes, go until we have a spanning tree.
			if len(g.edgeList)<len(nodes) or (reductionTarget=='edges' and len(g.edgeList)<minTargetItems): break
	if iHaveIGraph:				# If you have iGraph, use to check if the resulting graph was disconnected (should not happen for qOverS==0)
		iGraph = Graph()
		iGraph.add_vertices(g.nodeList)
		iGraph.add_edges(g.edgeList)
		if not iGraph.is_connected(): 
			print("Whoops! Disconnected. Retrying.")
		else:
			connected = True
	else:						# If your iGraph is not working, just hope that everything worked.  We will implement an iGraph-independent version soon.
		print("Did not check if graph is disconnected: Results invalid if graph is disconnected.")
		connected = True

##########################################
### Outputs.
##########################################

g.update_inverse_laplacian()
reducedLaplacian = g.nodeWeightedInverseLaplacian		# This is the reduced node-weighted laplacian of size $\tilde{V} \times \tilde{V}$
reducedLaplacianOriginalDimension = g.project_reduced_to_original(reducedLaplacian)		# This is the reduced node-weighted laplacian appropriately projected back to
																						# $V \times V$. Use this to get approximate solutions to your Lx=b problems.








 