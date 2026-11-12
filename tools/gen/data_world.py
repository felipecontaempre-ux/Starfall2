from common import *
from data_assets import MATS, TOOLS, ARMORS, WOODS, ENTITIES


def rgb(r, g, b):
    return (r << 16) | (g << 8) | b


def st(name):
    return {"Name": name}


# ===================================================================== DIMENSOES
def dimension_types():
    def dt(fixed_time, min_y, height, ambient):
        return {"ultrawarm": False, "natural": True, "coordinate_scale": 1.0, "has_skylight": True, "has_ceiling": False,
                "ambient_light": ambient, "fixed_time": fixed_time, "piglin_safe": False, "bed_works": True,
                "respawn_anchor_works": False, "has_raids": False, "logical_height": height, "min_y": min_y,
                "height": height, "infiniburn": "#minecraft:infiniburn_overworld", "effects": "minecraft:overworld",
                "monster_spawn_light_level": 7, "monster_spawn_block_light_limit": 0}
    D("dimension_type/whisperwood.json", dt(13500, -64, 384, 0.12))
    D("dimension_type/skyreach.json", dt(6000, 0, 256, 0.25))
    D("dimension_type/umbral.json", dt(18000, -64, 384, 0.02))


def multi_noise(entries):
    return {"type": "minecraft:multi_noise", "biomes": [
        {"biome": m(b), "parameters": {"temperature": [-2.0, 2.0], "humidity": h, "continentalness": [-2.0, 2.0],
                                       "erosion": [-2.0, 2.0], "depth": [-2.0, 2.0], "weirdness": [-2.0, 2.0],
                                       "offset": 0.0}} for b, h in entries]}


def dimensions():
    D("dimension/whisperwood.json", {"type": m("whisperwood"), "generator": {
        "type": "minecraft:noise", "settings": "minecraft:overworld",
        "biome_source": multi_noise([("whisper_forest", [-2.0, -0.15]), ("glowcap_grove", [-0.15, 0.35]),
                                     ("mist_marsh", [0.35, 2.0])])}})
    D("dimension/skyreach.json", {"type": m("skyreach"), "generator": {
        "type": "minecraft:noise", "settings": "minecraft:floating_islands",
        "biome_source": multi_noise([("cloud_meadows", [-2.0, 0.2]), ("storm_heights", [0.2, 2.0])])}})
    D("dimension/umbral.json", {"type": m("umbral"), "generator": {
        "type": "minecraft:noise", "settings": "minecraft:overworld",
        "biome_source": multi_noise([("umbral_wastes", [-2.0, 0.1]), ("crystal_caverns", [0.1, 2.0])])}})


# ===================================================================== BIOMAS
VANILLA_ORES = ["minecraft:ore_coal_upper", "minecraft:ore_iron_upper", "minecraft:ore_iron_middle", "minecraft:ore_gold",
                "minecraft:ore_redstone", "minecraft:ore_diamond", "minecraft:ore_lapis", "minecraft:ore_copper"]


# Ordem mestra: o Minecraft exige ordem consistente das features entre os biomas de uma dimensao.
MASTER = {
    0: [m("sky_paint")],
    4: [m(n) for n in ("whisper_ruin", "whisper_arena", "sky_ruin", "sky_arena", "umbral_ruin", "umbral_arena")],
    6: VANILLA_ORES + [m(n) for n in ("verdite_ore", "aerite_ore", "umbral_ore", "umbral_crystal_veins", "umbral_crystal_dense")],
    9: [m("cloud_clumps"), m("whisper_trees"), m("whisper_trees_sparse"), m("glowcap_trees"), m("glowcap_trees_few"),
        m("skyroot_trees"), m("gloom_trees"), m("lumibloom_patch"), m("sunbloom_patch"), m("gloomcap_patch"),
        "minecraft:patch_grass_forest", "minecraft:patch_grass_plain", "minecraft:patch_tall_grass_2",
        "minecraft:red_mushroom_normal", "minecraft:brown_mushroom_normal"],
}


