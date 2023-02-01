from app.api import MGM

mgm = MGM('test/config.ini')

mgm.minSetCover(mgm.G_c)









########################################################################################
#T451 - Take a subSet of Metric and run the min-set-cover-metric
#metrics = [node for node in mgm.G_c.nodes() if 'M' in node and random.random() > 0.65]
#mgm.minSetCoverByMetric(mgm.G_c, metrics)


#######################################################################################
#T452 - Take a subSet of CATEGORY Metric and run the min-set-cover-metric
category	=	['Vulnerability Metrics','Situation Metrics']
#mgm.minSetCoverByCategory(mgm.G_c, category)


#######################################################################################
#T453 - Take a subSet of INPUTS (or 1 INPUT) - what are all the metrics which I can cover?

#inputs	=	[node for node in mgm.G_c.nodes() if 'I' in node and random.random() > 0.65]
#mgm.minSetCoverByInput(mgm.G_c, inputs)


#######################################################################################
#T454 - Take a subSet of SOURCE (or 1 SOURCE) - what are all the metrics which I can cover?
sources    =   ['S001', 'S003', 'S004', 'S012', 'S020', 'S021', 'S022', 'S030', 'S032', 'S033', 'S036', 'S039']
#mgm.minSetCoverBySource(mgm.G_c, sources)

#######################################################################################
#T455 - Given in input a Graph and a MAXIMUM COST return all metric covered

maximumCost =   15
#mgm.maxSetCovByAttributeOnEdge(mgm.G_c,maximumCost)

#######################################################################################
#T456 - What is the minimum computational capacity to cover a list of metrics?

#mgm.minCapacitySetCover(mgm.G_c)

#mgm.maxSetCovByAttributeOnEdgev2(mgm.G_c,15)