import os
import random
from termcolor import colored


class Direction:
    Left = "left"
    Right = "right"
    NoneDirection = ""


class ProofElement:
    def __init__(self, hash, direction):
        self.hash = hash
        self.direction = direction


# for proof of non-membership
hash_value_proof_of_non_membership = (
    "d72518be626086284a0003d7365aa035e76eb1cab7646c7a506a4143af2fe5fd"
)

# for proof of membership
elems = [
    ProofElement(
        hash="349ddc594c2f21c67faf35a8f4275719449b2314356842d60a4be5e3e299da41",
        direction=Direction.Left,
    ),
    ProofElement(
        hash="a5925e7b615e4c904f8ae036e88ad26e8f4eb358f4bac944675ce134bad02ce9",
        direction=Direction.Left,
    ),
    ProofElement(
        hash="4d608c1fd840aa9dd005403b71c295b13481d754d22c76f056c7bfb917f9cbcd",
        direction=Direction.Left,
    ),
    ProofElement(
        hash="376797797561b820ade42d3273d1c6811d4351b71e76f893333121d6c7c405e8",
        direction=Direction.Left,
    ),
    ProofElement(
        hash="e76d2dbcd31d40d4ee87b850d1a806b3ebbec7f3fabeecdc2d2cb0f33846d827",
        direction=Direction.Left,
    ),
    ProofElement(
        hash="5efa87d2a8ad7be128600d56fade5bd8afb61d555369a232e14fe43e30f17667",
        direction=Direction.Left,
    ),
    ProofElement(
        hash="fdf954e5ce8cb5bf32ca292f9de64e80a7cdecf904de4fe50991222dd75202a6",
        direction=Direction.Right,
    ),
    ProofElement(
        hash="d135075ee5b8e87729e96821e9b798ee69d3ad0b8c68cc70cd462522b6ae7f6d",
        direction=Direction.NoneDirection,
    ),
]


def write_test_file(file):
    literals = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        " ",
        ".",
        '"',
        "'",
        ":",
        "?",
        "!",
        "(",
        ")",
        "[",
        "]",
    ]

    data = bytearray(8192000)

    print(colored("Writing Test File", "magenta"))

    for chunk in range(128):
        for i in range(len(data)):
            literal = random.choice(literals)
            data[i] = ord(literal)
        file.write(data)
        print("\r{}/1024 MB".format((chunk + 1) * 8), end="")
