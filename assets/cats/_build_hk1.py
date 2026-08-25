from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
P = 8
W, H = 24, 24
FRAMES = 8

PALETTE = {
    ".": (0, 0, 0, 0),
    "k": (40, 25, 55, 255),
    "W": (255, 250, 252, 255),
    "w": (235, 215, 230, 255),
    "S": (255, 205, 220, 255),
    "r": (255, 70, 120, 255),
    "R": (190, 30, 80, 255),
    "y": (255, 195, 60, 255),
    "p": (255, 150, 195, 255),
    "e": (50, 30, 60, 255),
    "E": (255, 255, 255, 255),
    "g": (60, 40, 70, 255),
}

# 24x24, with ear tips at cols 6 and 17, and bow centered between them at col 11-12
BASE = [
    "........................",  # 0
    ".......k..........k.....",  # 1   ear tips
    "......kWk........kWk....",  # 2
    "......kSk........kSk....",  # 3   inner ear
    ".....kWSSk......kSSWk...",  # 4
    "....kWSSSSk....kWSSSWk..",  # 5
    "...kSSSSSSSk..kSSSSSSSk.",  # 6
    "..kWSSSSSSSSkkSSSSSSSSk.",  # 7
    "..kWSSSSSSSSSSSSSSSSSSk.",  # 8
    "..kWSSSSSSSSSSSSSSSSSSk.",  # 9
    "..kWWSSSSSSSSSSSSSSSSWk.",  # 10
    "..kkSSSSSSSSSSSSSSSSSSkk",  # 11
    "...kWSSSSSSSSSSSSSSSSWk.",  # 12
    "....kSSSSSSSSSSSSSSSSk..",  # 13
    ".....kSSSSSSSSSSSSSSk...",  # 14
    "......kWSSSSSSSSSSWk....",  # 15
    "......kWSSSSSSSSSSWk....",  # 16
    ".......kWSSSSSSSSWk.....",  # 17
    "........kWSSSSSSWk......",  # 18
    "........kWWSSSSWWk......",  # 19
    ".........kSSSSSSk.......",  # 20
    ".........kSSSSSSk.......",  # 21
    "..........kWWWWk........",  # 22
    "...........kkkkk.........",  # 23
]

# Eyes: row 11, cols 9 and 14
# Nose: row 13, col 11-12
# Cheeks: row 13, cols 8 and 15
EYES = [(11, 9, "e"), (11, 10, "e"), (11, 13, "e"), (11, 14, "e")]
EYE_HIGHLIGHTS = [(10, 9, "E"), (10, 14, "E")]
NOSE = [(13, 11, "y"), (13, 12, "y")]
BLUSH = [(13, 8, "p"), (13, 15, "p")]


def place_bow(grid, anchor_x, anchor_y, frame):
    # compact 4-wide bow, with knot
    pattern = [
        [".r.r.", "rRrRr", ".rkr"],
        [".r.r.", "rRrRr", ".rkr"],
        ["rr.rr", "rRrRr", ".rkr"],
        [".r.r.", "rRrRr", "rkkk"],
        [".r.r.", "rRrRr", ".rkr"],
        ["rr.rr", "rRrRr", ".rkr"],
        [".r.r.", "rRrRr", ".rkr"],
        [".r.r.", "rRrRr", "rkkk"],
    ]
    p = pattern[frame % len(pattern)]
    for ry, row in enumerate(p):
        for rx, ch in enumerate(row):
            y = anchor_y + ry
            x = anchor_x + rx
            if 0 <= y < H and 0 <= x < W and ch != ".":
                grid[y][x] = ch


def render_frame(frame_idx):
    grid = [list(row) for row in BASE]

    blinking = (frame_idx % 7 == 4)
    if not blinking:
        for r, c, ch in EYES:
            grid[r][c] = ch
        for r, c, ch in EYE_HIGHLIGHTS:
            grid[r][c] = ch
    else:
        for (r, c) in [(11, 9), (11, 10), (11, 13), (11, 14)]:
            grid[r][c] = "k"

    for r, c, ch in NOSE:
        grid[r][c] = ch
    for r, c, ch in BLUSH:
        grid[r][c] = ch

    # Bow on the LEFT ear, sitting above-left of the left ear
    place_bow(grid, 1, 0, frame_idx)

    bob = [0, 0, -1, 0, 0, 0, 1, 0][frame_idx]
    if bob != 0:
        new = [row[:] for row in grid]
        for y in range(0, 19):
            for x in range(W):
                if grid[y][x] != "." and 0 <= y + bob < H:
                    new[y + bob][x] = grid[y][x]
        grid = new

    return grid


def make_image(grid, scale=P, palette=PALETTE):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in palette and palette[ch][3] > 0:
                img.putpixel((x, y), palette[ch])
    return img.resize((W*scale, H*scale), Image.NEAREST)


frames = [make_image(render_frame(i)) for i in range(FRAMES)]
out_path = os.path.join(OUT, "cat_hk1.gif")
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=140,
    loop=0,
    disposal=2,
    transparency=0,
)
print("wrote", out_path, "size", os.path.getsize(out_path))
