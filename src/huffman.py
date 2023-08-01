"""
CHANGE LOG
-----------------------------------------------------------
2023.07.30    Rewrote tree routines and encoder in python.
2004.05.09    Huffman encoder routines in VBscript on ASP
"""

DEBUG = False

leaf_list = []  # list of Leaf objects
leaf_ref = []  # list of Leaf objects
trace_id = 0  # each leaf that is created gets a trace id


# This is the main datastructure of each node.
class Leaf:
    """
The instantiated leaf object is a node in the Huffman tree.
    """
    parent_leaf = None  # as Leaf
    left = None  # as Leaf
    right = None  # as Leaf
    ascii_value = 0
    weight = 0
    bit = ""
    leaf_id = 0

    def __init__(self, ascii_value=0, weight=0):
        """
Constructor
        """
        # Each Leaf object gets its own unique identifier. Use a sequential number.
        self.leaf_id = _get_next_id()

        self.ascii_value = ascii_value
        self.weight = weight


def initialize_huffman(weight_filename, bit_on="1", bit_off="0"):
    """
Needs to be called before doing an encode or decode.
Builds a tree of nodes.
Your weighting file should cover all 256 ascii characters.
    """
    global leaf_list, leaf_ref

    if DEBUG:
        print("weight filename is [%s]" % weight_filename)

    # Read all lines of the weighting file
    node_count = 0
    with open(weight_filename, mode='r', encoding='utf-8') as fd_in:
        for line in fd_in:
            ascii_value, weight = line.split()
            if DEBUG:
                print("Tokens: ascii [%s] weight [%s]" % (ascii_value, weight))

            # Populate the initial leafs
            # leaf_list[node_count] = Leaf(ascii_value, weight)
            leaf_list.append(Leaf(ascii_value, weight))
            node_count = node_count + 1

    # Make a reference to each node before the combination
    leaf_ref = leaf_list.copy()

    # The initial leaves are already sorted from highest to lowest.
    # Start the combining.

    node_count = len(leaf_list) - 1
    while node_count > 0:

        # print("---------------------------------------\ntree loop [%d]" % node_count)

        leaf_new = Leaf()
        # print("created new leaf leaf_id [%d]" % leaf_new.leaf_id)

        # Swap contents of N - 1 (second to last) with X
        if DEBUG:
            print("Swapping new leaf_id [%d] with [%d]" % (
                leaf_new.leaf_id, leaf_list[node_count - 1].leaf_id
            ))
        leaf_new, leaf_list[node_count - 1] = leaf_list[node_count - 1], leaf_new

        # Make N - 1 into the combined X + N
        leaf_list[node_count - 1].left = leaf_new
        leaf_list[node_count - 1].right = leaf_list[node_count]
        leaf_list[node_count - 1].weight = int(leaf_new.weight) + int(leaf_list[node_count].weight)
        # print("the new weight is [%d]" % leaf_list[node_count-1].weight)

        # Set the parent_leaf
        leaf_list[node_count - 1].left.parent_leaf = leaf_list[node_count - 1]
        leaf_list[node_count - 1].right.parent_leaf = leaf_list[node_count - 1]
        if DEBUG:
            print("leaf_id [%d] has L [%d] R [%d]" % (
                leaf_list[node_count - 1].leaf_id, leaf_list[node_count - 1].left.leaf_id,
                leaf_list[node_count - 1].right.leaf_id
            ))

        # Set the bit of each node
        leaf_list[node_count - 1].left.bit = bit_on
        leaf_list[node_count - 1].right.bit = bit_off

        # Nix X
        del leaf_new

        # Re-sort taking advantage of the original sorting
        if node_count - 2 > -1:
            if int(leaf_list[node_count - 1].weight) > int(leaf_list[node_count - 2].weight):
                if DEBUG:
                    print("must sort because [%s] > [%s]" % (
                        leaf_list[node_count - 1].weight,
                        leaf_list[node_count - 2].weight
                    ))
                _sort_leaves(node_count)

        node_count = node_count - 1


def _sort_leaves(node_count):
    """
Sorts by weight. Swaps as part of sorting.
    """
    global leaf_list

    # print("node_count [%d]" % node_count)

    for i in range(0, node_count - 1):
        for j in range(i + 1, node_count - 0):
            # The order is determined by the < or > sign
            # < = highest to lowest
            # > = lowest to highest
            # print("checking I [%s] < J [%s]" % (leaf_list[i].weight, leaf_list[j].weight))
            if int(leaf_list[i].weight) < int(leaf_list[j].weight):
                # Swap
                if DEBUG:
                    print("Swapping I [%s] with J [%s]" % (leaf_list[i].weight, leaf_list[j].weight))
                leaf_list[i], leaf_list[j] = leaf_list[j], leaf_list[i]


