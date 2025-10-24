#!/usr/bin/python3

"""
###### PassForge ######
  Intelligence-Driven Password List Generator
  https://github.com/fxrhan/passforge

[Author]
    fxrhan
        - github.com/fxrhan

[License]
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.
"""


# ----- Import libraries -----

import argparse
import os
import itertools
import sys

# ----- ANSI Color Codes -----

class Colors:
    """ANSI color codes for terminal output"""
    # Text colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Reset
    RESET = '\033[0m'
    
    # Combined styles
    HEADER = '\033[95m\033[1m'  # Magenta + Bold
    SUCCESS = '\033[92m\033[1m'  # Green + Bold
    WARNING = '\033[93m\033[1m'  # Yellow + Bold
    ERROR = '\033[91m\033[1m'    # Red + Bold
    INFO = '\033[96m\033[1m'     # Cyan + Bold

# ----- Global variables -----

symbols = [".", "-", "_", "?", "!", "@", "#", "+", "*", "%", "&", "$"]

common_pwds = [
    "password",
    "admin",
    "123456",
    "1234567890",
    "qwerty",
    "qwertyuiop",
    "webadmin",
    "1q2w3e4r5t",
    "qwerty123",
    "11111111",
]
leet_chars = {letter: str(index) for index, letter in enumerate("oizeasgtb")}
"""
leet_chars:
{   'a': '4','b': '8','e': '3','g': '6',
    'i': '1','o': '0','s': '5','t': '7',
    'z': '2',}
"""
directory = "output"
starting_year = 1985
ending_year = 1999
starting_number = 1
ending_number = 20
words_in_passphrase_max = 2  # HIGHLY recommended: _don't_ edit this
min_pwd_length = 0

# Length constants for password generation
SYMBOL_LENGTH = 1
YEAR_LENGTH = 4
MAX_NUMBER_LENGTH = 2  # Max digits in numbers (1-20)

# Advanced password generation patterns
COMMON_SUFFIXES = ["123", "!", "@", "#", "1", "12", "123!", "!@#", "2024", "2025", "321"]
COMMON_PREFIXES = ["!", "@", "my", "the", "i", "love"]
KEYBOARD_PATTERNS = [
    "qwerty", "qwertyuiop", "asdf", "asdfgh", "zxcv", "zxcvbn",
    "qwerty123", "1qaz2wsx", "1q2w3e4r", "!qaz@wsx", "1234qwer"
]
MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
MONTHS_SHORT = ["jan", "feb", "mar", "apr", "may", "jun",
                "jul", "aug", "sep", "oct", "nov", "dec"]
SEASONS = ["spring", "summer", "autumn", "fall", "winter"]
ADVANCED_SUBSTITUTIONS = {
    'a': ['@', '4'],
    'e': ['3'],
    's': ['$', '5'],
    'o': ['0'],
    'i': ['!', '1'],
    't': ['7'],
    'l': ['1'],
}

# Phonetic replacements for common sound-alike patterns
PHONETIC_REPLACEMENTS = {
    'ph': 'f',      # phone -> fone
    'ck': 'k',      # nick -> nik
    'c': 'k',       # cool -> kool (when at start or before certain letters)
    'qu': 'kw',     # queen -> kween
    'x': 'ks',      # alex -> aleks
    'z': 's',       # buzz -> buss
    'oo': 'u',      # cool -> cul
    'ee': 'e',      # meet -> met
    'ght': 't',     # night -> nite
    'tion': 'shun', # action -> akshun
}

# Common password patterns from real-world analysis
COMMON_PASSWORD_PATTERNS = [
    # Year patterns
    lambda w, y: f"{w}{y}" if y else None,
    lambda w, y: f"{w.capitalize()}{y}" if y else None,
    lambda w, y: f"{w}{str(y)[-2:]}" if y else None,
    
    # Number patterns
    lambda w, _: f"{w}1",
    lambda w, _: f"{w}123",
    lambda w, _: f"{w}1234",
    lambda w, _: f"{w}12345",
    lambda w, _: f"{w}01",
    lambda w, _: f"{w}00",
    lambda w, _: f"1{w}",
    
    # Symbol patterns (most common positions)
    lambda w, _: f"{w}!",
    lambda w, _: f"{w}@",
    lambda w, _: f"{w}#",
    lambda w, _: f"{w}$",
    lambda w, _: f"{w}.",
    lambda w, _: f"{w}_",
    lambda w, _: f"{w}!1",
    lambda w, _: f"{w}@1",
    lambda w, _: f"{w}#1",
    
    # Capitalization + symbol/number
    lambda w, _: f"{w.capitalize()}!",
    lambda w, _: f"{w.capitalize()}@",
    lambda w, _: f"{w.capitalize()}1",
    lambda w, _: f"{w.capitalize()}123",
    
    # Double patterns
    lambda w, _: f"{w}{w}",
    lambda w, _: f"{w}{w}1",
    lambda w, _: f"{w}{w}!",
]


