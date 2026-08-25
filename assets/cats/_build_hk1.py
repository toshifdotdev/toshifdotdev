from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
P = 8
W, H = 28, 28
FRAMES = 8

# Hello-Kitty style: round head dominates, small body, big bow on ear
PALETTE = {
    ".": (0, 0, 0, 0),
    "k": (50, 30, 70, 255),      # outline (dark plum)
    "W": (255, 248, 252, 255),   # main white
    "w": (240, 220, 235, 255),   # shadow
    "S": (255, 210, 225, 255),   # inner ear pink
    "r": (255, 80, 130, 255),    # red bow
    "R": (200, 40, 90, 255),     # red bow shadow
    "y": (255, 200, 60, 255),    # yellow nose
    "p": (255, 150, 200, 255),   # pink cheek
    "e": (50, 30, 60, 255),      # eye dark
    "E": (255, 255, 255, 255),   # eye highlight
    "m": (80, 30, 60, 255),      # mouth
}

# 28x28 grid
# Head: rows 1-15 (round, with two pointy ears at top)
# Body: rows 16-26 (small sitting)
BASE = [
    "............................",  # 0
    "...........k......k.........",  # 1  ear tips
    "..........kWk....kWk........",  # 2
    "..........kSk....kSk........",  # 3  inner ear
    ".........kWSSk..kSSWk.......",  # 4
    "........kWSSSSkkSSSSSWk......",  # 5
    ".......kWSSSSSSSSSSSSSWk.....",  # 6
    "......kWSSSSSSSSSSSSSSSWk....",  # 7
    "......kWSSSSSSSSSSSSSSSWk....",  # 8
    "......kWSSSSSSSSSSSSSSSWk....",  # 9
    "......kWWSSSSSSSSSSSSSSWWk...",  # 10
    "......kkSSSSSSSSSSSSSSSSkk...",  # 11
    ".......kWSSSSSSSSSSSSSSWk....",  # 12
    "........kkSSSSSSSSSSSSkk.....",  # 13
    "..........kkSSSSSSSSkk.......",  # 14
    "...........kkSSSSSSkk........",  # 15  head->body
    "............kSSSSSSSk........",  # 16
    "...........kWWSSSSWWk........",  # 17
    "..........kWSSSSSSSSWk.......",  # 18
    "..........kWSSSSSSSSWk.......",  # 19
    "..........kWSSSSSSSSWk.......",  # 20
    "..........kWSSSSSSSSWk.......",  # 21
    "...........kWSSSSSSWk........",  # 22
    "............kWWSSWWk.........",  # 23
    ".............kSSSSk..........",  # 24
    ".............kSSSSk..........",  # 25
    ".............kkkkkk..........",  # 26
    "............................",  # 27
]

# Eye positions (row 10): cols 9-10 and 17-18
# Nose (row 12): col 13-14
# Blush (row 12): cols 9 and 18
# Mouth (row 13): col 13-14
# Bow: on left ear, anchored around (5, 3)

EYES = [(10, 10, "e"), (10, 11, "e"), (10, 16, "e"), (10, 17, "e")]
EYE_HIGHLIGHTS = [(9, 10, "E"), (9, 17, "E")]
NOSE = [(12, 13, "y"), (12, 14, "y")]
BLUSH = [(12, 9, "p"), (12, 18, "p")]
MOUTH = [(13, 13, "m")]


def place_bow(grid, anchor_x, anchor_y, frame):
    # bow pattern: 5x4 with little wings
    pattern = [
        [".r.r.", "rRrRr", "rkrkr", ".rrr."],
        [".r.r.", "rRrRr", "rkrkr", ".rkr."],
        [".r.r.", "rRrRr", "rkrkr", ".rrr."],
        ["rr.rr", "rRrRr", "rkrkr", "rr.rr"],
        [".r.r.", "rRrRr", "rkrkr", ".rrr."],
        [".r.r.", "rRrRr", "rkrkr", ".rkr."],
        [".r.r.", "rRrRr", "rkrkr", ".rrr."],
        ["rr.rr", "rRrRr", "rkrkr", "rr.rr"],
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

    # Eyes (with highlight unless blinking)
    blinking = (frame_idx % 6 == 3)
    if not blinking:
        for r, c, ch in EYES:
            grid[r][c] = ch
        for r, c, ch in EYE_HIGHLIGHTS:
            grid[r][c] = ch
    else:
        # closed eye: small line
        for (r, c) in [(10, 10), (10, 11), (10, 16), (10, 17)]:
            grid[r][c] = "k"

    for r, c, ch in NOSE:
        grid[r][c] = ch
    for r, c, ch in BLUSH:
        grid[r][c] = ch
    for r, c, ch in MOUTH:
        grid[r][c] = ch

    # Bow on the LEFT ear (around col 4, row 1)
    place_bow(grid, 2, 0, frame_idx)

    # Head bob
    bob = [0, 0, -1, 0, 0, 0, 1, 0][frame_idx]
    if bob != 0:
        new = [row[:] for row in grid]
        for y in range(0, 16):
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
