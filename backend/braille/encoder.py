"""
BrailleScript – Spanish Braille Encoder

Implements the complete Spanish Braille encoding system based on the
Símbolo Generador (6-dot cell) standard.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Braille Map – lowercase letters, accented vowels, special chars
# ---------------------------------------------------------------------------

BRAILLE_MAP: dict[str, frozenset[int]] = {
    # Series 1 (a–j): top 4 dots only
    "a": frozenset({1}),
    "b": frozenset({1, 2}),
    "c": frozenset({1, 4}),
    "d": frozenset({1, 4, 5}),
    "e": frozenset({1, 5}),
    "f": frozenset({1, 2, 4}),
    "g": frozenset({1, 2, 4, 5}),
    "h": frozenset({1, 2, 5}),
    "i": frozenset({2, 4}),
    "j": frozenset({2, 4, 5}),

    # Series 2 (k–t): Series 1 + dot 3
    "k": frozenset({1, 3}),
    "l": frozenset({1, 2, 3}),
    "m": frozenset({1, 3, 4}),
    "n": frozenset({1, 3, 4, 5}),
    "o": frozenset({1, 3, 5}),
    "p": frozenset({1, 2, 3, 4}),
    "q": frozenset({1, 2, 3, 4, 5}),
    "r": frozenset({1, 2, 3, 5}),
    "s": frozenset({2, 3, 4}),
    "t": frozenset({2, 3, 4, 5}),

    # Series 3 (u–z): Series 1 + dots 3 and 6
    "u": frozenset({1, 3, 6}),
    "v": frozenset({1, 2, 3, 6}),
    "x": frozenset({1, 3, 4, 6}),
    "y": frozenset({1, 3, 4, 5, 6}),
    "z": frozenset({1, 3, 5, 6}),

    # w is not native to Spanish Braille
    "w": frozenset({2, 4, 5, 6}),

    # Special Spanish characters
    "á": frozenset({1, 2, 3, 5, 6}),
    "é": frozenset({2, 3, 4, 6}),
    "í": frozenset({3, 4}),
    "ó": frozenset({3, 4, 6}),
    "ú": frozenset({2, 3, 4, 5, 6}),
    "ñ": frozenset({1, 2, 4, 5, 6}),
    "ü": frozenset({1, 2, 5, 6}),

    # Punctuation & signs
    ".": frozenset({3}),
    ",": frozenset({2}),
    ";": frozenset({2, 3}),
    ":": frozenset({2, 5}),
    "!": frozenset({2, 3, 5}),
    "¡": frozenset({2, 3, 5}),
    "?": frozenset({2, 6}),
    "¿": frozenset({2, 6}),
    "-": frozenset({3, 6}),
    "(": frozenset({1, 2, 6}),
    ")": frozenset({3, 4, 5}),
    "\u201c": frozenset({2, 3, 6}),  # "
    "\u201d": frozenset({3, 5, 6}),  # "
    '"': frozenset({2, 3, 6}),       # straight quote → open
    "+": frozenset({2, 3, 5}),
    "×": frozenset({2, 3, 6}),
    "*": frozenset({2, 3, 6}),          # asterisk → multiply
    "=": frozenset({2, 3, 5, 6}),
    "÷": frozenset({2, 5, 6}),
}

# Prefix signs
UPPERCASE_SIGN = frozenset({4, 6})
NUMBER_SIGN = frozenset({3, 4, 5, 6})

# Digits map to the same patterns as a–j
DIGIT_MAP: dict[str, frozenset[int]] = {
    "1": BRAILLE_MAP["a"],
    "2": BRAILLE_MAP["b"],
    "3": BRAILLE_MAP["c"],
    "4": BRAILLE_MAP["d"],
    "5": BRAILLE_MAP["e"],
    "6": BRAILLE_MAP["f"],
    "7": BRAILLE_MAP["g"],
    "8": BRAILLE_MAP["h"],
    "9": BRAILLE_MAP["i"],
    "0": BRAILLE_MAP["j"],
}

# Decimal separators used inside number runs
DECIMAL_COMMA_DOTS = frozenset({2})
DECIMAL_POINT_DOTS = frozenset({3})


# ---------------------------------------------------------------------------
# Helper: dots → Unicode Braille codepoint  (U+2800 base)
# ---------------------------------------------------------------------------

def dots_to_unicode(dots: frozenset[int] | set[int] | list[int]) -> str:
    """Convert a set of dot numbers (1-6) to a Unicode Braille character."""
    # Braille dot-to-bit mapping:
    # dot 1 → bit 0, dot 2 → bit 1, dot 3 → bit 2,
    # dot 4 → bit 3, dot 5 → bit 4, dot 6 → bit 5
    offset = 0
    for d in dots:
        offset |= 1 << (d - 1)
    return chr(0x2800 + offset)


# ---------------------------------------------------------------------------
# Main encoding function
# ---------------------------------------------------------------------------

def _extract_words(text: str) -> list[tuple[str, bool]]:
    """
    Split text into segments of (content, is_word).
    A "word" is a run of alphabetic characters (including accented).
    Everything else is returned as non-word segments.
    """
    segments: list[tuple[str, bool]] = []
    buf = ""
    for ch in text:
        is_alpha = ch.isalpha()
        if is_alpha:
            buf += ch
        else:
            if buf:
                segments.append((buf, True))
                buf = ""
            segments.append((ch, False))
    if buf:
        segments.append((buf, True))
    return segments


def _is_all_upper(word: str) -> bool:
    """Check if a word is entirely uppercase (at least 2 letters)."""
    return len(word) >= 2 and all(c.isupper() for c in word if c.isalpha())


def encode_text(text: str) -> list[dict]:
    """
    Encode a Spanish text string into a list of Braille cell descriptors.

    Each cell dict has:
        - char: the original character (or prefix label)
        - dots: sorted list of raised dot numbers
        - type: "letter" | "digit" | "special" | "sign" | "space" | "prefix"
    """
    cells: list[dict] = []
    in_number = False  # track whether we're inside a digit run

    segments = _extract_words(text)

    for segment, is_word in segments:
        if is_word:
            # --- Word segment ---
            in_number = False
            all_upper = _is_all_upper(segment)

            if all_upper:
                # Two capital indicators at the start for all-caps words
                for _ in range(2):
                    cells.append({
                        "char": "⠠",
                        "dots": sorted(UPPERCASE_SIGN),
                        "type": "prefix",
                    })

            for ch in segment:
                lower = ch.lower()
                if lower in BRAILLE_MAP:
                    # Single capital letter (not all-caps word)
                    if ch.isupper() and not all_upper:
                        cells.append({
                            "char": "⠠",
                            "dots": sorted(UPPERCASE_SIGN),
                            "type": "prefix",
                        })
                    cells.append({
                        "char": ch,
                        "dots": sorted(BRAILLE_MAP[lower]),
                        "type": "letter",
                    })
        else:
            # --- Non-word characters (digits, punctuation, spaces, etc.) ---
            for ch in segment:

                # --- Space ---
                if ch == " ":
                    cells.append({"char": " ", "dots": [], "type": "space"})
                    in_number = False
                    continue

                # --- Newline → treat as space ---
                if ch in ("\n", "\r"):
                    cells.append({"char": " ", "dots": [], "type": "space"})
                    in_number = False
                    continue

                # --- Digits ---
                if ch.isdigit():
                    if not in_number:
                        # Insert number sign prefix at start of digit run
                        cells.append({
                            "char": "#",
                            "dots": sorted(NUMBER_SIGN),
                            "type": "prefix",
                        })
                        in_number = True
                    cells.append({
                        "char": ch,
                        "dots": sorted(DIGIT_MAP[ch]),
                        "type": "digit",
                    })
                    continue

                # --- Decimal comma / point inside number ---
                # After the separator, set in_number = False so that
                # the number indicator is re-emitted for the next digit group.
                if in_number and ch == ",":
                    cells.append({
                        "char": ch,
                        "dots": sorted(DECIMAL_COMMA_DOTS),
                        "type": "sign",
                    })
                    in_number = False  # force re-emission of number indicator
                    continue
                if in_number and ch == ".":
                    cells.append({
                        "char": ch,
                        "dots": sorted(DECIMAL_POINT_DOTS),
                        "type": "sign",
                    })
                    in_number = False  # force re-emission of number indicator
                    continue

                # If we reach here, we're no longer in a number run
                in_number = False

                # --- Punctuation / special ---
                if ch in BRAILLE_MAP:
                    cells.append({
                        "char": ch,
                        "dots": sorted(BRAILLE_MAP[ch]),
                        "type": "sign",
                    })
                    continue

                # --- Unknown character → skip silently ---

    return cells


def cells_to_unicode(cells: list[dict]) -> str:
    """Convert a list of cell dicts into a single Unicode Braille string."""
    parts: list[str] = []
    for cell in cells:
        if cell["type"] == "space":
            parts.append(" ")
        else:
            parts.append(dots_to_unicode(cell["dots"]))
    return "".join(parts)