# ----- Initial swag -----


def banner():
    print("")
    print(f"{Colors.CYAN}{Colors.BOLD}  ____               _____                    ")
    print(r" |  _ \ __ _ ___ ___|  ___|__  _ __ __ _  ___ ")
    print(r" | |_) / _` / __/ __| |_ / _ \| '__/ _` |/ _ \\")
    print(r" |  __/ (_| \__ \__ \  _| (_) | | | (_| |  __/")
    print(r" |_|   \__,_|___/___/_|  \___/|_|  \__, |\___|")
    print(f"                                   |___/      {Colors.RESET}")
    print("")
    print(f" {Colors.BLUE}+{Colors.RESET} {Colors.UNDERLINE}github.com/fxrhan/passforge{Colors.RESET}")
    print(f" {Colors.BLUE}+{Colors.RESET} {Colors.YELLOW}fxrhan{Colors.RESET}")
    print(f" {Colors.BLUE}+{Colors.RESET} {Colors.GREEN}GPLv3 License{Colors.RESET}")
    print(f" {Colors.BLUE}+{Colors.RESET} {Colors.MAGENTA}Intelligence-Driven Password List Generator{Colors.RESET}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.RESET}")


def version():
    print(f"{Colors.SUCCESS}PassForge v1.0{Colors.RESET}\n")


# ----- Input -----


def get_parser():
    """Create and return a parser (argparse.ArgumentParser instance) for main()
    to use"""
    parser = argparse.ArgumentParser(
        description="PassForge - Intelligence-Driven Password List Generator"
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-p", "--person", action="store_true", help="Set the target to be a person"
    )
    group.add_argument(
        "-c",
        "--company",
        action="store_true",
        help="Set the target to be a company",
    )
    group.add_argument(
        "-v", "--version", action="store_true", help="Show the version of this program"
    )

    group_two = parser.add_mutually_exclusive_group(required=False)
    group_two.add_argument(
        "-l",
        "--leet",
        action="store_true",
        help="Add also complete 1337(leet) passwords",
    )
    group_two.add_argument(
        "-L",
        "--leetall",
        action="store_true",
        help="Add also ALL possible le37(leet) passwords",
    )
    group_three = parser.add_mutually_exclusive_group(required=False)
    group_three.add_argument(
        "-y",
        "--years",
        action="store_true",
        help="Add also years at password. See years range inside passforge.py",
    )
    group_four = parser.add_mutually_exclusive_group(required=False)
    group_four.add_argument(
        "-n",
        "--numbers",
        action="store_true",
        help="Add also numbers at password. See numbers range inside passforge.py",
    )
    group_five = parser.add_mutually_exclusive_group(required=False)
    group_five.add_argument(
        "-m",
        "--minlength",
        type=str,
        help="Set the minimum length for passwords (default 0).",
    )

    return parser


# ----- Utils -----


def create_output_folder():
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_output_file(input_filename):

    create_output_folder()
    filename = os.path.join(directory, input_filename)

    if os.path.exists(filename):
        choice = input(
            f"{Colors.WARNING}[!] {input_filename} already exists. Do you want to overwrite? (y/n):{Colors.RESET} "
        )
        if str(choice).lower() != "y":
            print(f"{Colors.ERROR}✗ Operation cancelled.{Colors.RESET}")
            sys.exit(1)
        # if choice == y: ====> go forward. The file's content will be flushed and overwritten
    else:
        open(filename, 'a').close()


def prepare_keywords(str_input):
    """
    It outputs None if blank
    It outputs an array if valid
    """
    if not str_input or len(str_input) == 0:
        return None
    temp = str_input.split(",")
    result = []
    for elem in temp:
        if elem.strip() != "":
            result.append(elem.strip())
    return result


def create_permutations_with_repetition(list_input, k):
    """
    It returns all the permutations with repetitions (with k elements) of list_input
    """
    unique_words = set(list_input)
    subsets = [p for p in itertools.product(unique_words, repeat=k)]

    return subsets


def flush_None_values(list_input):
    return [elem for elem in list_input if elem is not None and elem != ""]


def has_case_variations(text):
    """Check if text has letters that can be capitalized differently."""
    return text.lower() != text.capitalize()


def write_with_case_variations(file_handle, text, suffix=""):
    """
    Write text with case variations (lower, upper, capitalize) if applicable.
    
    Args:
        file_handle: Open file handle to write to
        text: Base text to write
        suffix: Optional suffix to append (e.g., symbol, number, year)
    """
    if has_case_variations(text):
        file_handle.write(f"{text.lower()}{suffix}\n")
        file_handle.write(f"{text.upper()}{suffix}\n")
        file_handle.write(f"{text.capitalize()}{suffix}\n")
    else:
        file_handle.write(f"{text}{suffix}\n")


