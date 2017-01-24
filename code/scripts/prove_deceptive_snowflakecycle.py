"""Generate (5,5,3)-snowflakecycle, then generate coefficients proving deceptiveness.
Call:  python3 -m prove_deceptive_snowflakecycle.py flake_num outer_len inner_len"""

# Imports
import networkx as nx
import numpy as np
import scipy as sp
import scipy.linalg as lin
import code.generators as gen

import sys

print("\nRunning prove_deceptive_snowflakecycle")

def main():
    num_args = len(sys.argv)
    if (num_args>4):
        print("No more than 3 arguments allowed")
        sys.exit(1)

    # Get graph and adj matrix
    # so far, snowflakecycle(5,5,3) is the only setting that produces a deceptive graph.
    num_flake = 5
    outer_len = 3
    inner_len = 5

    if num_args >= 2:
        num_flake = int(sys.argv[1])
    if num_args >= 3:
        outer_len = int(sys.argv[2])
    if num_args >= 4:
        inner_len = int(sys.argv[3])

    print("\nParameter settings: number_flakes, outer-cycle length, innter_cycle length")
    print(" " + str(num_flake) + " " + str(outer_len) + " " + str(inner_len) )

    G = gen.snowflakecycle(num_flake,inner_len,outer_len)
    AG = nx.to_numpy_matrix(G)

    # Build Walk-submatrix
    inds = [0,1,2]
    Ut = np.zeros((len(inds),4))

    A_temp = AG**2
    diag = np.diag(A_temp)
    Ut[:,0] = np.squeeze(diag[inds])

    A_temp = AG**int(outer_len)
    diag = np.diag(A_temp)
    Ut[:,1] = np.squeeze(diag[inds])

    A_temp = AG**int(inner_len)
    diag = np.diag(A_temp)
    Ut[:,2] = np.squeeze(diag[inds])

    A_temp = AG**4
    diag = np.diag(A_temp)
    Ut[:,3] = np.squeeze(diag[inds])


    Ut = np.matrix(Ut)
    print("\nUt")
    print(Ut)

    # Construct Linear Program
    num_rows, num_cols = Ut.shape

    A_eq = np.zeros( (num_rows, num_cols+2) )
    A_eq[:,0:num_cols] = Ut
    A_eq[:,num_cols] = -np.squeeze(np.ones(shape=(num_rows,1)))
    A_eq[:,-1] = -np.squeeze(np.zeros(shape=(num_rows,1)))
    A_eq = np.matrix(A_eq)

    num_rows,num_cols = np.shape(A_eq)
    c = np.ones(num_cols)

    A_ub = np.zeros( (num_rows+1, num_cols) )
    A_ub[:,0:num_rows+1] = -np.identity(num_rows+1)
    A_ub[0:3,-1] = np.squeeze(np.ones(shape=(num_rows,1)))
    A_ub = np.matrix(A_ub)

    # Get diagonal of expm(A)
    evals, evec = lin.eigh(AG)
    exp_vals = [np.exp(val) for val in evals]
    EXPM_AG = evec*(np.asmatrix(np.diag(exp_vals)))*evec.T
    d = np.diag(EXPM_AG)
    g = [d[idx] for idx in inds]
    b_eq = -np.asarray(g)

    b_ub = np.zeros(num_rows+1)
    b_ub[-1] = -max(abs(b_eq))

    print("\ng")
    print(np.asmatrix(g).T)

    print("\n")
    # Return result
    opt_obj = sp.optimize.linprog(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq
    )
    print(opt_obj)
    # Successful termination means we have constructed a deceptive function

    # Construct deceptive function using coefficients from the optimization problem
    x = opt_obj.x
    coeffs = np.asmatrix(x[0:-2])
    coeffs = coeffs.T

    final_diag = Ut*coeffs + np.asmatrix(g).T
    print('\nDiagonal entries of our constructed function of this graph:')
    print(final_diag)


main()
#if __name__ == '__main__':
#    main()