def biome(name, temp, sky, fog, water, water_fog, grass, foliage, steps, monsters, creatures, particle=None, carvers=True):
    features = [[] for _ in range(11)]
    for step, lst in steps.items():
        assert len(set(lst)) == len(lst), f"feature duplicada em {name} etapa {step}"
        features[step] = sorted(lst, key=MASTER[step].index)
    eff = {"sky_color": sky, "fog_color": fog, "water_color": water, "water_fog_color": water_fog,
           "grass_color": grass, "foliage_color": foliage}
    if particle:
        eff["particle"] = {"probability": 0.005, "options": {"type": particle}}
    D(f"worldgen/biome/{name}.json", {
        "temperature": temp, "downfall": 0.4, "has_precipitation": False, "effects": eff,
        "spawners": {"monster": monsters, "creature": creatures, "ambient": [], "axolotls": [],
                     "underground_water_creature": [], "water_creature": [], "water_ambient": [], "misc": []},
        "spawn_costs": {}, "creature_spawn_probability": 0.12,
        "carvers": {"air": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"] if carvers else []},
        "features": features})


def spawn(t, w, lo, hi):
    return {"type": m(t), "weight": w, "minCount": lo, "maxCount": hi}


def biomes():
    # Bosque Sussurrante
    common = {4: [m("whisper_ruin"), m("whisper_arena")], 6: VANILLA_ORES + [m("verdite_ore")]}
    biome("whisper_forest", 0.6, rgb(90, 58, 140), rgb(120, 90, 160), rgb(70, 120, 180), rgb(30, 50, 90),
          rgb(70, 160, 120), rgb(60, 170, 140),
          {**common, 9: [m("whisper_trees"), m("lumibloom_patch"), "minecraft:patch_grass_forest",
                         "minecraft:patch_tall_grass_2", "minecraft:brown_mushroom_normal", m("glowcap_trees_few")]},
          [spawn("thornback", 60, 1, 3)], [spawn("lumistag", 14, 2, 4), spawn("mossling", 10, 1, 2)])
    biome("glowcap_grove", 0.7, rgb(70, 50, 150), rgb(90, 80, 170), rgb(70, 130, 190), rgb(30, 60, 100),
          rgb(60, 180, 150), rgb(70, 200, 170),
          {**common, 9: [m("glowcap_trees"), m("whisper_trees_sparse"), m("lumibloom_patch"),
                         "minecraft:red_mushroom_normal", "minecraft:brown_mushroom_normal", "minecraft:patch_grass_forest"]},
          [spawn("thornback", 40, 1, 2)], [spawn("lumistag", 12, 2, 3), spawn("mossling", 16, 1, 3)])
    biome("mist_marsh", 0.8, rgb(100, 90, 150), rgb(150, 150, 190), rgb(70, 110, 150), rgb(40, 70, 90),
          rgb(60, 110, 100), rgb(50, 120, 110),
          {**common, 9: [m("whisper_trees_sparse"), m("lumibloom_patch"), "minecraft:patch_grass_plain",
                         "minecraft:brown_mushroom_normal"]},
          [spawn("thornback", 50, 1, 3)], [spawn("mossling", 14, 1, 2)])
    # Cumes do Ceu
    sky_common = {0: [m("sky_paint")], 4: [m("sky_ruin"), m("sky_arena")], 6: [m("aerite_ore")]}
    biome("cloud_meadows", 0.7, rgb(120, 190, 255), rgb(220, 235, 255), rgb(80, 160, 255), rgb(30, 80, 160),
          rgb(120, 210, 110), rgb(110, 200, 140),
          {**sky_common, 9: [m("cloud_clumps"), m("skyroot_trees"), m("sunbloom_patch"),
                             "minecraft:patch_grass_plain", "minecraft:patch_tall_grass_2"]},
          [spawn("stormwisp", 20, 1, 2)], [spawn("cloud_puff", 22, 2, 4)], carvers=False)
    biome("storm_heights", 0.4, rgb(90, 110, 160), rgb(160, 175, 205), rgb(70, 130, 220), rgb(30, 60, 130),
          rgb(100, 180, 120), rgb(90, 170, 150),
          {**sky_common, 9: [m("cloud_clumps"), m("skyroot_trees"), "minecraft:patch_grass_plain"]},
          [spawn("stormwisp", 55, 1, 3)], [spawn("cloud_puff", 8, 1, 3)], carvers=False)
    # Reino Umbrio
    um_common = {4: [m("umbral_ruin"), m("umbral_arena")], 6: VANILLA_ORES + [m("umbral_ore"), m("umbral_crystal_veins")]}
    biome("umbral_wastes", 0.3, rgb(20, 12, 40), rgb(40, 24, 70), rgb(60, 40, 110), rgb(20, 10, 40),
          rgb(80, 56, 110), rgb(120, 66, 150),
          {**um_common, 9: [m("gloom_trees"), m("gloomcap_patch"), "minecraft:patch_grass_plain"]},
          [spawn("gloom_crawler", 80, 1, 3)], [], particle="minecraft:ash")
    biome("crystal_caverns", 0.2, rgb(30, 14, 56), rgb(54, 30, 90), rgb(80, 50, 140), rgb(24, 12, 50),
          rgb(90, 60, 130), rgb(140, 70, 170),
          {**um_common, 6: VANILLA_ORES + [m("umbral_ore"), m("umbral_crystal_veins"), m("umbral_crystal_dense")],
           9: [m("gloom_trees"), m("gloomcap_patch")]},
          [spawn("gloom_crawler", 100, 2, 4)], [], particle="minecraft:ash")


# ===================================================================== FEATURES
def tree(trunk, foliage, trunk_placer, foliage_placer, size, trunk_state=None):
    return {"type": "minecraft:tree", "config": {
        "ignore_vines": True, "force_dirt": False, "minimum_size": size,
        "dirt_provider": {"type": "minecraft:simple_state_provider", "state": st("minecraft:dirt")},
        "trunk_provider": {"type": "minecraft:simple_state_provider", "state": trunk_state or st(trunk)},
        "foliage_provider": {"type": "minecraft:simple_state_provider", "state": st(foliage)},
        "trunk_placer": trunk_placer, "foliage_placer": foliage_placer, "decorators": []}}


SIZE1 = {"type": "minecraft:two_layers_feature_size", "limit": 1, "lower_size": 0, "upper_size": 1}
SIZE0 = {"type": "minecraft:two_layers_feature_size", "limit": 0, "lower_size": 0, "upper_size": 0}


def patch(block, tries=24):
    return {"type": "minecraft:random_patch", "config": {
        "tries": tries, "xz_spread": 6, "y_spread": 2,
        "feature": {"feature": {"type": "minecraft:simple_block", "config": {
            "to_place": {"type": "minecraft:simple_state_provider", "state": st(block)}}},
            "placement": [{"type": "minecraft:block_predicate_filter",
                           "predicate": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}}]}}}