def attr_keywords_in_unique_list(target):

    attributes = vars(target)
    attributes = flush_None_values(attributes.values())

    keywords = []
    for elem in attributes:
        if isinstance(elem, list):
            keywords.extend(elem)

    attributes = [elem for elem in attributes if not isinstance(elem, list)]

    attributes.extend(keywords)
    #  now attributes == all attributes + keywords

    result = list(set(attributes))

    return result


# ----- Advanced Password Generation Functions -----


def add_reverse_words(attributes):
    """Add reversed versions of words."""
    reversed_words = []
    for word in attributes:
        if len(word) > 3:  # Only reverse meaningful words
            reversed_words.append(word[::-1])
    return reversed_words


def add_common_patterns(word):
    """Add realistic password patterns with common suffixes/prefixes."""
    patterns = []
    
    # Common suffixes
    for suffix in COMMON_SUFFIXES:
        patterns.append(f"{word}{suffix}")
        if has_case_variations(word):
            patterns.append(f"{word.capitalize()}{suffix}")
    
    # Common prefixes
    for prefix in COMMON_PREFIXES:
        patterns.append(f"{prefix}{word}")
        if has_case_variations(word):
            patterns.append(f"{prefix}{word.capitalize()}")
    
    return patterns


def add_special_multipliers(word):
    """Add common special character patterns at end."""
    patterns = [
        f"{word}!",
        f"{word}!!",
        f"{word}!!!",
        f"{word}@",
        f"{word}#",
        f"{word}*",
        f"{word}!@",
        f"{word}!@#",
        f"{word}@#$",
    ]
    return patterns


def advanced_capitalization(word):
    """Generate realistic capitalization patterns."""
    if len(word) < 2:
        return [word]
    
    variations = [
        word.lower(),
        word.upper(),
        word.capitalize(),
    ]
    
    # Additional patterns for longer words
    if len(word) > 3:
        # First and last letter capitalized
        variations.append(word[0].upper() + word[1:-1].lower() + word[-1].upper())
        # Alternating case (first half lower, second half upper)
        mid = len(word) // 2
        variations.append(word[:mid].lower() + word[mid:].upper())
    
    return list(set(variations))


def generate_date_variations(day, month, year):
    """Generate common date formats used in passwords."""
    formats = []
    
    # Ensure inputs are strings
    day = str(day) if day else ""
    month = str(month) if month else ""
    year = str(year) if year else ""
    
    # Pad day and month with zeros if needed
    if day and len(day) == 1:
        day = f"0{day}"
    if month and len(month) == 1:
        month = f"0{month}"
    
    if day and month and year:
        # Full dates
        formats.extend([
            f"{day}{month}{year}",           # 15031990
            f"{day}{month}{year[-2:]}",      # 150390
            f"{month}{day}{year[-2:]}",      # 031590 (US format)
            f"{day}-{month}-{year}",         # 15-03-1990
            f"{day}/{month}/{year}",         # 15/03/1990
            f"{month}-{day}-{year}",         # 03-15-1990 (US)
            f"{year}{month}{day}",           # 19900315 (ISO)
            f"{day}{month}",                 # 1503
        ])
    
    if month and year:
        # Month/Year only
        formats.extend([
            f"{month}{year}",                # 031990
            f"{month}{year[-2:]}",           # 0390
        ])
    
    return formats


def generate_temporal_passwords(name, birth_year=None):
    """Generate season/month combinations."""
    passwords = []
    
    if not name:
        return passwords
    
    # Month combinations
    for month in MONTHS_SHORT:
        passwords.append(f"{name}{month}")
        passwords.append(f"{month}{name}")
        if has_case_variations(name):
            passwords.append(f"{name.capitalize()}{month}")
    
    # Season combinations
    for season in SEASONS:
        passwords.append(f"{name}{season}")
        passwords.append(f"{season}{name}")
        if has_case_variations(name):
            passwords.append(f"{name.capitalize()}{season}")
    
    # Add year if provided
    if birth_year:
        year_str = str(birth_year)
        for month in MONTHS_SHORT:
            passwords.append(f"{month}{year_str}")
            passwords.append(f"{month}{year_str[-2:]}")
        for season in SEASONS:
            passwords.append(f"{season}{year_str}")
            passwords.append(f"{season}{year_str[-2:]}")
    
    return passwords


def advanced_substitutions(word):
    """Generate advanced character substitutions."""
    if not word or len(word) < 3:
        return []
    
    variations = []
    word_lower = word.lower()
    
    # Single character substitutions
    for char, replacements in ADVANCED_SUBSTITUTIONS.items():
        if char in word_lower:
            for replacement in replacements:
                variations.append(word_lower.replace(char, replacement))
                # Also try capitalized version
                if has_case_variations(word):
                    variations.append(word_lower.replace(char, replacement).capitalize())
    
    # Multiple substitutions (common patterns)
    # a->@, e->3, o->0
    multi_sub = word_lower
    if 'a' in multi_sub:
        multi_sub = multi_sub.replace('a', '@')
    if 'e' in multi_sub:
        multi_sub = multi_sub.replace('e', '3')
    if 'o' in multi_sub:
        multi_sub = multi_sub.replace('o', '0')
    if multi_sub != word_lower:
        variations.append(multi_sub)
        if has_case_variations(word):
            variations.append(multi_sub.capitalize())
    
    return list(set(variations))


