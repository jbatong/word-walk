import random

# Stanford GraphBase list of five-letter words
FILENAME_SGB = "sgb-words.txt"


def load_words(filename=FILENAME_SGB):
    with open(filename, "r") as f:
        words = f.read().splitlines()

    # Validate words
    word_length = len(words[0])
    if not all(len(word) == word_length for word in words):
        raise ValueError("Words in file must all be the same length.")
    return words


def compute_overlap(word: str, other_word: str) -> int:
    """Count the number of letters that appear in both words."""
    count = 0
    to_match = [letter for letter in other_word]
    for letter in word:
        if letter in to_match:
            to_match.remove(letter)
            count += 1
    return count


# --- CLI functions

def display_rules():
    rules_strs = [
        " ******** WORD WALK RULES **************************",
        " ***   You get two 5-letter words.               ***",
        " ***   Try to get from one word to the other.    ***",
        " ***   Each step, give a new word by replacing   ***",
        " ***   a single letter from the previous word.   ***",
        " ***   Letters may be rearanged.                 ***",
        " ***   The word must exist.                      ***",
        " ***                                Good luck!   ***",
        " ***************************************************",
    ]
    print("\n".join(rules_strs))
    print()


def display_goal(word_start, word_target):
    print(f"GOAL: Word walk from [ {word_start} ] to [ {word_target} ]")


def display_progress(words, target_word):
    length = len(target_word)
    distances = [length - compute_overlap(word, target_word) for word in words]

    progress_strs = ["Current progress (distance)"]
    progress_strs += [f"[ {word} ] ({distance})" for word, distance in zip(words, distances)]
    if words[-1] != target_word:
        progress_strs += [
            "  " + "-" * length,
            f"[ {target_word} ]"
        ]
    else:
        progress_strs += [" Target reached!"]
    print()
    print("\n ".join(progress_strs))
    print()


def do_turn(word: str, allowed_words: set[str]):
    """User chooses the next word."""
    while True:
        new_word = input(f"The current word is '{word}'. Enter the next word:\n > ").lower().strip()
        if len(word) != len(new_word):
            print(f">< Oops, word must be {len(word)} letters long.")
        elif new_word not in allowed_words:
            print(f">< Oops, word '{new_word}' does not exist.")
        elif (distance := len(word) - compute_overlap(word, new_word)) != 1:
            print(f">< Oops, exactly 1 letter must be different, but I found {distance}.")
        else:
            print("Nice word!")
            return new_word
        print(">< Try again!")


def auto_pick_words(word_list):
    """Pick 2 words from list, which have no common letters."""
    word0 = random.choice(word_list)
    while True:
        word1 = random.choice(word_list)
        if not compute_overlap(word0, word1):
            return word0, word1


def play(word_list: list[str], word_start: str, word_target: str):
    word_set = set(word_list)

    display_rules()
    display_goal(word_start, word_target)
    progress_words = [word_start]

    # play turns
    while (word_current := progress_words[-1]) != word_target:
        display_progress(progress_words, word_target)
        new_word = do_turn(word_current, word_set)
        progress_words.append(new_word)

    display_progress(progress_words, word_target)
    print(f"Congratulations, finished in {len(progress_words) - 1} moves!")


def main():
    word_list = load_words(FILENAME_SGB)
    word_start, word_target = auto_pick_words(word_list)
    play(word_list, word_start, word_target)


if __name__ == "__main__":
    main()
