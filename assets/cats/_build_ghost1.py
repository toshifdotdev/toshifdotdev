from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
P = 8
W, H = 22, 24
FRAMES = 10

# Cute ghost under a sheet, with little eyes peeking out and arms poking through
# Outline dark plum, sheet white, cheeks pink, eyes dark
PALETTE = {
    ".": (0, 0, 0, 0),
    "k": (40, 25, 55, 255),       # outline
    "W": (255, 250, 252, 255),    # sheet white
    "w": (225, 215, 235, 255),    # sheet shadow
    "e": (50, 30, 60, 255),       # eyes
    "E": (255, 255, 255, 255),    # eye highlight
    "p": (255, 150, 195, 255),    # pink cheeks
    "m": (180, 70, 110, 255),     # mouth (visible)
    "h": (255, 215, 0, 255),      # hands
    "s": (180, 160, 200, 255),    # sheet folds (visible against white)
}

# 22x24 — round-top ghost with wavy bottom hem and a peak on top
# Arms poke out around row 11-13
# Eyes at row 9-10
# Mouth at row 12
BASE = [
    "........................",  # 0
    "..........kk............",  # 1   peak
    ".........kWWk...........",  # 2
    "........kWWWWk..........",  # 3
    ".......kWWWWWWk.........",  # 4
    "......kWWWWWWWWk........",  # 5
    ".....kWWWWWWWWWWk.......",  # 6
    "....kWWWWWWWWWWWWk......",  # 7
    "...kWWWWWWWWWWWWWWk.....",  # 8
    "...kWSSSSSSSSSSSSk.....",  # 9   eyes row top
    "..kWSeEeSSSSSSSeEeSk....",  # 10  eyes + arm area
    "..kWSeEeSSSSSSSeEeSk....",  # 11
    "..kWSSSSSSmmSSSSSSk.....",  # 12  mouth
    "..kWWSSSSSSSSSSSSWWk....",  # 13
    "...kWSSSSSSSSSSSSSk.....",  # 14
    "....kWSSSSSSSSSSSk......",  # 15
    "....kWSSSSSSSSSSSk......",  # 16
    "...kWSSSSSSSSSSSSSk.....",  # 17
    "..kWSSpSSSSSSSSpSSSk....",  # 18  blush + wavy start
    ".kWWkSSSSSSSSSSSSkWWk...",  # 19
    "kWWk..kSSSSSSSSk..kWWk..",  # 20  wave 1
    "kWk...kSSSSSSSSk...kWk..",  # 21
    ".k....kSSSSSSSSk....k...",  # 22  wave 2
    "......kWWWWWWWWk........",  # 23
]

EYES = [(9, 6, "e"), (9, 7, "e"), (9, 14, "e"), (9, 15, "e")]
EYE_HL = [(8, 6, "E"), (8, 15, "E")]
MOUTH = [(11, 10, "m"), (11, 11, "m")]
BLUSH = [(12, 5, "p"), (12, 16, "p")]

# Arms that wave — small hand pixels at the side
# Left arm hand at (10, 2..3), right arm at (10, 18..19)


def render_frame(frame_idx):
    grid = [list(row) for row in BASE]

    # Eyes (with blink)
    blinking = (frame_idx % 7 == 4)
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

    # Floating motion: shift whole thing up/down
    bob = [0, 0, -1, 0, 0, 1, 0, 0, -1, 0][frame_idx]
    if bob != 0:
        new = [["."] * W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                ny = y + bob
                if 0 <= ny < H and grid[y][x] != ".":
                    new[ny][x] = grid[y][x]
        grid = new

    # Wave — extra sparkles
    if frame_idx in (1, 6):
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
out_path = os.path.join(OUT, "ghost1.gif")
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
