# -*- coding: utf-8 -*-
"""
NAME:
===============================
Shared (shared.py)


BY:
===============================
Mark Gotham, 2022


LICENCE:
===============================
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================
Shared functions for the 'freie Leittoneinstellung' work.
Feilen and Gotham (forthcoming).

"""


from itertools import combinations


pitch_name_to_PC = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}


def pitch_name_to_MIDI(pitch_name: str) -> int:
    """
    Convert a pitch name string to a MIDI number.

    :param pitch_name: a pitch name string in the format `<name><octave>`.
    :return: MIDI integer.

    >>> pitch_name_to_MIDI("C1")
    24

    >>> pitch_name_to_MIDI("C4")
    60

    >>> pitch_name_to_MIDI("C-4")
    59

    >>> pitch_name_to_MIDI("C#4")
    61

    >>> pitch_name_to_MIDI("C##4")
    62

    """
    try:
        octave = int(pitch_name[-1])  # always exactly one, last character.
    except:
        raise ValueError("Last character must be an integer denoting the octave")

    midi_number = (octave + 1) * 12

    try:
        pitch_step = pitch_name_to_PC[pitch_name[0]]  # always exactly one, last character.
    except:
        raise ValueError(f"First character must be in {pitch_name_to_PC.keys()}")

    midi_number += pitch_step

    if len(pitch_name) > 2:
        for i in pitch_name[1:-1]:
            if i in ["-", "b"]:
                midi_number -= 1
            elif i == "#":
                midi_number += 1
            else:
                raise ValueError("Middle characters must denote sharp or flat.")

    return midi_number


def pitches_string_to_MIDI_list(pitches_string: str) -> list[int]:
    """
    >>> pitches_string_to_MIDI_list("E-6 G#5 B4 G4")
    [87, 80, 71, 67]

    >>> pitches_string_to_MIDI_list("D6 A5 C5 F#4")
    [86, 81, 72, 66]

    :param pitches_string: a string listing pitches in the form "D6 A5 C5 F#4".
    :return:
    """
    pitches_list = pitches_string.split(" ")
    return [pitch_name_to_MIDI(x) for x in pitches_list]


def pitches_to_iv(pitches: list[int]):
    """
    From https://github.com/MarkGotham/Serial_Analyser/blob/main/pc_sets.py#L385
    In: a list or tuple of pitches.
    Out: the interval vector.
    """
    distinct = [p % 12 for p in pitches]
    vector = [0, 0, 0, 0, 0, 0]
    for p in combinations(distinct, 2):
        ic = p[1] - p[0]
        if ic < 0:
            ic *= -1
        if ic > 6:
            ic = 12 - ic
        vector[ic - 1] += 1
    return tuple(vector)


def is_of_type(
        midi_list: list[int],
        cardinality: int = 3,
        accepted_ivs: tuple[tuple] = ((0, 0, 2, 0, 0, 1), (0, 0, 1, 1, 1, 0), (0, 0, 0, 3, 0, 0))
) -> bool:
    """
    Shared function for checking chords against types.
    E.g., defaults set up for (see notes at) is_triad.
    """
    if not len(midi_list) == cardinality:
        return False

    if pitches_to_iv(midi_list) in accepted_ivs:
        return True

    return False


def is_triad(midi_list: list[int]) -> bool:
    """
    >>> is_triad([0, 3, 6])
    True

    >>> is_triad([0, 3, 7])
    True

    >>> is_triad([0, 4, 8])
    True

    >>> is_triad([0, 4, 7, 11])
    False

    >>> is_triad([0, 4, 7, 10])
    False

    >>> is_triad([0, 3, 7, 10])
    False

    >>> is_triad([0, 3, 6, 10])
    False

    :param midi_list:
    :return: bool
    """
    return is_of_type(midi_list)  # defaults


def is_seventh(midi_list: list[int]) -> bool:
    """
    >>> is_seventh([0, 3, 6])
    False

    >>> is_seventh([0, 3, 7])
    False

    >>> is_seventh([0, 4, 8])
    False

    >>> is_seventh([0, 4, 7, 11])  # maj
    True

    >>> is_seventh([0, 4, 7, 10])  # dom
    True

    >>> is_seventh([0, 3, 7, 10])  # min
    True

    >>> is_seventh([0, 3, 6, 10])  # half-dim
    True

    :param midi_list:
    :return: bool
    """
    return is_of_type(
        midi_list,
        cardinality=4,
        accepted_ivs=(
            (1, 0, 1, 2, 2, 0),
            (0, 1, 2, 1, 2, 0),
            (0, 1, 2, 1, 1, 1)
        )
    )


iv_to_str = {
    (0, 0, 2, 0, 0, 1): "diminished",
    (0, 0, 1, 1, 1, 0): "triad",  # maj/min
    (0, 0, 0, 3, 0, 0): "augmented",
    (1, 0, 1, 2, 2, 0): "major 7th",
    (0, 1, 2, 1, 2, 0): "minor 7th",
    (0, 1, 2, 1, 1, 1): "Dom7/half-dim7"
}


def norm_progression_to_lowest(
        pitches_string_1: str,
        pitches_string_2: str,
) -> list[list[int]]:
    """
    Takes two pitch strings
    (i.e., "slices" from the data set)
    and returns both as MIDI numbers,
    normalised to the lowest note that appears.

    Here's an example progression in close position (possibly V6-I):

    >>> norm_progression_to_lowest("E-5 B-4 G4", "E-5 C5 A-4")
    [[8, 3, 0], [8, 5, 1]]
    """
    list_1 = pitches_string_to_MIDI_list(pitches_string_1)
    list_2 = pitches_string_to_MIDI_list(pitches_string_2)

    min_val = min(list_1)
    if min(list_2) < min_val:
        min_val = min(list_2)

    return [[x - min_val for x in list_1], [x - min_val for x in list_2]]


def norm_by_key(
        pitches_string_1: str,
        pitches_string_2: str,
        tonic: int
) -> list[list[int]]:
    """
    Takes two pitch strings
    (i.e., "slices" from the data set)
    and returns both as lists of ints,
    normalised to the `tonic` argument.

    Here's the example progression, now explicitly as a V6-I:

    >>> norm_by_key("E-5 B-4 G4", "E-5 C5 A-4", 8)
    [[7, 2, 11], [7, 4, 0]]

    Suggested usage:
    take the YCAC team's estimate of local tonic (provided in the third column of the CSV files)
    and where that's missing `?`, use the global key provided in the metadata and file name.

    Note this function makes the distinction between major and minor keys:
    scale positions expressed in semi-tones from the tonic (0-11), not scale degrees (1-7).
    """
    list_1 = pitches_string_to_MIDI_list(pitches_string_1)
    list_2 = pitches_string_to_MIDI_list(pitches_string_2)
    return [[(x - tonic) % 12 for x in list_1], [(x - tonic) % 12 for x in list_2]]


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
