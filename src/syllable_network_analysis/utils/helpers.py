"""
Helper utility functions for syllable network analysis.
"""

from typing import Dict, Tuple
import copy


def get_syl_color(bird_id: str) -> Tuple[str, Dict[str, str]]:
    """
    Map colors to each syllable.
    
    Parameters
    ----------
    bird_id : str
        Bird identifier
        
    Returns
    -------
    Tuple[str, Dict[str, str]]
        Note sequence and color mapping for syllables
    """
    # Note: This function references external dependencies that would need to be
    # properly imported or refactored based on your specific setup
    try:
        from analysis.parameters import sequence_color
        from database.load import ProjectLoader
    except ImportError:
        # Fallback for when dependencies aren't available
        print("Warning: External dependencies not available. Using default colors.")
        return "", {}
    
    # Load database
    db = ProjectLoader().load_db()
    df = db.to_dataframe(
        f"""SELECT (introNotes || songNote || calls || '*') AS note_sequence, 
        introNotes, songNote, calls FROM bird WHERE birdID='{bird_id}'"""
    )

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