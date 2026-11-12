from common import *

# paleta por reino: (principal, escuro, claro, brilho)
WHISPER = dict(wood=(86, 52, 110), wood_d=(52, 30, 72), leaf=(46, 130, 120), glow=(120, 255, 210),
               stone=(70, 74, 78), gem=(90, 235, 130), brick=(78, 84, 92), moss=(60, 120, 60))
SKY = dict(wood=(226, 232, 240), wood_d=(170, 182, 205), leaf=(120, 190, 240), glow=(255, 240, 150),
           stone=(150, 160, 182), gem=(120, 205, 255), brick=(176, 188, 214), moss=(130, 190, 120))
UMBRAL = dict(wood=(40, 32, 52), wood_d=(22, 16, 32), leaf=(120, 50, 150), glow=(190, 110, 255),
              stone=(52, 48, 64), gem=(175, 105, 255), brick=(46, 42, 62), moss=(70, 40, 100))


def planks(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            n = rng.randint(-7, 7)
            col = (cl(c["wood"][0] + n), cl(c["wood"][1] + n), cl(c["wood"][2] + n))
            if y % 4 == 3:
                col = mul(c["wood_d"], 1.0)
            seam = (x + (y // 4) * 5) % 16
            if seam == 0 and y % 4 != 3:
                col = mul(c["wood_d"], 1.1)
            im.set(x, y, col)
    return im


def log_side(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            n = rng.randint(-5, 5)
            streak = 14 if x % 4 in (0, 1) else 0
            col = mix(c["wood_d"], c["wood"], 0.35)
            im.set(x, y, (cl(col[0] - streak + n), cl(col[1] - streak + n), cl(col[2] - streak + n)))
    return im


def log_top(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            d = max(abs(x - 7.5), abs(y - 7.5))
            ring = int(d) % 2
            base = c["wood"] if ring == 0 else mix(c["wood"], c["wood_d"], 0.6)
            if d >= 7:
                base = mix(c["wood_d"], c["wood"], 0.3)
            n = rng.randint(-4, 4)
            im.set(x, y, (cl(base[0] + n), cl(base[1] + n), cl(base[2] + n)))
    return im


def leaves(c, speck=True):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            r = rng.random()
            if r < 0.18:
                continue
            n = rng.randint(-18, 18)
            col = (cl(c["leaf"][0] + n), cl(c["leaf"][1] + n), cl(c["leaf"][2] + n))
            if speck and r > 0.95:
                col = c["glow"]
            im.set(x, y, col)
    return im


def stone(c):
    im = Img(16, 16)
    noise_fill(im, c["stone"], 8)
    return im


def ore(c, base_color):
    im = Img(16, 16)
    noise_fill(im, base_color, 8)
    centers = [(3, 3), (11, 4), (6, 9), (12, 12), (2, 12)]
    for (cx, cy) in centers:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if abs(dx) + abs(dy) < 2 or rng.random() < 0.4:
                    t = rng.random()
                    im.set(cx + dx, cy + dy, mix(mul(c["gem"], 0.6), c["gem"], t))
        im.set(cx, cy, (255, 255, 255))
    return im


def gem_block(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            edge = x in (0, 15) or y in (0, 15)
            d = abs(x - 7.5) + abs(y - 7.5)
            t = 1 - d / 15.0
            col = mix(mul(c["gem"], 0.45), c["gem"], max(0, t))
            if (x + y) % 8 == 0:
                col = mix(col, (255, 255, 255), 0.35)
            if edge:
                col = mul(c["gem"], 0.4)
            n = rng.randint(-5, 5)
            im.set(x, y, (cl(col[0] + n), cl(col[1] + n), cl(col[2] + n)))
    return im


def bricks(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            n = rng.randint(-6, 6)
            col = (cl(c["brick"][0] + n), cl(c["brick"][1] + n), cl(c["brick"][2] + n))
            row = y // 4
            off = 4 if row % 2 else 0
            if y % 4 == 3 or (x + off) % 8 == 7:
                col = mul(c["brick"], 0.6)
            if rng.random() < 0.05:
                col = c["moss"]
            im.set(x, y, col)
    return im


def tablet(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            n = rng.randint(-5, 5)
            col = (cl(c["brick"][0] + n), cl(c["brick"][1] + n), cl(c["brick"][2] + n))
            if x in (0, 15) or y in (0, 15):
                col = mul(c["brick"], 0.55)
            im.set(x, y, col)
    # runas brilhantes
    runes = [(4, 3, 7, 3), (4, 5, 4, 8), (4, 8, 10, 8), (9, 5, 9, 11), (5, 11, 11, 11), (11, 4, 11, 7), (6, 6, 8, 6)]
    for (x0, y0, x1, y1) in runes:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                im.set(x, y, c["glow"])
    return im


def altar(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            n = rng.randint(-4, 4)
            col = (cl(c["brick"][0] * 0.55 + n), cl(c["brick"][1] * 0.55 + n), cl(c["brick"][2] * 0.55 + n))
            d = math.hypot(x - 7.5, y - 7.5)
            if abs(d - 6) < 0.7 or abs(d - 3) < 0.6:
                col = c["glow"]
            if abs(x - 7.5) < 0.8 or abs(y - 7.5) < 0.8:
                if d < 6:
                    col = mix(col, c["glow"], 0.7)
            im.set(x, y, col)
    return im


def cloud():
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            n = rng.randint(-8, 8)
            v = 246 + n // 2
            col = (cl(v), cl(v + 2), cl(v + 6))
            if (x // 4 + y // 4) % 2:
                col = (cl(col[0] - 8), cl(col[1] - 6), cl(col[2] - 2))
            im.set(x, y, col)
    return im


def crystal(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            n = rng.randint(-10, 10)
            d = math.hypot(x - 7.5, y - 7.5)
            col = mix(mul(c["gem"], 0.55), (255, 255, 255), max(0, 0.35 - d / 28))
            if (x - y) % 6 == 0:
                col = mix(col, (255, 255, 255), 0.35)
            im.set(x, y, (cl(col[0] + n), cl(col[1] + n), cl(col[2] + n)))
    return im


def glowcap_block(c):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            n = rng.randint(-6, 6)
            col = (cl(70 + n), cl(150 + n), cl(190 + n))
            im.set(x, y, col)
    for _ in range(9):
        cx, cy = rng.randint(1, 14), rng.randint(1, 14)
        for dx in (0, 1):
            for dy in (0, 1):
                im.set(cx + dx, cy + dy, c["glow"])
    return im


def sapling(c):
    im = Img(16, 16)
    for y in range(8, 16):
        im.set(8, y, (80, 56, 40)); im.set(7, y, (96, 66, 46))
    for (cx, cy, r) in ((8, 5, 4), (5, 8, 3), (11, 8, 3)):
        for y in range(16):
            for x in range(16):
                if math.hypot(x - cx, y - cy) <= r and rng.random() < 0.92:
                    n = rng.randint(-14, 14)
                    im.set(x, y, (cl(c["leaf"][0] + n), cl(c["leaf"][1] + n), cl(c["leaf"][2] + n)))
    im.set(8, 4, c["glow"]); im.set(5, 8, c["glow"])
    return im


def flower(petal, center, stem=(50, 130, 60)):
    im = Img(16, 16)
    for y in range(7, 16):
        im.set(8, y, stem)
    im.set(7, 12, stem); im.set(6, 11, stem); im.set(9, 10, stem); im.set(10, 9, stem)
    for (dx, dy) in ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)):
        im.set(8 + dx * 2, 5 + dy * 2, petal)
        im.set(8 + dx, 5 + dy, mix(petal, (255, 255, 255), 0.2))
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            im.set(8 + dx, 5 + dy, center)
    return im


def gate(c, frames=8):
    out = []
    for f in range(frames):
        im = Img(16, 16)
        for y in range(16):
            for x in range(16):
                a = math.atan2(y - 7.5, x - 7.5) + f * (2 * math.pi / frames)
                d = math.hypot(x - 7.5, y - 7.5)
                v = 0.5 + 0.5 * math.sin(d * 0.9 - a * 2 + f * 0.8)
                col = mix(mul(c["gem"], 0.35), c["glow"], v)
                alpha = 170 + int(70 * v)
                if d > 10.5:
                    alpha = 120
                im.set(x, y, (col[0], col[1], col[2], alpha))
        out.append(im)
    return out


def run():
    B = "block/"
    for realm, pal, prefix, wood in (("whisper", WHISPER, "whisper", "whisper"),
                                      ("sky", SKY, "skyroot", "skyroot"),
                                      ("umbral", UMBRAL, "gloom", "gloom")):
        planks(pal).save(f"{B}{wood}_planks.png")
        log_side(pal).save(f"{B}{wood}_log.png")
        log_top(pal).save(f"{B}{wood}_log_top.png")
        leaves(pal).save(f"{B}{wood}_leaves.png")
        sapling(pal).save(f"{B}{wood}_sapling.png")
        gem_block(pal).save(f"{B}{realm if realm != 'sky' else 'aerite'}_block_tmp.png")
    # nomes finais por reino
    gem_block(WHISPER).save(B + "verdite_block.png")
    gem_block(SKY).save(B + "aerite_block.png")
    gem_block(UMBRAL).save(B + "umbral_block.png")
    for tmp in ("whisper_block_tmp", "aerite_block_tmp", "umbral_block_tmp"):
        p = os.path.join(TEX, B + tmp + ".png")
        if os.path.exists(p):
            os.remove(p)

    ore(WHISPER, (92, 96, 100)).save(B + "verdite_ore.png")
    ore(SKY, (160, 170, 190)).save(B + "aerite_ore.png")
    ore(UMBRAL, (62, 58, 76)).save(B + "umbral_ore.png")
    bricks(WHISPER).save(B + "whisper_bricks.png")
    bricks(SKY).save(B + "sky_bricks.png")
    bricks(UMBRAL).save(B + "gloom_bricks.png")
    tablet(WHISPER).save(B + "whisper_tablet.png")
    tablet(SKY).save(B + "sky_tablet.png")
    tablet(UMBRAL).save(B + "umbral_tablet.png")
    altar(WHISPER).save(B + "whisper_altar.png")
    altar(SKY).save(B + "sky_altar.png")
    altar(UMBRAL).save(B + "umbral_altar.png")
    cloud().save(B + "cloud_block.png")
    stone(SKY).save(B + "skystone.png")
    crystal(UMBRAL).save(B + "umbral_crystal.png")
    glowcap_block(WHISPER).save(B + "glowcap_block.png")
    flower((120, 255, 230), (255, 255, 200)).save(B + "lumibloom.png")
    flower((255, 220, 70), (255, 140, 30)).save(B + "sunbloom.png")
    flower((200, 110, 255), (255, 255, 255), (60, 40, 80)).save(B + "gloomcap.png")
    save_animated(B + "whisper_gate.png", gate(dict(gem=(90, 235, 130), glow=(200, 255, 220))), 3)
    save_animated(B + "sky_gate.png", gate(dict(gem=(120, 205, 255), glow=(255, 255, 255))), 3)
    save_animated(B + "umbral_gate.png", gate(dict(gem=(175, 105, 255), glow=(255, 190, 255))), 3)
