from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
P = 8
W, H = 28, 28
FRAMES = 8

# Same shape as hk1 but with cyan bow on the RIGHT ear
PALETTE = {
    ".": (0, 0, 0, 0),
    "k": (30, 30, 60, 255),
    "W": (245, 250, 255, 255),
    "w": (220, 230, 250, 255),
    "S": (200, 240, 255, 255),
    "r": (0, 230, 255, 255),    # cyan bow
    "R": (0, 150, 200, 255),
    "y": (255, 200, 80, 255),
    "p": (255, 100, 200, 255),
    "e": (30, 20, 60, 255),
    "E": (255, 255, 255, 255),
    "m": (30, 20, 60, 255),
}

BASE = [
    "............................",
    "...........k......k.........",
    "..........kWk....kWk........",
    "..........kSk....kSk........",
    ".........kWSSk..kSSWk.......",
    "........kWSSSSkkSSSSSWk......",
    ".......kWSSSSSSSSSSSSSWk.....",
    "......kWSSSSSSSSSSSSSSSWk....",
    "......kWSSSSSSSSSSSSSSSWk....",
    "......kWSSSSSSSSSSSSSSSWk....",
    "......kWWSSSSSSSSSSSSSSWWk...",
    "......kkSSSSSSSSSSSSSSSSkk...",
    ".......kWSSSSSSSSSSSSSSWk....",
    "........kkSSSSSSSSSSSSkk.....",
    "..........kkSSSSSSSSkk.......",
    "...........kkSSSSSSkk........",
    "............kSSSSSSSk........",
    "...........kWWSSSSWWk........",
    "..........kWSSSSSSSSWk.......",
    "..........kWSSSSSSSSWk.......",
    "..........kWSSSSSSSSWk.......",
    "..........kWSSSSSSSSWk.......",
    "...........kWSSSSSSWk........",
    "............kWWSSWWk.........",
    ".............kSSSSk..........",
    ".............kSSSSk..........",
    ".............kkkkkk..........",
    "............................",
]

EYES = [(10, 10, "e"), (10, 11, "e"), (10, 16, "e"), (10, 17, "e")]
EYE_HIGHLIGHTS = [(9, 10, "E"), (9, 17, "E")]
NOSE = [(12, 13, "y"), (12, 14, "y")]
BLUSH = [(12, 9, "p"), (12, 18, "p")]
MOUTH = [(13, 13, "m")]


def place_bow(grid, anchor_x, anchor_y, frame):
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

    blinking = (frame_idx % 6 == 4)
    if not blinking:
        for r, c, ch in EYES:
            grid[r][c] = ch
        for r, c, ch in EYE_HIGHLIGHTS:
            grid[r][c] = ch
    else:
        for (r, c) in [(10, 10), (10, 11), (10, 16), (10, 17)]:
            grid[r][c] = "k"

    for r, c, ch in NOSE:
        grid[r][c] = ch
    for r, c, ch in BLUSH:
        grid[r][c] = ch
    for r, c, ch in MOUTH:
        grid[r][c] = ch

    # Bow on the RIGHT ear: anchor around col 20, row 0
    place_bow(grid, 19, 0, frame_idx)

    bob = [0, 0, 0, -1, 0, 1, 0, 0][frame_idx]
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
out_path = os.path.join(OUT, "cat_hk2.gif")
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
