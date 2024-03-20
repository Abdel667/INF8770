from PIL import Image
import numpy as np
import time

def lzw(data):
    start_time = time.time()

    # Create a sorted list of unique symbols
    unique_symbols = sorted(set(data))

    # Compute binary code length and the initial message length
    code_length = len(format(len(unique_symbols) - 1, 'b'))
    initial_message_length = code_length * len(data)

    # Create the initial dictionary with keys as unique symbols and values as formatted binary codes
    dictionary = {symbol: format(i, '0' + str(code_length) + 'b') for i, symbol in enumerate(unique_symbols)}

    next_code = len(dictionary) 
    compressed_data = []
    current_sequence = data[0]

    for symbol in data[1:]:
        current_sequence += symbol
        if current_sequence not in dictionary:
            # Append the code for the previous sequence to the compressed data
            compressed_data.append(dictionary[current_sequence[:-len(symbol)]])

            # Check if the binary codes need to be resized
            if next_code >= 2**code_length:
                code_length += 1
                for key in dictionary:
                    dictionary[key] = format(int(dictionary[key], 2), '0' + str(code_length) + 'b')

            # Add the current_sequence to the dictionary
            dictionary[current_sequence] = format(next_code, '0' + str(code_length) + 'b')
            next_code += 1

            # Reset the current sequence to the last symbol
            current_sequence = symbol

    # Append the code for the last sequence
    compressed_data.append(dictionary[current_sequence])

    # Result of compression
    print("Longueur = {0}".format(sum(len(code) for code in compressed_data)))
    print("Longueur originale = {0}".format(initial_message_length))

    end_time = time.time()
    print("Temps d'encodage: {0} secondes".format(end_time - start_time))

    return compressed_data, dictionary


def compress_text(path):
    # Read the text file
    with open(path, 'r') as file:
        message = file.read()
    
    # Run lzw compression on the text message
    lzw(message)


def compress_image(path):
    # Read the image file
    image = np.array(Image.open(path))
    print(image.shape)

    # Flatten the image array
    flattened_image = image.reshape(-1)

    # Convert each rgb value to a char
    data = [chr(rgb) for rgb in flattened_image]

    # Run lzw compression on the pixels
    lzw(data)


def main():
    path = 'Images/image_1.png'

    # Use for image compression
    compress_image(path)

    # Use for text compression
    # compress_text(path)

if __name__ == "__main__":
    main()