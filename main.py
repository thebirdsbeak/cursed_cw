import curses
from curses import wrapper
from random import choice
from tones import SINE_WAVE, SAWTOOTH_WAVE
from tones.mixer import Mixer
from playsound import playsound

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H",
            "I", "J", "K", "L", "M", "N", "O", "P",
            "Q", "R", "S", "T", "U", "V", "W", "X",
            "Y", "Z"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
prefixes = ["M2", "M6", "2M0", "G1", "G2", "G3",
            "G4", "G5", "G6", "G7", "M1", "M3", "M0"]
punctuation = ["!", "&", "'", "(", ")", "+", ",", "-", ";",
               "=", "@", "_", ".", "/"]

def splashscreen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "(c) 2025 Craig McIntyre", curses.color_pair(1))
    add_ascii(stdscr)
    stdscr.addstr("\nCALLSIGN MODE")
    stdscr.addstr("\nPress any key to begin...")
    stdscr.refresh()
    key = stdscr.getkey()
    return


def add_ascii(stdscr, filename="image.txt"):
    # Clear screen
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        stdscr.addstr(10, 10, f"File '{filename}' not found!")
        return

    max_y, max_x = stdscr.getmaxyx()

    for y, line in enumerate(lines):
        if y >= max_y:
            break  # Don't draw beyond the screen height
        # Truncate line if it's too long for the terminal width
        stdscr.addstr(y+2, 0, line[:max_x-1])


def morse_text(stdscr):
    target_text = callsigns()
    entered_text = []

    while True:
        stdscr.clear()

        display_text(stdscr, target_text, entered_text)

        stdscr.refresh()

        key = stdscr.getkey()
        try:
            if ord(key) == 27:
                break
        except TypeError:
            pass
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(entered_text) > 0:
                entered_text.pop()
        else:
            entered_text.append(key)


def display_text(stdscr, target_text, entered_text):
    stdscr.addstr(target_text)
    score = len(target_text)
    result = len(target_text)

    make_beep(target_text, stdscr)

    for i, keys in enumerate(entered_text):
        if i != score:
            correct_keys = target_text[i]
            feedback = curses.color_pair(3)
            if keys.upper() != correct_keys:
                feedback = curses.color_pair(1)
                result -= 1
            stdscr.addstr(0, i, keys.upper(), feedback)
            if i + 1 == score:
                chicken_dinner(stdscr, score, result)


def chicken_dinner(stdscr, score, result):
    stdscr.clear()
    stdscr.addstr(str(result))
    stdscr.addstr("/")
    stdscr.addstr(str(score))
    stdscr.addstr("\nPress any key to continue...")
    stdscr.refresh()
    stdscr.getkey()
    morse_text(stdscr)
    

def callsigns():
    prefix = choice(prefixes)
    suffix = ""
    for i in range(3):
        suffix += choice(alphabet)
    contact = prefix + suffix
    return contact


def make_beep(morse_in, stdscr):

    characters = [
    ['A', '.-'], ['B', '-...'], ['C', '-.-.'], ['D', '-..'], ['E', '.'],
    ['F', '..-.'], ['G', '--.'], ['H', '....'], ['I', '..'], ['J', '.---'],
    ['K', '-.-'], ['L', '.-..'], ['M', '--'], ['N', '-.'], ['O', '---'],
    ['P', '.--.'], ['Q', '--.-'], ['R', '.-.'], ['S', '...'], ['T', '-'],
    ['U', '..-'], ['V', '...-'], ['W', '.--'], ['X', '-..-'], ['Y', '-.--'],
    ['Z', '--..'],

    ['0', '-----'], ['1', '.----'], ['2', '..---'], ['3', '...--'],
    ['4', '....-'], ['5', '.....'], ['6', '-....'], ['7', '--...'],
    ['8', '---..'], ['9', '----.'],

    ['period', '.-.-.-'], [',', '--..--'], ['?', '..--..'], ["'", '.----.'],
    ['!', '-.-.--'], ['slash', '-..-.'], ['(', '-.--.'], [')', '-.--.-'],
    ['&', '.-...'], [':', '---...'], [';', '-.-.-.'], ['=', '-...-'],
    ['+', '.-.-.'], ['-', '-....-'], ['_', '..--.-'], ['"', '.-..-.'],
    ['$', '...-..-'], ['@', '.--.-.']]

    mixer = Mixer(44100, 0.5)
    mixer.create_track(0, SINE_WAVE, attack=0, decay=0.0)
    mixer.create_track(1, SAWTOOTH_WAVE, vibrato_frequency=200.0, vibrato_variance=200.0, attack=0.00, decay=0.0)

    for x in morse_in:
        for char in characters:
            if x == char[0]:
                glyph = char[1]
                for mod in glyph:
                    if mod == ".":
                        mixer.add_note(0, note='D', octave=5, duration=0.06)
                        mixer.add_note(0, note='D', octave=5, duration=0.06, amplitude=0)
                        mixer.add_note(1, note='E', octave=4, duration=0.12, endnote='E', amplitude=0.2)

                    elif mod == "-":
                        mixer.add_note(0, note='D', octave=5, duration=0.180)
                        mixer.add_note(0, note='D', octave=5, duration=0.06, amplitude=0)
                        mixer.add_note(1, note='E', octave=4, duration=0.24, endnote='E', amplitude=0.2)

        mixer.add_note(0, note='D', octave=5, duration=0.12, amplitude=0)
        mixer.add_note(1, note='E', octave=4, duration=0.12, endnote='E', amplitude=0.2)
    mixer.write_wav("soundfile.wav")
    playsound("soundfile.wav")
                

    



def main(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    splashscreen(stdscr)
    stdscr.clear()

    morse_text(stdscr)

wrapper(main)
