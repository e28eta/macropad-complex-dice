from adafruit_macropad import MacroPad
import time

macropad = MacroPad()

text_lines = macropad.display_text()
text_lines[0].text = "1d4     1d6    1d8"
text_lines[1].text = "1d10    2d10   1d12"
text_lines[2].text = "1d20    2d20   3d20"
text_lines[3].text = "1d100   3d8    {mute}"
text_lines.show()

while True:
    key_event = macropad.keys.events.get()

    if key_event and key_event.pressed:
        if key_event.key_number is 0:
            macropad.keyboard_layout.write("/r 1d4\n")
        if key_event.key_number is 1:
            macropad.keyboard_layout.write("/r 1d6\n")
        if key_event.key_number is 2:
            macropad.keyboard_layout.write("/r 1d8\n")
        if key_event.key_number is 3:
            macropad.keyboard_layout.write("/r 1d10\n")
        if key_event.key_number is 4:
            macropad.keyboard_layout.write("/r 2d10\n")
        if key_event.key_number is 5:
            macropad.keyboard_layout.write("/r 1d12\n")
        if key_event.key_number is 6:
            macropad.keyboard_layout.write("/r 1d20\n")
        if key_event.key_number is 7:
            macropad.keyboard_layout.write("/r 2d20\n")
        if key_event.key_number is 8:
            macropad.keyboard_layout.write("/r 3d20\n")
        if key_event.key_number is 9:
            macropad.keyboard_layout.write("/r 1d100\n")
        if key_event.key_number is 10:
            macropad.keyboard_layout.write("/r 3d8\n")
        if key_event.key_number is 11:
            macropad.keyboard.press(macropad.Keycode.SHIFT, macropad.Keycode.COMMAND, macropad.Keycode.A)
            macropad.keyboard.release_all()
