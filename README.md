# A-Unifying-Framework-for-Spectrum-Preserving-Graph-Sparsification-and-Coarsening
Python code associated with the paper ``A Unifying Framework for Spectrum-Preserving Graph Sparsification and Coarsening'' (NeurIPS, 2019)

##########################################
### Information for:
### 	graph_reduction.py
###		and GLGraph.py
##########################################

dependencies: numpy, random, time

inputs: 
	reductionTarget:			Target item to reduce.
	actionSwitch:				Allowed actions.
	numSamplesS:				Max number of edges to be sampled.  Choosing 'all' samples the entire graph when q=1, and a maximal matching when q>1.
	qOverS = 1.0/8				Fraction (0<=x<=1): Perturbed edges per sampled edges. Setting to 0 gives q=1 per 									round using the single-edge method.
	minProbPerActionD = 1.0/4	Fraction (0<x<1): 	Minimum expected (target items removed)/(num actions taken).
								We tend to set around d=1/4.
	minTargetItems = 1024		integer or 'all':	End the reduction when the number of target items is below this number.
								If 'all', then reduce until one cannot.

outputs:
	reducedLaplacian:			The reduced node-weighted Laplacian of dimension \tilde{n} \times \tilde{n}
	reducedLaplacianOriginalDimension:			The reduced node-weighted Laplacian of dimension n \times n
