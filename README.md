This encoder turns a string of the most common ascii characters and turns it into a string with "5"-bits per char (on average it's more 5.1 bits).

At the moment, a length is included in the packed string and limits the string length to 64 code-points.  This isn't strictly necessary and will probably be removed in the near future.

To run an example

    python3 encoder5bit.py "This is a test?"

Output:

    Orig. String:   This is a test?
    Orig. Length:   15
    Encoded String: D19FCE896912D035324A7FE0
    Encoded length: 12
    Decoded String: This is a test?

