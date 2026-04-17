"""
UK postcode validator using a regular expression.
MSc Secure Software Development Module

Rules from idealpostcodes (2020) / Royal Mail PAF:

    AN   NAA -> e.g. M1 1AA
    ANN  NAA -> e.g. M60 1NW
    AAN  NAA -> e.g. CR2 6XH
    AANN NAA -> e.g. DN55 1PT
    ANA  NAA -> e.g. W1A 1HQ
    AANA NAA -> e.g. EC1A 1BB

    A = letter, N = digit.

"""

import re

UK_POSTCODE_PATTERN = re.compile(
    r"^(GIR 0AA|"
    r"[A-PR-UWYZ]"                 # 1: first letter, not QVX
    r"(?:[0-9]"                    # 2a: single-letter area  + digit
    r"(?:[0-9]|[A-HJKPSTUW])?"     # 3: optional second digit OR specific letter
    r"|[A-HK-Y][0-9]"              # 2b: two-letter area + digit
    r"(?:[0-9]|[ABEHMNPRV-Y])?)"   # 4: optional second digit OR specific letter
    r" "                           # mandatory single space between outward/inward
    r"[0-9][ABD-HJLNP-UW-Z]{2})$",  # inward: digit + two letters from allowed set
    flags=re.IGNORECASE,
)

# Hard input cap — any valid postcode is at most 8 characters including the space.
# Refusing longer input stops an attacker feeding the engine pathological strings.
MAX_POSTCODE_LEN = 8


def is_valid_postcode(candidate: str) -> bool:
    """Return True if valid UK postcode."""
    if not isinstance(candidate, str):
        return False
    if len(candidate) > MAX_POSTCODE_LEN:
        return False
    return UK_POSTCODE_PATTERN.match(candidate.strip()) is not None


def _run_tests():
    """Self-test against the examples in the assignment brief."""
    should_pass = [
        "M1 1AA",
        "M60 1NW",
        "CR2 6XH",
        "DN55 1PT",
        "W1A 1HQ",
        "EC1A 1BB",
        "GIR 0AA",  # the Girobank special-case
    ]
    should_fail = [
        "ST7 9HV",          # V not allowed as a trailing inward letter
        "QA1 1AA",          # first letter Q not allowed
        "M1  1AA",          # double space
        "M1-1AA",           # wrong separator
        "m1 1aa extra",     # trailing junk
        "",                 # empty
        "AAAAAAAAA",        # shape wrong / too long
    ]

    print("Expected PASS:")
    for pc in should_pass:
        ok = is_valid_postcode(pc)
        print(f"  {pc!r:15}  -> {'PASS' if ok else 'FAIL'}")

    print("\nExpected FAIL:")
    for pc in should_fail:
        ok = is_valid_postcode(pc)
        print(f"  {pc!r:15}  -> {'PASS' if ok else 'FAIL'}")


if __name__ == "__main__":
    _run_tests()
    print("\nEnter a postcode to validate (blank line to quit).")
    while True:
        try:
            user_input = input("> ")
        except EOFError:
            break
        if not user_input:
            break
        print("Valid" if is_valid_postcode(user_input) else "Not valid")


# ---------------------------------------------------------------------------
# ReDoS / evil-regex notes
# ---------------------------------------------------------------------------
# An "evil regex" is one that allows catastrophic backtracking on crafted input,
# e.g. /^(a+)+$/ against "aaaaaaaaaaaaaaaaaaaaaaaaaaX".  Guard-rails used here:
#
#   1. No nested or overlapping quantifiers.  Every repetition is either
#      fixed-length ({2}) or optional (?), so the engine cannot explore
#      exponentially many match paths.
#   2. The pattern is fully anchored (^ ... $).  The engine cannot slide it
#      over the input to find alternative starting positions.
#   3. Character classes are disjoint within each alternative, so the
#      engine does not need to back-track between them.
#   4. Input length is capped (MAX_POSTCODE_LEN) before the regex runs,
#      which puts a hard upper bound on work regardless of the pattern.
#   5. The regex is compiled once at import time; re-compiling in a loop
#      would be an easy DoS vector.
#   6. Python's default `re` engine uses backtracking, but with the above
#      precautions worst-case behaviour is linear.  For hostile environments
#      (public-facing APIs) the `re2` library, which guarantees linear-time
#      matching, would be a stronger control.
