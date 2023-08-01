"""
Main module of application
"""
import huffman


def main():
    """
Main routine of python application.
    """
    huffman.initialize_huffman("weight_files/w_us_constitution.txt")

    test_string = "Just a simple test."

    # Verify encode
    encoded = huffman.huffman_encode(test_string)
    expected = "000011111110000001010111111000111001000010011111101010100100101111011010001010110000001"

    print()
    print(" encoded %s" % encoded)
    print("expected %s" % expected)
    print()

    # Just letter A
    # print("To chars [%s]" % huffman.binary_string_to_chars("1000001"))

    print("To chars [%s]" % huffman.binary_string_to_chars(encoded))

    # Verify decode
    decoded = huffman.huffman_decode(encoded)
    print()
    print(" decoded %s" % decoded)
    print("expected %s" % test_string)
    print()


if __name__ == '__main__':
    main()
