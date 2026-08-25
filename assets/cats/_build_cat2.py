from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
P = 10
W, H = 24, 24
FRAMES = 8

# Orange calico pixel cat head, same square pixel-grid style
PALETTE = {
    ".": (0, 0, 0, 0),
    "k": (30, 20, 40, 255),
    "W": (255, 250, 252, 255),
    "w": (220, 205, 230, 255),
    "O": (255, 140, 50, 255),      # orange
    "o": (220, 90, 30, 255),       # dark orange
    "e": (30, 20, 40, 255),
    "p": (255, 130, 170, 255),
    "y": (255, 200, 60, 255),
    "m": (30, 20, 40, 255),
    "h": (30, 20, 40, 255),
}

BASE = [
    "........................",
    "....kkkk........kkkk....",
    "...kOOOk........kOOOk...",  # orange ears
    "..kOoooOk....kOoooOk....",
    "..kOoooOOOk..kOOoooOk...",
    "..kOoooOOOk..kOOoooOk...",
    "..kOOOOOOOOOkkOOOOOOOOO..",  # extra 'O' to make 24 cols
    "...kOOOOOOOOOOOOOOOOOOO..",
    "...kOOOOOOOOOOOOOOOOOOO..",
    "..kOOOOOOOOOOOOOOOOOOOOO",
    "..kOOOOOOOOOOOOOOOOOOOOO",
    "..kOOOOOOOOOOOOOOOOOOOOO",
    "..kOOOOOOOOOOOOOOOOOOOOO",
    "..kOOOOOOOOOOOOOOOOOOOOO",
    "...kOOOOOOOOOOOOOOOOOOO..",
    "....kkOOOOOOOOOOOOOOOOOk.",
    "......kOOOOOOOOOOOOOOOk..",
    ".......kOOOOOOOOOOOOOk...",
    "........kOOOOOOOOOOOk....",
    ".........kOOOOOOOOOk.....",
    "..........kOOOOOOOk......",
    "...........kOOOOOk.......",
    "............kkkk.........",
    "........................",
]

# pad to 24 cols exactly — let me re-emit with exact width 24
def _w(s): return len(s)
for i, row in enumerate(BASE):
    if _w(row) != 24:
        # pad to 24
        BASE[i] = row + "." * (24 - _w(row))

# Eyes at row 11
EYES = [(11, 8, "e"), (11, 9, "e"), (11, 14, "e"), (11, 15, "e")]
NOSE = [(12, 11, "y"), (12, 12, "y")]
BLUSH = [(12, 6, "p"), (12, 7, "p"), (12, 16, "p"), (12, 17, "p"),
         (13, 6, "p"), (13, 7, "p"), (13, 16, "p"), (13, 17, "p")]
MOUTH = [(14, 11, "m"), (14, 12, "m")]
WHISKERS_L = [(12, 4, "h"), (12, 5, "h"), (13, 3, "h"), (13, 4, "h")]
WHISKERS_R = [(12, 18, "h"), (12, 19, "h"), (13, 19, "h"), (13, 20, "h")]


def render_frame(frame_idx):
    grid = [list(row) for row in BASE]

    if frame_idx % 6 == 4:
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

    bob = [0, 0, 0, -1, 0, 0, 1, 0][frame_idx]
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
out_path = os.path.join(OUT, "cat_pixel2.gif")
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