def phonetic_variations(word):
    """
    Generate phonetic spelling variations.
    Based on common sound-alike replacements people use in passwords.
    """
    if not word or len(word) < 3:
        return []
    
    variations = []
    word_lower = word.lower()
    
    # Apply phonetic replacements
    for old_pattern, new_pattern in PHONETIC_REPLACEMENTS.items():
        if old_pattern in word_lower:
            # Replace the pattern
            phonetic = word_lower.replace(old_pattern, new_pattern)
            if phonetic != word_lower:
                variations.append(phonetic)
                # Also add capitalized version
                if has_case_variations(word):
                    variations.append(phonetic.capitalize())
    
    # Special case: 'c' to 'k' only at start or before vowels
    if word_lower.startswith('c'):
        k_version = 'k' + word_lower[1:]
        variations.append(k_version)
        if has_case_variations(word):
            variations.append(k_version.capitalize())
    
    return list(set(variations))


def word_mutations(word):
    """
    Generate word mutations including plurals, repetitions, and truncations.
    """
    if not word or len(word) < 3:
        return []
    
    mutations = []
    
    # Plural forms
    if not word.endswith('s'):
        mutations.append(f"{word}s")
        if word.endswith('y') and len(word) > 3:
            # baby -> babies
            mutations.append(f"{word[:-1]}ies")
    
    # Remove last letter (common typo/variation)
    if len(word) > 4:
        mutations.append(word[:-1])
    
    # Repeat last letter
    mutations.append(f"{word}{word[-1]}")
    
    # Repeat last two letters
    if len(word) > 2:
        mutations.append(f"{word}{word[-2:]}")
    
    # Double the word
    mutations.append(f"{word}{word}")
    
    # Truncate to first 4 characters (common for long words)
    if len(word) > 6:
        mutations.append(word[:4])
        mutations.append(word[:5])
    
    # Remove vowels (txt speak)
    vowels = 'aeiou'
    no_vowels = ''.join([c for c in word if c.lower() not in vowels])
    if no_vowels and len(no_vowels) >= 2:
        mutations.append(no_vowels)
    
    return list(set(mutations))


def ml_pattern_analysis(word, birth_year=None):
    """
    Apply ML-inspired pattern analysis based on real-world password databases.
    Uses patterns observed in leaked password datasets (RockYou, LinkedIn, etc.)
    """
    if not word:
        return []
    
    patterns = []
    
    # Apply each pattern function
    for pattern_func in COMMON_PASSWORD_PATTERNS:
        try:
            result = pattern_func(word, birth_year)
            if result and len(result) >= min_pwd_length:
                patterns.append(result)
        except:
            continue
    
    # Additional ML-observed patterns
    word_lower = word.lower()
    
    # Common transformations from password analysis
    # 1. First letter upper + numbers at end (most common pattern)
    patterns.extend([
        f"{word.capitalize()}1!",
        f"{word.capitalize()}2024",
        f"{word.capitalize()}2025",
        f"{word.capitalize()}@123",
    ])
    
    # 2. All caps + exclamation (aggressive passwords)
    patterns.append(f"{word.upper()}!")
    patterns.append(f"{word.upper()}!!")
    
    # 3. Sandwich patterns (symbol-word-symbol)
    patterns.extend([
        f"!{word}!",
        f"@{word}@",
        f"#{word}#",
        f"*{word}*",
    ])
    
    # 4. Year in middle (less common but exists)
    if birth_year:
        patterns.append(f"{word[:len(word)//2]}{birth_year}{word[len(word)//2:]}")
    
    # 5. Alternating case (less common but seen in analysis)
    if len(word) > 3:
        alternating = ''.join([c.upper() if i % 2 == 0 else c.lower() 
                              for i, c in enumerate(word)])
        patterns.append(alternating)
        patterns.append(f"{alternating}1")
    
    # 6. Reverse with number (creative users)
    patterns.append(f"{word[::-1]}1")
    patterns.append(f"{word[::-1]}!")
    
    # 7. Keyboard adjacent characters (typo-based)
    # Common typos: a->s, e->r, i->o, etc.
    typo_map = {'a': 's', 'e': 'r', 'i': 'o', 's': 'a', 'o': 'i'}
    for old_char, new_char in typo_map.items():
        if old_char in word_lower:
            typo_version = word_lower.replace(old_char, new_char, 1)  # Replace first occurrence
            if typo_version != word_lower:
                patterns.append(typo_version)
    
    return list(set([p for p in patterns if p and len(p) >= min_pwd_length]))


