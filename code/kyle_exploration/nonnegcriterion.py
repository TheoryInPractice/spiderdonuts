import numpy as np
import numpy.linalg as lin
import scipy as sp

def check_nonnegative_criterion(A, W, representatives):
    # Construct Linear Program
    num_rows, num_cols = W.shape

    A_eq = np.zeros( (num_rows, num_cols + 1) )
    A_eq[:,0:num_cols] = W
    A_eq[:,num_cols] = -np.squeeze(np.ones(shape=(num_rows,1)))
    A_eq = np.matrix(A_eq)

    c = np.ones(num_cols + 1)

    A_ub = -np.identity(num_cols + 1)

    # Get diagonal of expm(A)
    evals, evec = lin.eigh(A)
    exp_vals = [np.exp(val) for val in evals]
    EXPM_AG = evec * (np.asmatrix(np.diag(exp_vals))) * evec.T
    d = np.diag(EXPM_AG)
    g = [d[idx] for idx in representatives]
    b_eq = -np.asarray(g)

    b_ub = np.zeros( (num_cols + 1, 1) )

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
    coeffs = np.asmatrix(x[0:-1])

    final_diag = W*coeffs.T + np.asmatrix(g).T
    print('\nDiagonal entries of our constructed function of this graph:')
    print(final_diag)
