"""
Unit 4 Seminar: Programming Language Concepts - Recursion
Towers of Hanoi

This program solves the Towers of Hanoi puzzle using recursion.
Disks are represented by asterisks (a disk of size n is shown as "n stars").
The program asks the user for the number of disks, executes every move,
and displays the total number of moves performed at the end.
"""

import sys


# A safety cap applied on top of Python's recursion limit.
# It prevents the program from running for impractical lengths of time
# (the algorithm performs 2**n - 1 moves) and blocks the most obvious
# Denial-of-Service style inputs. See the accompanying report for details.
MAX_DISKS = 25


def tower_of_hanoi(n, source, target, auxiliary, pegs, move_counter):
    """
    Recursively move `n` disks from `source` peg to `target` peg,
    using `auxiliary` as the helper peg.

    Parameters
    ----------
    n            : int   - number of disks still to move
    source       : str   - name of the peg we are moving from
    target       : str   - name of the peg we are moving to
    auxiliary    : str   - name of the helper peg
    pegs         : dict  - maps peg name -> list of disks (largest at index 0)
    move_counter : list  - single-element list acting as a mutable counter
    """
    # Base case: nothing to do when there are zero disks left to move.
    if n == 0:
        return

    # Step 1: move the top n-1 disks out of the way, onto the auxiliary peg.
    tower_of_hanoi(n - 1, source, auxiliary, target, pegs, move_counter)

    # Step 2: move the single largest remaining disk from source to target.
    disk = pegs[source].pop()
    pegs[target].append(disk)
    move_counter[0] += 1
    print(f"Move {move_counter[0]:>4}: disk {'*' * disk:<{MAX_DISKS}} "
          f"{source} -> {target}")

    # Step 3: move the n-1 disks from auxiliary onto the target, on top
    # of the disk we just placed.
    tower_of_hanoi(n - 1, auxiliary, target, source, pegs, move_counter)


def read_disk_count():
    """
    Prompt the user for a disk count and validate it.
    Returns a safe, positive integer or None if the input is rejected.
    """
    try:
        value = int(input(f"Enter the number of disks (1-{MAX_DISKS}): "))
    except ValueError:
        print("Invalid input: please enter a whole number.")
        return None

    if value < 1:
        print("Invalid input: the number of disks must be a positive integer.")
        return None

    if value > MAX_DISKS:
        print(f"Invalid input: the maximum allowed is {MAX_DISKS} disks "
              f"(2**{MAX_DISKS} - 1 moves is already a very large number).")
        return None

    return value


def main():
    n = read_disk_count()
    if n is None:
        sys.exit(1)

    # Build the initial state: all disks on peg A, peg B and C empty.
    # Largest disk (value n) is at index 0; smallest disk (value 1) is on top.
    pegs = {
        "A": list(range(n, 0, -1)),
        "B": [],
        "C": [],
    }

    move_counter = [0]
    tower_of_hanoi(n, "A", "C", "B", pegs, move_counter)

    print(f"\nTotal moves executed : {move_counter[0]}")
    print(f"Theoretical minimum  : {2 ** n - 1}")


if __name__ == "__main__":
    main()
