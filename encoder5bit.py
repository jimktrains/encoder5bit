#!/usr/bin/env python3
import sys

encode = True

#if (sys.argv[1] == 'd'):
#    encode = False
#
#if(len(sys.argv) == 3):
#    val = sys.argv[2]
#else:
#    val = input("> ")

val = sys.argv[1]
VERBOSE = True

class Encoder5Bit:
    # These are hard-coded conversion tables

    # hex-char -> bin
    hex_table = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    # These are the mappings for
    # the different modes to code-points. 
    # Each mode needs to have a <forward>
    # and <back> entries
    mode = [ {
        "A": "00000",
        "B": "00001",
        "C": "00010",
        "D": "00011",
        "E": "00100",
        "F": "00101",
        "G": "00110",
        "H": "00111",
        "I": "01000",
        "J": "01001",
        "K": "01010",
        "L": "01011",
        "M": "01100",
        "N": "01101",
        "O": "01110",
        "P": "01111",
        "Q": "10000",
        "R": "10001",
        "S": "10010",
        "T": "10011",
        "U": "10100",
        "V": "10101",
        "W": "10110",
        "X": "10111",
        "Y": "11000",
        "Z": "11001",
        " ": "11010",
        "<stop>":    "11011",
        "<back>":    "11110",
        "<forward>": "11111"
    },
    {
        "a": "00000",
        "b": "00001",
        "c": "00010",
        "d": "00011",
        "e": "00100",
        "f": "00101",
        "g": "00110",
        "h": "00111",
        "i": "01000",
        "j": "01001",
        "k": "01010",
        "l": "01011",
        "m": "01100",
        "n": "01101",
        "o": "01110",
        "p": "01111",
        "q": "10000",
        "r": "10001",
        "s": "10010",
        "t": "10011",
        "u": "10100",
        "v": "10101",
        "w": "10110",
        "x": "10111",
        "y": "11000",
        "z": "11001",
        " ": "11010",
        ",": "11011",
        ".": "11100",
        "<back>":    "11110",
        "<forward>": "11111"
    },
    {
        "0": "00000",
        "1": "00001",
        "2": "00010",
        "3": "00011",
        "4": "00100",
        "5": "00101",
        "6": "00110",
        "7": "00111",
        "8": "01000",
        "9": "01001",
        " ": "01010",
        "+": "01011",
        "-": "01100",
        "*": "01101",
        "(": "01110",
        ")": "01111",
        "_": "10000",
        "=": "10001",
        "/": "10010",
        "": "10011",
        "": "10100",
        "": "10101",
        "": "10110",
        "": "10111",
        "": "11000",
        "": "11001",
        "": "11010",
        "": "11011",
        "": "11100",
        "<back>":    "11110",
        "<forward>": "11111"
    },
    {
        "~": "00000",
        "`": "00001",
        "!": "00010",
        "@": "00011",
        "@": "00100",
        "#": "00101",
        "$": "00110",
        "%": "00111",
        "^": "01000",
        "&": "01001",
        "": "01010",
        "": "01011",
        "": "01100",
        "": "01101",
        "": "01110",
        "": "01111",
        "": "10000",
        "[": "10001",
        "]": "10010",
        "{": "10011",
        "}": "10100",
        "\\": "10101",
        "|": "10110",
        ":": "10111",
        ";": "11000",
        "\"": "11001",
        "<": "11010",
        ">": "11011",
        "?": "11100",
        " ": "11101",
        "<back>":    "11110",
        "<forward>": "11111"
        
    }]

    b = [""]
    mode_flip = []
    hex_flip = {}
    def __init__(self):
        # This creates a table of int -> binary
        # for ints 0-63
        for k in range(6):
            self.b = [i+j for i in ['0','1'] for j in self.b]

        # Flips the mode mappings
        # to do binary -> char mapping
        for i in range(len(self.mode)):
            self.mode_flip.append({self.mode[i][k] : k for k in self.mode[i]})

        self.hex_flip = { self.hex_table[i] : i for i in self.hex_table }
    # Maps a char to a code-point
    # with possible mode-switch code-points
    def encode_char(self, c, state):
        if c in self.mode[state.current_mode]:
            return self.mode[state.current_mode][c]
        else:
            if state.current_mode == state.last_mode:
                raise Exception("character not found")
            s = self.mode[state.current_mode]['<forward>']
            state.inc_mode()
            return s + self.encode_char(c, state)

    def decode_str(self, s):
        h = ""
        dec = ""
        state = EncoderState()

        for c in s:
            h += self.hex_table[c]
        s = h

        if len(s) % 5 != 0:
            s = s[:(len(s) - (len(s) % 5))]
        # Not going to store length anymore
        ## Reads the number of code-points
        ## stored in this string
        #m = (int(s[2:8], 2))
        ## Extract the code points from the
        ## string
        #s = s[8:8 + m*5] 
        lgth = len(s)

        # Runs though the string, switching modes
        # and extracting code-points as necessary
        for i in range(0, lgth, 5):
            c = self.mode_flip[state.current_mode][s[i:i+5]]
            if VERBOSE:
                print("Code Point: " + c)
            if c == "<forward>":
                state.inc_mode()
            elif c == "<back>":
                state.dec_mode()
            elif c == "<stop>":
                break
            else:
                dec += c
        return dec
        
    # Takes a string, converts each character to
    # one or more code-points and prepends the
    # length
    def encode_str(self, s):
        enc = []
        state = EncoderState()

        for c in s:
            enc.append(self.encode_char(c, state))
        enc.append(self.encode_char('<stop>', state))
        # Not going to store length anymore
        #enc_len = int(len(enc) / 5)
        #enc = "11" + self.b[enc_len] + enc

        one_back = len(self.mode) - 1

        fwd_cp = 0
        i = 0
        while i < len(enc):
            if enc[i].startswith('11111'*one_back):
               enc[i] = '11110' + enc[i][(5*(one_back)):]
            i += 1


        enc = "".join(enc)
        while len(enc) % 4 != 0:
            enc += '0'



        h = ""
        for i in range(0, len(enc), 4):
            h += self.hex_flip[enc[i:i+4]]

        return h

class EncoderState:
    current_mode = 0
    last_mode = -1
    def inc_mode(self, by=1):
        self.last_mode = self.current_mode
        self.current_mode += by
        self.current_mode = (self.current_mode % len(Encoder5Bit.mode))
    def dec_mode(self):
        return self.inc_mode(-1)


encoder = Encoder5Bit()

print("Orig. String:\t" + val)
print("Orig. Length:\t" + str(len(val)))
if encode or True:
    enc = encoder.encode_str(val)
    
    print("Encoded String:\t" + enc)
    print("Encoded length:\t" + str(int(len(enc)/2)))
    val = enc
#else:
    dec = encoder.decode_str(val)
    print("Decoded String:\t" + dec)

