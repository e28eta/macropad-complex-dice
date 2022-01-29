from adafruit_macropad import MacroPad
import time

# Mode of the rotary switch, changed by pressing the switch
class CurrentMode():
    # Change the number of dice being rolled
    COUNT = 1
    # Change the +/- modifier added to the roll
    MODIFIER = 2

# The dice available to roll, in the order they're presented
# There's some flexibility to change this, but changing the length will require additional changes
dice = [
    "2",
    "4",
    "6",
    "8",
    "10",
    "12",
    "20",
    "100"
]

# string format for a die to display
die_format = "{{0:2d}}d{:3}"
# All string formats for the display: dice to roll, plus last line
text_formats = [
    "{0} {0}  {0}".format(die_format).format(*dice[0:3]),
    "{0} {0}  {0}".format(die_format).format(*dice[3:6]),
    "{0} {0}".format(die_format).format(*dice[6:]),
    "{0:6s}  {1:<+3d}    {{mute}}"
]

# Refreshes the macropad's display given the mode, dice_count, dice_modifier, and whether newlines should be sent
# This calls refresh_pixels
def refresh_display(macropad, current_mode, dice_count, dice_modifier, send_newline):
    text_lines = macropad.display_text()
    text_lines[0].text = text_formats[0].format(dice_count)
    text_lines[1].text = text_formats[1].format(dice_count)
    text_lines[2].text = text_formats[2].format(dice_count)
    text_lines[3].text = text_formats[3].format(" \\n" if send_newline else "", dice_modifier)
    text_lines.show()
    
    refresh_pixels(macropad.pixels, current_mode, dice_count, dice_modifier, send_newline)

# Refreshes the macropad's pixels for a given mode, dice_count and dice_modifier.
# Helper for refresh_display, don't call directly
#
# Uses the pixels to display (in white) the number of dice that'll be rolled
# Uses green/red for magnitude of the modifier
# Blended color if the pixel is lit up for both dice count & modifier
# Auto-send toggle in bottom left in blue
# Reset button in bottom middle, red if it'll do anything
# Mute button on bottom right
def refresh_pixels(pixels, current_mode, dice_count, dice_modifier, send_newline):
    new_pixels = []
    for i in range(9):
        is_on_for_count = i < dice_count
        
        if i >= abs(dice_modifier) and not is_on_for_count:
            # completely off
            color = 0x0
        elif i >= abs(dice_modifier):
            # Only on for dice count
            color = 0x808080
        elif dice_modifier >= 0 and not is_on_for_count:
            # positive modifier, not on for count
            color = 0x00C000 
        elif dice_modifier >= 0:
            # positive modifier and dice count
            color = 0X40FF40
        elif not is_on_for_count:
            # negative modifier, not on for count
            color = 0xC00000
        else:
            # negative modifier and dice count
            color = 0XFF2020
            
        new_pixels.append(color)
        
    new_pixels.extend([
        0x0000C0 if send_newline else 0x000010,
        0x800000 if not (current_mode == CurrentMode.COUNT and dice_count is 1 and dice_modifier is 0) else 0x0,
        0x808000
    ])
    
    pixels[:] = new_pixels

macropad = MacroPad()

previous_encoder = macropad.encoder
current_mode = CurrentMode.COUNT
dice_count = 1
dice_modifier = 0
send_newline = True
debug_output = False

refresh_display(macropad, current_mode, dice_count, dice_modifier, send_newline)

while True:
    macropad.encoder_switch_debounced.update()
    
    if macropad.encoder_switch_debounced.pressed:
        current_mode = CurrentMode.MODIFIER if current_mode == CurrentMode.COUNT else CurrentMode.COUNT
        continue
    
    encoder_delta = macropad.encoder - previous_encoder
    previous_encoder = macropad.encoder
    if encoder_delta != 0:
        if current_mode == CurrentMode.COUNT:
            dice_count = max(1, dice_count + encoder_delta)
        else:
            dice_modifier += encoder_delta
        refresh_display(macropad, current_mode, dice_count, dice_modifier, send_newline)
    
    key_event = macropad.keys.events.get()

    if key_event and key_event.pressed:
        if key_event.key_number in range(len(dice)):
            # Send key presses matching the "roll" string for this die
            output = "/r {}d{}{}{}".format(
                dice_count,
                dice[key_event.key_number],
                " {:+d}".format(dice_modifier) if dice_modifier != 0 else "",
                "\n" if send_newline else ""
            )
            macropad.keyboard_layout.write(output)
            if debug_output:
                print(output.replace("\n", "\\n"))
        if key_event.key_number is 9:
            # toggle whether or not newline is sent at the end of the string
            send_newline = not send_newline
            refresh_display(macropad, current_mode, dice_count, dice_modifier, send_newline)
        if key_event.key_number is 10:
            # Reset dice count, modifier, and current mode
            dice_count = 1
            dice_modifier = 0
            current_mode = CurrentMode.COUNT
            refresh_display(macropad, current_mode, dice_count, dice_modifier, send_newline)
        if key_event.key_number is 11:
            # Send key combination for Zoom's global mute/un-mute shortcut
            macropad.keyboard.press(macropad.Keycode.SHIFT, macropad.Keycode.COMMAND, macropad.Keycode.A)
            macropad.keyboard.release_all()