def trivial_pwds(attributes, years, numbers, output_file):
    """
    Write trivial passwords to output file.
    Generates passwords from attributes with optional symbols, numbers, and years.
    """
    with open(output_file, "w") as f:
        for elem in attributes:
            if len(elem) >= min_pwd_length:
                f.write(f"{elem}\n")

            for symbol in symbols:
                # Symbol and attribute
                if len(elem) + SYMBOL_LENGTH >= min_pwd_length:
                    write_with_case_variations(f, elem, symbol)

                # Symbol, attribute and number
                if numbers and len(elem) + SYMBOL_LENGTH + MAX_NUMBER_LENGTH >= min_pwd_length:
                    for number in range(starting_number, ending_number + 1):
                        write_with_case_variations(f, elem, f"{symbol}{number}")

                # Symbol, attribute and year
                if years and len(elem) + SYMBOL_LENGTH + YEAR_LENGTH >= min_pwd_length:
                    for year in range(starting_year, ending_year + 1):
                        write_with_case_variations(f, elem, f"{symbol}{year}")


def permutations_first_round(attributes, years, numbers, output_file):
    """
    Write first round of word combinations.
    - word1 + word2
    - word1 + word2 + number
    - word1 + word2 + year
    """
    subsets = create_permutations_with_repetition(attributes, words_in_passphrase_max)

    with open(output_file, "a") as f:
        for subset in subsets:
            # ATTENTION - THIS WORKS WITH words_in_passphrase_max = 2 ONLY !
            word1, word2 = subset

            # word1 + word2
            if len(word1) + len(word2) >= min_pwd_length:
                write_with_case_variations(f, word1, word2)

            # word1 + word2 + number
            if numbers and len(word1) + len(word2) + MAX_NUMBER_LENGTH >= min_pwd_length:
                for number in range(starting_number, ending_number + 1):
                    write_with_case_variations(f, word1, f"{word2}{number}")

            # word1 + word2 + year
            if years and len(word1) + len(word2) + YEAR_LENGTH >= min_pwd_length:
                for year in range(starting_year, ending_year + 1):
                    write_with_case_variations(f, word1, f"{word2}{year}")

    return subsets


def permutations_second_round(subsets, years, numbers, output_file):
    """
    Write second round of word combinations with symbols.
    - word1 + symbol + word2
    - word1 + symbol + word2 + number
    - word1 + word2 + symbol + number
    - word1 + symbol + word2 + year
    - word1 + word2 + symbol + year
    """
    with open(output_file, "a") as f:
        for subset in subsets:
            # ATTENTION - THIS WORKS WITH words_in_passphrase_max = 2 ONLY !
            word1, word2 = subset

            for symbol in symbols:
                # word1 + symbol + word2
                if len(word1) + len(word2) + SYMBOL_LENGTH >= min_pwd_length:
                    write_with_case_variations(f, word1, f"{symbol}{word2}")

                # word1 + symbol + word2 + number (two positions)
                if numbers and len(word1) + len(word2) + SYMBOL_LENGTH + MAX_NUMBER_LENGTH >= min_pwd_length:
                    for number in range(starting_number, ending_number + 1):
                        write_with_case_variations(f, word1, f"{symbol}{word2}{number}")
                        write_with_case_variations(f, word1, f"{word2}{symbol}{number}")

                # word1 + symbol + word2 + year (two positions)
                if years and len(word1) + len(word2) + SYMBOL_LENGTH + YEAR_LENGTH >= min_pwd_length:
                    for year in range(starting_year, ending_year + 1):
                        write_with_case_variations(f, word1, f"{symbol}{word2}{year}")
                        write_with_case_variations(f, word1, f"{word2}{symbol}{year}")


def permutations_third_round(subsets, years, numbers, output_file):
    """
    Write third round of word combinations with two symbols.
    - word1 + symbol + word2 + symbol2 + number
    - word1 + symbol + word2 + symbol2 + year
    """
    with open(output_file, "a") as f:
        for subset in subsets:
            # ATTENTION - THIS WORKS WITH words_in_passphrase_max = 2 ONLY !
            word1, word2 = subset

            for symbol in symbols:
                for symbol2 in symbols:
                    # word1 + symbol + word2 + symbol2 + number
                    if numbers and len(word1) + len(word2) + (2 * SYMBOL_LENGTH) + MAX_NUMBER_LENGTH >= min_pwd_length:
                        for number in range(starting_number, starting_number + 1):
                            write_with_case_variations(f, word1, f"{symbol}{word2}{symbol2}{number}")

                    # word1 + symbol + word2 + symbol2 + year
                    if years and len(word1) + len(word2) + (2 * SYMBOL_LENGTH) + YEAR_LENGTH >= min_pwd_length:
                        for year in range(starting_year, ending_year + 1):
                            write_with_case_variations(f, word1, f"{symbol}{word2}{symbol2}{year}")