def huffman_encode(value_str):
    """
Does the actual encoding of a text string.
    """
    length = len(value_str)
    ret_string = ""

    print("About to encode [%s] len [%d]" % (value_str, length))

    # Loop over characters in the string
    for i in range(0, length):
        # Get the ascii value of the current character
        cur_ascii = ord(value_str[i])
        # print("i [%d] character [%s] cur_ascii [%d]" % (i, value_str[i], cur_ascii))

        # Find the character in the list of nodes
        node_count = len(leaf_list)
        for j in range(0, node_count - 1):

            # Did we find our character in the leaves?
            # print("Ascii [%d] cur_ascii [%d]" % (leaf_ref[j].ascii_value, cur_ascii))
            if int(leaf_ref[j].ascii_value) == cur_ascii:
                if DEBUG:
                    print("i [%d] j [%d] found letter [%s] @ leaf_id [%d]" % (
                        i, j, chr(cur_ascii), leaf_ref[j].leaf_id
                    ))

                # Now trace the tree
                ptr_leaf = leaf_ref[j]
                encoded_chr = ""
                while True:
                    # Move the pointer to the parent
                    if ptr_leaf.parent_leaf is not None:
                        # Print out the bit (don't print the top level)
                        encoded_chr = "%s%s" % (encoded_chr, ptr_leaf.bit)
                        # print("bit [%s] encoded_chr [%s]" % (ptr_leaf.bit, encoded_chr))

                        # Become the parent
                        ptr_leaf = ptr_leaf.parent_leaf
                        # print( "trace . . . leaf_id [%d]" % ptr_leaf.leaf_id)
                    else:
                        break

                # The letter is encoded.  Reverse it and add to the stream.
                ret_string = "%s%s" % (ret_string, _reverse(encoded_chr))
                break

    return ret_string


def huffman_decode(value_str, bit_on="1", bit_off="0"):
    """
Decodes an encoded huffman string
    """
    global leaf_list

    length = len(value_str)
    top_leaf = leaf_list[0]  # The top level node.
    ret_string = ""

    bit_idx = 0
    bit_string = ""
    found = False
    ptr_leaf = top_leaf
    while bit_idx < length - 1:

        # Did we find the node corresponding to a character?
        if found:
            ret_string = ret_string + chr(int(ptr_leaf.ascii_value))
            found = False
            ptr_leaf = top_leaf  # Always re-start at the top of the tree
        else:
            # Get the next bit for processing
            bit_string = value_str[bit_idx]
            # print("handling bit [%s] for bit_idx [%d]" % (bit_string, bit_idx))
            bit_idx = bit_idx + 1

        # Process the bit by scanning down the tree
        if bit_string == bit_off:
            # Bit = 0 (off)
            if ptr_leaf.right is not None:
                ptr_leaf = ptr_leaf.right
            else:
                found = True  # Got it!
        elif bit_string == bit_on:
            # Bit = 1 (on)
            if ptr_leaf.left is not None:
                ptr_leaf = ptr_leaf.left
            else:
                found = True  # Got it!

    ret_string = "%s%s" % (ret_string, chr(int(ptr_leaf.ascii_value)))

    return ret_string


def _reverse(value_str):
    """
Reverses the letters in a string
    """

    ret_string = ""
    length = len(value_str)

    for i in range(length - 1, -1, -1):
        # print("length [%d] i [%d] char at i [%s]" % (length, i, value_str[i]))
        ret_string = "%s%s" % (ret_string, value_str[i])

    # print("reversal of [%s] is [%s]" % (value_str, ret_string))
    return ret_string


def _get_next_id():
    """
Returns an ID for tracing
    """
    global trace_id

    trace_id = trace_id + 1
    return trace_id


def binary_string_to_chars(line):
    """
Converts a string of 10110001. . .  to equivalent characters.
    """
    print("line [%s]" % line)
    segments = [line[i:i + 8] for i in range(0, len(line), 8)]
    print("segments [%s]" % segments)
    for segment in segments:
        ascii_value = int(segment, 2)
        # char = chr(ascii_value)
        print("segment [%s] converted to [%s]" % (segment, ascii_value))

    # TODO: figure best way to return this
    return ""
