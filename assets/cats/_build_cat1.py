from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
# Big chunky pixel size so the grid is clearly visible
P = 10
W, H = 24, 24
FRAMES = 8

# Square pixel-grid cat head, 8-bit retro style
# - hard blocky outline (3px wide feel via thick outline)
# - tiny dot eyes (1-2 pixel each)
# - whiskers on both sides
# - pink blush circles
# - yellow nose
# - WIDE head, very square/boxy

PALETTE = {
    ".": (0, 0, 0, 0),
    "k": (30, 20, 40, 255),        # dark outline
    "W": (255, 250, 252, 255),     # white face
    "w": (220, 205, 230, 255),     # shadow white
    "e": (30, 20, 40, 255),        # eyes (same as outline)
    "p": (255, 130, 170, 255),     # pink blush
    "y": (255, 200, 60, 255),      # yellow nose
    "m": (30, 20, 40, 255),        # mouth
    "h": (30, 20, 40, 255),        # whisker
    "o": (255, 170, 50, 255),      # calico orange patch
    "O": (220, 100, 30, 255),
}

# 24x24 — chunky squarish cat head with two triangular ears on top
# The outline is THICK (2px) so the pixel grid is obvious
BASE = [
    "........................",  # 0
    "....kkkk........kkkk....",  # 1   ear tops
    "...kWWWWk......kWWWWk...",  # 2
    "..kWwwwwWk....kWwwwwWk..",  # 3
    "..kWwwwwWWk..kWWwwwwWk..",  # 4
    "..kWwwwwWWk..kWWwwwwWk..",  # 5
    "..kWWWWWWWWkkWWWWWWWWWk..",  # 6
    "...kWWWWWWWWWWWWWWWWWWk.",  # 7
    "...kWWWWWWWWWWWWWWWWWWk.",  # 8
    "..kWWWWWWWWWWWWWWWWWWWWk",  # 9
    "..kWWWWWWWWWWWWWWWWWWWWk",  # 10
    "..kWWWWWWWWWWWWWWWWWWWWk",  # 11
    "..kWWWWWWWWWWWWWWWWWWWWk",  # 12
    "..kWWWWWWWWWWWWWWWWWWWWk",  # 13
    "...kWWWWWWWWWWWWWWWWWWk.",  # 14
    "....kkWWWWWWWWWWWWWWkk..",  # 15
    "......kWWWWWWWWWWWWk....",  # 16
    ".......kWWWWWWWWWWk.....",  # 17
    "........kWWWWWWWWk......",  # 18
    ".........kWWWWWWk.......",  # 19
    "..........kWWWWk........",  # 20
    "...........kWWk.........",  # 21
    "............kk..........",  # 22
    "........................",  # 23
]

# Tiny dot eyes at row 11, cols 8 and 15
# Blush at row 12, cols 6-7 and 17-18 (chunky square patches)
# Nose at row 12, cols 11-12
# Whiskers at rows 12-13, extending out

EYES = [(11, 8, "e"), (11, 9, "e"), (11, 14, "e"), (11, 15, "e")]
NOSE = [(12, 11, "y"), (12, 12, "y")]
BLUSH = [(12, 6, "p"), (12, 7, "p"), (12, 16, "p"), (12, 17, "p"),
         (13, 6, "p"), (13, 7, "p"), (13, 16, "p"), (13, 17, "p")]
MOUTH = [(14, 11, "m"), (14, 12, "m")]
WHISKERS_L = [(12, 4, "h"), (12, 5, "h"), (13, 3, "h"), (13, 4, "h")]
WHISKERS_R = [(12, 18, "h"), (12, 19, "h"), (13, 19, "h"), (13, 20, "h")]


def render_frame(frame_idx):
    grid = [list(row) for row in BASE]

    # Blinking
    if frame_idx % 6 == 3:
        # closed eyes: horizontal line
        for (r, c) in [(11, 8), (11, 9), (11, 14), (11, 15)]:
            grid[r][c] = "k"
    else:
        for r, c, ch in EYES:
            grid[r][c] = ch

    for r, c, ch in NOSE:
        grid[r][c] = ch
    for r, c, ch in BLUSH:
        grid[r][c] = ch
    for r, c, ch in MOUTH:
        grid[r][c] = ch
    for r, c, ch in WHISKERS_L + WHISKERS_R:
        grid[r][c] = ch

    # Head bob (subtle 1px)
    bob = [0, 0, -1, 0, 0, 0, 1, 0][frame_idx]
    if bob != 0:
        new = [row[:] for row in grid]
        for y in range(0, 22):
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
out_path = os.path.join(OUT, "cat_pixel1.gif")
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=160,
    loop=0,
    disposal=2,
    transparency=0,
)
print("wrote", out_path, "size", os.path.getsize(out_path))