def common_passwords(attributes, years, numbers, output_file):
    """
    Write common passwords to output file.
    Includes standard passwords like 'password', 'admin', '123456', etc.
    """
    with open(output_file, "a") as f:
        for elem in common_pwds:
            if len(elem) >= min_pwd_length:
                f.write(f"{elem}\n")


def advanced_patterns_passwords(attributes, target, output_file):
    """
    Write advanced password patterns to output file.
    Includes: reverse words, common patterns, special multipliers, 
    advanced capitalization, date variations, temporal passwords, 
    advanced substitutions, and keyboard patterns.
    """
    with open(output_file, "a") as f:
        # 1. Reverse words
        reversed_words = add_reverse_words(attributes)
        for word in reversed_words:
            if len(word) >= min_pwd_length:
                f.write(f"{word}\n")
        
        # 2. Common patterns (suffixes/prefixes)
        for word in attributes:
            patterns = add_common_patterns(word)
            for pattern in patterns:
                if len(pattern) >= min_pwd_length:
                    f.write(f"{pattern}\n")
        
        # 3. Special multipliers
        for word in attributes:
            multipliers = add_special_multipliers(word)
            for mult in multipliers:
                if len(mult) >= min_pwd_length:
                    f.write(f"{mult}\n")
        
        # 4. Advanced capitalization
        for word in attributes:
            if len(word) > 3:
                caps = advanced_capitalization(word)
                for cap in caps:
                    if len(cap) >= min_pwd_length:
                        f.write(f"{cap}\n")
        
        # 5. Date variations
        if hasattr(target, 'birth_day') and hasattr(target, 'birth_month') and hasattr(target, 'birth_year'):
            date_formats = generate_date_variations(
                target.birth_day, 
                target.birth_month, 
                target.birth_year
            )
            for date_fmt in date_formats:
                if len(date_fmt) >= min_pwd_length:
                    f.write(f"{date_fmt}\n")
                    
                    # Combine dates with names
                    if hasattr(target, 'name') and target.name:
                        f.write(f"{target.name}{date_fmt}\n")
                        f.write(f"{date_fmt}{target.name}\n")
                        if hasattr(target, 'surname') and target.surname:
                            f.write(f"{target.surname}{date_fmt}\n")
                            f.write(f"{date_fmt}{target.surname}\n")
        
        # 6. Temporal passwords (seasons/months)
        if hasattr(target, 'name') and target.name:
            birth_year = target.birth_year if hasattr(target, 'birth_year') else None
            temporal = generate_temporal_passwords(target.name, birth_year)
            for temp in temporal:
                if len(temp) >= min_pwd_length:
                    f.write(f"{temp}\n")
            
            # Also for surname
            if hasattr(target, 'surname') and target.surname:
                temporal_surname = generate_temporal_passwords(target.surname, birth_year)
                for temp in temporal_surname:
                    if len(temp) >= min_pwd_length:
                        f.write(f"{temp}\n")
        
        # 7. Advanced substitutions
        for word in attributes:
            subs = advanced_substitutions(word)
            for sub in subs:
                if len(sub) >= min_pwd_length:
                    f.write(f"{sub}\n")
        
        # 8. Keyboard patterns
        for pattern in KEYBOARD_PATTERNS:
            if len(pattern) >= min_pwd_length:
                f.write(f"{pattern}\n")


def ultra_advanced_passwords(attributes, target, output_file):
    """
    Write ultra-advanced password patterns to output file.
    Includes: phonetic variations, word mutations, and ML-based pattern analysis.
    """
    with open(output_file, "a") as f:
        birth_year = target.birth_year if hasattr(target, 'birth_year') else None
        
        # 1. Phonetic variations
        for word in attributes:
            phonetics = phonetic_variations(word)
            for phonetic in phonetics:
                if len(phonetic) >= min_pwd_length:
                    f.write(f"{phonetic}\n")
                    # Also add with common suffixes
                    f.write(f"{phonetic}123\n")
                    f.write(f"{phonetic}!\n")
                    if birth_year:
                        f.write(f"{phonetic}{birth_year}\n")
        
        # 2. Word mutations
        for word in attributes:
            mutations = word_mutations(word)
            for mutation in mutations:
                if len(mutation) >= min_pwd_length:
                    f.write(f"{mutation}\n")
                    # Add with common patterns
                    f.write(f"{mutation}1\n")
                    f.write(f"{mutation}!\n")
                    if has_case_variations(mutation):
                        f.write(f"{mutation.capitalize()}\n")
                        f.write(f"{mutation.capitalize()}1\n")
        
        # 3. ML-based pattern analysis
        for word in attributes:
            ml_patterns = ml_pattern_analysis(word, birth_year)
            for pattern in ml_patterns:
                if len(pattern) >= min_pwd_length:
                    f.write(f"{pattern}\n")
        
        # 4. Combined advanced patterns
        # Phonetic + mutations
        for word in attributes:
            phonetics = phonetic_variations(word)
            for phonetic in phonetics:
                mutations = word_mutations(phonetic)
                for mutation in mutations:
                    if len(mutation) >= min_pwd_length:
                        f.write(f"{mutation}\n")
        
        # 5. ML patterns on phonetic variations
        for word in attributes:
            phonetics = phonetic_variations(word)
            for phonetic in phonetics:
                ml_patterns = ml_pattern_analysis(phonetic, birth_year)
                for pattern in ml_patterns:
                    if len(pattern) >= min_pwd_length:
                        f.write(f"{pattern}\n")


