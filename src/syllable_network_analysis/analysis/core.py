"""
Core analysis functions for syllable network analysis.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional


def nb_song_note_in_bout(song_notes: str, bout: str) -> int:
    """
    Returns the number of song notes within a bout.
    
    Parameters
    ----------
    song_notes : str
        String containing song notes
    bout : str
        String containing bout information
        
    Returns
    -------
    int
        Number of song notes in the bout
    """
    nb_song_note_in_bout = len([note for note in song_notes if note in bout])
    return nb_song_note_in_bout


def get_trans_matrix(
    syllables: str, 
    note_seq: str, 
    normalize: bool = False
) -> np.ndarray:
    """
    Build a syllable transition matrix.
    
    Parameters
    ----------
    syllables : str
        String of syllables to analyze
    note_seq : str
        Reference note sequence
    normalize : bool, optional
        Whether to normalize the matrix, by default False
        
    Returns
    -------
    np.ndarray
        Transition matrix
    """
    trans_matrix = np.zeros((len(note_seq), len(note_seq)), dtype='int16')
    
    for i, note in enumerate(syllables):
        if i < len(syllables) - 1:
            if not (syllables[i] in note_seq) or not (syllables[i + 1] in note_seq):
                continue
            ind1 = note_seq.index(syllables[i])
            ind2 = note_seq.index(syllables[i + 1])
            if ind1 < len(note_seq) - 1:
                trans_matrix[ind1, ind2] += 1
                
    if normalize:
        trans_matrix = trans_matrix / trans_matrix.sum()
    return trans_matrix


def get_syllable_network(trans_matrix: np.ndarray) -> List[Tuple[int, int, int]]:
    """
    Build sparse representation of a syllable network.
    
    Parameters
    ----------
    trans_matrix : np.ndarray
        Transition matrix
        
    Returns
    -------
    List[Tuple[int, int, int]]
        List of tuples (start node, end node, weight)
    """
    start_node = np.transpose(np.nonzero(trans_matrix))[:, 0].T.tolist()
    end_node = np.transpose(np.nonzero(trans_matrix))[:, 1].T.tolist()
    weight = []
    
    for ind in range(0, len(start_node)):
        weight.append(int(trans_matrix[start_node[ind], end_node[ind]]))
    
    syl_network = list(zip(start_node, end_node, weight))
    return syl_network


def get_trans_entropy(trans_matrix: np.ndarray) -> float:
    """
    Calculate transition entropy.
    
    Entropy will be equal to zero if all notes transition to only one syllable.
    
    Parameters
    ----------
    trans_matrix : np.ndarray
        Transition matrix
        
    Returns
    -------
    float
        Mean transition entropy
    """
    trans_entropy = []
    for row in trans_matrix:
        if np.sum(row):
            prob = row / np.sum(row)
            entropy = -np.nansum(prob * np.log2(prob))
            trans_entropy.append(entropy)
    
    trans_entropy = np.mean(trans_entropy)
    return trans_entropy


def get_sequence_linearity(note_seq: str, syl_network: List[Tuple[int, int, int]]) -> float:
    """
    Calculate sequence linearity.
    
    Parameters
    ----------
    note_seq : str
        Note sequence
    syl_network : List[Tuple[int, int, int]]
        Syllable network
        
    Returns
    -------
    float
        Sequence linearity score
    """
    nb_unique_transitions = len(syl_network)
    nb_unique_syllables = len(note_seq) - 1  # stop syllable (*) not counted here
    sequence_linearity = nb_unique_syllables / nb_unique_transitions
    return sequence_linearity


def get_sequence_consistency(note_seq: str, trans_matrix: np.ndarray) -> float:
    """
    Calculate sequence consistency.
    
    Parameters
    ----------
    note_seq : str
        Note sequence
    trans_matrix : np.ndarray
        Transition matrix
        
    Returns
    -------
    float
        Sequence consistency score
    """
    typical_transition = []
    for i, row in enumerate(trans_matrix):
        max_ind = np.where(row == np.amax(row))
        if ((max_ind[0].shape[0]) == 1) and (np.sum(row)):
            typical_transition.append((note_seq[i], note_seq[max_ind[0][0]]))
    
    nb_typical_transition = len(typical_transition)
    nb_total_transition = np.count_nonzero(trans_matrix)
    sequence_consistency = nb_typical_transition / nb_total_transition
    return sequence_consistency


def get_song_stereotypy(sequence_linearity: float, sequence_consistency: float) -> float:
    """
    Calculate song stereotypy.
    
    Parameters
    ----------
    sequence_linearity : float
        Sequence linearity score
    sequence_consistency : float
        Sequence consistency score
        
    Returns
    -------
    float
        Song stereotypy score
    """
    song_stereotypy = (sequence_linearity + sequence_consistency) / 2
    return song_stereotypy