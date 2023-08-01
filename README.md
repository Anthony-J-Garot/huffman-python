Huffman Encoder using golang.

# Introduction

In 2004, as a lark, I created a Huffman Encoder web page using VBscript/ASP. I found the code and decided to migrate it
to python.

# What is Huffman?

It's an encoding mechanism whereby a tree of nodes is formed from a source text, then strings can be encoded using that
tree to potentially make the string smaller.

The nodes are typically binary, 1 and 0.

As an example:

```
Just a simple test.
```

coverts into

```
000011111110000001010111111000111001000010011111101010100100101111011010001010110000001
```

While that seems to be longer, the binary can be converted into characters, so the actual length is the binary stream
divided by 8.

# Huffman Reference

- [Wikipedia Page](https://en.wikipedia.org/wiki/Huffman_coding)
- [Stack Overflow](https://stackoverflow.com/questions/70245937/why-huffmans-coding-algorithm-takes-more-bit-than-the-original-size)

# Features

- lossless compression

# Uses

- obfuscate a string