def ore_cfg(size, targets, discard=0.0):
    return {"type": "minecraft:ore", "config": {"size": size, "discard_chance_on_air_exposure": discard, "targets": targets}}


def tgt_tag(tag, block):
    return {"target": {"predicate_type": "minecraft:tag_match", "tag": tag}, "state": st(block)}


def tgt_block(src, block):
    return {"target": {"predicate_type": "minecraft:block_match", "block": src}, "state": st(block)}


def survive(sapling):
    return {"type": "minecraft:block_predicate_filter",
            "predicate": {"type": "minecraft:would_survive", "state": st(sapling)}}


def tree_placed(feature, count, extra_chance, extra_count, sapling):
    return {"feature": m(feature), "placement": [
        {"type": "minecraft:count_extra", "count": count, "extra_chance": extra_chance, "extra_count": extra_count},
        {"type": "minecraft:in_square"}, {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0},
        {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR"}, {"type": "minecraft:biome"}, survive(sapling)]}


def uniform_h(lo, hi):
    return {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform",
                                                         "min_inclusive": {"absolute": lo}, "max_inclusive": {"absolute": hi}}}


def ore_placed(feature, count, lo, hi):
    return {"feature": m(feature), "placement": [{"type": "minecraft:count", "count": count},
                                                 {"type": "minecraft:in_square"}, uniform_h(lo, hi), {"type": "minecraft:biome"}]}


def on_grass_struct(feature, rarity):
    return {"feature": m(feature), "placement": [
        {"type": "minecraft:rarity_filter", "chance": rarity}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"},
        {"type": "minecraft:block_predicate_filter", "predicate": {
            "type": "minecraft:matching_blocks", "offset": [0, -1, 0], "blocks": "minecraft:grass_block"}},
        {"type": "minecraft:biome"}]}


def patch_placed(feature, count):
    return {"feature": m(feature), "placement": [{"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
                                                 {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"},
                                                 {"type": "minecraft:biome"}]}


def features():
    CF, PF = "worldgen/configured_feature/", "worldgen/placed_feature/"
    # ---- arvores
    D(CF + "whisper_tree.json", tree("starfall:whisper_log", "starfall:whisper_leaves",
        {"type": "minecraft:fancy_trunk_placer", "base_height": 3, "height_rand_a": 11, "height_rand_b": 0},
        {"type": "minecraft:fancy_foliage_placer", "radius": 2, "offset": 4, "height": 4}, SIZE0))
    D(CF + "skyroot_tree.json", tree("starfall:skyroot_log", "starfall:skyroot_leaves",
        {"type": "minecraft:straight_trunk_placer", "base_height": 5, "height_rand_a": 2, "height_rand_b": 1},
        {"type": "minecraft:blob_foliage_placer", "radius": 2, "offset": 0, "height": 3}, SIZE1))
    D(CF + "gloom_tree.json", tree("starfall:gloom_log", "starfall:gloom_leaves",
        {"type": "minecraft:forking_trunk_placer", "base_height": 5, "height_rand_a": 2, "height_rand_b": 2},
        {"type": "minecraft:acacia_foliage_placer", "radius": 2, "offset": 0}, SIZE1))
    D(CF + "glowcap_tree.json", tree("minecraft:mushroom_stem", "starfall:glowcap_block",
        {"type": "minecraft:straight_trunk_placer", "base_height": 4, "height_rand_a": 2, "height_rand_b": 0},
        {"type": "minecraft:blob_foliage_placer", "radius": 3, "offset": 0, "height": 2}, SIZE1))
    # ---- flores
    D(CF + "lumibloom_patch.json", patch("starfall:lumibloom"))
    D(CF + "sunbloom_patch.json", patch("starfall:sunbloom"))
    D(CF + "gloomcap_patch.json", patch("starfall:gloomcap"))
    # ---- nuvens e minerios
    D(CF + "cloud_clump.json", ore_cfg(28, [tgt_block("minecraft:air", "starfall:cloud_block")]))
    D(CF + "verdite_ore.json", ore_cfg(8, [tgt_tag("minecraft:stone_ore_replaceables", "starfall:verdite_ore"),
                                           tgt_tag("minecraft:deepslate_ore_replaceables", "starfall:verdite_ore")]))
    D(CF + "umbral_ore.json", ore_cfg(7, [tgt_tag("minecraft:stone_ore_replaceables", "starfall:umbral_ore"),
                                          tgt_tag("minecraft:deepslate_ore_replaceables", "starfall:umbral_ore")]))
    D(CF + "umbral_crystal_veins.json", ore_cfg(7, [tgt_tag("minecraft:stone_ore_replaceables", "starfall:umbral_crystal"),
                                                    tgt_tag("minecraft:deepslate_ore_replaceables", "starfall:umbral_crystal")], 0.2))
    D(CF + "aerite_ore.json", ore_cfg(8, [tgt_block("starfall:skystone", "starfall:aerite_ore")]))
    D(CF + "sky_paint.json", {"type": m("sky_paint"), "config": {}})
    # ---- estruturas
    for realm, bricks, tablet, loot in (("whisper", "whisper_bricks", "whisper_tablet", "whisper_ruin"),
                                        ("sky", "sky_bricks", "sky_tablet", "sky_ruin"),
                                        ("umbral", "gloom_bricks", "umbral_tablet", "umbral_ruin")):
        D(CF + f"{realm}_ruin.json", {"type": m("ruin"), "config": {
            "wall": st(m(bricks)), "floor": st(m(bricks)), "tablet": st(m(tablet)),
            "loot": m(f"chests/{loot}"), "radius": 5}})
    D(CF + "whisper_arena.json", {"type": m("arena"), "config": {
        "floor": st(m("whisper_bricks")), "pillar": st(m("whisper_log")), "lamp": st(m("glowcap_block")),
        "altar": st(m("whisper_altar")), "radius": 11}})
    D(CF + "sky_arena.json", {"type": m("arena"), "config": {
        "floor": st(m("sky_bricks")), "pillar": st(m("sky_bricks")), "lamp": st("minecraft:glowstone"),
        "altar": st(m("sky_altar")), "radius": 11}})
    D(CF + "umbral_arena.json", {"type": m("arena"), "config": {
        "floor": st(m("gloom_bricks")), "pillar": st(m("gloom_bricks")), "lamp": st(m("umbral_crystal")),
        "altar": st(m("umbral_altar")), "radius": 11}})

    # ---- placed
    D(PF + "whisper_trees.json", tree_placed("whisper_tree", 7, 0.1, 1, "starfall:whisper_sapling"))
    D(PF + "whisper_trees_sparse.json", tree_placed("whisper_tree", 1, 0.3, 1, "starfall:whisper_sapling"))
    D(PF + "glowcap_trees.json", tree_placed("glowcap_tree", 5, 0.1, 1, "starfall:whisper_sapling"))
    D(PF + "glowcap_trees_few.json", tree_placed("glowcap_tree", 0, 0.25, 1, "starfall:whisper_sapling"))
    D(PF + "skyroot_trees.json", tree_placed("skyroot_tree", 3, 0.1, 1, "starfall:skyroot_sapling"))
    D(PF + "gloom_trees.json", tree_placed("gloom_tree", 3, 0.1, 1, "starfall:gloom_sapling"))
    D(PF + "lumibloom_patch.json", patch_placed("lumibloom_patch", 2))
    D(PF + "sunbloom_patch.json", patch_placed("sunbloom_patch", 2))
    D(PF + "gloomcap_patch.json", patch_placed("gloomcap_patch", 2))
    D(PF + "cloud_clumps.json", ore_placed("cloud_clump", 14, 70, 210))
    D(PF + "verdite_ore.json", ore_placed("verdite_ore", 16, -48, 100))
    D(PF + "umbral_ore.json", ore_placed("umbral_ore", 12, -60, 40))
    D(PF + "umbral_crystal_veins.json", ore_placed("umbral_crystal_veins", 20, -50, 90))
    D(PF + "umbral_crystal_dense.json", ore_placed("umbral_crystal_veins", 45, -50, 90))
    D(PF + "aerite_ore.json", ore_placed("aerite_ore", 20, 0, 140))
    D(PF + "sky_paint.json", {"feature": m("sky_paint"), "placement": []})
    for realm in ("whisper", "sky", "umbral"):
        D(PF + f"{realm}_ruin.json", on_grass_struct(f"{realm}_ruin", 22))
        D(PF + f"{realm}_arena.json", on_grass_struct(f"{realm}_arena", 55))


# ===================================================================== RECEITAS
def key(item):
    return {"item": item} if ":" in item else {"item": "minecraft:" + item}


def shaped(name, pattern, keys, result, count=1, cat="misc"):
    D(f"recipes/{name}.json", {"type": "minecraft:crafting_shaped", "category": cat, "pattern": pattern,
                               "key": {k: key(v) for k, v in keys.items()}, "result": {"item": m(result) if ":" not in result else result, "count": count}})


def shapeless(name, ingredients, result, count=1, cat="misc"):
    D(f"recipes/{name}.json", {"type": "minecraft:crafting_shapeless", "category": cat,
                               "ingredients": [key(i) for i in ingredients],
                               "result": {"item": m(result) if ":" not in result else result, "count": count}})


def recipes():
    for w, log in (("whisper", "whisper_log"), ("skyroot", "skyroot_log"), ("gloom", "gloom_log")):
        shapeless(f"{w}_planks", [m(log)], f"{w}_planks", 4, "building")
        shaped(f"{w}_slab", ["PPP"], {"P": m(f"{w}_planks")}, f"{w}_slab", 6, "building")
    for mat in MATS:
        g = m(f"{mat}_gem")
        shaped(f"{mat}_block", ["GGG", "GGG", "GGG"], {"G": g}, f"{mat}_block", 1, "building")
        shapeless(f"{mat}_gem_from_block", [m(f"{mat}_block")], f"{mat}_gem", 9)
        k = {"G": g, "S": "stick"}
        shaped(f"{mat}_sword", ["G", "G", "S"], k, f"{mat}_sword", 1, "equipment")
        shaped(f"{mat}_pickaxe", ["GGG", " S ", " S "], k, f"{mat}_pickaxe", 1, "equipment")
        shaped(f"{mat}_axe", ["GG", "GS", " S"], k, f"{mat}_axe", 1, "equipment")
        shaped(f"{mat}_shovel", ["G", "S", "S"], k, f"{mat}_shovel", 1, "equipment")
        shaped(f"{mat}_hoe", ["GG", " S", " S"], k, f"{mat}_hoe", 1, "equipment")
        shaped(f"{mat}_helmet", ["GGG", "G G"], {"G": g}, f"{mat}_helmet", 1, "equipment")
        shaped(f"{mat}_chestplate", ["G G", "GGG", "GGG"], {"G": g}, f"{mat}_chestplate", 1, "equipment")
        shaped(f"{mat}_leggings", ["GGG", "G G", "G G"], {"G": g}, f"{mat}_leggings", 1, "equipment")
        shaped(f"{mat}_boots", ["G G", "G G"], {"G": g}, f"{mat}_boots", 1, "equipment")
    # portais
    shaped("whisper_gate", ["VOV", "OPO", "VOV"], {"V": m("verdite_gem"), "O": "obsidian", "P": "ender_pearl"}, "whisper_gate")
    shaped("whisper_gate_from_emerald", ["EOE", "OPO", "EOE"], {"E": "emerald", "O": "obsidian", "P": "ender_pearl"}, "whisper_gate")
    shaped("sky_gate", ["AOA", "OPO", "AOA"], {"A": m("aerite_gem"), "O": "obsidian", "P": "ender_pearl"}, "sky_gate")
    shaped("umbral_gate", ["UOU", "OPO", "UOU"], {"U": m("umbral_gem"), "O": "obsidian", "P": "ender_pearl"}, "umbral_gate")
    # sigilos e coracao estelar
    shaped("thorn_sigil", ["VGV", "GEG", "VGV"], {"V": m("verdite_gem"), "G": "gold_ingot", "E": "emerald"}, "thorn_sigil")
    shaped("storm_sigil", ["AFA", "FDF", "AFA"], {"A": m("aerite_gem"), "F": m("cloud_fluff"), "D": "diamond"}, "storm_sigil")
    shaped("gloom_sigil", ["UPU", "PDP", "UPU"], {"U": m("umbral_gem"), "P": "ender_pearl", "D": "diamond"}, "gloom_sigil")
    shapeless("starheart", [m("verdant_shard"), m("tempest_shard"), m("umbral_shard"), "nether_star"], "starheart")
    # comidas / utilidades
    shaped("cloud_block", ["FF", "FF"], {"F": m("cloud_fluff")}, "cloud_block", 1, "building")
    shapeless("sky_pie", [m("cloud_fluff"), m("cloud_fluff"), "sugar", "egg", "wheat"], "sky_pie")
    for typ, t in (("smelting", 200), ("smoking", 100), ("campfire_cooking", 600)):
        D(f"recipes/cooked_lumi_venison_{typ}.json", {"type": f"minecraft:{typ}", "category": "food",
            "ingredient": {"item": m("lumi_venison")}, "result": m("cooked_lumi_venison"), "experience": 0.35, "cookingtime": t})


# ===================================================================== LOOT
SURV = [{"condition": "minecraft:survives_explosion"}]
SILK = {"condition": "minecraft:match_tool", "predicate": {"enchantments": [{"enchantment": "minecraft:silk_touch", "levels": {"min": 1}}]}}
SHEARS = {"condition": "minecraft:match_tool", "predicate": {"items": ["minecraft:shears"]}}


def count_fn(lo, hi):
    return {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": float(lo), "max": float(hi)}}


def entry(item, lo=1, hi=1, funcs=None):
    e = {"type": "minecraft:item", "name": item}
    f = []
    if (lo, hi) != (1, 1):
        f.append(count_fn(lo, hi))
    f += funcs or []
    if f:
        e["functions"] = f
    return e


def pool(entries, rolls=1.0, conds=None):
    p = {"rolls": rolls, "bonus_rolls": 0.0, "entries": entries}
    if conds:
        p["conditions"] = conds
    return p


def loot():
    LB, LE, LC = "loot_tables/blocks/", "loot_tables/entities/", "loot_tables/chests/"
    simple = [n for n in ("whisper_log", "whisper_planks", "skyroot_log", "skyroot_planks", "gloom_log", "gloom_planks",
                          "verdite_block", "aerite_block", "umbral_block", "whisper_bricks", "sky_bricks", "gloom_bricks",
                          "skystone", "cloud_block", "glowcap_block", "umbral_crystal", "whisper_tablet", "sky_tablet",
                          "umbral_tablet", "whisper_gate", "sky_gate", "umbral_gate", "whisper_sapling", "skyroot_sapling",
                          "gloom_sapling", "lumibloom", "sunbloom", "gloomcap")]
    for n in simple:
        D(LB + f"{n}.json", {"type": "minecraft:block", "pools": [pool([entry(m(n))], 1.0, SURV)]})
    for w in WOODS:
        D(LB + f"{w}_slab.json", {"type": "minecraft:block", "pools": [pool([entry(m(f"{w}_slab"), 1, 1, [
            {"function": "minecraft:set_count", "count": 2.0, "add": False, "conditions": [
                {"condition": "minecraft:block_state_property", "block": m(f"{w}_slab"), "properties": {"type": "double"}}]},
            {"function": "minecraft:explosion_decay"}])])]})
        sapling = {"whisper": "whisper_sapling", "skyroot": "skyroot_sapling", "gloom": "gloom_sapling"}[w]
        extra = [pool([entry(m("glow_fruit"))], 1.0, [{"condition": "minecraft:random_chance", "chance": 0.04}])] if w == "whisper" else []
        D(LB + f"{w}_leaves.json", {"type": "minecraft:block", "pools": [
            pool([{"type": "minecraft:alternatives", "children": [
                {"type": "minecraft:item", "name": m(f"{w}_leaves"),
                 "conditions": [{"condition": "minecraft:alternative", "terms": [SHEARS, SILK]}]},
                {"type": "minecraft:item", "name": m(sapling), "conditions": SURV + [
                    {"condition": "minecraft:table_bonus", "enchantment": "minecraft:fortune",
                     "chances": [0.05, 0.0625, 0.0833, 0.1]}]}]}]),
            pool([entry("minecraft:stick")], 1.0, [{"condition": "minecraft:random_chance", "chance": 0.1}])] + extra})
    for ore, gem in (("verdite_ore", "verdite_gem"), ("aerite_ore", "aerite_gem"), ("umbral_ore", "umbral_gem")):
        D(LB + f"{ore}.json", {"type": "minecraft:block", "pools": [pool([{"type": "minecraft:alternatives", "children": [
            {"type": "minecraft:item", "name": m(ore), "conditions": [SILK]},
            entry(m(gem), 1, 3, [{"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune",
                                  "formula": "minecraft:ore_drops"}, {"function": "minecraft:explosion_decay"}])]}])]})

    looting = {"function": "minecraft:looting_enchant", "count": {"min": 0.0, "max": 1.0}}

    def ent(pools):
        return {"type": "minecraft:entity", "pools": pools}

    D(LE + "thorn_matriarch.json", ent([pool([entry(m("verdant_shard"))]), pool([entry(m("verdant_staff"))]),
                                        pool([entry(m("verdite_gem"), 6, 10)]), pool([entry(m("glow_fruit"), 4, 8)])]))
    D(LE + "storm_sovereign.json", ent([pool([entry(m("tempest_shard"))]), pool([entry(m("wind_staff"))]),
                                        pool([entry(m("aerite_gem"), 6, 10)]), pool([entry(m("cloud_fluff"), 4, 8)])]))
    D(LE + "gloom_king.json", ent([pool([entry(m("umbral_shard"))]), pool([entry(m("gloom_scythe"))]),
                                   pool([entry(m("umbral_gem"), 6, 10)])]))
    D(LE + "aurelion.json", ent([pool([entry(m("star_fragment"))]), pool([entry(m("star_blade"))]),
                                 pool([entry("minecraft:nether_star")]), pool([entry("minecraft:diamond", 8, 14)])]))
    D(LE + "thornback.json", ent([pool([entry("minecraft:stick", 0, 2, [looting])]),
                                  pool([entry(m("verdite_gem"))], 1.0, [{"condition": "minecraft:random_chance", "chance": 0.15}])]))
    D(LE + "stormwisp.json", ent([pool([entry(m("cloud_fluff"), 0, 2, [looting])]),
                                  pool([entry(m("aerite_gem"))], 1.0, [{"condition": "minecraft:random_chance", "chance": 0.15}])]))
    D(LE + "gloom_crawler.json", ent([pool([entry("minecraft:string", 0, 2, [looting])]),
                                      pool([entry(m("umbral_gem"))], 1.0, [{"condition": "minecraft:random_chance", "chance": 0.15}])]))
    smelt = {"function": "minecraft:furnace_smelt", "conditions": [
        {"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {"is_on_fire": True}}}]}
    D(LE + "lumistag.json", ent([pool([entry("minecraft:leather", 0, 2, [looting])]),
                                 pool([entry(m("lumi_venison"), 1, 3, [smelt, looting])])]))
    D(LE + "cloud_puff.json", ent([pool([entry(m("cloud_fluff"), 1, 3, [looting])])]))
    D(LE + "mossling.json", ent([pool([entry("minecraft:moss_block", 0, 1)]),
                                 pool([entry(m("glow_fruit"))], 1.0, [{"condition": "minecraft:random_chance", "chance": 0.3}])]))

    def chest(special, spec_range):
        return {"type": "minecraft:chest", "pools": [
            pool([entry("minecraft:iron_ingot", 1, 4, []), entry("minecraft:gold_ingot", 1, 3), entry("minecraft:emerald", 1, 3),
                  entry(m(glow := "glow_fruit"), 2, 5), entry("minecraft:arrow", 4, 12), entry("minecraft:bread", 2, 4)], 3.0),
            pool([entry(m(special), *spec_range)], 1.0),
            pool([entry("minecraft:diamond")], 1.0, [{"condition": "minecraft:random_chance", "chance": 0.15}])]}

    D(LC + "whisper_ruin.json", chest("verdite_gem", (1, 3)))
    D(LC + "sky_ruin.json", chest("aerite_gem", (1, 3)))
    D(LC + "umbral_ruin.json", chest("umbral_gem", (1, 3)))


# ===================================================================== TAGS / ADVANCEMENTS / MODIFIER
def tags():
    ores = [m(n) for n in ("verdite_ore", "aerite_ore", "umbral_ore")]
    gembl = [m(n) for n in ("verdite_block", "aerite_block", "umbral_block")]
    stones = [m(n) for n in ("whisper_bricks", "sky_bricks", "gloom_bricks", "skystone", "umbral_crystal",
                             "whisper_tablet", "sky_tablet", "umbral_tablet")]
    woods = [m(f"{w}_{k}") for w in WOODS for k in ("log", "planks", "slab")]
    MC("tags/blocks/mineable/pickaxe.json", {"replace": False, "values": ores + gembl + stones})
    MC("tags/blocks/mineable/axe.json", {"replace": False, "values": woods})
    MC("tags/blocks/needs_iron_tool.json", {"replace": False, "values": [m("verdite_ore"), m("aerite_ore")] + gembl})
    MC("tags/blocks/needs_diamond_tool.json", {"replace": False, "values": [m("umbral_ore")]})
    leaves = [m(f"{w}_leaves") for w in WOODS]
    MC("tags/blocks/leaves.json", {"replace": False, "values": leaves})
    MC("tags/blocks/mineable/hoe.json", {"replace": False, "values": leaves})
    logs = [m(f"{w}_log") for w in WOODS]
    planks = [m(f"{w}_planks") for w in WOODS]
    slabs = [m(f"{w}_slab") for w in WOODS]
    saplings = [m(f"{w}_sapling") for w in WOODS]
    flowers = [m("lumibloom"), m("sunbloom"), m("gloomcap")]
    for kind, vals in (("logs", logs), ("logs_that_burn", logs), ("planks", planks), ("wooden_slabs", slabs),
                       ("saplings", saplings), ("small_flowers", flowers)):
        MC(f"tags/blocks/{kind}.json", {"replace": False, "values": vals})
        MC(f"tags/items/{kind}.json", {"replace": False, "values": vals})
    MC("tags/items/leaves.json", {"replace": False, "values": leaves})


def adv(name, parent, icon, frame, trigger, cond, hidden=False, toast=True):
    d = {"display": {"icon": {"item": icon}, "title": {"translate": f"advancement.starfall.{name}.title"},
                     "description": {"translate": f"advancement.starfall.{name}.desc"}, "frame": frame,
                     "show_toast": toast, "announce_to_chat": toast, "hidden": hidden},
         "criteria": {"c": {"trigger": trigger, "conditions": cond}}}
    if parent:
        d["parent"] = m(parent)
    else:
        d["display"]["background"] = "minecraft:textures/gui/advancements/backgrounds/stone.png"
        d["display"]["show_toast"] = False
        d["display"]["announce_to_chat"] = False
    D(f"advancements/{name}.json", d)


def killed(entity):
    return {"entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": m(entity)}}]}


def advancements():
    adv("root", None, m("starheart"), "task", "minecraft:tick", {})
    adv("whisperwood", "root", m("whisper_gate"), "task", "minecraft:changed_dimension", {"to": m("whisperwood")})
    adv("skyreach", "whisperwood", m("sky_gate"), "task", "minecraft:changed_dimension", {"to": m("skyreach")})
    adv("umbral", "skyreach", m("umbral_gate"), "task", "minecraft:changed_dimension", {"to": m("umbral")})
    adv("kill_matriarch", "whisperwood", m("verdant_shard"), "goal", "minecraft:player_killed_entity", killed("thorn_matriarch"))
    adv("kill_sovereign", "skyreach", m("tempest_shard"), "goal", "minecraft:player_killed_entity", killed("storm_sovereign"))
    adv("kill_king", "umbral", m("umbral_shard"), "goal", "minecraft:player_killed_entity", killed("gloom_king"))
    adv("starheart", "kill_king", m("starheart"), "goal", "minecraft:inventory_changed", {"items": [{"items": [m("starheart")]}]})
    adv("kill_aurelion", "starheart", m("star_blade"), "challenge", "minecraft:player_killed_entity", killed("aurelion"))
    adv("tame_mossling", "whisperwood", m("glow_fruit"), "goal", "minecraft:tame_animal",
        {"entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": m("mossling")}}]})


def modifiers():
    D("forge/biome_modifier/lorekeeper.json", {"type": "forge:add_spawns", "biomes": "#minecraft:is_overworld",
                                               "spawners": {"type": m("lorekeeper"), "weight": 3, "minCount": 1, "maxCount": 1}})


def run():
    dimension_types()
    dimensions()
    biomes()
    features()
    recipes()
    loot()
    tags()
    advancements()
    modifiers()
