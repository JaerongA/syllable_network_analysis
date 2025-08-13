"""
Plotting functions for syllable network analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any


def plot_transition_diag(
    ax: plt.Axes,
    note_seq: str,
    syl_network: List[Tuple[int, int, int]],
    syl_color: Dict[str, str],
    syl_circ_size: int = 450,
    line_width: float = 0.5
) -> None:
    """
    Plot syllable transition diagram.
    
    Parameters
    ----------
    ax : plt.Axes
        Matplotlib axes object
    note_seq : str
        Note sequence
    syl_network : List[Tuple[int, int, int]]
        Syllable network
    syl_color : Dict[str, str]
        Color mapping for syllables
    syl_circ_size : int, optional
        Size of syllable circles, by default 450
    line_width : float, optional
        Width of transition lines, by default 0.5
    """
    import math
    np.random.seed(0)

    # Set node location
    theta = np.linspace(-math.pi, math.pi, num=len(note_seq) + 1)

    node_xpos = [math.cos(node) for node in theta]
    node_ypos = [math.sin(node) for node in theta][::-1]

    # Plot the syllable node
    ax.axis('off')
    ax.set_aspect('equal', adjustable='datalim')
    ax.scatter(
        node_xpos[:-1], 
        node_ypos[:-1], 
        s=syl_circ_size, 
        facecolors='w',
        edgecolors=list(syl_color.values()),
        zorder=2.5,
        linewidth=2.5
    )
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])

    circle_size = 0.25  # circle size for the repeat syllable

    for i, (start_node, end_node, weight) in enumerate(syl_network):
        if start_node != end_node:
            start_nodex = node_xpos[start_node] + (np.random.uniform(-1, 1, weight) / 10)
            start_nodey = node_ypos[start_node] + (np.random.uniform(-1, 1, weight) / 10)

            end_nodex = node_xpos[end_node] + (np.random.uniform(-1, 1, weight) / 10)
            end_nodey = node_ypos[end_node] + (np.random.uniform(-1, 1, weight) / 10)

            ax.scatter(start_nodex, start_nodey, s=0, facecolors='k')
            ax.scatter(end_nodex, end_nodey, s=0, facecolors='k')

            ax.plot(
                [start_nodex, end_nodex], 
                [start_nodey, end_nodey], 
                'k',
                color=list(syl_color.values())[start_node],
                linewidth=line_width
            )
        else:  # repeating syllables
            factor = 1.25  # adjust center of the circle for the repeat
            syl_loc = (
                (np.array(node_xpos) * factor).tolist(), 
                (np.array(node_ypos) * factor).tolist()
            )

            start_nodex = syl_loc[0][start_node] + (np.random.uniform(-1, 1, weight) / 8)
            start_nodey = syl_loc[1][start_node] + (np.random.uniform(-1, 1, weight) / 8)

            for x, y in zip(start_nodex, start_nodey):
                circle = plt.Circle(
                    (x, y), 
                    circle_size, 
                    color=list(syl_color.values())[start_node], 
                    fill=False,
                    clip_on=False,
                    linewidth=0.3
                )
                ax.add_artist(circle)

        # Set text labeling location
        factor = 1.7
        text_loc = (
            (np.array(node_xpos) * factor).tolist(), 
            (np.array(node_ypos) * factor).tolist()
        )

        for ind, note in enumerate(note_seq):
            ax.text(
                text_loc[0][ind], 
                text_loc[1][ind], 
                note_seq[ind], 
                fontsize=15
            )