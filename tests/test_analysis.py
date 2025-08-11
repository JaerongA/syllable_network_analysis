"""
Tests for the analysis module.
"""

import pytest
import numpy as np
from syllable_network_analysis.analysis import (
    get_trans_matrix,
    get_syllable_network,
    get_trans_entropy,
    get_sequence_linearity,
    get_sequence_consistency,
    get_song_stereotypy,
    nb_song_note_in_bout,
)


class TestAnalysis:
    """Test class for analysis functions."""
    
    def test_nb_song_note_in_bout(self):
        """Test song note counting in bout."""
        song_notes = "abc"
        bout = "abcdef"
        result = nb_song_note_in_bout(song_notes, bout)
        assert result == 3
        
    def test_get_trans_matrix(self):
        """Test transition matrix creation."""
        syllables = "abcabc"
        note_seq = "abc"
        result = get_trans_matrix(syllables, note_seq)
        expected = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype='int16')
        np.testing.assert_array_equal(result, expected)
        
    def test_get_trans_matrix_normalized(self):
        """Test normalized transition matrix creation."""
        syllables = "abcabc"
        note_seq = "abc"
        result = get_trans_matrix(syllables, note_seq, normalize=True)
        expected = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype='float64')
        np.testing.assert_array_almost_equal(result, expected)
        
    def test_get_syllable_network(self):
        """Test syllable network creation."""
        trans_matrix = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype='int16')
        result = get_syllable_network(trans_matrix)
        expected = [(0, 1, 1), (1, 2, 1), (2, 0, 1)]
        assert result == expected
        
    def test_get_trans_entropy(self):
        """Test transition entropy calculation."""
        trans_matrix = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype='int16')
        result = get_trans_entropy(trans_matrix)
        assert result == 0.0  # All transitions are deterministic
        
    def test_get_sequence_linearity(self):
        """Test sequence linearity calculation."""
        note_seq = "abc"
        syl_network = [(0, 1, 1), (1, 2, 1)]
        result = get_sequence_linearity(note_seq, syl_network)
        expected = 2 / 2  # 2 syllables / 2 transitions
        assert result == expected
        
    def test_get_sequence_consistency(self):
        """Test sequence consistency calculation."""
        note_seq = "abc"
        trans_matrix = np.array([[0, 1, 0], [0, 0, 1], [0, 0, 0]], dtype='int16')
        result = get_sequence_consistency(note_seq, trans_matrix)
        expected = 2 / 2  # 2 typical transitions / 2 total transitions
        assert result == expected
        
    def test_get_song_stereotypy(self):
        """Test song stereotypy calculation."""
        linearity = 0.5
        consistency = 0.7
        result = get_song_stereotypy(linearity, consistency)
        expected = (0.5 + 0.7) / 2
        assert result == expected


if __name__ == "__main__":
    pytest.main([__file__])