def leet_pwds(leetall, output_file):
    """
    Generate 1337 (leet) speak passwords.
    
    Args:
        leetall: If True, generate all possible leet combinations (e.g., leet -> l3e7)
                 If False, replace all leet chars (e.g., leet -> l337)
        output_file: Path to output file
    """
    # Read existing passwords
    with open(output_file, "r") as f:
        pwds = f.read().split()

    with open(output_file, "a") as f:
        for elem in pwds:
            # Check if password contains leet-able characters
            if not any(key in elem for key in leet_chars.keys()):
                continue

            if leetall:
                # Generate all possible leet combinations
                possibles = []
                for lower in elem.lower():
                    ll = leet_chars.get(lower, lower)
                    possibles.append((lower,) if ll == lower else (lower, ll))

                leets = ["".join(t) for t in itertools.product(*possibles)]
                for leet in leets:
                    f.write(f"{leet}\n")
            else:
                # Replace all leet chars
                leet = elem
                for char, replacement in leet_chars.items():
                    leet = leet.replace(char, replacement)
                f.write(f"{leet}\n")


# ----- Person -----


class Person:
    def __init__(
        self,
        name=None,
        middle_name=None,
        surname=None,
        nickname=None,
        username=None,
        age=None,
        birth_day=None,
        birth_month=None,
        birth_year=None,
        email=None,
        birth_place=None,
        first_pet=None,
        second_pet=None,
        favourite_band=None,
        person_keywords=None,
    ):

        self.name = name
        self.middle_name = middle_name
        self.surname = surname
        self.nickname = nickname
        self.username = username
        self.age = age
        self.birth_day = birth_day
        self.birth_month = birth_month
        self.birth_year = birth_year
        self.email = email
        self.birth_place = birth_place
        self.first_pet = first_pet
        self.second_pet = second_pet
        self.favourite_band = favourite_band
        self.person_keywords = person_keywords


def person(add_leet, years, leetall, numbers):
    print(f"{Colors.INFO}🎯 Targeting a person...{Colors.RESET}\n")
    target = input_person()
    default_output = False

    # output filename
    if target.name and target.name != "":
        create_output_file(target.name + "-" + target.surname + ".txt")

    else:
        create_output_file("passforge-output.txt")
        default_output = True

    if default_output:
        output_file = os.path.join("output", "passforge-output.txt")
    else:
        output_file = os.path.join("output", target.name + "-" + target.surname + ".txt")

    # real computation here

    attributes = attr_keywords_in_unique_list(target)

    print(f"\n{Colors.CYAN}[+]{Colors.RESET} Generating basic passwords...")
    trivial_pwds(attributes, years, numbers, output_file)

    print(f"{Colors.CYAN}[+]{Colors.RESET} Adding common passwords...")
    common_passwords(attributes, years, numbers, output_file)

    print(f"{Colors.CYAN}[+]{Colors.RESET} Generating word combinations...")
    subsets = permutations_first_round(attributes, years, numbers, output_file)

    permutations_second_round(subsets, years, numbers, output_file)

    permutations_third_round(subsets, years, numbers, output_file)

    print(f"{Colors.MAGENTA}[+]{Colors.RESET} Generating advanced patterns...")
    advanced_patterns_passwords(attributes, target, output_file)

    print(f"{Colors.YELLOW}[+]{Colors.RESET} Generating ultra-advanced patterns (phonetic, mutations, ML)...")
    ultra_advanced_passwords(attributes, target, output_file)

    if add_leet or leetall:
        print(f"{Colors.BLUE}[+]{Colors.RESET} Adding leet speak variations...")
        leet_pwds(leetall, output_file)
    
    print(f"\n{Colors.SUCCESS}✓ Password list generated:{Colors.RESET} {Colors.UNDERLINE}{output_file}{Colors.RESET}")
    print(f"{Colors.SUCCESS}✓ Total passwords:{Colors.RESET} {Colors.BOLD}{sum(1 for _ in open(output_file)):,}{Colors.RESET}")


