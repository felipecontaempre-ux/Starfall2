from common import *
import math


def an(t, **k):
    d = {"type": t}
    d.update(k)
    return d


def look(f=1.0): return an("look", f=f)
def walk(phase, axis="x", amp=1.2): return an("walk", phase=phase, axis=axis, amp=amp)
def sway(axis="z", amp=0.1, speed=0.08, phase=0.0): return an("sway", axis=axis, amp=amp, speed=speed, phase=phase)
def bob(amp=1.0, speed=0.1): return an("bob", amp=amp, speed=speed)
def spin(axis="y", speed=0.1): return an("spin", axis=axis, speed=speed)
def flap(axis="z", amp=0.5, speed=0.2, phase=0.0, ps=0): return an("flap", axis=axis, amp=amp, speed=speed, phase=phase, ps=ps)
def orbit(radius, speed, idx, count, hover=2.0, ps=0): return an("orbit", radius=radius, speed=speed, idx=idx, count=count, hover=hover, ps=ps)
def arm(phase, side, raise_=0.5, swing=2.0): return an("arm", phase=phase, side=side, **{"raise": raise_}, swing=swing)


class Rig:
    def __init__(self, name):
        self.name = name
        self.parts = []
        self.decals = []

    def part(self, name, box, pivot, parent=None, rot=(0, 0, 0), color=(60, 60, 60), trim=None,
             glow=None, anim=None, grow=0.0, uv_from=None, noise=9, mirror=False):
        self.parts.append(dict(name=name, box=list(box), pivot=list(pivot), parent=parent, rot=list(rot),
                               color=color, trim=trim, glow=glow, anim=anim or [], grow=grow,
                               uv_from=uv_from, noise=noise, mirror=mirror))
        return name

    def decal(self, part, face, x, y, w, h, color, glow=False):
        self.decals.append((part, face, x, y, w, h, color, glow))


def pack(parts):
    own = [p for p in parts if not p["uv_from"]]
    dims = {p["name"]: tuple(int(math.ceil(v)) for v in p["box"][3:6]) for p in parts}
    W = 128
    for p in own:
        w, h, d = dims[p["name"]]
        if 2 * d + 2 * w > W:
            W = 256
    own.sort(key=lambda p: -(dims[p["name"]][2] + dims[p["name"]][1]))
    x = y = rowh = 0
    for p in own:
        w, h, d = dims[p["name"]]
        rw, rh = 2 * d + 2 * w, d + h
        if x + rw > W:
            x, y, rowh = 0, y + rowh, 0
        p["uv"] = (x, y)
        x += rw
        rowh = max(rowh, rh)
    H = y + rowh
    by = {p["name"]: p for p in parts}
    for p in parts:
        if p["uv_from"]:
            src = by[p["uv_from"]]
            assert dims[p["name"]] == dims[src["name"]], f"uv_from dims differ: {p['name']} vs {src['name']}"
            p["uv"] = src["uv"]
    return W, H, dims


def generate(rig):
    W, H, dims = pack(rig.parts)
    base, glow = Img(W, H), Img(W, H)
    has_glow = False
    by = {p["name"]: p for p in rig.parts}
    for p in rig.parts:
        if p["uv_from"]:
            continue
        w, h, d = dims[p["name"]]
        u, v = p["uv"]
        g = p["glow"]
        if g:
            has_glow = True
        paint_box(base, glow, u, v, w, h, d, p["color"], p["trim"], g, p["noise"])
    for (part, face, x, y, w, h, color, g) in rig.decals:
        p = by[part]
        pw, ph, pd = dims[part]
        x0, y0, x1, y1 = faces(p["uv"][0], p["uv"][1], pw, ph, pd)[face]
        for yy in range(h):
            for xx in range(w):
                px, py = x0 + x + xx, y0 + y + yy
                if px < x1 and py < y1:
                    base.set(px, py, tuple(color))
                    if g:
                        glow.set(px, py, tuple(color) + (255,))
                        has_glow = True
    base.save(f"entity/{rig.name}.png")
    if has_glow:
        glow.save(f"entity/{rig.name}_glow.png")
    out = dict(texW=W, texH=H, glow=has_glow, parts=[])
    for p in rig.parts:
        e = dict(name=p["name"], pivot=p["pivot"], rot=p["rot"], tex=list(p["uv"]), box=p["box"], anim=p["anim"])
        if p["parent"]:
            e["parent"] = p["parent"]
        if p["grow"]:
            e["grow"] = p["grow"]
        if p["mirror"]:
            e["mirror"] = True
        out["parts"].append(e)
    wj(ASSETS, f"rigs/{rig.name}.json", out)


