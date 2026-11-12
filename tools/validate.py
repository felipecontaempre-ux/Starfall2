import json, glob, os, re, struct, sys
R = "src/main/resources"
A = f"{R}/assets/starfall"; D = f"{R}/data/starfall"
errs = []
def err(m): errs.append(m)

# 1. todo JSON valido
for f in glob.glob(f"{R}/**/*.json", recursive=True):
    try: json.load(open(f, encoding="utf-8"))
    except Exception as e: err(f"JSON invalido {f}: {e}")

# 2. registros Java
jb = open("src/main/java/com/starfall/registry/ModBlocks.java").read()
blocks = set(re.findall(r'reg\("([a-z_]+)"', jb))
ji = open("src/main/java/com/starfall/registry/ModItems.java").read()
items = set(re.findall(r'(?:simple|shard|sigil)\("([a-z_]+)"', ji))
items |= set(re.findall(r'ITEMS\.register\("([a-z_]+)"', ji))
for mat in ("verdite","aerite","umbral"):
    for t in ("sword","pickaxe","axe","shovel","hoe","helmet","chestplate","leggings","boots"): items.add(f"{mat}_{t}")
items |= blocks
je = open("src/main/java/com/starfall/registry/ModEntities.java").read()
ents = set(re.findall(r'reg\("([a-z_]+)"', je))
for e in set(re.findall(r'egg\("([a-z_]+)"', ji)): items.add(e + "_spawn_egg")
items -= {"m + \"_sword\""}
print(f"blocos={len(blocks)} itens={len(items)} entidades={len(ents)}")

lang = json.load(open(f"{A}/lang/en_us.json")); langpt = json.load(open(f"{A}/lang/pt_br.json"))
def tex_ok(ref):
    ns, p = ref.split(":"); return os.path.exists(f"{R}/assets/{ns}/textures/{p}.png") if ns == "starfall" else True

for b in blocks:
    for f in (f"blockstates/{b}.json", f"models/item/{b}.json"):
        if not os.path.exists(f"{A}/{f}"): err(f"falta {f}")
    if not os.path.exists(f"{A}/models/block/{b}.json") and not b.endswith("_slab") : err(f"falta modelo de bloco {b}")
    if f"block.starfall.{b}" not in lang: err(f"lang en falta bloco {b}")
    if f"block.starfall.{b}" not in langpt: err(f"lang pt falta bloco {b}")
    if "altar" not in b and not os.path.exists(f"{D}/loot_tables/blocks/{b}.json"): err(f"falta loot de {b}")
for i in items - blocks:
    if not os.path.exists(f"{A}/models/item/{i}.json"): err(f"falta modelo de item {i}")
    if f"item.starfall.{i}" not in lang: err(f"lang en falta item {i}")
    if f"item.starfall.{i}" not in langpt: err(f"lang pt falta item {i}")
for e in ents:
    if f"entity.starfall.{e}" not in lang: err(f"lang falta entidade {e}")
    if e != "lorekeeper" and not os.path.exists(f"{A}/rigs/{e}.json"): err(f"falta rig {e}")
    if e != "lorekeeper" and not os.path.exists(f"{D}/loot_tables/entities/{e}.json") and e != "lorekeeper": err(f"falta loot entidade {e}")

# 3. texturas referenciadas por modelos
for f in glob.glob(f"{A}/models/**/*.json", recursive=True):
    d = json.load(open(f))
    for k, v in d.get("textures", {}).items():
        if isinstance(v, str) and v.startswith("starfall:") and not tex_ok(v): err(f"textura faltando {v} em {f}")
# modelos referenciados por blockstates
for f in glob.glob(f"{A}/blockstates/*.json"):
    for var in json.load(open(f))["variants"].values():
        ref = var["model"].split(":")[1]
        if not os.path.exists(f"{A}/models/{ref}.json"): err(f"blockstate {f} -> modelo faltando {ref}")

# 4. referencias de receitas / loot a itens
def check_item(ref, where):
    if ref.startswith("starfall:") and ref.split(":")[1] not in items: err(f"item inexistente {ref} em {where}")
for f in glob.glob(f"{D}/recipes/*.json") + glob.glob(f"{D}/loot_tables/**/*.json", recursive=True):
    txt = open(f).read()
    for ref in re.findall(r'"(starfall:[a-z_/]+)"', txt):
        if "chests/" in ref: continue
        check_item(ref, os.path.basename(f))

# 5. features
pf = {os.path.basename(f)[:-5] for f in glob.glob(f"{D}/worldgen/placed_feature/*.json")}
cf = {os.path.basename(f)[:-5] for f in glob.glob(f"{D}/worldgen/configured_feature/*.json")}
for f in glob.glob(f"{D}/worldgen/biome/*.json"):
    for step in json.load(open(f))["features"]:
        for ref in step:
            if ref.startswith("starfall:") and ref.split(":")[1] not in pf: err(f"{f}: placed feature faltando {ref}")
for f in glob.glob(f"{D}/worldgen/placed_feature/*.json"):
    ref = json.load(open(f))["feature"]
    if ref.startswith("starfall:") and ref.split(":")[1] not in cf: err(f"{f}: configured faltando {ref}")
bio = {os.path.basename(f)[:-5] for f in glob.glob(f"{D}/worldgen/biome/*.json")}
for f in glob.glob(f"{D}/dimension/*.json"):
    for b in json.load(open(f))["generator"]["biome_source"]["biomes"]:
        if b["biome"].split(":")[1] not in bio: err(f"{f}: bioma faltando {b['biome']}")
for f in glob.glob(f"{D}/worldgen/biome/*.json"):
    for cat in json.load(open(f))["spawners"].values():
        for s in cat:
            if s["type"].split(":")[1] not in ents: err(f"{f}: spawner {s['type']} desconhecido")
# loot tables de bau
for f in glob.glob(f"{D}/worldgen/configured_feature/*_ruin.json"):
    ref = json.load(open(f))["config"]["loot"].split(":")[1]
    if not os.path.exists(f"{D}/loot_tables/{ref}.json"): err(f"{f}: loot de bau faltando {ref}")
# rigs: pais antes dos filhos, uv dentro da textura
for name in ents:
    p = f"{A}/rigs/{name}.json"
    if not os.path.exists(p): continue
    r = json.load(open(p)); seen = set()
    for part in r["parts"]:
        if part.get("parent") and part["parent"] not in seen: err(f"rig {name}: pai {part['parent']} depois de {part['name']}")
        seen.add(part["name"])
        w, h, d = [int(-(-v // 1)) for v in part["box"][3:6]]
        u, v = part["tex"]
        if u + 2*d + 2*w > r["texW"] or v + d + h > r["texH"]: err(f"rig {name}: UV fora da textura em {part['name']}")
    if not os.path.exists(f"{A}/textures/entity/{name}.png"): err(f"textura entidade {name}")
    if r["glow"] and not os.path.exists(f"{A}/textures/entity/{name}_glow.png"): err(f"glow {name}")
if "--quiet" not in sys.argv:
    print("RIGS:", sorted(e for e in ents if e != "lorekeeper"))
print("ERROS:" if errs else "TUDO OK", *errs, sep="\n")
