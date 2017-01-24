import generators as gen
import networkx as nx
G = gen.pyramid_prism(4,0)

import polygraph as wks
walk_obj = wks.walk_classes(G)
# W = walk_obj['uniq_matrix']
W = walk_obj['diag_matrix']

import scipy
import numpy
from scipy import linalg

def get_nullspace_matrix( M, thresh=1e-10 ):
    u, s, vh = scipy.linalg.svd(M,1,1) #options force full SVD
    indices_of_null = numpy.where( (s <= thresh) )[0]
    r,c = M.shape
    if r >= c:
      nullspace_basis = vh[:,indices_of_null]
    else:
      nullspace_basis = vh[:, numpy.concatenate( (indices_of_null, list(range(r, c))), axis=0 ) ]
    return nullspace_basis

nullspace_basis = get_nullspace_matrix( W )

print( nullspace_basis.shape )
