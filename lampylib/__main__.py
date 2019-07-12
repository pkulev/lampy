import collections

from lampylib import Color, Command, Launchpad


def main():
    launchpad = Launchpad().connect()

    colors = [
        (0b00, 0b00),  # 0:  0 0 no color
        (0b00, 0b01),  # 1:  0 1 red
        (0b00, 0b10),  # 2:  0 2 no color
        (0b00, 0b11),  # 3:  0 3 red
        (0b01, 0b00),  # 4:  1 0 pale green
        (0b01, 0b01),  # 5:  1 1 pale red-green
        (0b01, 0b10),  # 6:  1 2 medium green
        (0b01, 0b11),  # 7:  1 3 
        (0b10, 0b00),  # 8:  2 0
        (0b10, 0b01),  # 9:  2 1
        (0b10, 0b10),  # 10: 2 2
        (0b10, 0b11),  # 11: 2 3
        (0b11, 0b00),  # 12: 3 0
        (0b11, 0b01),  # 13: 3 1
        (0b11, 0b10),  # 14: 3 2
        (0b11, 0b11),  # 15: 3 3
    ]
    indexes = collections.defaultdict(lambda: 0)

    while True:
        msg = launchpad.input.get_message()
        if msg:
            cmd = Command.from_message(msg)
            print(cmd)

            if cmd.type == cmd.TYPE_NOTE_ON and cmd.value == 0x7F:
                print(cmd.value)
                r, g = colors[indexes[cmd.key]]
                launchpad.output.send_message([0x90, cmd.key, Color(r, g).as_binary()])

                print(f"index = {indexes[cmd.key]}")
                indexes[cmd.key] += 1
                if indexes[cmd.key] == len(colors):
                    indexes[cmd.key] = 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGot ^C, exitting...")
    except Exception as exc:
        print(exc)
