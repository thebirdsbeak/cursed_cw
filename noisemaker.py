from tones import SINE_WAVE, SAWTOOTH_WAVE
from tones.mixer import Mixer

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


def create(name, morse):
    # Create mixer, set sample rate and amplitude
    mixer = Mixer(44100, 0.5)
    # Create mixer track 0 (more tracks e.g. create_track(1, ...)
    mixer.create_track(0, SINE_WAVE, attack=0, decay=0.0)
    mixer.create_track(1, SAWTOOTH_WAVE, vibrato_frequency=200.0, vibrato_variance=200.0, attack=0.00, decay=0.0)


    for x in morse:
        for glyph in x:
            if glyph == ".":
                mixer.add_note(0, note='D', octave=5, duration=0.06)
                mixer.add_note(0, note='D', octave=5, duration=0.06, amplitude=0)
                mixer.add_note(1, note='E', octave=4, duration=0.12, endnote='E', amplitude=0.2)
                print("dits added")
            elif glyph == "-":
                mixer.add_note(0, note='D', octave=5, duration=0.180)
                mixer.add_note(0, note='D', octave=5, duration=0.06, amplitude=0)
                mixer.add_note(1, note='E', octave=4, duration=0.24, endnote='E', amplitude=0.2)
                print("dahs added")
            else:
                make_space()

    # Mix all tracks into a single list of samples and write to .wav file
    mixer.write_wav('sounds/noisy/{}.wav'.format(name[0]))
 
def make_space():
    mixer = Mixer(44100, 0.5)
    # Create mixer track 0 (more tracks e.g. create_track(1, ...)
    mixer.create_track(0, SINE_WAVE, attack=0, decay=0.0)
    mixer.create_track(1, SAWTOOTH_WAVE, vibrato_frequency=200.0, vibrato_variance=200.0, attack=0.00, decay=0.0)

    mixer.add_note(0, note='D', octave=5, duration=0.42, amplitude=0)
    mixer.add_note(1, note='E', octave=4, duration=0.12, endnote='E', amplitude=0.2)
    # Mix all tracks into a single list of samples and write to .wav file
    mixer.write_wav('sounds/noisy/space.wav')

for i in characters:
    create(i[0], i[1])

make_space()
    
