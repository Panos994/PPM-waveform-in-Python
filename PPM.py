import numpy as np
import matplotlib.pyplot as plt


#from commlib library 
def gray_code(m):
    if m == 1:
        g = ['0', '1']
    elif m > 1:
        gs = gray_code(m - 1)
        gsr = gs[::-1]
        gs0 = ['0' + x for x in gs]
        gs1 = ['1' + x for x in gsr]
        g = gs0 + gs1
    return g


def encode_to_gray_code_bits(ascii_bits):
    gray_code_result = [0]
    gray_code_result += [int(gray_code_result[-1]) ^ bit for bit in ascii_bits]
    return gray_code_result[1:]

def ppm_waveform(M, bits, TS):
    t_ppm = np.repeat(np.arange(0, len(bits) * TS / M, TS / M), M)
    x_ppm = np.tile(bits, M)

    return t_ppm, x_ppm

def encode_name_to_bits(name):
    # Μετατροπή κάθε χαρακτήρα με βάσει 8-bit ASCII
    ascii_bits = [format(ord(char), '08b') for char in name]

    # μετατροπή σε numpy array
    all_bits = np.array([int(bit) for bit in ''.join(ascii_bits)])

    return all_bits  #  0 και 1 σαν amplitudes

def bits_to_symbols(bits, M):
    log2M = int(np.log2(M))
    symbols = []

    for i in range(0, len(bits), log2M):
        symbol_bits = bits[i:i+log2M]

        # Αν το τελευταιο  group ειανι λιγότερο από log2M, γέμισμα με zeroes
        while len(symbol_bits) < log2M:
            symbol_bits.append(0)

        symbols.append(symbol_bits)

    return symbols

# Το full name μου
name = "Panagiotis Foteinopoulos"

# M values 
M_values = [2, 4, 8, 16]
Rb = 1.0e9  # 1 Gb/s

#TS = 1.0 / Rb (=)
#Ts είναι : Ts = log2 (M) / Rb 8α το χρησιμοποιήσω μετά

# Δημιουργία συμβόλων και Plots για διαφορετικές M values
for M in M_values:
    # το ονομά μου σε ASCII bits
    ascii_bits = encode_name_to_bits(name)
    
    TS = np.log2(M) / Rb # είναι το Ts = log2M / Rb
    
    # από ASCII bits σε Gray code bits
    gray_code_bits = encode_to_gray_code_bits(ascii_bits)

    # μετατροπή total bits σε symbols για M-PPM
    symbols = bits_to_symbols(gray_code_bits, M)

    # Plot PPM κυματομορφή
    t_ppm, x_ppm = ppm_waveform(M, gray_code_bits, TS)
    plt.figure()
    plt.plot(t_ppm, x_ppm, drawstyle='steps-post')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title(f'PPM Waveform for M={M}')
    plt.grid(True)
    plt.show()

    print(f'Symbols for M={M}: {symbols}')
