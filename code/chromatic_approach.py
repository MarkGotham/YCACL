# -*- coding: utf-8 -*-
"""
NAME:
===============================
Chromatic Approach (chromatic_approach.py)


BY:
===============================
Mark Gotham, 2022


LICENCE:
===============================
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================
Instead of finding possible cases of the 'freie Leittoneinstellung',
make them ;).
As defined in Feilen and Gotham (forthcoming).

"""


from shared import *
from itertools import chain, combinations, product
from music21 import chord, metadata, stream


def all_options(
        pitches_string: str,
        max_step: int = 1,
        cardinality: int = 3,
        common_tones: bool = False,
        require_all_destination: bool = True,
) -> tuple:
    """
    Return all voice-leading options, given constraints.

    :param pitches_string: a string listing the pitches of the destination chord.
    :param max_step: the maximum step size of voice leading approaching the destination.
    :param cardinality: the number of distinct notes in the preceding chord.
    :param common_tones: should common tones be considered as part of this, or excluded.
    :param require_all_destination: Require at least one approach to each of the destination chord tones.
    :return: tuple
    """

    slice_pitches = pitches_string_to_MIDI_list(pitches_string)

    # Voice-leading 2: step size
    expanded = {}
    for x in slice_pitches:
        expanded[x] = list(range(x - max_step, x + max_step + 1))
        if not common_tones:
            expanded[x].remove(x)

    if require_all_destination:
        list_of_lists = []
        for k in expanded:  # check more succinct version of this.
            list_of_combinations = []  # [60, 62, (60, 62), ...
            for i in range(1, len(expanded[k]) + 1):  # Note: the 1, range denotes the min one from each
                for x in combinations(expanded[k], i):
                    list_of_combinations.append(list(x))
            list_of_lists.append(list(list_of_combinations))  # replace list of single tones, with the combinations
        if len(list_of_lists) == 3:
            a, b, c = list_of_lists
            options = product(a, b, c)
        elif len(list_of_lists) == 4:
            a, b, c, d = list_of_lists
            options = product(a, b, c, d)
        else:
            raise ValueError("This function expects destination chords of cardinality 3 or 4")

    else:
        options = combinations(list(expanded.values()), cardinality)

    return pitches_string, options


def write_as_score(
        data: tuple,
        out_path: str = "./Chromatic_Approaches.mxl"
) -> None:
    """
    Write the options data in the form of a score
    :param data: output of `all_options`
    :param out_path: where to write to.
    :return: None (writes a score)
    """
    p = stream.Part()
    for this_perm in data[1]:
        this_perm = list(chain(*this_perm))  # flatten
        this_chord = chord.Chord(this_perm)
        iv = pitches_to_iv(this_perm)
        if iv in iv_to_str:
            this_chord.lyric = iv_to_str[iv]
        else:
            this_chord.lyric = iv
        this_chord.duration.quarterLength = 2
        p.append(this_chord)

        # Sic, re-make each time (it's that or make copies)
        destination_chord = chord.Chord(data[0])
        destination_chord.duration.quarterLength = 2
        p.append(destination_chord)

    md = metadata.Metadata()
    md.title = f"Chromatic Approaches to {data[0]}"
    md.composer = "Prepared by Mark Gotham for (redacted, forthcoming)"
    p.insert(0, md)
    p.write("mxl", out_path)


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    write_as_score(all_options("E4 G4 B4"))
