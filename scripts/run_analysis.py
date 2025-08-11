#!/usr/bin/env python3
"""
Script to run syllable network analysis.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

import matplotlib.pyplot as plt
import numpy as np

from syllable_network_analysis.analysis import (
    get_sequence_consistency,
    get_sequence_linearity,
    get_song_stereotypy,
    get_syllable_network,
    get_trans_entropy,
    get_trans_matrix,
)
from syllable_network_analysis.plot import plot_transition_diag


def main():
    """Main analysis function."""
    print("Running syllable network analysis...")

    # Sample data (you can modify this or load from file)
    syllables = "kiiiiabcdjiabcdjiabcd*iiiabcdk*iiii*iiiabcdjiabcdk*kiiiiiabcdjia*kiiiiiabcdjjabcd*iiiiabcd*iiiiabcdk*iiiiab*k*iiiiabcdk*iiiabcdjiabcd*iiiabcd*iiiabcdjiabcdk*iiabcd*iiiiiabcdjiabcd*iiiiabcd*iiiiiabcdjiabcdk*k*iiiabcdjiak*iiiabcdjiaj*kmmiiiabcdjiabcd*iiiiabcdjiabcd*iiiiiabcdk*iiiiabcdjiabcd*iiiiabcd*"
    note_seq = ("i", "a", "b", "c", "d", "j", "k", "m", "*")

    # Run analysis
    print(f"Analyzing {len(syllables)} syllables...")

    # Build transition matrix
    trans_matrix = get_trans_matrix(syllables, note_seq)
    print(f"Transition matrix shape: {trans_matrix.shape}")

    # Get syllable network
    syl_network = get_syllable_network(trans_matrix)
    print(f"Number of transitions: {len(syl_network)}")

    # Calculate metrics
    trans_entropy = get_trans_entropy(trans_matrix)
    sequence_linearity = get_sequence_linearity(note_seq, syl_network)
    sequence_consistency = get_sequence_consistency(note_seq, trans_matrix)
    song_stereotypy = get_song_stereotypy(sequence_linearity, sequence_consistency)

    print("\nAnalysis Results:")
    print(f"  Transition Entropy: {trans_entropy:.4f}")
    print(f"  Sequence Linearity: {sequence_linearity:.4f}")
    print(f"  Sequence Consistency: {sequence_consistency:.4f}")
    print(f"  Song Stereotypy: {song_stereotypy:.4f}")

    # Create visualization
    print("\nCreating visualization...")

    # Simple color mapping
    colors = [
        "red",
        "blue",
        "green",
        "orange",
        "purple",
        "brown",
        "pink",
        "gray",
        "yellow",
    ]
    syl_color = dict(zip(note_seq, colors))

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    plot_transition_diag(ax, note_seq, syl_network, syl_color)
    plt.title("Syllable Transition Network", fontsize=16)

    # Save plot
    output_path = Path(__file__).parent.parent / "reports" / "syllable_network.png"
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Plot saved to: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
