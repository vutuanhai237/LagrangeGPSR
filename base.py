import polynomial
import numpy as np

def upper_matrix(M):
    """Example:

    [[1,2,3,4],

    [5,6,7,8],

    [9,10,12,13],

    [14,15,16,17]]

    Return: 
        [4, 7, 13]


    Args:
        M (np.ndarray): non-zero square matrix  

    Returns:
        np.ndarray: zic-zac elements except the first
    """
    upper_elements = []
    for i in range(0, M.shape[0]):
        for j in range(i + 1, M.shape[0], 2):           
            upper_elements.append(M[i, j])
    return np.expand_dims(np.asarray(upper_elements[1:]), 1)

def calculate_Lambda(lambdas: list, x):
    """Convert the exponential expression to polynomial expression

    Args:
        lambdas (list): assume that we have already the eigenvalues = {\lambda_i}
        x: parameter value of quantum gate

    Returns:
        polynomial.Polynomial: polynomial expression of quantum gate
    """
    # 
    n = len(lambdas)
    Ss = []
    for k in range(0, n):
        P = np.exp(-1j * x * lambdas[k])
        Vs = []
        for l in range(0, n):
            if l != k: 
                P = P / (lambdas[k] - lambdas[l])
                Vs.append(polynomial.Polymonial([-lambdas[l], 1]))
        V = polynomial.multiXPoly(Vs)
        Ss.append(V.multiX(P))
    S = polynomial.addXPoly(Ss)
    return S

def calculate_Lambda_matrix(lambdas: np.ndarray, x: float):
    """Return square matrix which contains Lambda_i * Lambda_j at each element

    Args:
        lambdas (np.ndarray): eigenvalues of quantum gate
        x (float): phase

    Returns:
        np.ndarray: square matrix
    """
    Lambdas = calculate_Lambda(lambdas, x).coeff
    M = np.zeros([len(Lambdas), len(Lambdas)], dtype = np.complex128)
    for i in range(0, len(Lambdas)):
        for j in range(0, len(Lambdas)):
            M[i, j] = np.conjugate(Lambdas[i]) * Lambdas[j]
    return M

def check_symmetric(matrix, rtol=1e-05, atol=1e-08):
    return np.allclose(matrix, np.conjugate(matrix.T), rtol=rtol, atol=atol)