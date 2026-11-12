import os, json, math, random, struct, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, "..", "..", "src", "main", "resources"))
ASSETS = os.path.join(RES, "assets", "starfall")
DATA = os.path.join(RES, "data", "starfall")
MCDATA = os.path.join(RES, "data", "minecraft")
TEX = os.path.join(ASSETS, "textures")
MOD = "starfall"
rng = random.Random(2026)


def cl(v):
    return max(0, min(255, int(v)))


def mul(c, f):
    return (cl(c[0] * f), cl(c[1] * f), cl(c[2] * f))


def mix(a, b, t):
    return (cl(a[0] + (b[0] - a[0]) * t), cl(a[1] + (b[1] - a[1]) * t), cl(a[2] + (b[2] - a[2]) * t))


class Img:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = [[(0, 0, 0, 0)] * w for _ in range(h)]

    def set(self, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = tuple(c) if len(c) == 4 else (c[0], c[1], c[2], 255)

    def get(self, x, y):
        return self.px[y][x]

    def fill(self, c):
        for y in range(self.h):
            for x in range(self.w):
                self.px[y][x] = tuple(c) if len(c) == 4 else (c[0], c[1], c[2], 255)

    def encode(self):
        raw = b"".join(b"\x00" + bytes(v for p in row for v in p) for row in self.px)

        def chunk(t, d):
            c = struct.pack(">I", len(d)) + t + d
            return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

        return (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw, 9))
                + chunk(b"IEND", b""))

    def save(self, rel, root=None):
        path = os.path.join(root or TEX, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(self.encode())


def save_animated(rel, frames, frametime=3):
    """Textura animada: tira vertical de frames 16x16 + .mcmeta."""
    h = len(frames) * 16
    strip = Img(16, h)
    for i, fr in enumerate(frames):
        for y in range(16):
            for x in range(16):
                strip.px[i * 16 + y][x] = fr.px[y][x]
    strip.save(rel)
    with open(os.path.join(TEX, rel + ".mcmeta"), "w") as f:
        json.dump({"animation": {"frametime": frametime, "interpolate": True}}, f)


def faces(u, v, w, h, d):
    return {
        "top": (u + d, v, u + d + w, v + d),
        "bottom": (u + d + w, v, u + d + 2 * w, v + d),
        "right": (u, v + d, u + d, v + d + h),
        "front": (u + d, v + d, u + d + w, v + d + h),
        "left": (u + d + w, v + d, u + 2 * d + w, v + d + h),
        "back": (u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h),
    }


def paint_box(base, glow, u, v, w, h, d, color, trim=None, glow_all=None, noise=9):
    for name, (x0, y0, x1, y1) in faces(u, v, w, h, d).items():
        f = 1.2 if name == "top" else 0.65 if name == "bottom" else 1.0
        for y in range(y0, y1):
            for x in range(x0, x1):
                n = rng.randint(-noise, noise)
                c = tuple(cl(ch * f + n) for ch in color)
                if trim and (x in (x0, x1 - 1) or y in (y0, y1 - 1)):
                    c = tuple(trim)
                base.set(x, y, c)
                if glow_all and glow is not None:
                    glow.set(x, y, tuple(glow_all) + (255,))


def wj(root, rel, data):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def A(rel, data): wj(ASSETS, rel, data)
def D(rel, data): wj(DATA, rel, data)
def MC(rel, data): wj(MCDATA, rel, data)
def m(name): return f"{MOD}:{name}"


def noise_fill(img, base, var=8, x0=0, y0=0, x1=None, y1=None):
    x1 = img.w if x1 is None else x1
    y1 = img.h if y1 is None else y1
    for y in range(y0, y1):
        for x in range(x0, x1):
            n = rng.randint(-var, var)
            img.set(x, y, (cl(base[0] + n), cl(base[1] + n), cl(base[2] + n)))