# =============================================================== ESPINHOSO
def thornback():
    r = Rig("thornback")
    bark, bark_l, moss, thorn, eye = (84, 60, 40), (112, 82, 54), (60, 115, 52), (225, 215, 175), (150, 255, 120)
    r.part("body", (-5, -5, -8, 10, 10, 16), (0, 12, 0), color=bark)
    r.part("moss_patch", (-4, -1, -6, 8, 1, 10), (0, -5, 0), parent="body", color=moss)
    r.part("head", (-3, -3, -6, 6, 6, 6), (0, 11, -8), color=bark_l, anim=[look()])
    r.part("snout", (-2, 0, -3, 4, 3, 3), (0, 0, -6), parent="head", color=moss)
    r.part("tusk_l", (0, 0, -1, 1, 3, 1), (2, 3, -6), parent="head", color=thorn)
    r.part("tusk_r", (-1, 0, -1, 1, 3, 1), (-2, 3, -6), parent="head", color=thorn)
    for nm, x, z, ph in (("fl", -3, -6, 0), ("fr", 3, -6, 1), ("bl", -3, 6, 1), ("br", 3, 6, 0)):
        r.part(f"leg_{nm}", (-2, 0, -2, 4, 7, 4), (x, 17, z), color=bark, anim=[walk(ph)],
               uv_from=None if nm == "fl" else "leg_fl")
    for i, (x, z, rz) in enumerate([(-3, -5, -0.2), (3, -2, 0.2), (-3, 1, -0.2), (3, 4, 0.2), (0, -7, 0.0)]):
        r.part(f"spike{i}", (-1, -6, -1, 2, 6, 2), (x, -5, z), parent="body", rot=(0, 0, rz), color=thorn,
               anim=[sway("z", 0.05, 0.1, i)], uv_from=None if i == 0 else "spike0")
    r.decal("head", "front", 1, 2, 1, 1, eye, True)
    r.decal("head", "front", 4, 2, 1, 1, eye, True)
    generate(r)


# =============================================================== FOGO-FATUO
def stormwisp():
    r = Rig("stormwisp")
    white, blue, glowc = (215, 225, 250), (130, 160, 240), (150, 220, 255)
    r.part("core", (-4, -4, -4, 8, 8, 8), (0, 17, 0), color=blue, anim=[bob(1.5, 0.1), spin("y", 0.03)])
    for i in range(4):
        r.part(f"ring{i}", (-1, -1, -3, 2, 2, 6), (0, 0, 0), parent="core", color=glowc, glow=glowc,
               anim=[orbit(8, 0.08, i, 4, 2)], uv_from=None if i == 0 else "ring0")
    r.part("wing_l", (0, -6, 0, 10, 12, 1), (4, -1, 0), parent="core", color=white, trim=blue,
           anim=[flap("y", 0.6, 0.9)])
    r.part("wing_r", (-10, -6, 0, 10, 12, 1), (-4, -1, 0), parent="core", color=white, trim=blue,
           anim=[flap("y", -0.6, 0.9)])
    r.part("tail0", (-1, 0, 0, 2, 2, 5), (0, 3, 4), parent="core", color=blue, anim=[sway("x", 0.3, 0.15)])
    r.part("tail1", (-1, 0, 0, 2, 2, 5), (0, 0, 5), parent="tail0", color=white, anim=[sway("x", 0.3, 0.15, 0.6)],
           uv_from="tail0")
    r.part("tail2", (-1, 0, 0, 2, 2, 4), (0, 0, 5), parent="tail1", color=glowc, anim=[sway("x", 0.3, 0.15, 1.2)])
    r.decal("core", "front", 2, 3, 1, 2, (255, 255, 255), True)
    r.decal("core", "front", 5, 3, 1, 2, (255, 255, 255), True)
    generate(r)


