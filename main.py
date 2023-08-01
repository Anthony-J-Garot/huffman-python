import huffman


def main():

    huffman.initialize_huffman("w_us_constitution.txt")

    test_string = "Just a simple test."

    # Verify encode
    encoded = huffman.huffman_encode(test_string)
    expected = "000011111110000001010111111000111001000010011111101010100100101111011010001010110000001"

    print()
    print(" encoded %s" % encoded)
    print("expected %s" % expected)
    print()

    # Just letter A
    #print("To chars [%s]" % huffman.binary_string_to_chars("1000001"))

    print("To chars [%s]" % huffman.binary_string_to_chars(encoded))

    # Verify decode
    decoded = huffman.huffman_decode(encoded)
    print()
    print(" decoded %s" % decoded)
    print("expected %s" % test_string)
    print()

    longer_test_string = "Huffman Coding is a technique of compressing data to reduce its size without losing any of the details. It was first developed by David Huffman. Huffman Coding is generally useful to compress the data in which there are frequently occurring characters."
    encoded = huffman.huffman_encode(longer_test_string)
    print()
    print(" encoded %s" % encoded)
    #print("expected %s" % expected)
    print()


if __name__ == '__main__':
    main()

