import numpy as np
import torch


def all_pairs(lst):
    if len(lst) < 2:
        yield []
        return
    else:
        a = lst[0]
        for i in range(1,len(lst)):
            pair = (a,lst[i])
            for rest in all_pairs(lst[1:i]+lst[i+1:]):
                yield [pair] + rest

def loop_rec(y, n):
    if n >= 1:
        for x in range(y):
            #print(n, x)
            for rest in loop_rec(y, n-1):
                yield [x] + rest
            #loop_rec(y, n - 1)
    else:
        yield []    
        return


def generate_basis_matrices(n: int, k: int, l: int):
    """Geenerates string diagrams that determine the basis matriecs for the symplectic matrices
    Input: 
        n: Even integer denoting the dimension of symplectic basis. The symmetry group will be Sp(m=2n).
        k: the input tensor order
        l: the output tensor order 
    Output:
        Equivariant Basis of Matrices that span Hom_g(V^k, V^l).
    """    
    assert type(n) == int, "n must be an int"
    assert type(k) == int, "n must be an int"
    assert type(l) == int, "n must be an int"
    assert n % 2 == 0, "n must be even"

    
    if (n%2 == 1 or (k+l) % 2 == 1):
        return None
        
    #n = 2
    #l = 3
    #k = 1
    m = int(n/2)
    upper = [*range(1,l+1,1)]
    lower = [*range(l+1, l+k+1, 1)]
    dimensions = [n] * (k+l) 
    #zero_tensor = torch.zeros(dimensions)
    indices = []
    basis_list = []
    for tuples in loop_rec(n, k+l):
        indices.append(tuples)
    for partition in all_pairs(upper+lower):
        basis_matrix = torch.zeros(dimensions)
        
    
        for index_combination in indices:
            val = 1
            for line in partition:
                if ((line[0] in upper and line[1] in upper) or (line[0] in lower and line[1] in lower)):
                    if index_combination[line[1]-1] == index_combination[line[0]-1] + m:
                        val *= 1
                    elif index_combination[line[1]-1] == index_combination[line[0]-1] -m:
                        val *= -1
                    else:
                        val *= 0
                    
                if (line[0] in upper and line[1] in lower):
                    if index_combination[line[0]-1] != index_combination[line[1]-1]:
                        val *= 0
            basis_matrix[tuple(index_combination)] = val
        basis_list.append(basis_matrix.reshape(n**l,n**k))
        #print(basis_matrix.size())


    return torch.stack(basis_list, dim=0)




    