def input_person():

    target = Person()

    print(f"{Colors.YELLOW}Enter all the information you know. Leave blank and hit enter if you don't know.{Colors.RESET}\n")
    
    target.name = input(f"{Colors.GREEN}[>]{Colors.RESET} Name: ")
    target.middle_name = input(f"{Colors.GREEN}[>]{Colors.RESET} Middle Name: ")
    target.surname = input(f"{Colors.GREEN}[>]{Colors.RESET} Surname: ")
    target.nickname = input(f"{Colors.GREEN}[>]{Colors.RESET} Nickname: ")
    target.username = input(f"{Colors.GREEN}[>]{Colors.RESET} Username: ")
    target.age = input(f"{Colors.GREEN}[>]{Colors.RESET} Age: ")
    target.birth_day = input(f"{Colors.GREEN}[>]{Colors.RESET} Birth day: ")
    target.birth_month = input(f"{Colors.GREEN}[>]{Colors.RESET} Birth month: ")
    target.birth_year = input(f"{Colors.GREEN}[>]{Colors.RESET} Birth year(YYYY): ")
    target.email = input(f"{Colors.GREEN}[>]{Colors.RESET} Email: ")
    target.birth_place = input(f"{Colors.GREEN}[>]{Colors.RESET} Birth place: ")
    target.first_pet = input(f"{Colors.GREEN}[>]{Colors.RESET} First pet: ")
    target.second_pet = input(f"{Colors.GREEN}[>]{Colors.RESET} Second pet: ")
    target.favourite_band = input(f"{Colors.GREEN}[>]{Colors.RESET} Favourite Band: ")

    person_keywords = input(f"{Colors.MAGENTA}[>]{Colors.RESET} Useful keywords (separated by comma): ")

    target.person_keywords = prepare_keywords(person_keywords)

    return target


# ----- Company -----


class Company:
    def __init__(
        self,
        name=None,
        web_domain=None,
        birth_year=None,
        company_keywords=None,
    ):

        self.name = name
        self.web_domain = web_domain
        self.birth_year = birth_year
        self.company_keywords = company_keywords


def company(add_leet, years, leetall, numbers):
    print(f"{Colors.INFO}🏢 Targeting a company...{Colors.RESET}\n")
    target = input_company()
    default_output = False

    # output filename
    if target.name and target.name != "":
        create_output_file(target.name + ".txt")
    else:
        create_output_file("passforge-output.txt")
        default_output = True

    if default_output:
        output_file = os.path.join("output", "passforge-output.txt")
    else:
        output_file = os.path.join("output", target.name + ".txt")

    # real computation here

    attributes = attr_keywords_in_unique_list(target)

    print(f"\n{Colors.CYAN}[+]{Colors.RESET} Generating basic passwords...")
    trivial_pwds(attributes, years, numbers, output_file)

    print(f"{Colors.CYAN}[+]{Colors.RESET} Adding common passwords...")
    common_passwords(attributes, years, numbers, output_file)

    print(f"{Colors.CYAN}[+]{Colors.RESET} Generating word combinations...")
    subsets = permutations_first_round(attributes, years, numbers, output_file)

    permutations_second_round(subsets, years, numbers, output_file)

    permutations_third_round(subsets, years, numbers, output_file)

    print(f"{Colors.MAGENTA}[+]{Colors.RESET} Generating advanced patterns...")
    advanced_patterns_passwords(attributes, target, output_file)

    print(f"{Colors.YELLOW}[+]{Colors.RESET} Generating ultra-advanced patterns (phonetic, mutations, ML)...")
    ultra_advanced_passwords(attributes, target, output_file)

    if add_leet or leetall:
        print(f"{Colors.BLUE}[+]{Colors.RESET} Adding leet speak variations...")
        leet_pwds(leetall, output_file)
    
    print(f"\n{Colors.SUCCESS}✓ Password list generated:{Colors.RESET} {Colors.UNDERLINE}{output_file}{Colors.RESET}")
    print(f"{Colors.SUCCESS}✓ Total passwords:{Colors.RESET} {Colors.BOLD}{sum(1 for _ in open(output_file)):,}{Colors.RESET}")


def input_company():

    target = Company()

    print(f"{Colors.YELLOW}Enter all the information you know. Leave blank and hit enter if you don't know.{Colors.RESET}\n")
    
    target.name = input(f"{Colors.GREEN}[>]{Colors.RESET} Name: ")
    target.web_domain = input(f"{Colors.GREEN}[>]{Colors.RESET} Web domain (without protocol): ")
    target.birth_year = input(f"{Colors.GREEN}[>]{Colors.RESET} Birth year (YYYY): ")

    company_keywords = input(f"{Colors.MAGENTA}[>]{Colors.RESET} Useful keywords (separated by comma): ")
    target.company_keywords = prepare_keywords(company_keywords)

    return target


# ----- Main function -----


def main():

    banner()

    parser = get_parser()
    args = parser.parse_args()

    if args.version:
        version()
    if args.minlength:
        global min_pwd_length
        try:
            min_pwd_length = int(args.minlength)
        except ValueError:
            print("-m requires an integer greater than 0.")
            sys.exit(1)
        if min_pwd_length <= 0:
            print("-m requires an integer greater than 0.")
            sys.exit(1)
    if args.company:
        company(args.leet, args.years, args.leetall, args.numbers)
    elif args.person:
        person(args.leet, args.years, args.leetall, args.numbers)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
