"""
NNDSVD (Non-Negative Double Singular Value Decomposition) initialization for NMF.

This module implements NNDSVD initialization methods to replace the nimfa dependency.
Based on the algorithm described in:
Boutsidis & Gallopoulos (2008) "SVD based initialization: A head start for 
nonnegative matrix factorization"
"""

import numpy as np
# Use scipy.linalg.svd to match nimfa's implementation and avoid SVD sign ambiguity issues
# Note: SVD has sign ambiguity - for any singular vector u, -u is also valid.
# Using the same SVD solver (scipy.linalg.svd) as nimfa ensures consistent results.
from scipy.linalg import svd


class Nndsvd:
    """
    NNDSVD initialization class compatible with nimfa's interface.
    
    This class provides the same interface as nimfa.methods.seeding.nndsvd.Nndsvd
    to ensure compatibility with existing code.
    
    Note: Uses scipy.linalg.svd to match nimfa's implementation and avoid SVD sign
    ambiguity issues. SVD has sign ambiguity - for any singular vector u, -u is also
    valid. Using the same SVD solver ensures consistent results.
    """
    
    def initialize(self, V, rank, options=None):
        """
        Initialize W and H matrices using NNDSVD.
        
        Parameters:
        -----------
        V : array-like, shape (m, n)
            Input matrix to factorize (must be non-negative).
        rank : int
            Number of components (rank of factorization).
        options : dict, optional
            Dictionary with initialization options:
            - "flag": int, one of {0, 1, 2}
                0: Basic NNDSVD (default)
                1: NNDSVDa (fill zeros with average)
                2: NNDSVDar (fill zeros with small random values)
            - "generator": numpy.random.Generator, optional
                Random number generator for reproducible random initialization.
                If None, uses numpy's default random state.
        
        Returns:
        --------
        W : ndarray, shape (m, rank)
            Initial basis matrix.
        H : ndarray, shape (rank, n)
            Initial coefficient matrix.
        """
        if options is None:
            options = {}
        
        flag = options.get("flag", 0)
        generator = options.get("generator", None)
        
        # Convert to numpy array if needed (handles matrix inputs)
        V = np.asarray(V)
        
        # Ensure non-negative
        V = np.maximum(V, 0)
        
        m, n = V.shape
        
        # Compute SVD
        U, S, Vt = svd(V, full_matrices=False)
        
        # Use all available SVD components (at most min(m, n))
        # If rank > number of SVD components, we'll only use what's available
        # and leave the rest as zeros (which will be filled by variants if flag > 0)
        max_rank = min(len(S), rank)
        
        W = np.zeros((m, rank), dtype=float)
        H = np.zeros((rank, n), dtype=float)
        
        eps = 1e-6
        
        # If no SVD components available, leave all zeros
        if max_rank == 0:
            # Apply variants if needed (will fill zeros)
            if flag == 1:
                avg = V.mean()
                W[:] = avg
                H[:] = avg
            elif flag == 2:
                avg = V.mean()
                noise_scale = avg * 0.01
                if generator is not None:
                    W[:] = generator.uniform(0, noise_scale, size=W.shape)
                    H[:] = generator.uniform(0, noise_scale, size=H.shape)
                else:
                    W[:] = np.random.uniform(0, noise_scale, size=W.shape)
                    H[:] = np.random.uniform(0, noise_scale, size=H.shape)
            return W, H
        
        # First component: use positive parts only
        # If the vector is all negative, use its absolute value (sign is arbitrary in SVD)
        u0 = U[:, 0]
        v0 = Vt[0, :]
        sqrt_s0 = np.sqrt(S[0])
        
        # For first component, if all negative, use absolute value
        if np.all(u0 <= 0):
            u0 = -u0
        if np.all(v0 <= 0):
            v0 = -v0
            
        W[:, 0] = sqrt_s0 * np.maximum(u0, 0)
        H[0, :] = sqrt_s0 * np.maximum(v0, 0)
        
        # For remaining SVD components: choose positive or negative parts
        for j in range(1, max_rank):
            uj = U[:, j]
            vj = Vt[j, :]
            
            # Split into positive and negative parts
            u_pos = np.maximum(uj, 0)
            u_neg = np.maximum(-uj, 0)
            v_pos = np.maximum(vj, 0)
            v_neg = np.maximum(-vj, 0)
            
            # Compute norms
            norm_u_pos = np.linalg.norm(u_pos)
            norm_v_pos = np.linalg.norm(v_pos)
            norm_u_neg = np.linalg.norm(u_neg)
            norm_v_neg = np.linalg.norm(v_neg)
            
            # Choose the pair with larger product of norms
            term_pos = norm_u_pos * norm_v_pos
            term_neg = norm_u_neg * norm_v_neg
            
            if term_pos >= term_neg:
                wj = u_pos
                hj = v_pos
                norm_u = norm_u_pos
                norm_v = norm_v_pos
            else:
                wj = u_neg
                hj = v_neg
                norm_u = norm_u_neg
                norm_v = norm_v_neg
            
            # Scale appropriately
            if norm_u * norm_v > eps:
                W[:, j] = np.sqrt(S[j] * norm_v / (norm_u + eps)) * wj
                H[j, :] = np.sqrt(S[j] * norm_u / (norm_v + eps)) * hj
            else:
                # If norms are too small, leave as zeros
                W[:, j] = 0
                H[j, :] = 0
        
        # Apply variants based on flag
        if flag == 0:
            # Basic NNDSVD: keep zeros as zeros
            pass
        elif flag == 1:
            # NNDSVDa: fill zeros with average
            avg = V.mean()
            W[W == 0] = avg
            H[H == 0] = avg
        elif flag == 2:
            # NNDSVDar: fill zeros with small random values
            avg = V.mean()
            noise_scale = avg * 0.01
            # Use provided generator for reproducibility, or default random state
            if generator is not None:
                W_mask = (W == 0)
                H_mask = (H == 0)
                W[W_mask] = generator.uniform(0, noise_scale, size=W_mask.sum())
                H[H_mask] = generator.uniform(0, noise_scale, size=H_mask.sum())
            else:
                W_mask = (W == 0)
                H_mask = (H == 0)
                W[W_mask] = np.random.uniform(0, noise_scale, size=W_mask.sum())
                H[H_mask] = np.random.uniform(0, noise_scale, size=H_mask.sum())
        else:
            raise ValueError(f"Unknown flag value: {flag}. Must be 0, 1, or 2.")
        
        return W, H
