from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
P = 8
W, H = 22, 24
FRAMES = 10

# Cyan-tinted ghost (sheet is icy blue), with magenta eyes for contrast
PALETTE = {
    ".": (0, 0, 0, 0),
    "k": (20, 30, 70, 255),
    "W": (230, 250, 255, 255),
    "w": (190, 220, 240, 255),
    "e": (180, 50, 130, 255),     # magenta eyes
    "E": (255, 255, 255, 255),
    "p": (255, 150, 195, 255),
    "m": (180, 70, 110, 255),
    "h": (255, 215, 0, 255),
    "s": (140, 180, 220, 255),
}

BASE = [
    "........................",
    "..........kk............",
    ".........kWWk...........",
    "........kWWWWk..........",
    ".......kWWWWWWk.........",
    "......kWWWWWWWWk........",
    ".....kWWWWWWWWWWk.......",
    "....kWWWWWWWWWWWWk......",
    "...kWWWWWWWWWWWWWWk.....",
    "...kWSSSSSSSSSSSSk.....",
    "..kWSeEeSSSSSSSeEeSk....",
    "..kWSeEeSSSSSSSeEeSk....",
    "..kWSSSSSSmmSSSSSSk.....",
    "..kWWSSSSSSSSSSSSWWk....",
    "...kWSSSSSSSSSSSSSk.....",
    "....kWSSSSSSSSSSSk......",
    "....kWSSSSSSSSSSSk......",
    "...kWSSSSSSSSSSSSSk.....",
    "..kWSSpSSSSSSSSpSSSk....",
    ".kWWkSSSSSSSSSSSSkWWk...",
    "kWWk..kSSSSSSSSk..kWWk..",
    "kWk...kSSSSSSSSk...kWk..",
    ".k....kSSSSSSSSk....k...",
    "......kWWWWWWWWk........",
]

EYES = [(9, 6, "e"), (9, 7, "e"), (9, 14, "e"), (9, 15, "e")]
EYE_HL = [(8, 6, "E"), (8, 15, "E")]
MOUTH = [(11, 10, "m"), (11, 11, "m")]
BLUSH = [(12, 5, "p"), (12, 16, "p")]


def render_frame(frame_idx):
    grid = [list(row) for row in BASE]

    blinking = (frame_idx % 7 == 5)
    if not blinking:
        for r, c, ch in EYES:
            grid[r][c] = ch
        for r, c, ch in EYE_HL:
            grid[r][c] = ch
    else:
        for (r, c) in [(9, 6), (9, 7), (9, 14), (9, 15)]:
            grid[r][c] = "k"

    for r, c, ch in MOUTH:
        grid[r][c] = ch
    for r, c, ch in BLUSH:
        grid[r][c] = ch

    bob = [0, 0, 0, -1, 0, 0, 1, 0, 0, -1][frame_idx]
    if bob != 0:
        new = [["."] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                ny = y + bob
                if 0 <= ny < H and grid[y][x] != ".":
                    new[ny][x] = grid[y][x]
        grid = new

    if frame_idx in (2, 7):
        for (r, c) in [(2, 4), (2, 17), (3, 3), (3, 18)]:
            if 0 <= r < H and 0 <= c < W and grid[r][c] == ".":
                grid[r][c] = "E"

    return grid


def make_image(grid, scale=P, palette=PALETTE):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in palette and palette[ch][3] > 0:
                img.putpixel((x, y), palette[ch])
    return img.resize((W*scale, H*scale), Image.NEAREST)


frames = [make_image(render_frame(i)) for i in range(FRAMES)]
out_path = os.path.join(OUT, "ghost2.gif")
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=150,
    loop=0,
    disposal=2,
    transparency=0,
)
print("wrote", out_path, "size", os.path.getsize(out_path))
