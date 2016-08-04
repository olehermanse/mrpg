#!/usr/bin/env python3
import json

def main():
    character = {}
    character["name"] = input("Character name: ");
    character["level"] = int(input("Character level: "))

    def fill_number_list(l, num):
        for i in range(num):
            l.append(int(input("Enter #{}: ".format(i))))


    passives = []
    print("Please enter passive skill numbers:")
    fill_number_list(passives, 4)
    character["passives"] = passives

    actives = []
    print("Please enter active skill numbers:")
    fill_number_list(actives, 8)
    character["actives"] = actives

    with open('../data/character.json', 'w') as f:
        json.dump(character, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