# =============================================================== RASTEJANTE UMBRIO
def gloom_crawler():
    r = Rig("gloom_crawler")
    dark, purple, eyec = (32, 24, 48), (120, 60, 190), (190, 110, 255)
    r.part("abdomen", (-5, -4, -3, 10, 8, 12), (0, 17, 5), color=dark)
    r.part("thorax", (-4, -3, -4, 8, 6, 8), (0, 17, -2), color=(40, 30, 60))
    r.part("head", (-3, -3, -6, 6, 6, 6), (0, 17, -6), color=(46, 34, 70), anim=[look()])
    first = {-1: None, 1: None}
    for side in (-1, 1):
        for j, (z, yaw) in enumerate([(-3, 0.6), (-1, 0.25), (1, -0.25), (3, -0.6)]):
            name = f"leg_{'r' if side < 0 else 'l'}{j}"
            box = (-10, -1, -1, 10, 2, 2) if side < 0 else (0, -1, -1, 10, 2, 2)
            ph = (j % 2) + (1 if side > 0 else 0)
            r.part(name, box, (side * 3, 17, z), rot=(0, yaw * (1 if side < 0 else -1), -0.7 * (1 if side < 0 else -1)),
                   color=dark, anim=[walk(ph, "y", 0.5)], uv_from=first[side])
            if first[side] is None:
                first[side] = name
    for (x, y) in ((1, 1), (4, 1), (1, 3), (4, 3)):
        r.decal("head", "front", x, y, 1, 1, eyec, True)
    r.decal("abdomen", "top", 3, 3, 4, 6, purple, True)
    generate(r)


# =============================================================== CERVO-LUMINOSO
def lumistag():
    r = Rig("lumistag")
    fur, fur_l, antler, tip = (150, 108, 70), (205, 170, 130), (205, 195, 170), (140, 255, 225)
    r.part("body", (-4, -5, -8, 8, 10, 16), (0, 10, 0), color=fur)
    r.part("neck", (-2, -9, -2, 4, 10, 4), (0, -3, -7), parent="body", rot=(0.6, 0, 0), color=fur)
    r.part("head", (-2, -4, -5, 4, 4, 6), (0, -9, 0), parent="neck", rot=(-0.6, 0, 0), color=fur, anim=[look(0.8)])
    r.part("ear_l", (0, -1, -1, 3, 1, 2), (2, -3, 1), parent="head", rot=(0, 0, -0.3), color=fur_l)
    r.part("ear_r", (-3, -1, -1, 3, 1, 2), (-2, -3, 1), parent="head", rot=(0, 0, 0.3), color=fur_l)
    r.part("antler_l", (0, -8, 0, 1, 8, 1), (1, -4, 2), parent="head", rot=(0, 0, 0.35), color=antler)
    r.part("antler_r", (0, -8, 0, 1, 8, 1), (-2, -4, 2), parent="head", rot=(0, 0, -0.35), color=antler, uv_from="antler_l")
    r.part("tine_l", (0, -4, 0, 1, 4, 1), (0, -6, 0), parent="antler_l", rot=(0, 0, 0.7), color=tip, glow=tip)
    r.part("tine_r", (0, -4, 0, 1, 4, 1), (0, -6, 0), parent="antler_r", rot=(0, 0, -0.7), color=tip, glow=tip, uv_from="tine_l")
    r.part("tine2_l", (0, -3, 0, 1, 3, 1), (0, -3, 0), parent="antler_l", rot=(-0.6, 0, 0), color=tip, glow=tip)
    r.part("tine2_r", (0, -3, 0, 1, 3, 1), (0, -3, 0), parent="antler_r", rot=(-0.6, 0, 0), color=tip, glow=tip, uv_from="tine2_l")
    for nm, x, z, ph in (("fl", -3, -6, 0), ("fr", 3, -6, 1), ("bl", -3, 6, 1), ("br", 3, 6, 0)):
        r.part(f"leg_{nm}", (-1, 0, -1, 3, 10, 3), (x, 14, z), color=fur, anim=[walk(ph, "x", 1.1)],
               uv_from=None if nm == "fl" else "leg_fl")
    r.part("tail", (-1, -1, 0, 2, 3, 2), (0, -4, 8), parent="body", color=fur_l, anim=[sway("x", 0.2, 0.12)])
    for (x, z) in ((1, 2), (5, 5), (2, 9), (6, 12), (3, 14)):
        r.decal("body", "top", x, z, 1, 1, (250, 240, 225))
    for (x, y) in ((1, 2), (5, 5), (3, 8)):
        r.decal("body", "right", x + 2, y, 1, 1, (250, 240, 225))
        r.decal("body", "left", x + 2, y, 1, 1, (250, 240, 225))
    r.decal("head", "front", 0, 1, 1, 1, (30, 20, 20))
    r.decal("head", "front", 3, 1, 1, 1, (30, 20, 20))
    r.decal("head", "front", 1, 3, 2, 1, (40, 28, 24))
    generate(r)


