from PIL import Image
import os

OUT = os.path.dirname(os.path.abspath(__file__))
P = 6
W, H = 32, 32
FRAMES = 10

# black cat with cyan eyes & gold accents
PALETTE = {
    ".": (0, 0, 0, 0),
    "k": (8, 8, 14, 255),
    "b": (30, 30, 48, 255),   # body (near-black with blue tint)
    "B": (60, 60, 90, 255),
    "w": (200, 200, 220, 255),  # belly highlight
    "e": (0, 240, 255, 255),  # cyan eyes
    "E": (255, 255, 255, 255),
    "c": (255, 60, 130, 255),  # nose (hot pink)
    "g": (255, 200, 50, 255),  # gold collar
    "G": (255, 130, 30, 255),
}

BASE = [
    "................................",
    "................................",
    "........kk....kk................",
    ".......kbbk..kbbk...............",
    "......kbbbbkkbbbbk..............",
    "......kBbbbbbbBbbk......kk......",
    "....kkbbbbbbbbbbbbkk....kbBbk....",
    "...kbbwbbbbbbbbbwbbkkkkbbbbbbbk..",
    "...kbwwbbbbbbbbbbbwwbbbbbbbbbbbk.",
    "...kbwbbbeEebbbbbwbwbbbeEebbbbbk.",
    "...kbwbbbeeebbbbbwbbbbbeeebbbbbk.",
    "...kbbbwwwwbbwwwwbbwwwwbbwwwwbbk.",
    "....kbbbbbbkkbbbbbbbbkkbbbbbbk...",
    ".....kbBbk.kbbgggggbbbk.kbBbk....",
    "......kbBk..kbggggggbbk..kbBk....",
    "......kbbk...kkggggkk...kbbk.....",
    "......kbbk.............kbbk.....",
    "......kbbk.............kbbk.....",
    "......kbbk.............kbbk.....",
    "......kbbk.............kbbk.....",
    "......kbbk.............kbbk.....",
    "......kbbk.............kbbk.....",
    "......kbbk.............kbbk.....",
    "......kbbk.............kbbk.....",
    ".....kbbbbk...........kbbbbk....",
    ".....kbbbbbbkk.....kkbbbbbbk....",
    ".....kkbbbbbbkk..kkbbbbbbbk.....",
    "......kkkbbbbbbbbbbbbbbkkk......",
    "........kkkkbbbbbbbbkkkk........",
    "...........kkkbbkkkk............",
    ".............kkk................",
    "................................",
]

def render_frame(frame_idx):
    grid = [list(row) for row in BASE]
    # tail wag (left side this time)
    pattern = [
        [(15, 3), (14, 2), (13, 1), (12, 1)],
        [(14, 3), (13, 2), (12, 1)],
        [(13, 3), (12, 2), (11, 2), (10, 3)],
        [(14, 3), (13, 2), (12, 1)],
    ]
    pat = pattern[frame_idx % len(pattern)]
    for r, c in pat:
        if r < H and c < W:
            grid[r][c] = "b"
            if r-1 >= 0:
                grid[r-1][c] = "k"
            grid[r][c-1] = "k"

    # body bob (translate whole thing up/down 1px)
    bob = [0, -1, 0, 0, 1, 0, 0, -1, 0, 0][frame_idx]
    if bob != 0:
        new = [["."]*W for _ in range(H)]
        for y in range(H):
            for x in range(W):
                ny = y + bob
                if 0 <= ny < H:
                    new[ny][x] = grid[y][x]
        grid = new

    # blink
    if frame_idx % 5 == 3:
        for r in (9, 10):
            for c in (10, 11, 20, 21):
                if 0 <= c < W:
                    grid[r][c] = "k"

    # sparkles around eyes occasionally
    if frame_idx in (1, 6):
        # tiny '+' next to eyes
        for (r, c) in [(8, 13), (8, 22), (7, 13), (7, 22)]:
            if 0 <= r < H and 0 <= c < W and grid[r][c] == ".":
                grid[r][c] = "E"

    # collar shimmer
    if frame_idx in (2, 7):
        grid[14] = list(grid[14])
        for c in (12, 13, 14, 15, 16, 17, 18, 19):
            if grid[14][c] == "g":
                grid[14][c] = "G"

    return grid


def make_image(grid, scale=P, palette=PALETTE):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in palette and palette[ch][3] > 0:
                img.putpixel((x, y), palette[ch])
    return img.resize((W*scale, H*scale), Image.NEAREST)


frames = [make_image(render_frame(i)) for i in range(FRAMES)]
out_path = os.path.join(OUT, "cat2_cyan.gif")
frames[0].save(
    out_path,
    save_all=True,
    append_images=frames[1:],
    duration=110,
    loop=0,
    disposal=2,
    transparency=0,
)
print("wrote", out_path)
