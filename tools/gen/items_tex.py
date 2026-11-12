from common import *

PAL = {
    "verdite": dict(b=(70, 200, 100), a=(160, 255, 180), c=(30, 110, 60), o=(14, 50, 28)),
    "aerite": dict(b=(110, 190, 245), a=(215, 242, 255), c=(50, 110, 190), o=(22, 48, 100)),
    "umbral": dict(b=(130, 80, 210), a=(195, 155, 255), c=(60, 30, 120), o=(24, 12, 54)),
    "star": dict(b=(255, 205, 80), a=(255, 245, 190), c=(200, 140, 30), o=(110, 70, 10)),
}
HANDLE = (122, 86, 52)
HANDLE_D = (80, 54, 32)


def pts(im, points, col):
    for (x, y) in points:
        im.set(x, y, col)


# ------------------------------------------------------------------ ferramentas
def handle(im):
    for i, (x, y) in enumerate([(2, 13), (3, 12), (4, 11), (5, 10), (6, 9), (7, 8), (8, 7), (9, 6), (10, 5), (11, 4)]):
        im.set(x, y, HANDLE if i % 2 == 0 else HANDLE_D)


def head_pixels(im, points, p):
    for (x, y) in points:
        im.set(x, y, p["b"])
    for (x, y) in points:
        if (x, y - 1) not in points or (x - 1, y) not in points:
            im.set(x, y, p["a"])
        elif (x + 1, y) not in points or (x, y + 1) not in points:
            im.set(x, y, p["c"])


