import os
import sys
import time
import math
from termcolor import colored
from utils import print_help_manual
from utils import print_event
from utils import check
from data import write_test_file
from merkle_tree import MerkleTree
from data import ProofElement
from data import Direction
from data import elems
from data import hash_value_proof_of_non_membership


def handle_command(args):
    command = args[1]
    if command == "create-file":
        print_event("writing into data.txt...")
        elapsed_time = exec_command(command)
        print(colored("\nFile written successfully!", "green"))
        print(colored("\t{:2f}ms".format(elapsed_time / 1000 * 1000), "yellow"))
        print("\nHint: run 'make run' to run the program")
    else:
        print_help_manual()


def exec_command(command):
    start_time = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    if command == "create-file":
        try:
            with open("data.txt", "ab") as file:
                write_test_file(file)
        except Exception as e:
            check(e)
    return time.clock_gettime_ns(time.CLOCK_MONOTONIC) - start_time


def read_file_chunks(file):
    file_size = os.path.getsize(file.name)
    bytes_to_read = math.ceil(file_size / 128)
    chunks = []

    while True:
        data = file.read(bytes_to_read)
        if not data:
            break
        chunks.append(data.decode("utf-8"))

    return chunks


def proof_of_membership(tree):
    last_elem_hash = elems[-1].hash
    print_event(f"verifying membership of {last_elem_hash}")
    node = tree.prove_membership(elems)

    bytes_to_print = 512
    if node is not None:
        print(
            colored(
                f"Data exists in the Merkle tree! Data Head ({bytes_to_print}/{8192000} bytes):",
                "green",
            )
        )
        print(node.content[:bytes_to_print])
    else:
        print(colored("No such data.\n", "red"))


def proof_of_non_membership(tree):
    print_event(f"verifying non-membership of {hash_value_proof_of_non_membership}")
    exists = not tree.prove_non_membership(hash_value_proof_of_non_membership)

    if exists:
        print(colored("Data exists in the Merkle tree!\n", "red"))
    else:
        print(colored("Data does not exist!\n", "green"))


def main():
    args = sys.argv

    if len(args) > 1:
        handle_command(args)
        return

    filepath = "data.txt"
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            print_event("reading file...")
            chunks = read_file_chunks(f)

            print_event("generating merkle tree...")
            tree = MerkleTree(chunks)

            tree.print_tree()

            # print("Merkle Tree Root:", tree.root_hash())

            proof_of_membership(tree)
            proof_of_non_membership(tree)

    else:
        print(
            f"File not found: {filepath}\nYou may want to run 'make create-file' first."
        )


if __name__ == "__main__":
    main()
