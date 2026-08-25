from PIL import Image, ImageDraw
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Pixel scale
P = 6
W, H = 32, 32
FRAMES = 8

PALETTE = {
    ".": (0, 0, 0, 0),       # transparent
    "k": (12, 12, 18, 255),  # outline
    "p": (255, 80, 170, 255),  # body (hot pink)
    "P": (200, 30, 130, 255),
    "w": (255, 220, 240, 255),  # belly
    "e": (255, 200, 50, 255),  # eyes (gold)
    "E": (255, 130, 30, 255),  # eye highlight
    "c": (255, 60, 200, 255),  # cheek
    "h": (0, 0, 0, 0),
}

# base sitting cat (32x32)
BASE = [
    "................................",
    "................................",
    "........kk....kk................",
    ".......kppk..kppk...............",
    "......kppppkkppppk..............",
    "......kpPppppppPpk......kk......",
    "....kkppppppppppppkk....kppk.....",
    "...kpppwpppppppppwppkkkkpppppk..",
    "...kpwwppppppppppwwpppppppppppk.",
    "...kpwppppepeeppppwppppepeepppk.",
    "...kpwpppepepeppppwpppepepepppk.",
    "...kppwwppppppwwwwwppppppppwwpk.",
    "....kppppppkkppppppppkkppppppk..",
    ".....kpppk.kppppppppk.kppppk....",
    "......kppk..kppppppk..kpppk.....",
    "......kppk...kkppkk...kpppk.....",
    "......kppk.....kk.....kpppk.....",
    "......kppk............kpppk.....",
    "......kppk............kpppk.....",
    "......kppk............kpppk.....",
    "......kppk............kpppk.....",
    "......kppk............kpppk.....",
    "......kppk............kpppk.....",
    "......kppk............kpppk.....",
    ".....kppppk..........kppppk.....",
    ".....kpppppkk......kkpppppk.....",
    ".....kkppppppkk..kkppppppkk.....",
    "......kkkppppppppppppppkkk......",
    "........kkkkppppppppkkkk........",
    "...........kkkkppkkk............",
    ".............kkkk...............",
    "................................",
]

# Frame variations: tail + ear twitch + eye blink + paw wiggle
# We'll produce frames by shifting tail/ears/paws across frames.

def render_frame(frame_idx):
    grid = [list(row) for row in BASE]
    # tail wag: replace tail pixels on the right
    if frame_idx % 4 == 0:
        # tail up-right
        for r, c in [(14, 28), (13, 29), (12, 30), (11, 31)]:
            if r < H and c < W:
                grid[r][c] = "p"
                grid[r-1][c] = "k"
    elif frame_idx % 4 == 1:
        for r, c in [(15, 29), (14, 30), (13, 31)]:
            if r < H and c < W:
                grid[r][c] = "p"
                grid[r-1][c] = "k"
    elif frame_idx % 4 == 2:
        for r, c in [(16, 30), (15, 31), (14, 31)]:
            if r < H and c < W:
                grid[r][c] = "p"
                grid[r-1][c] = "k"
    else:
        for r, c in [(15, 29), (14, 30), (13, 31)]:
            if r < H and c < W:
                grid[r][c] = "p"
                grid[r-1][c] = "k"

    # paw wiggle (rows 23-24, columns 7 and 23)
    paw_shift = [0, 0, 1, 1, 0, 0, -1, -1][frame_idx]
    # left paw (col 7, rows 23-24) — wiggle horizontally by replacing
    if paw_shift != 0:
        # shift 1 pixel by recoloring
        for r in (23, 24):
            for c in range(7, 13):
                if 0 <= c+paw_shift < W and grid[r][c] in ("p", "k"):
                    v = grid[r][c]
                    grid[r][c] = "."
                    grid[r][c+paw_shift] = v

    # blink every 4th frame
    if frame_idx % 4 == 2:
        # eyes are at row 9 (cols 11,12) and row 10 (cols 9,10,11) and 22,23 row 9
        # simplify: cover right eye and left eye (rows 9-10, cols 9-12, 19-22)
        for r in (9, 10):
            for c in (10, 11, 20, 21):
                if 0 <= c < W:
                    grid[r][c] = "k"

    # ear twitch
    if frame_idx in (1, 5):
        # tilt left ear down a pixel by changing its top
        grid[2] = list(grid[2])
        grid[2][8] = "p"
        grid[2][23] = "p"

    return grid


def make_image(grid, scale=P, palette=PALETTE):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in palette and palette[ch][3] > 0:
                img.putpixel((x, y), palette[ch])
    return img.resize((W*scale, H*scale), Image.NEAREST)


frames = [make_image(render_frame(i)) for i in range(FRAMES)]

# Save
out_path = os.path.join(OUT, "cat1_pink.gif")
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=120,
    loop=0,
    disposal=2,
    transparency=0,
)
print("wrote", out_path)