def tool(kind, p):
    im = Img(16, 16)
    if kind == "sword":
        for i in range(0, 101):
            t = i / 100.0
            x, y = int(round(5 + 9 * t)), int(round(10 - 9 * t))
            im.set(x, y, p["b"]); im.set(x + 1, y, p["c"]); im.set(x, y - 1, p["a"])
        for (x, y) in [(3, 8), (4, 9), (5, 10), (6, 11), (7, 12)]:
            im.set(x, y, (200, 170, 70))
        for (x, y) in [(2, 13), (3, 12), (4, 11)]:
            im.set(x, y, HANDLE)
        im.set(1, 14, (200, 170, 70))
        return im
    handle(im)
    if kind == "pickaxe":
        pts_ = [(4, 5), (5, 4), (6, 3), (7, 3), (8, 2), (9, 2), (10, 2), (11, 3), (12, 3), (13, 4), (13, 5), (14, 6),
                (5, 5), (6, 4), (7, 4), (8, 3), (9, 3), (10, 3), (11, 4), (12, 4), (13, 6)]
    elif kind == "axe":
        pts_ = [(9, 2), (10, 2), (11, 2), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (8, 4), (9, 4), (10, 4),
                (12, 4), (13, 4), (9, 5), (10, 5), (12, 5)]
    elif kind == "shovel":
        pts_ = [(x, y) for x in range(9, 16) for y in range(0, 7)
                if ((x - 12.5) / 2.6) ** 2 + ((y - 3) / 3.2) ** 2 <= 1.0 and (x, y) != (11, 4)]
    else:  # hoe
        pts_ = [(7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (12, 4), (13, 4), (12, 5), (7, 4), (8, 4)]
    head_pixels(im, pts_, p)
    return im


# ------------------------------------------------------------------ armaduras (metade esquerda espelhada)
ARMOR = {
    "helmet": ["........", "........", "...ooooo", "..oaaabb", ".oaabbbb", ".oabbbbb", ".oabbbbb", ".oabbbbb",
               ".oabbooo", ".oabo...", ".oooo...", "........", "........", "........", "........", "........"],
    "chestplate": ["........", "..ooo...", ".oaabo..", "oaabbooo", "oabbbbbb", "oabbbbbb", ".oabbbbb", ".oabbbbb",
                   ".oabbbbb", ".oabbbbb", ".oabbbbb", ".ooooooo", "........", "........", "........", "........"],
    "leggings": ["........", "........", "..oooooo", "..oaabbb", "..oabbbb", "..oabbbb", "..oabbbb", "..oabboo",
                 "..oabbo.", "..oabbo.", "..oabbo.", "..oabbo.", "..oabbo.", "..ooooo.", "........", "........"],
    "boots": ["........", "........", "........", "........", "........", "........", "........", "..oooo..",
              "..oabo..", "..oabo..", "..oabo..", ".oabbbo.", ".oabbbbo", ".ooooooo", "........", "........"],
}


def armor(kind, p):
    im = Img(16, 16)
    col = {"o": p["o"], "a": p["a"], "b": p["b"], "c": p["c"]}
    for y, half in enumerate(ARMOR[kind]):
        right = half[::-1].replace("a", "c")
        row = half + right
        for x, ch in enumerate(row):
            if ch in col:
                im.set(x, y, col[ch])
    return im


# ------------------------------------------------------------------ itens variados
def gem(p):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            dx, dy = abs(x - 7.5), abs(y - 7.5)
            v = dx / 5.5 + dy / 7.0
            if v <= 1.0:
                col = p["b"]
                if v > 0.8:
                    col = p["o"]
                elif x < 8 and y < 8:
                    col = p["a"]
                elif x >= 8 and y >= 8:
                    col = p["c"]
                im.set(x, y, col)
    im.set(5, 5, (255, 255, 255)); im.set(6, 4, (255, 255, 255))
    return im


def shard(p, tilt=35):
    im = Img(16, 16)
    ca, sa = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            rx, ry = dx * ca + dy * sa, -dx * sa + dy * ca
            v = abs(rx) / 3.0 + abs(ry) / 7.2
            if v <= 1.0:
                col = p["o"] if v > 0.78 else mix(p["c"], p["a"], (rx + 3) / 6.0)
                im.set(x, y, col)
    im.set(9, 3, (255, 255, 255)); im.set(6, 12, (255, 255, 255))
    return im


def star_icon(p, medal=False):
    im = Img(16, 16)
    if medal:
        for y in range(16):
            for x in range(16):
                d = math.hypot(x - 7.5, y - 8.5)
                if d <= 5.5:
                    im.set(x, y, p["o"] if d > 4.6 else mix(p["c"], p["a"], 1 - d / 5.5))
        for (x, y) in [(6, 0), (7, 1), (6, 2), (9, 0), (8, 1), (9, 2)]:
            im.set(x, y, (200, 40, 40))
    for y in range(16):
        for x in range(16):
            dx, dy = abs(x - 7.5), abs(y - (8.5 if medal else 7.5))
            if (dx ** 0.6 + dy ** 0.6) ** (1 / 0.6) <= (3.0 if medal else 6.2):
                im.set(x, y, mix(p["b"], (255, 255, 255), 0.5 if dx + dy < 2 else 0.0))
    return im


def sigil(p):
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            d = math.hypot(dx, dy)
            if d <= 7.2:
                im.set(x, y, (cl(24 + rng.randint(-4, 4)), 14, cl(40 + rng.randint(-4, 4))))
            if abs(abs(dx) + abs(dy) - 5.5) < 0.6:
                im.set(x, y, p["a"])
            if d <= 2.4:
                im.set(x, y, p["b"])
            if d <= 1.2:
                im.set(x, y, (255, 255, 255))
    return im


def starheart():
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            px, py = (x - 7.5) / 6.2, -(y - 7.0) / 6.2
            v = (px * px + py * py - 1) ** 3 - px * px * py ** 3
            if v <= 0:
                t = 1 - math.hypot(px, py) / 1.3
                im.set(x, y, mix((200, 60, 50), (255, 235, 150), max(0, t)))
    for (x, y) in [(7, 6), (8, 6), (7, 7), (8, 7), (7, 5), (8, 8), (6, 6), (9, 6)]:
        im.set(x, y, (255, 255, 255))
    return im


def fluff():
    im = Img(16, 16)
    for (cx, cy, r) in ((6, 9, 4), (10, 8, 4.5), (8, 6, 3.5), (12, 10, 3)):
        for y in range(16):
            for x in range(16):
                if math.hypot(x - cx, y - cy) <= r:
                    v = 250 - int(max(0, (y - 5)) * 3) + rng.randint(-4, 4)
                    im.set(x, y, (cl(v), cl(v + 2), cl(v + 6)))
    return im


def glow_fruit():
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 9)
            if d <= 5:
                im.set(x, y, mix((40, 150, 130), (170, 255, 230), max(0, 1 - d / 5) * (1.0 if x < 8 else 0.6)))
    for (x, y) in [(8, 4), (8, 3), (9, 2), (10, 2), (7, 3), (6, 2)]:
        im.set(x, y, (60, 170, 70))
    im.set(6, 8, (255, 255, 255))
    return im


