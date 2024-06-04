# -*- coding: utf-8 -*-
"""
NAME:
===============================
Freie Leittoneinstellung (freieLeittoneinstellung.py)


BY:
===============================
Mark Gotham, 2022


LICENCE:
===============================
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/


ABOUT:
===============================
Find possible cases of the 'freie Leittoneinstellung'
as defined in Feilen and Gotham (forthcoming).

"""

from shared import *


def is_freie_Leittoneinstellung(
        slice_1: str,
        slice_2: str,
        require_no_common_tone: bool = False,
        require_slice_1_not_common: bool = True,
        require_slice_2_common: bool = True,
        min_distinct: int = 3,
        max_step: int = 1
):
    """
    Checks if a pair of successive 'slices' (vertical cross-section)
    make a potential case of the 'freie Leittoneinstellung' as defined in the following.

    As so often, reference to this in music theoretic literature
    lacks a robust definition, so this is a first attempt to implement one.
    
    Here then are the proposed rules based on trial and error for catching 
    all and only the relevant cases.

    IN THEORY

    1. `slice_1`: the moment of potential freie Leittoneinstellung.
    Expressed as a chord, this slice may be required to
    - have a certain number of distinct pitches (`min_distinct`: default = 3)
    - not be triad or a seventh, nor an incomplete case of either.

    2. `slice_2`: the slice after (the 'destination' chord or 'moment of resolution')
    This chord, by contrast, must be either a triad or a seventh.

    Note that as long as `slice_1` isn't a complete/incomplete triad or seventh
    and the `slice_2` is, then definitely we don't have a simple repetition
    or even a sub-/superset relationship.
    
    3. Chromatic Motion
    This is key to the freie Leittoneinstellung character.
    Every pitch may be requried to move by
    not more than a specific interval (`max_step`: default = 1)
    half-step away from at least one note in the second chord.
    Given the highly chromatic character, and the tendency of such moments to 
    give rise to a variety of pitch spellings,
    this is calculated without pitch spelling at all, on MIDI pitch numbers.
    There can also be a de facto minimum step by excuding common tones ...

    4. No common tones
    By default (`require_no_common_tone`),
    we require that all tones move from the `slice_1` to the resolution.
    Apart from the maximum inteval (discussed above),
    this requires that all tones do indeed move (i.e., a lack of common tones).
    This is because some chromatic motion over common tones typically
    indicates other musical devices such as incomplete neighbour tones and appogiature.

    Classic examples include the following passage in
    measures 148-152 of Mozart 40, movement i.
    We analyse that passage as follows.

    First we have a pair parallel diminished 7ths.
    Although highly dissonant, our defaults exclude this as the first slice is a common chord:

    >>> is_freie_Leittoneinstellung("B5 G#5 D5 E#4", "C6 A5 E-5 F#4")
    False

    Then, next time the E-flat to D motion is reversed
    (the notes are "swapped"), making for a
    highly dissonant first chord, and a
    V7 on D as the resolution chord.
    This would not necessarily be enough,
    as "E-6 G#5 B4" can be spelt as "E-6 Ab-5 C-4"
    (i.e., another common chord).
    Mozart also adds a G-F# motion
    (the G being a false-relation against the G#).
    This seals the deal.

    >>> is_freie_Leittoneinstellung("E-6 G#5 B4 G4", "D6 A5 C5 F#4")
    True

    The third iteration sees the same pitches as this second case, re-voiced.
    """

    # Slice 1
    slice_pitches_1 = pitches_string_to_MIDI_list(slice_1)
    pcs1 = [p % 12 for p in slice_pitches_1]
    num_distinct = len(pcs1)

    if min_distinct < 3:
        raise ValueError("The `min_distinct` value must be 3 or more.")

    if num_distinct < min_distinct:
        return False

    if require_slice_1_not_common:
        if num_distinct == 3:
            if is_triad(pcs1):
                return False
        elif num_distinct == 4:
            if is_seventh(pcs1):
                return False

    # Slice 2
    slice_pitches_2 = pitches_string_to_MIDI_list(slice_2)
    pcs2 = [p % 12 for p in slice_pitches_2]

    if require_slice_2_common:
        if num_distinct == 3:
            if not is_triad(pcs2):  # NB: not
                return False
        elif num_distinct == 4:
            if not is_seventh(pcs2):  # NB: not
                return False

    # Voice-leading 1: comon-tones
    if require_no_common_tone:
        intersect = [i for i in slice_pitches_1 if i in slice_pitches_2]
        # Note: this specifies octave. To run on PC alone, use pcs_1, pcs_2.  TODO: review octave: common pitch class?
        if not len(intersect) == 0:
            print(f"Common tones: {intersect}")
            return False

    # Voice-leading 2: step size
    expanded = []
    for x in slice_pitches_1:
        expanded += range(x - max_step, x + max_step + 1)  # TODO poss. refactor with common tones (including x)
    for p in list(set(slice_pitches_2)):
        if p not in list(set(expanded)):
            print(f"Beyond a step of {max_step} semitones: {p}")
            return False

    return True


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest
    doctest.testmod()
