This encoder turns a string of the most common ascii characters and turns it into a string with "5"-bits per char (on average it's more 5.1 bits).

To run an example

    python3 encoder5bit.py "This is a test?"

Output:


    Orig. String:   This is a Test!
    Orig. Length:   15
    Encoded String: 9FCE896912D035E9FC929FFE2FEC
    Encoded length: 14
    Code Point: T
    Code Point: <forward>
    Code Point: h
    Code Point: i
    Code Point: s
    Code Point:  
    Code Point: i
    Code Point: s
    Code Point:  
    Code Point: a
    Code Point:  
    Code Point: <back>
    Code Point: T
    Code Point: <forward>
    Code Point: e
    Code Point: s
    Code Point: t
    Code Point: <forward>
    Code Point: <forward>
    Code Point: !
    Code Point: <forward>
    Code Point: <stop>
    Decoded String: This is a Test!