# =============================================================== NUVENZINHA
def cloud_puff():
    r = Rig("cloud_puff")
    white, pink = (245, 248, 255), (255, 190, 205)
    r.part("body", (-5, -4, -5, 10, 8, 10), (0, 16, 0), color=white, noise=5, anim=[bob(1.0, 0.1)])
    for i, (x, y, z) in enumerate([(-3, -3, -2), (3, -3, 1), (0, -4, -3), (-2, -3, 3)]):
        r.part(f"bump{i}", (-3, -3, -3, 6, 5, 6), (x, y, z), parent="body", color=white, noise=5,
               uv_from=None if i == 0 else "bump0")
    r.part("wing_l", (0, -4, -1, 6, 5, 1), (5, -1, 0), parent="body", color=white, trim=pink, anim=[flap("z", 0.7, 0.6)])
    r.part("wing_r", (-6, -4, -1, 6, 5, 1), (-5, -1, 0), parent="body", color=white, trim=pink, anim=[flap("z", -0.7, 0.6)])
    r.part("tail", (-2, -2, 0, 4, 4, 3), (0, 0, 5), parent="body", color=white, noise=5)
    r.decal("body", "front", 2, 3, 1, 2, (40, 40, 60))
    r.decal("body", "front", 7, 3, 1, 2, (40, 40, 60))
    r.decal("body", "front", 1, 5, 2, 1, pink)
    r.decal("body", "front", 7, 5, 2, 1, pink)
    r.decal("body", "front", 4, 5, 2, 1, (255, 150, 170))
    generate(r)


# =============================================================== MOSSLING
def mossling():
    r = Rig("mossling")
    moss, moss_d, capc = (78, 140, 62), (50, 100, 44), (70, 160, 200)
    r.part("body", (-4, -3, -5, 8, 6, 9), (0, 19, 0), color=moss)
    r.part("head", (-3, -3, -3, 6, 5, 4), (0, -1, -5), parent="body", color=moss, anim=[look()])
    r.part("eye_l", (-1, -2, -1, 2, 2, 2), (2, -3, -1), parent="head", color=(255, 230, 90))
    r.part("eye_r", (-1, -2, -1, 2, 2, 2), (-2, -3, -1), parent="head", color=(255, 230, 90), uv_from="eye_l")
    r.part("leg_bl", (-1, 0, -1, 3, 3, 4), (-3, 2, 3), parent="body", color=moss_d, anim=[walk(0, "x", 0.9)])
    r.part("leg_br", (-1, 0, -1, 3, 3, 4), (3, 2, 3), parent="body", color=moss_d, anim=[walk(1, "x", 0.9)], uv_from="leg_bl")
    r.part("leg_fl", (-1, 0, -1, 2, 3, 2), (-3, 2, -3), parent="body", color=moss_d, anim=[walk(1, "x", 0.9)])
    r.part("leg_fr", (-1, 0, -1, 2, 3, 2), (3, 2, -3), parent="body", color=moss_d, anim=[walk(0, "x", 0.9)], uv_from="leg_fl")
    r.part("stem", (-1, -3, -1, 2, 3, 2), (0, -3, 1), parent="body", color=(230, 220, 190))
    r.part("cap", (-3, -2, -3, 6, 2, 6), (0, -3, 0), parent="stem", color=capc, glow=(60, 150, 180), anim=[sway("z", 0.06, 0.1)])
    r.decal("eye_l", "front", 0, 0, 1, 1, (20, 20, 20))
    r.decal("eye_r", "front", 1, 0, 1, 1, (20, 20, 20))
    generate(r)


