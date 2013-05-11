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

class Encoder5Bit:
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
        "*": "01010",
        "(": "01011",
        ")": "01100",
        "_": "01101",
        "-": "01110",
        "+": "01111",
        "=": "10000",
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
        "/": "11101",
        "<back>":    "11110",
        "<forward>": "11111"
        
    }]

    b = [""]
    mode_flip = []

    def __init__(self):
        for k in range(6):
            self.b = [i+j for i in ['0','1'] for j in self.b]

        for i in range(len(self.mode)):
            self.mode_flip.append({self.mode[i][k] : k for k in self.mode[i]})
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
        m = (int(s[2:8], 2))
        s = s[8:8 + m*5] 
        lgth = len(s)
        for i in range(0, lgth, 5):
            c = self.mode_flip[state.current_mode][s[i:i+5]]
            if c == "<forward>":
                state.inc_mode()
            elif c == "<back>":
                state.dec_mode()
            else:
                dec += c
        return dec
        
    def encode_str(self, s):
        enc = ""
        state = EncoderState()
        for c in s:
            enc += self.encode_char(c, state)

        enc_len = int(len(enc) / 5)
        enc = "11" + self.b[enc_len] + enc

        while len(enc) % 8 != 0:
            enc += '0'
        enc = ("%X" % int(enc, 2))

        return enc

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

