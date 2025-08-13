"""
Syllable Network Analysis Package

A package for analyzing syllable sequence variability over time in bird songs.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .analysis import (
    get_sequence_consistency,
    get_sequence_linearity,
    get_song_stereotypy,
    get_syllable_network,
    get_trans_entropy,
    get_trans_matrix,
    nb_song_note_in_bout,
)
from .plot import plot_transition_diag

__all__ = [
    "get_trans_matrix",
    "get_syllable_network",
    "get_trans_entropy",
    "get_sequence_linearity",
    "get_sequence_consistency",
    "get_song_stereotypy",
    "nb_song_note_in_bout",
    "plot_transition_diag",
]
