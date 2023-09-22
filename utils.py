import hashlib
import sys
import logging
from termcolor import colored


def hash256(val):
    return hashlib.sha256(val.encode()).hexdigest()


def ensure_even(hashes):
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])


def check(err):
    if err is not None:
        logging.error(err)
        sys.exit(1)


def print_event(*args):
    magenta = lambda x: colored(x, "magenta")
    print(magenta("event"), " ".join(args))


def is_leaf(node):
    return node.left is None and node.right is None


def print_help_manual():
    print(
        "Available commands:\n\t1. make create-file - create a random test file, size: 1GB\n\t2. make run -\n\t\ta) create a Merkle tree using 'data.txt' generated in (1)\n\t\tb) print the Merkle tree (hashes only)\n\t\tc) run membership and non-membership proofs using the generated Merkle tree and hardcoded hashes"
    )
