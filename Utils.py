import math

def str_to_bin(text):
    return ''.join(format(ord(i), '08b') for i in text)

def str_to_hex(text):
    return text.encode("utf-8").hex()

def hex_to_bin(text):
    return format(int(text, 16), "064b")

def substitution(text,table):
    return ''.join(text[i-1] for i in table)

def split_key(text):
    return text[:28], text[28:]

def split_text(text):
    return text[:32], text[32:]

def xor_text(text,key):
    return ''.join(str(int(a) ^ int(b)) for a,b in zip(text,key))

def sbox(bin,table):
    row = int(bin[0] + bin[-1],2)
    col = int(bin[1:-1],2)
    return dec_to_bin(table[row][col])

def dec_to_bin(dec):
    return bin(dec)[2:].zfill(4)

def bin_to_hex(bin_str):
        result = ""
        for char in range(0, len(bin_str), 4):
            result = result + hex(int(bin_str[char: char + 4], 2))[2:]
        return result

def bin_to_str(bin):
    return ''.join(chr(int(bin[i:i+8],2)) for i in range(0,len(bin),8))

def pad_plaintext(text):
    padding = math.ceil(len(text) / 8) * 8
    return text.ljust(padding, " ")