def venison(cooked):
    im = Img(16, 16)
    main = (120, 70, 40) if cooked else (200, 90, 90)
    dark = (70, 40, 24) if cooked else (140, 50, 56)
    for y in range(16):
        for x in range(16):
            dx, dy = (x - 8) / 5.5, (y - 8) / 4.2
            if dx * dx + dy * dy <= 1:
                im.set(x, y, mix(dark, main, 0.5 + 0.5 * (1 - (x + y) / 28.0)))
    for (x, y) in [(11, 11), (12, 12), (13, 13), (14, 13), (13, 14)]:
        im.set(x, y, (240, 235, 220))
    return im


def pie():
    im = Img(16, 16)
    for y in range(16):
        for x in range(16):
            dx, dy = (x - 7.5) / 7, (y - 9) / 4.5
            if dx * dx + dy * dy <= 1:
                top = y < 9
                im.set(x, y, (240, 242, 255) if top else (190, 140, 90))
    for (x, y) in [(5, 7), (8, 6), (10, 8), (7, 9)]:
        im.set(x, y, (255, 200, 90))
    for x in range(1, 15):
        im.set(x, 12, (150, 100, 60))
    return im


def staff(kind):
    im = Img(16, 16)
    handle(im)
    for (x, y) in [(12, 3), (11, 3)]:
        im.set(x, y, HANDLE)
    if kind == "verdant":
        for y in range(16):
            for x in range(16):
                if math.hypot(x - 12.5, y - 3.5) <= 2.8:
                    im.set(x, y, mix((40, 150, 70), (200, 255, 190), max(0, 1 - math.hypot(x - 12, y - 3) / 3)))
        pts(im, [(9, 2), (10, 1), (14, 6), (15, 7)], (80, 200, 100))
    else:
        for (x, y) in [(10, 2), (11, 1), (12, 1), (13, 2), (14, 3), (13, 4), (12, 4), (11, 3), (12, 2), (13, 3)]:
            im.set(x, y, (225, 245, 255))
        pts(im, [(10, 3), (14, 2), (15, 4)], (140, 200, 255))
    return im


def scythe(p):
    im = Img(16, 16)
    handle(im)
    arc = [(11, 4), (11, 3), (11, 2), (12, 1), (13, 1), (14, 2), (15, 3), (15, 4), (14, 5), (12, 3), (13, 2), (14, 3)]
    for (x, y) in arc:
        im.set(x, y, p["b"])
    pts(im, [(12, 1), (13, 1), (14, 2)], p["a"])
    pts(im, [(15, 4), (14, 5), (15, 3)], p["c"])
    return im


def run():
    I = "item/"
    for name, pal in (("verdite", PAL["verdite"]), ("aerite", PAL["aerite"]), ("umbral", PAL["umbral"])):
        gem(pal).save(f"{I}{name}_gem.png")
        for k in ("sword", "pickaxe", "axe", "shovel", "hoe"):
            tool(k, pal).save(f"{I}{name}_{k}.png")
        for k in ("helmet", "chestplate", "leggings", "boots"):
            armor(k, pal).save(f"{I}{name}_{k}.png")
    shard(PAL["verdite"]).save(I + "verdant_shard.png")
    shard(PAL["aerite"], 20).save(I + "tempest_shard.png")
    shard(PAL["umbral"], 50).save(I + "umbral_shard.png")
    star_icon(PAL["star"]).save(I + "star_fragment.png")
    star_icon(PAL["star"], True).save(I + "star_medal.png")
    sigil(PAL["verdite"]).save(I + "thorn_sigil.png")
    sigil(PAL["aerite"]).save(I + "storm_sigil.png")
    sigil(PAL["umbral"]).save(I + "gloom_sigil.png")
    starheart().save(I + "starheart.png")
    fluff().save(I + "cloud_fluff.png")
    glow_fruit().save(I + "glow_fruit.png")
    venison(False).save(I + "lumi_venison.png")
    venison(True).save(I + "cooked_lumi_venison.png")
    pie().save(I + "sky_pie.png")
    staff("verdant").save(I + "verdant_staff.png")
    staff("wind").save(I + "wind_staff.png")
    scythe(PAL["umbral"]).save(I + "gloom_scythe.png")
    tool("sword", PAL["star"]).save(I + "star_blade.png")
