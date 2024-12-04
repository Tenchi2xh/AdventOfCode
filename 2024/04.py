def parse_grid(grid: str) -> list[str]:
    lines = grid.strip().splitlines()

    width = len(lines[0])
    height = len(lines)

    columns = ["" for _ in range(width)]
    rows = ["" for _ in range(height)]
    forward_diagonals = ["" for _ in range(height + width - 1)]
    backward_diagonals = ["" for _ in range(len(forward_diagonals))]

    min_backwards_diagonal = -height + 1

    for x in range(width):
        for y in range(height):
            columns[x] += lines[y][x]
            rows[y] += lines[y][x]
            forward_diagonals[x + y] += lines[y][x]
            backward_diagonals[x - y - min_backwards_diagonal] += lines[y][x]

    return columns + rows + forward_diagonals + backward_diagonals


def find_xmas(line: str):
    return line.count("XMAS") + line[::-1].count("XMAS")


def process_grid(grid: str):
    return sum(find_xmas(l) for l in parse_grid(grid))


def find_crosses(grid: str):
    lines = grid.strip().splitlines()

    width = len(lines[0])
    height = len(lines)

    crosses = 0

    for x in range(width - 2):
        for y in range(height - 2):
            diagonal0 = lines[y][x] + lines[y + 1][x + 1] + lines[y + 2][x + 2]
            diagonal1 = lines[y][x + 2] + lines[y + 1][x + 1] + lines[y + 2][x]
            if diagonal0 in ("SAM", "MAS") and diagonal1 in ("SAM", "MAS"):
                crosses += 1

    return crosses


example_grid = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".strip()


def example():
    assert process_grid(example_grid) == 18
    assert find_crosses(example_grid) == 9


if __name__ == "__main__":
    example()

    with open("2024/04.input", "r") as f:
        grid = f.read()

    print(process_grid(grid))
    print(find_crosses(grid))