# =============================================================== MATRIARCA DOS ESPINHOS
def thorn_matriarch():
    r = Rig("thorn_matriarch")
    bark, bark_d, bark_l = (86, 60, 40), (60, 42, 30), (118, 86, 56)
    moss, thorn, glowg = (62, 122, 52), (228, 216, 176), (140, 255, 120)
    r.part("leg_l", (-4, 0, -4, 8, 12, 8), (6, 12, 0), color=bark_d, anim=[walk(0, "x", 0.8)])
    r.part("leg_r", (-4, 0, -4, 8, 12, 8), (-6, 12, 0), color=bark_d, anim=[walk(1, "x", 0.8)], uv_from="leg_l")
    r.part("trunk", (-9, -22, -6, 18, 22, 12), (0, 12, 0), color=bark)
    r.part("moss_chest", (-6, -8, -1, 12, 8, 1), (0, -4, -6), parent="trunk", color=moss)
    r.part("core", (-2, -2, -2, 4, 4, 2), (0, -8, -7), parent="trunk", color=glowg, glow=glowg, anim=[spin("z", 0.08)])
    r.part("head", (-5, -10, -5, 10, 10, 10), (0, -22, 0), parent="trunk", color=bark_l, anim=[look(0.7)])
    for i, x in enumerate((-4, -2, 0, 2, 4)):
        r.part(f"crown{i}", (-1, -9, -1, 2, 9, 2), (x, -10, 0), parent="head", rot=(0, 0, x * 0.12), color=thorn,
               anim=[sway("z", 0.05, 0.07, i)], uv_from=None if i == 0 else "crown0")
    r.part("arm_l", (-3, -2, -3, 6, 24, 6), (12, -18, 0), parent="trunk", color=bark, anim=[arm(1, 1, 0.9, 2.4)])
    r.part("arm_r", (-3, -2, -3, 6, 24, 6), (-12, -18, 0), parent="trunk", color=bark, anim=[arm(0, -1, 0.9, 2.4)], uv_from="arm_l")
    r.part("claw_l0", (-1, 0, -1, 2, 7, 2), (-2, 22, -1), parent="arm_l", rot=(0, 0, 0.3), color=thorn)
    r.part("claw_l1", (-1, 0, -1, 2, 7, 2), (2, 22, 1), parent="arm_l", rot=(0, 0, -0.3), color=thorn, uv_from="claw_l0")
    r.part("claw_r0", (-1, 0, -1, 2, 7, 2), (-2, 22, -1), parent="arm_r", rot=(0, 0, 0.3), color=thorn, uv_from="claw_l0")
    r.part("claw_r1", (-1, 0, -1, 2, 7, 2), (2, 22, 1), parent="arm_r", rot=(0, 0, -0.3), color=thorn, uv_from="claw_l0")
    for i, (x, z) in enumerate([(-9, 4), (9, 4), (-6, 6), (6, 6)]):
        r.part(f"vine{i}", (-1, 0, -1, 2, 18, 2), (x, -20, z), parent="trunk", color=moss,
               anim=[sway("z", 0.15, 0.07, i)], uv_from=None if i == 0 else "vine0")
    for i in range(5):
        r.part(f"spore{i}", (-2, -2, -2, 4, 4, 4), (0, -14, 0), parent="trunk", color=glowg, glow=glowg,
               anim=[orbit(16, 0.04, i, 5, 3, 1)], uv_from=None if i == 0 else "spore0")
    r.decal("head", "front", 2, 4, 2, 2, glowg, True)
    r.decal("head", "front", 6, 4, 2, 2, glowg, True)
    r.decal("head", "front", 3, 7, 4, 1, (20, 12, 8))
    r.decal("trunk", "front", 9, 3, 1, 16, glowg, True)
    r.decal("trunk", "front", 6, 8, 3, 1, glowg, True)
    r.decal("trunk", "front", 10, 13, 3, 1, glowg, True)
    generate(r)


