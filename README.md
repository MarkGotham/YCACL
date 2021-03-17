# YCACL
'YCACL' stands for 'YCAC Light' and reads as 'Why Cackle?'

This is light(er) version of the 'Yale-Classical Archives Corpus' (YCAC) as reported in White and Quinn (EMR 2014) and available here: [https://ycac.yale.edu/](https://ycac.yale.edu/).

The YCAC corpus is useful for a range of tasks, though it is a little unwieldy in some ways.
This is an attempt to make YCAC more readily and immediately usable for the majority of prospective use cases including as training data for machine learning.

YCACL also represents a significant compression of the corpus' size.
Overall, this repo is about 8x smaller than the original, while offering the same content and functionality for most purposes.
For instance, there are 639 pieces by J.S. Bach in the corpus.
YCAC represents them in 1 file of 70Mb; YCACL has them in one file per piece with a combined size of 9Mb.

## What's changed?

YCACL mostly serves to repackage the same content more efficiently through a series of small changes that amount to a significant size reduction when scaled up to the size of this corpus (some 6 million 'slice' entries).
Those changes are as follows:
- **Single files per work.** As mentioned above, YCAC broadly uses one file per composer, while YCACL moves to one per piece. This rearrangement removes the need for the `file` column of YCAC which duplicated statement of the file name anew for every slice.
- **Simplification of the `chord` column.** YCAC entries for chords which take the form `<music21.chord.Chord A4 A5>` are simplified to simply `A4 A5`. This represents no loss of functionality. In fact, it helps speed up processing by extracting the relevant information necessary to any use case. Even turning these entries into `music21.chord` objects would require this modification as a first step: `chord.Chord()` accepts strings like `A4 A5`, but not the longer form.
- **Remove entries that can be retrieved from the chord.** The columns `NormalForm`, `PCsInNormalForm`, `GlobalScaleDegrees`, `HighestPitch`, `LowestPitch` are all removed as they can be easily and unambiguously recreated from the chord. For instance, a `music21.chord` object has `.normalForm` among its attributes and other code libraries work in a broadly similar way. That said, creating these objects anew adds computational load, so use cases working specifically on normal form for which computational efficiency is a priority may prefer to use with the original YCAC.
- **Compress `LocalTonic` and `LocalMode` columns**. Use shorter strings, preserving all the information in a more compressed way.
- **Remove `confidence` column**. The most controversial change in YCACL is the outright removal of the `confidence` column. Again, use cases for which this is important should use the original dataset.
- **All files parse.** Processing all of this have also meant resolving some issues with YCAC files that certain libraries for reading csvs could not parse them.
- **Version control.** Finally, hosting the corpus here makes PRs possible and will mean that any future changes there might be are both publicly visible and recorded with version control.

## Summary of the columns, old and new

In summary: YCAC's column listings are processed as follows:
- `offset`: retained and directly interpretable when converted from string to float.
- `Chord`: retained as a shorter and more immediately usable string.
- `NormalForm`, `PCsInNormalForm`, `GlobalScaleDegrees`, `HighestPitch`, `LowestPitch`: all removed as retrievable from the chord.
- `file` and `Composer`: removed as now present exactly once in the file name.
- `LocalTonic`: retained and directly interpretable when converted from string to int (range 0-11).
- `LocalMode`: retained but compressed from
  - 'Ambiguous' to '?',
  - 'major' to 'M', and 
  - 'minor' to 'm'.
- `LocalSDForm_BassSD` and `Confidence`: removed

As such, the columns and data types for YCACL files are thus:
0. `offset`: `float`
1. `chord`: `str`
2. `LocalTonic`: `int` in the range 0-11, or `str` (`?`) when ambiguous.
3. `LocalMode`: `str`, one of `['?', 'M', 'm']`


## People, Licence, Acknowledgements

The original YCAC website: 
- Acknowledges that it was developed 'in connection with the ELVIS Project and funded in part by a grant from the Digging Into Data Challenge, with additional support from the Allen Forte Research Fund at Yale University.'
- Does not currently specify a licence.

This 'YCACL' version:
- Is provided with the permission of YCAC's original authors (White and Quinn).
- Does not stipulate any additional restrictions.

Acknowledgement in public facing work (e.g. research publication) making use of this data is welcome.

Finally, for code producing new files in a format like directly from scores, head to [this repo](https://github.com/MarkGotham/Moments) as reported in [this paper]( https://doi.org/10.1145/3358664.3358676).
