from typing import List, Union

Blocks = List[Union[int, None]]


def parse_disk_map(disk_map: str):
    int_disk_map = list(map(int, disk_map.strip()))
    blocks: Blocks = []

    for i in range(0, len(int_disk_map), 2):
        file_id = i // 2

        file_len = int_disk_map[i]
        blocks += [file_id] * file_len

        if i + 1 < len(int_disk_map):
            empty_len = int_disk_map[i + 1]
            blocks += [None] * empty_len

    return blocks


def compact_blocks(blocks: Blocks) -> Blocks:
    blocks = [b for b in blocks]
    i = 0
    j = len(blocks) - 1
    while i < j:
        while i < j and blocks[i] != None:
            i += 1
        while i < j and blocks[j] == None:
            j -= 1
        blocks[i], blocks[j] = blocks[j], blocks[i]

    return blocks


def compact_files(blocks: Blocks) -> Blocks:
    blocks = [b for b in blocks]

    j = len(blocks)
    while j > 0:
        j -= 1

        # Seek to next (from the back) non-empty block
        while j > 0 and blocks[j] is None:
            j -= 1
        if j == 0: break
        file_id = blocks[j]

        # Seek to beginning of file
        file_len = 1
        while blocks[j - 1] == file_id:
            j -= 1
            file_len += 1
        # print("File", file_id, "offset", j, "length", file_len)

        # Find space from 0 to j
        i = 0
        found = False
        while i < j:
            if blocks[i] is not None:
                i += 1
                continue
            space = 0
            while blocks[i + space] is None:
                space += 1
            if space >= file_len:
                found = True
                break
            i += space
        if found:
            # print("Space found, offset", i, "length", space)
            blocks[j : j + file_len] = [None] * file_len
            blocks[i : i + file_len] = [file_id] * file_len

    return blocks


def checksum(blocks: Blocks) -> int:
    return sum(i * b for i, b in enumerate(blocks) if b is not None)


def process(disk_map: str):
    blocks = parse_disk_map(disk_map)
    compacted0 = compact_blocks(blocks)
    compacted1 = compact_files(blocks)
    return checksum(compacted0), checksum(compacted1)


example_disk_map = """
2333133121414131402
"""


def example():
    a, b = process(example_disk_map)
    assert a == 1928
    assert b == 2858


if __name__ == "__main__":
    example()

    with open("2024/09.input", "r") as f:
        disk_map = f.read()

    a, b = process(disk_map)
    print(a)
    print(b)