# =============================================================== SOBERANO DA TEMPESTADE
def storm_sovereign():
    r = Rig("storm_sovereign")
    plum, plum_d, gold, elec = (210, 220, 240), (150, 170, 215), (240, 205, 90), (255, 240, 120)
    r.part("body", (-6, -6, -10, 12, 12, 20), (0, 12, 0), color=plum, trim=plum_d, anim=[bob(1.5, 0.1)])
    r.part("neck", (-3, -8, -3, 6, 8, 6), (0, -2, -10), parent="body", rot=(0.5, 0, 0), color=plum)
    r.part("head", (-4, -4, -6, 8, 8, 8), (0, -8, 0), parent="neck", rot=(-0.5, 0, 0), color=plum, anim=[look(0.8)])
    r.part("beak", (-2, -1, -5, 4, 2, 5), (0, 1, -6), parent="head", color=gold)
    for i, x in enumerate((-2, 0, 2)):
        r.part(f"crest{i}", (-1, -8, -1, 2, 8, 2), (x, -4, 0), parent="head", rot=(-0.6, 0, x * 0.15), color=elec, glow=elec,
               uv_from=None if i == 0 else "crest0")
    r.part("wing_l_in", (0, -1, -5, 14, 2, 12), (6, -4, 0), parent="body", color=plum, trim=plum_d, anim=[flap("z", 0.45, 0.11, 0, 1)])
    r.part("wing_l_out", (0, -1, -4, 16, 1, 10), (14, 0, 0), parent="wing_l_in", color=plum_d, trim=elec, anim=[flap("z", 0.35, 0.11, 0.7, 1)])
    r.part("wing_r_in", (-14, -1, -5, 14, 2, 12), (-6, -4, 0), parent="body", color=plum, trim=plum_d, anim=[flap("z", -0.45, 0.11, 0, 1)])
    r.part("wing_r_out", (-16, -1, -4, 16, 1, 10), (-14, 0, 0), parent="wing_r_in", color=plum_d, trim=elec, anim=[flap("z", -0.35, 0.11, 0.7, 1)])
    r.part("tail", (-3, -1, 0, 6, 2, 8), (0, 0, 10), parent="body", color=plum_d, anim=[sway("x", 0.1, 0.09)])
    for i, (x, ry) in enumerate(((-3, 0.3), (0, 0.0), (3, -0.3))):
        r.part(f"tail_f{i}", (-1, -1, 0, 2, 1, 12), (x, 0, 8), parent="tail", rot=(0, ry, 0), color=gold,
               uv_from=None if i == 0 else "tail_f0")
    r.part("leg_l", (-1, 0, -1, 2, 6, 2), (3, 6, -2), parent="body", rot=(0.3, 0, 0), color=gold)
    r.part("leg_r", (-1, 0, -1, 2, 6, 2), (-3, 6, -2), parent="body", rot=(0.3, 0, 0), color=gold, uv_from="leg_l")
    for i in range(4):
        r.part(f"halo{i}", (-1, -1, -4, 2, 2, 8), (0, -2, 0), parent="body", color=elec, glow=elec,
               anim=[orbit(16, 0.06, i, 4, 2, 1)], uv_from=None if i == 0 else "halo0")
    r.decal("head", "front", 1, 3, 2, 1, elec, True)
    r.decal("head", "front", 5, 3, 2, 1, elec, True)
    r.decal("body", "top", 5, 4, 2, 12, elec, True)
    generate(r)


