"""
Tests for the plot module.
"""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from syllable_network_analysis.plot import plot_transition_diag


class TestPlot:
    """Test class for plot functions."""

    def test_plot_transition_diag(self):
        """Test transition diagram plotting."""
        # Create test data
        note_seq = "abc"
        syl_network = [(0, 1, 1), (1, 2, 1)]
        syl_color = {"a": "red", "b": "blue", "c": "green"}

        # Create figure and axes
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))

        # Test that the function runs without error
        try:
            plot_transition_diag(ax, note_seq, syl_network, syl_color)
            # Check that the plot was created
            assert len(ax.get_children()) > 0
        except Exception as e:
            pytest.fail(f"plot_transition_diag raised {e} unexpectedly!")
        finally:
            plt.close(fig)

    def test_plot_transition_diag_with_repeats(self):
        """Test transition diagram plotting with repeating syllables."""
        # Create test data with self-loops
        note_seq = "abc"
        syl_network = [(0, 1, 1), (1, 2, 1), (2, 2, 2)]  # c->c transition
        syl_color = {"a": "red", "b": "blue", "c": "green"}

        # Create figure and axes
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))

        # Test that the function runs without error
        try:
            plot_transition_diag(ax, note_seq, syl_network, syl_color)
            # Check that the plot was created
            assert len(ax.get_children()) > 0
        except Exception as e:
            pytest.fail(f"plot_transition_diag raised {e} unexpectedly!")
        finally:
            plt.close(fig)


if __name__ == "__main__":
    pytest.main([__file__])
