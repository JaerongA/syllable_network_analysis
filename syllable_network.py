"""
Syllable network analysis and calculates transition entropy
"""

from pyfinch.analysis.song import SongInfo
from database.load import ProjectLoader, DBInfo
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from util import save


def nb_song_note_in_bout(song_notes: str , bout: str) -> int:
    """
    Returns the number of song notes within a bout
    """
    nb_song_note_in_bout = len([note for note in song_notes if note in bout])
    return nb_song_note_in_bout


def get_syl_color(bird_id: str) -> dict:
    """Map colors to each syllable"""
    from analysis.parameters import sequence_color
    import copy
    from database.load import ProjectLoader

    # Load database
    db = ProjectLoader().load_db()
    df = db.to_dataframe(f"""SELECT (introNotes || songNote || calls || '*') AS note_sequence, 
                        introNotes, songNote, calls FROM bird WHERE birdID='{bird_id}'""")

    note_seq = df['note_sequence'][0]
    intro_notes = df['introNotes'][0]
    song_notes = df['songNote'][0]
    calls = df['calls'][0]

    syl_color = dict()
    sequence_color2 = copy.deepcopy(sequence_color)

    for i, note in enumerate(note_seq[:-1]):
        if note in song_notes:
            syl_color[note] = sequence_color2['song_note'].pop(0)
        elif note in intro_notes:
            syl_color[note] = sequence_color2['intro'].pop(0)
        elif note in calls:
            syl_color[note] = sequence_color2['call'].pop(0)
        else:
            syl_color[note] = sequence_color2['intro'].pop(0)
    syl_color['*'] = 'y'  # syllable stop

    return note_seq, syl_color


def get_trans_matrix(syllables: str, note_seq: str, normalize=False) -> np.ndarray:
    """Build a syllable transition matrix"""

    trans_matrix = np.zeros((len(note_seq), len(note_seq)), dtype='int16')  # initialize the matrix
    # print(syllables)
    for i, note in enumerate(syllables):
        if i < len(syllables) - 1:
            if not (syllables[i] in note_seq) or not (syllables[i + 1] in note_seq):
                continue
            # print(syllables[i] + '->' + syllables[i + 1])  # for debugging
            ind1 = note_seq.index(syllables[i])
            ind2 = note_seq.index(syllables[i + 1])
            if ind1 < len(note_seq) - 1:
                trans_matrix[ind1, ind2] += 1
    if normalize:
        trans_matrix = trans_matrix / trans_matrix.sum()
    return trans_matrix


def plot_transition_diag(ax, note_seq, syl_network, syl_color,
                         syl_circ_size=450, line_width=0.5):
    """Plot syllable transition diagram"""
    import math
    np.random.seed(0)

    # Set node location
    theta = np.linspace(-math.pi, math.pi, num=len(note_seq) + 1)  # for each node

    node_xpos = [math.cos(node) for node in theta]
    node_ypos = [math.sin(node) for node in theta][::-1]

    # Plot the syllable node
    ax.axis('off')
    ax.set_aspect('equal', adjustable='datalim')
    ax.scatter(node_xpos[:-1], node_ypos[:-1], s=syl_circ_size, facecolors='w',
               edgecolors=list(syl_color.values()),
               zorder=2.5,
               linewidth=2.5)
    ax.set_xlim([-1.2, 1.2]), ax.set_ylim([-1.2, 1.2])

    circle_size = 0.25  # circle size for the repeat syllable

    for i, (start_node, end_node, weight) in enumerate(syl_network):
        if start_node != end_node:

            start_nodex = node_xpos[start_node] + (np.random.uniform(-1, 1, weight) / 10)
            start_nodey = node_ypos[start_node] + (np.random.uniform(-1, 1, weight) / 10)

            end_nodex = node_xpos[end_node] + (np.random.uniform(-1, 1, weight) / 10)
            end_nodey = node_ypos[end_node] + (np.random.uniform(-1, 1, weight) / 10)

            ax.scatter(start_nodex, start_nodey, s=0, facecolors='k')
            ax.scatter(end_nodex, end_nodey, s=0, facecolors='k')

            ax.plot([start_nodex, end_nodex], [start_nodey, end_nodey], 'k',
                    color=list(syl_color.values())[start_node],
                    linewidth=line_width)
        else:  # repeating syllables
            factor = 1.25  # adjust center of the circle for the repeat
            syl_loc = ((np.array(node_xpos) * factor).tolist(), (np.array(node_ypos) * factor).tolist())

            start_nodex = syl_loc[0][start_node] + (np.random.uniform(-1, 1, weight) / 8)
            start_nodey = syl_loc[1][start_node] + (np.random.uniform(-1, 1, weight) / 8)

            for x, y in zip(start_nodex, start_nodey):
                circle = plt.Circle((x, y), circle_size, color=list(syl_color.values())[start_node], fill=False,
                                    clip_on=False,
                                    linewidth=0.3)
                ax.add_artist(circle)

        # Set text labeling location
        factor = 1.7
        text_loc = ((np.array(node_xpos) * factor).tolist(), (np.array(node_ypos) * factor).tolist())

        for ind, note in enumerate(note_seq):
            ax.text(text_loc[0][ind], text_loc[1][ind], note_seq[ind], fontsize=15)


def get_syllable_network(trans_matrix: np.ndarray) -> list:
    """
    Build sparse representation of a syllable network

    Parameters
    ----------
    trans_matrix : np.ndarray
        transition matrix
    Returns
    -------
    syl_network : list of tuple (start node, end node, weight)
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
    Calculate transition entropy
    entropy will be equal to zero if all notes transition to only one syllable
    """
    trans_entropy = []
    for row in trans_matrix:
        if np.sum(row):
            prob = row / np.sum(row)
            entropy = - np.nansum(prob * np.log2(prob))
            trans_entropy.append(entropy)
    # print(trans_entropy)
    trans_entropy = np.mean(trans_entropy)
    return trans_entropy


def get_sequence_linearity(note_seq: str, syl_network: list) -> float:

    nb_unique_transitions = len(syl_network)
    # print(nb_unique_transitions)
    nb_unique_syllables = len(note_seq) - 1  # stop syllable (*) not counted here
    sequence_linearity = nb_unique_syllables / nb_unique_transitions
    # print(nb_unique_syllables)
    return sequence_linearity


def get_sequence_consistency(note_seq: str, trans_matrix: np.ndarray) -> float:

    typical_transition = []
    for i, row in enumerate(trans_matrix):
        max_ind = np.where(row == np.amax(row))
        if ((max_ind[0].shape[0]) == 1) \
                and (
                np.sum(row)):  # skip if there are more than two max weight values or the sum of weights equals zero
            # print(f"{note_seq[i]} -> {note_seq[max_ind[0][0]]}") # starting syllable -> syllable with the highest prob of transition"
            typical_transition.append((note_seq[i], note_seq[max_ind[0][0]]))

    nb_typical_transition = len(typical_transition)
    nb_total_transition = np.count_nonzero(trans_matrix)
    sequence_consistency = nb_typical_transition / nb_total_transition
    return sequence_consistency


def get_song_stereotypy(sequence_linearity: float, sequence_consistency: float) -> float:
    song_stereotypy = (sequence_linearity + sequence_consistency) / 2
    return song_stereotypy