# =============================================================== REI UMBRIO
def gloom_king():
    r = Rig("gloom_king")
    armor, armor_l, trimc = (40, 36, 60), (60, 54, 92), (110, 80, 190)
    bone, gold, soul, purple = (228, 222, 208), (150, 120, 60), (150, 255, 230), (175, 100, 255)
    r.part("leg_l", (-3, 0, -3, 6, 12, 6), (5, 12, 0), color=armor, trim=trimc, anim=[walk(0, "x", 0.9)])
    r.part("leg_r", (-3, 0, -3, 6, 12, 6), (-5, 12, 0), color=armor, trim=trimc, anim=[walk(1, "x", 0.9)], uv_from="leg_l")
    r.part("torso", (-8, -16, -5, 16, 16, 10), (0, 12, 0), color=armor_l, trim=trimc)
    r.part("plate", (-7, -7, -1, 14, 12, 1), (0, -8, -5), parent="torso", color=armor, trim=trimc)
    r.part("gem", (-2, -2, -1, 4, 4, 1), (0, -8, -6), parent="torso", color=purple, glow=purple)
    r.part("head", (-4, -8, -4, 8, 8, 8), (0, -16, 0), parent="torso", color=armor, trim=trimc, anim=[look(0.8)])
    for i, x in enumerate((-3, -1.5, 0, 1.5, 3)):
        r.part(f"crown{i}", (-1, -6, -1, 2, 6, 2), (x, -8, 0), parent="head", color=gold, uv_from=None if i == 0 else "crown0")
    r.part("horn_l", (-1, -8, -1, 2, 8, 2), (4, -6, 0), parent="head", rot=(0, 0, 0.6), color=bone)
    r.part("horn_r", (-1, -8, -1, 2, 8, 2), (-4, -6, 0), parent="head", rot=(0, 0, -0.6), color=bone, uv_from="horn_l")
    r.part("arm_l", (-3, -2, -3, 6, 18, 6), (11, -14, 0), parent="torso", color=armor, trim=trimc, anim=[arm(1, 1, 0.7, 2.2)])
    r.part("arm_r", (-3, -2, -3, 6, 18, 6), (-11, -14, 0), parent="torso", color=armor, trim=trimc, anim=[arm(0, -1, 1.1, 2.2)], uv_from="arm_l")
    r.part("pauld_l", (-4, -3, -4, 8, 3, 8), (0, -2, 0), parent="arm_l", color=armor_l, trim=gold)
    r.part("pauld_r", (-4, -3, -4, 8, 3, 8), (0, -2, 0), parent="arm_r", color=armor_l, trim=gold, uv_from="pauld_l")
    r.part("guard", (-4, -1, -1, 8, 2, 2), (0, 19, 0), parent="arm_r", color=gold)
    r.part("blade", (-1, 0, -1, 2, 28, 2), (0, 19, 0), parent="arm_r", rot=(-1.57, 0, 0), color=(120, 100, 190), glow=(150, 100, 255))
    r.part("cape", (-8, 0, 0, 16, 24, 1), (0, -16, 5), parent="torso", color=(52, 26, 86), trim=trimc, anim=[sway("x", 0.12, 0.08)])
    for i in range(3):
        r.part(f"soul{i}", (-2, -2, -2, 4, 4, 4), (0, -6, 0), parent="torso", color=soul, glow=soul,
               anim=[orbit(15, 0.05, i, 3, 3, 1)], uv_from=None if i == 0 else "soul0")
    r.decal("head", "front", 1, 3, 2, 1, soul, True)
    r.decal("head", "front", 5, 3, 2, 1, soul, True)
    r.decal("plate", "front", 6, 1, 2, 10, purple, True)
    r.decal("plate", "front", 2, 5, 10, 2, purple, True)
    generate(r)


# =============================================================== AURELION
def aurelion():
    r = Rig("aurelion")
    ga, gd, gt, white, star = (238, 226, 188), (200, 160, 70), (255, 205, 80), (250, 246, 230), (255, 235, 130)
    r.part("leg_l", (-3, 0, -3, 6, 12, 6), (5, 12, 0), color=ga, trim=gt, anim=[walk(0, "x", 0.9)])
    r.part("leg_r", (-3, 0, -3, 6, 12, 6), (-5, 12, 0), color=ga, trim=gt, anim=[walk(1, "x", 0.9)], uv_from="leg_l")
    r.part("torso", (-8, -16, -5, 16, 16, 10), (0, 12, 0), color=white, trim=gt)
    r.part("plate", (-7, -7, -1, 14, 12, 1), (0, -8, -5), parent="torso", color=gd, trim=gt)
    r.part("core", (-3, -3, -1, 6, 6, 1), (0, -8, -6), parent="torso", color=star, glow=star, anim=[spin("z", 0.1)])
    r.part("head", (-4, -8, -4, 8, 8, 8), (0, -16, 0), parent="torso", color=ga, trim=gt, anim=[look(0.8)])
    for i, x in enumerate((-3, -1, 1, 3)):
        r.part(f"ray{i}", (-1, -9, 0, 2, 9, 1), (x, -8, 0), parent="head", rot=(0, 0, x * 0.18), color=star, glow=star,
               uv_from=None if i == 0 else "ray0")
    r.part("arm_l", (-3, -2, -3, 6, 18, 6), (11, -14, 0), parent="torso", color=ga, trim=gt, anim=[arm(1, 1, 0.7, 2.2)])
    r.part("arm_r", (-3, -2, -3, 6, 18, 6), (-11, -14, 0), parent="torso", color=ga, trim=gt, anim=[arm(0, -1, 1.1, 2.2)], uv_from="arm_l")
    r.part("pauld_l", (-4, -3, -4, 8, 3, 8), (0, -2, 0), parent="arm_l", color=gt, trim=gd)
    r.part("pauld_r", (-4, -3, -4, 8, 3, 8), (0, -2, 0), parent="arm_r", color=gt, trim=gd, uv_from="pauld_l")
    r.part("guard", (-5, -1, -1, 10, 2, 2), (0, 19, 0), parent="arm_r", color=gt)
    r.part("blade", (-1, 0, -1, 2, 34, 2), (0, 19, 0), parent="arm_r", rot=(-1.57, 0, 0), color=(255, 248, 210), glow=(255, 225, 120))
    for i, ln in enumerate((20, 17, 14)):
        r.part(f"wing_l{i}", (0, -1, -1, ln, 2, 3), (4, -12 + i * 3, 5), parent="torso", rot=(0, -(0.5 + 0.15 * i), 0),
               color=white, trim=gt, anim=[flap("z", 0.22, 0.1, i * 0.35, 1)])
        r.part(f"wing_r{i}", (-ln, -1, -1, ln, 2, 3), (-4, -12 + i * 3, 5), parent="torso", rot=(0, 0.5 + 0.15 * i, 0),
               color=white, trim=gt, anim=[flap("z", -0.22, 0.1, i * 0.35, 1)], uv_from=f"wing_l{i}")
    for i in range(8):
        r.part(f"star{i}", (-2, -2, -2, 4, 4, 4), (0, -28, 0), parent="torso", color=star, glow=star,
               anim=[orbit(12, 0.05, i, 8, 2, 1)], uv_from=None if i == 0 else "star0")
    r.decal("head", "front", 1, 3, 2, 1, (255, 255, 255), True)
    r.decal("head", "front", 5, 3, 2, 1, (255, 255, 255), True)
    r.decal("plate", "front", 6, 1, 2, 10, star, True)
    r.decal("plate", "front", 2, 5, 10, 2, star, True)
    generate(r)


# =============================================================== LOREKEEPER (pele de aldeao 64x64)
def lorekeeper():
    base = Img(64, 64)
    skin, purple, purple_d, gold = (222, 172, 134), (92, 60, 164), (62, 40, 112), (240, 200, 90)
    paint_box(base, None, 0, 0, 8, 10, 8, skin)                      # cabeca
    paint_box(base, None, 32, 0, 8, 10, 8, purple, gold)             # chapeu
    paint_box(base, None, 30, 47, 16, 16, 1, purple_d, gold)         # aba do chapeu
    paint_box(base, None, 24, 0, 2, 4, 2, (200, 148, 112))           # nariz
    paint_box(base, None, 16, 20, 8, 12, 6, (70, 46, 120))           # corpo
    paint_box(base, None, 0, 38, 8, 18, 6, purple, gold)             # manto
    paint_box(base, None, 44, 22, 4, 8, 4, purple_d)                 # bracos
    paint_box(base, None, 40, 38, 8, 4, 4, purple_d, gold)           # bracos cruzados
    paint_box(base, None, 0, 22, 4, 12, 4, (46, 32, 82))             # pernas
    x0, y0, _, _ = faces(0, 0, 8, 10, 8)["front"]
    for (x, y, w, c) in ((1, 4, 2, (245, 245, 245)), (5, 4, 2, (245, 245, 245))):
        for xx in range(w):
            base.set(x0 + x + xx, y0 + y, c)
    for (x, y) in ((2, 4), (6, 4)):
        base.set(x0 + x, y0 + y, (60, 40, 120))
    for y in range(7, 10):                                           # barba
        for x in range(1, 7):
            base.set(x0 + x, y0 + y, (200, 200, 212))
    rx0, ry0, _, _ = faces(0, 38, 8, 18, 6)["front"]                 # estrela no manto
    for (x, y) in ((3, 4), (4, 4), (3, 5), (4, 5), (2, 5), (5, 5), (3, 3), (4, 3), (3, 6), (4, 6)):
        base.set(rx0 + x, ry0 + y, gold)
    base.save("entity/lorekeeper.png")


def run():
    for fn in (thornback, stormwisp, gloom_crawler, lumistag, cloud_puff, mossling,
               thorn_matriarch, storm_sovereign, gloom_king, aurelion, lorekeeper):
        fn()
