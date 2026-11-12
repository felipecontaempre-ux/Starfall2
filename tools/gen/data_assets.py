from common import *

WOODS = ["whisper", "skyroot", "gloom"]
MATS = ["verdite", "aerite", "umbral"]
TOOLS = ["sword", "pickaxe", "axe", "shovel", "hoe"]
ARMORS = ["helmet", "chestplate", "leggings", "boots"]
ENTITIES = ["thorn_matriarch", "storm_sovereign", "gloom_king", "aurelion", "thornback", "stormwisp",
            "gloom_crawler", "lumistag", "cloud_puff", "mossling", "lorekeeper"]

# nome -> tipo de modelo
BLOCKS = {}
for w in WOODS:
    BLOCKS[f"{w}_log"] = "log"
    BLOCKS[f"{w}_planks"] = "cube"
    BLOCKS[f"{w}_slab"] = "slab"
    BLOCKS[f"{w}_leaves"] = "leaves"
    BLOCKS[f"{w}_sapling"] = "cross"
for n in ("lumibloom", "sunbloom", "gloomcap"):
    BLOCKS[n] = "cross"
for n in ("glowcap_block", "verdite_ore", "verdite_block", "whisper_bricks", "cloud_block", "skystone", "aerite_ore",
          "aerite_block", "sky_bricks", "umbral_crystal", "umbral_ore", "umbral_block", "gloom_bricks"):
    BLOCKS[n] = "cube"
for r in ("whisper", "sky", "umbral"):
    BLOCKS[f"{r}_tablet"] = "tablet"
    BLOCKS[f"{r}_altar"] = "altar"
    BLOCKS[f"{r}_gate"] = "gate"
# skyroot_sapling usa o nome de arquivo do gerador (skyroot_sapling) - ja consistente

PLAIN_ITEMS = ["verdite_gem", "aerite_gem", "umbral_gem", "cloud_fluff", "verdant_shard", "tempest_shard",
               "umbral_shard", "star_fragment", "star_medal", "thorn_sigil", "storm_sigil", "gloom_sigil",
               "starheart", "glow_fruit", "lumi_venison", "cooked_lumi_venison", "sky_pie"]
HANDHELD = ["verdant_staff", "wind_staff", "gloom_scythe", "star_blade"]


def faces6(tex):
    return {d: {"uv": [0, 0, 16, 16], "texture": tex} for d in ("north", "east", "south", "west", "up", "down")}


def block_assets():
    for name, kind in BLOCKS.items():
        tex = m(f"block/{name}")
        if kind == "cube":
            A(f"blockstates/{name}.json", {"variants": {"": {"model": m(f"block/{name}")}}})
            A(f"models/block/{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": tex}})
            A(f"models/item/{name}.json", {"parent": m(f"block/{name}")})
        elif kind == "log":
            A(f"blockstates/{name}.json", {"variants": {
                "axis=y": {"model": m(f"block/{name}")},
                "axis=z": {"model": m(f"block/{name}"), "x": 90},
                "axis=x": {"model": m(f"block/{name}"), "x": 90, "y": 90}}})
            A(f"models/block/{name}.json", {"parent": "minecraft:block/cube_column",
                                            "textures": {"end": m(f"block/{name}_top"), "side": tex}})
            A(f"models/item/{name}.json", {"parent": m(f"block/{name}")})
        elif kind == "leaves":
            A(f"blockstates/{name}.json", {"variants": {"": {"model": m(f"block/{name}")}}})
            A(f"models/block/{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": tex},
                                            "render_type": "minecraft:cutout_mipped"})
            A(f"models/item/{name}.json", {"parent": m(f"block/{name}")})
        elif kind == "cross":
            A(f"blockstates/{name}.json", {"variants": {"": {"model": m(f"block/{name}")}}})
            A(f"models/block/{name}.json", {"parent": "minecraft:block/cross", "textures": {"cross": tex},
                                            "render_type": "minecraft:cutout"})
            A(f"models/item/{name}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": tex}})
        elif kind == "slab":
            planks = name.replace("_slab", "_planks")
            ptex = m(f"block/{planks}")
            A(f"blockstates/{name}.json", {"variants": {
                "type=bottom": {"model": m(f"block/{name}")},
                "type=top": {"model": m(f"block/{name}_top")},
                "type=double": {"model": m(f"block/{planks}")}}})
            t = {"bottom": ptex, "top": ptex, "side": ptex}
            A(f"models/block/{name}.json", {"parent": "minecraft:block/slab", "textures": t})
            A(f"models/block/{name}_top.json", {"parent": "minecraft:block/slab_top", "textures": t})
            A(f"models/item/{name}.json", {"parent": m(f"block/{name}")})
        elif kind == "tablet":
            A(f"blockstates/{name}.json", {"variants": {"": {"model": m(f"block/{name}")}}})
            A(f"models/block/{name}.json", {
                "parent": "minecraft:block/block", "textures": {"0": tex, "particle": tex},
                "elements": [{"from": [2, 0, 5], "to": [14, 15, 11], "faces": faces6("#0")}]})
            A(f"models/item/{name}.json", {"parent": m(f"block/{name}")})
        elif kind == "altar":
            A(f"blockstates/{name}.json", {"variants": {"": {"model": m(f"block/{name}")}}})
            A(f"models/block/{name}.json", {
                "parent": "minecraft:block/block", "textures": {"0": tex, "particle": tex},
                "elements": [
                    {"from": [1, 0, 1], "to": [15, 4, 15], "faces": faces6("#0")},
                    {"from": [4, 4, 4], "to": [12, 9, 12], "faces": faces6("#0")},
                    {"from": [2, 9, 2], "to": [14, 12, 14], "faces": faces6("#0")}]})
            A(f"models/item/{name}.json", {"parent": m(f"block/{name}")})
        elif kind == "gate":
            A(f"blockstates/{name}.json", {"variants": {"": {"model": m(f"block/{name}")}}})
            A(f"models/block/{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": tex},
                                            "render_type": "minecraft:translucent"})
            A(f"models/item/{name}.json", {"parent": m(f"block/{name}")})


def item_assets():
    for n in PLAIN_ITEMS:
        A(f"models/item/{n}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": m(f"item/{n}")}})
    for n in HANDHELD:
        A(f"models/item/{n}.json", {"parent": "minecraft:item/handheld", "textures": {"layer0": m(f"item/{n}")}})
    for mat in MATS:
        for t in TOOLS:
            A(f"models/item/{mat}_{t}.json", {"parent": "minecraft:item/handheld", "textures": {"layer0": m(f"item/{mat}_{t}")}})
        for a in ARMORS:
            A(f"models/item/{mat}_{a}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": m(f"item/{mat}_{a}")}})
    for e in ENTITIES:
        A(f"models/item/{e}_spawn_egg.json", {"parent": "minecraft:item/template_spawn_egg"})


# ===================================================================== TEXTOS
BLOCK_NAMES = {
    "whisper_log": ("Whisperwood Log", "Tronco Sussurrante"), "whisper_planks": ("Whisperwood Planks", "Tábuas Sussurrantes"),
    "whisper_slab": ("Whisperwood Slab", "Laje Sussurrante"), "whisper_leaves": ("Whisperwood Leaves", "Folhas Sussurrantes"),
    "whisper_sapling": ("Whisperwood Sapling", "Muda Sussurrante"), "lumibloom": ("Lumibloom", "Lumiflor"),
    "glowcap_block": ("Glowcap Block", "Bloco de Cogumelo Luminoso"), "verdite_ore": ("Verdite Ore", "Minério de Verdita"),
    "verdite_block": ("Block of Verdite", "Bloco de Verdita"), "whisper_bricks": ("Whisperstone Bricks", "Tijolos Sussurrantes"),
    "whisper_tablet": ("Whispering Tablet", "Tábua Sussurrante"), "whisper_altar": ("Altar of Thorns", "Altar dos Espinhos"),
    "whisper_gate": ("Whisperwood Rift Gate", "Portal do Bosque Sussurrante"),
    "skyroot_log": ("Skyroot Log", "Tronco de Raiz-do-Céu"), "skyroot_planks": ("Skyroot Planks", "Tábuas de Raiz-do-Céu"),
    "skyroot_slab": ("Skyroot Slab", "Laje de Raiz-do-Céu"), "skyroot_leaves": ("Skyroot Leaves", "Folhas de Raiz-do-Céu"),
    "skyroot_sapling": ("Skyroot Sapling", "Muda de Raiz-do-Céu"), "sunbloom": ("Sunbloom", "Solflor"),
    "cloud_block": ("Cloud Block", "Bloco de Nuvem"), "skystone": ("Skystone", "Pedra do Céu"),
    "aerite_ore": ("Aerite Ore", "Minério de Aerita"), "aerite_block": ("Block of Aerite", "Bloco de Aerita"),
    "sky_bricks": ("Skystone Bricks", "Tijolos do Céu"), "sky_tablet": ("Skyward Tablet", "Tábua Celeste"),
    "sky_altar": ("Altar of the Storm", "Altar da Tempestade"), "sky_gate": ("Skyreach Rift Gate", "Portal de Cumes do Céu"),
    "gloom_log": ("Gloom Log", "Tronco Sombrio"), "gloom_planks": ("Gloom Planks", "Tábuas Sombrias"),
    "gloom_slab": ("Gloom Slab", "Laje Sombria"), "gloom_leaves": ("Gloom Leaves", "Folhas Sombrias"),
    "gloom_sapling": ("Gloom Sapling", "Muda Sombria"), "gloomcap": ("Gloomcap", "Chapéu-Sombrio"),
    "umbral_crystal": ("Umbral Crystal", "Cristal Umbrio"), "umbral_ore": ("Umbral Ore", "Minério Umbrio"),
    "umbral_block": ("Block of Umbral Gem", "Bloco de Gema Umbria"), "gloom_bricks": ("Gloom Bricks", "Tijolos Sombrios"),
    "umbral_tablet": ("Umbral Tablet", "Tábua Umbria"), "umbral_altar": ("Altar of Gloom", "Altar das Sombras"),
    "umbral_gate": ("Umbral Rift Gate", "Portal do Reino Umbrio"),
}
MAT_NAMES = {"verdite": ("Verdite", "Verdita"), "aerite": ("Aerite", "Aerita"), "umbral": ("Umbral", "Umbria")}
TOOL_NAMES = {"sword": ("Sword", "Espada"), "pickaxe": ("Pickaxe", "Picareta"), "axe": ("Axe", "Machado"),
              "shovel": ("Shovel", "Pá"), "hoe": ("Hoe", "Enxada"), "helmet": ("Helmet", "Capacete"),
              "chestplate": ("Chestplate", "Peitoral"), "leggings": ("Leggings", "Calças"), "boots": ("Boots", "Botas")}
ITEM_NAMES = {
    "verdite_gem": ("Verdite Gem", "Gema de Verdita"), "aerite_gem": ("Aerite Gem", "Gema de Aerita"),
    "umbral_gem": ("Umbral Gem", "Gema Umbria"), "cloud_fluff": ("Cloud Fluff", "Algodão de Nuvem"),
    "verdant_shard": ("Verdant Shard", "Fragmento Verdejante"), "tempest_shard": ("Tempest Shard", "Fragmento da Tempestade"),
    "umbral_shard": ("Umbral Shard", "Fragmento Umbrio"), "star_fragment": ("Star Fragment", "Fragmento Estelar"),
    "star_medal": ("Medal of the Warden", "Medalha do Guardião"), "thorn_sigil": ("Thorn Sigil", "Sigilo dos Espinhos"),
    "storm_sigil": ("Storm Sigil", "Sigilo da Tempestade"), "gloom_sigil": ("Gloom Sigil", "Sigilo das Sombras"),
    "starheart": ("Starheart", "Coração Estelar"), "glow_fruit": ("Glow Fruit", "Fruta Luminosa"),
    "lumi_venison": ("Raw Lumi Venison", "Carne Crua de Lumicervo"), "cooked_lumi_venison": ("Cooked Lumi Venison", "Carne Assada de Lumicervo"),
    "sky_pie": ("Sky Pie", "Torta do Céu"), "verdant_staff": ("Verdant Staff", "Cajado Verdejante"),
    "wind_staff": ("Wind Staff", "Cajado do Vento"), "gloom_scythe": ("Gloom Scythe", "Foice Umbria"),
    "star_blade": ("Star Blade", "Lâmina Estelar"),
}
ENTITY_NAMES = {
    "thorn_matriarch": ("Thorn Matriarch", "Matriarca dos Espinhos"), "storm_sovereign": ("Storm Sovereign", "Soberano da Tempestade"),
    "gloom_king": ("Gloom King", "Rei Umbrio"), "aurelion": ("Aurelion, the Fallen Warden", "Aurelion, o Guardião Caído"),
    "thornback": ("Thornback", "Espinhoso"), "stormwisp": ("Stormwisp", "Fogo-fátuo da Tempestade"),
    "gloom_crawler": ("Gloom Crawler", "Rastejante Umbrio"), "lumistag": ("Lumistag", "Lumicervo"),
    "cloud_puff": ("Cloud Puff", "Nuvenzinha"), "mossling": ("Mossling", "Mossling"),
    "lorekeeper": ("Lorekeeper", "Guardião das Histórias"),
}

LORE = {
    "whisper": [
        ("Before the Starfall, these woods were only trees. Now every root remembers the light.",
         "Antes da Queda da Estrela, estes bosques eram só árvores. Agora cada raiz se lembra da luz."),
        ("The Matriarch was no monster once. She wrapped the fallen shard in her roots to keep it from the dark.",
         "A Matriarca nem sempre foi um monstro. Ela envolveu o fragmento caído com suas raízes para protegê-lo da escuridão."),
        ("Lumistags follow the glow of the shard. Their antlers still shine with borrowed starlight.",
         "Os lumicervos seguem o brilho do fragmento. Suas galhadas ainda reluzem com luz estelar emprestada."),
        ("Do not sleep beneath the glowcaps. They dream aloud, and the dreams are hungry.",
         "Não durma sob os cogumelos luminosos. Eles sonham em voz alta, e os sonhos têm fome."),
        ("Mosslings are the forest's apology: small, patient, and kind to those who offer fruit.",
         "Os mosslings são o pedido de desculpas da floresta: pequenos, pacientes e gentis com quem oferece frutas."),
        ("A mother guards what she loves. A mother also bites when you come too close.",
         "Uma mãe protege o que ama. Uma mãe também morde quando você chega perto demais."),
        ("Thorns for the greedy, sap for the grieving. Which will she give you?",
         "Espinhos para os gananciosos, seiva para os enlutados. Qual ela dará a você?"),
        ("The forest hums in three notes. The fourth is missing: it fell with the star.",
         "A floresta cantarola em três notas. A quarta está faltando: caiu junto com a estrela."),
    ],
    "sky": [
        ("Once, islands drifted here on the breath of the Star. Now they drift on habit.",
         "Um dia, ilhas flutuavam aqui ao sopro da Estrela. Agora flutuam por hábito."),
        ("The Sovereign hoarded the storms to keep the sky from falling. He forgot why he started.",
         "O Soberano guardou as tempestades para o céu não cair. Esqueceu por que começou."),
        ("Cloud puffs sing only when no one listens. Be very quiet.",
         "As nuvenzinhas só cantam quando ninguém ouve. Fique bem quieto."),
        ("Skystone remembers wind. Strike it and it hums.", "A pedra do céu se lembra do vento. Bata nela e ela zumbe."),
        ("Those who wear aerite fall like feathers. Those who do not learn quickly.",
         "Quem veste aerita cai como pena. Quem não veste aprende rápido."),
        ("He answers every thunderclap with one of his own. Do not shout at a god of storms.",
         "Ele responde cada trovão com outro. Não grite com um deus das tempestades."),
        ("The wind staff was carved from his first feather. He never noticed it was gone.",
         "O cajado do vento foi talhado da primeira pena dele. Ele nunca notou que sumiu."),
        ("Above the highest cloud, the Warden once looked down. Perhaps he still does.",
         "Acima da nuvem mais alta, o Guardião olhava para baixo. Talvez ainda olhe."),
    ],
    "umbral": [
        ("The Gloom King's court fell silent the night the Star cracked. Then the silence began to rule.",
         "A corte do Rei Umbrio calou na noite em que a Estrela rachou. Então o silêncio passou a reinar."),
        ("Darkness here is not an absence. It is a presence with patience.",
         "A escuridão aqui não é ausência. É uma presença com paciência."),
        ("Crawlers weave their webs from shadows the king no longer needs.",
         "Os rastejantes tecem suas teias com sombras de que o rei não precisa mais."),
        ("He drinks the souls of the brave to remember what courage felt like.",
         "Ele bebe a alma dos bravos para lembrar como era a coragem."),
        ("Umbral crystal glows because it is hurt. Do not mistake pain for light.",
         "O cristal umbrio brilha porque está ferido. Não confunda dor com luz."),
        ("Wear umbral armor and the dark will stop hiding from you.",
         "Vista armadura umbria e a escuridão deixará de se esconder de você."),
        ("The king's crown holds a shard. His heart holds only hunger.",
         "A coroa do rei guarda um fragmento. O coração dele guarda só fome."),
        ("Beyond the three realms, the Warden waits, half star, half sorrow.",
         "Além dos três reinos, o Guardião espera, meio estrela, meio tristeza."),
    ],
}

NPC = {
    "0": ("Ah, a traveler! I am the Lorekeeper. Long ago a Star watched over this world, until it shattered into three shards that fell into three realms. Take these Rift Gates: place one, step through, and find the Verdant Shard in the Whisperwood. Show it to me.",
          "Ah, um viajante! Sou o Guardião das Histórias. Há muito tempo uma Estrela velava por este mundo, até se partir em três fragmentos que caíram em três reinos. Pegue estes Portais: coloque um, atravesse e encontre o Fragmento Verdejante no Bosque Sussurrante. Mostre-o a mim."),
    "1": ("The Whisperwood awaits. Find its altar of thorns, craft a Thorn Sigil and face the Matriarch. Bring me the Verdant Shard (hold it in your hand).",
          "O Bosque Sussurrante espera. Encontre o altar dos espinhos, crie um Sigilo dos Espinhos e enfrente a Matriarca. Traga o Fragmento Verdejante (segure-o na mão)."),
    "1b": ("The Verdant Shard! It still sings. Here, gates to Skyreach, where the Storm Sovereign hoards the second shard.",
           "O Fragmento Verdejante! Ele ainda canta. Tome, portais para Cumes do Céu, onde o Soberano da Tempestade guarda o segundo fragmento."),
    "2": ("Skyreach floats above the clouds. Craft a Storm Sigil from aerite and wake the Sovereign. Show me the Tempest Shard.",
          "Cumes do Céu flutua acima das nuvens. Crie um Sigilo da Tempestade com aerita e desperte o Soberano. Mostre-me o Fragmento da Tempestade."),
    "2b": ("The Tempest Shard... the wind remembers you. One more waits in the dark: the Umbral Reach. Take these gates.",
           "O Fragmento da Tempestade... o vento se lembra de você. Mais um espera no escuro: o Reino Umbrio. Leve estes portais."),
    "3": ("In the Umbral Reach the Gloom King sits upon the last shard. Bring a Gloom Sigil and enough light to see.",
          "No Reino Umbrio o Rei Umbrio senta sobre o último fragmento. Leve um Sigilo das Sombras e luz suficiente para enxergar."),
    "3b": ("Three shards! Combine them with a Nether Star and the Starheart will beat again. But beware: it will call Aurelion, the fallen Warden.",
           "Três fragmentos! Combine-os com uma Estrela do Nether e o Coração Estelar baterá de novo. Mas cuidado: ele chamará Aurelion, o Guardião caído."),
    "4": ("Forge the Starheart, use it on open ground, and face Aurelion. Bring me the Star Fragment he leaves behind.",
          "Forje o Coração Estelar, use-o em campo aberto e enfrente Aurelion. Traga-me o Fragmento Estelar que ele deixar."),
    "4b": ("You freed him. The Star is whole in spirit, if not in stone. Take this medal and these diamonds: you are the Warden of the Realms now.",
           "Você o libertou. A Estrela está inteira em espírito, se não em pedra. Aceite esta medalha e estes diamantes: agora você é o Guardião dos Reinos."),
    "5": ("The realms are at peace, hero. Explore the ruins, read the tablets, tame a mossling. The stars remember you.",
          "Os reinos estão em paz, herói. Explore as ruínas, leia as tábuas, domestique um mossling. As estrelas se lembram de você."),
    "tablets": ("You have been reading the tablets! A scholar after my own heart. Take these as thanks.",
                "Você tem lido as tábuas! Um estudioso depois do meu próprio coração. Aceite isto como agradecimento."),
}

MSG = {
    "message.starfall.tablet.new": ("New tablet read! (%s total)", "Nova tábua lida! (%s no total)"),
    "message.starfall.boss_exists": ("The guardian is already awake nearby!", "O guardião já está acordado por perto!"),
    "message.starfall.altar.need": ("The altar requires: %s", "O altar exige: %s"),
    "message.starfall.gate.whisperwood": ("The rift opens... mist and murmurs.", "A fenda se abre... névoa e murmúrios."),
    "message.starfall.gate.skyreach": ("The rift opens... the world drops away.", "A fenda se abre... o mundo some lá embaixo."),
    "message.starfall.gate.umbral": ("The rift opens... the light forgets you.", "A fenda se abre... a luz esquece você."),
    "message.starfall.phase.thorn_matriarch.2": ("The Matriarch calls her thornbacks!", "A Matriarca chama seus Espinhosos!"),
    "message.starfall.phase.thorn_matriarch.3": ("OVERGROWTH! The forest mends her!", "SUPERCRESCIMENTO! A floresta a cura!"),
    "message.starfall.phase.storm_sovereign.2": ("The Sovereign summons the stormwisps!", "O Soberano invoca os fogos-fátuos!"),
    "message.starfall.phase.storm_sovereign.3": ("THE TEMPEST IS UNLEASHED!", "A TEMPESTADE FOI LIBERTADA!"),
    "message.starfall.phase.gloom_king.2": ("The Gloom King's shadows stir...", "As sombras do Rei Umbrio se agitam..."),
    "message.starfall.phase.gloom_king.3": ("THE VOID OPENS!", "O VAZIO SE ABRE!"),
    "message.starfall.phase.aurelion.2": ("Aurelion blinks through the light...", "Aurelion cintila através da luz..."),
    "message.starfall.phase.aurelion.3": ("Aurelion rains meteors!", "Aurelion faz chover meteoros!"),
    "message.starfall.phase.aurelion.4": ("THE STAR REMEMBERS ITS FURY!", "A ESTRELA LEMBRA DE SUA FÚRIA!"),
}

TIPS = {
    "tooltip.starfall.shard": ("A shard of the fallen Star. Show it to the Lorekeeper.", "Um fragmento da Estrela caída. Mostre ao Guardião das Histórias."),
    "tooltip.starfall.star_fragment": ("A fragment of the freed Star. Show it to the Lorekeeper.", "Um fragmento da Estrela libertada. Mostre ao Guardião das Histórias."),
    "tooltip.starfall.star_medal": ("Awarded to the Warden of the Realms.", "Concedida ao Guardião dos Reinos."),
    "tooltip.starfall.thorn_sigil": ("Offer it at the Altar of Thorns.", "Ofereça no Altar dos Espinhos."),
    "tooltip.starfall.storm_sigil": ("Offer it at the Altar of the Storm.", "Ofereça no Altar da Tempestade."),
    "tooltip.starfall.gloom_sigil": ("Offer it at the Altar of Gloom.", "Ofereça no Altar das Sombras."),
    "tooltip.starfall.starheart": ("Use on open ground to summon Aurelion, the Fallen Warden.", "Use em campo aberto para invocar Aurelion, o Guardião Caído."),
    "tooltip.starfall.verdant_staff": ("Right-click: heal yourself and nearby allies", "Botão direito: cura você e aliados por perto"),
    "tooltip.starfall.wind_staff": ("Right-click: gust leap, pushes enemies away", "Botão direito: salto de vento, empurra inimigos"),
    "tooltip.starfall.gloom_scythe.hit": ("On hit: Darkness, Weakness and lifesteal", "Ao acertar: Escuridão, Fraqueza e roubo de vida"),
    "tooltip.starfall.gloom_scythe.use": ("Right-click: Shadow Step", "Botão direito: Passo Sombrio"),
    "tooltip.starfall.star_blade.hit": ("On hit: sets the target ablaze", "Ao acertar: incendeia o alvo"),
    "tooltip.starfall.star_blade.use": ("Right-click: hurl a star", "Botão direito: arremessa uma estrela"),
}

ADV = {
    "root": ("Starfall", "The Star is broken. The realms await.", "Starfall", "A Estrela está partida. Os reinos aguardam."),
    "whisperwood": ("Murmuring Mist", "Enter the Whisperwood.", "Névoa Murmurante", "Entre no Bosque Sussurrante."),
    "skyreach": ("Head in the Clouds", "Enter Skyreach.", "Cabeça nas Nuvens", "Entre em Cumes do Céu."),
    "umbral": ("Into the Dark", "Enter the Umbral Reach.", "Rumo à Escuridão", "Entre no Reino Umbrio."),
    "kill_matriarch": ("Mother Knows Best", "Defeat the Thorn Matriarch.", "A Mãe Sabe o Que Faz", "Derrote a Matriarca dos Espinhos."),
    "kill_sovereign": ("Calm After the Storm", "Defeat the Storm Sovereign.", "Calmaria Após a Tempestade", "Derrote o Soberano da Tempestade."),
    "kill_king": ("Long Live the Light", "Defeat the Gloom King.", "Viva a Luz", "Derrote o Rei Umbrio."),
    "starheart": ("The Heart Beats Again", "Forge the Starheart.", "O Coração Bate de Novo", "Forje o Coração Estelar."),
    "kill_aurelion": ("Warden of the Realms", "Free Aurelion, the Fallen Warden.", "Guardião dos Reinos", "Liberte Aurelion, o Guardião Caído."),
    "tame_mossling": ("Small and Kind", "Tame a Mossling.", "Pequeno e Gentil", "Domestique um Mossling."),
}


def lang():
    en, pt = {}, {}

    def put(k, v):
        en[k], pt[k] = v

    put("itemGroup.starfall.tab", ("Starfall: Shattered Realms", "Starfall: Reinos Partidos"))
    for n, v in BLOCK_NAMES.items():
        put(f"block.starfall.{n}", v)
    for n, v in ITEM_NAMES.items():
        put(f"item.starfall.{n}", v)
    for mat, (men, mpt) in MAT_NAMES.items():
        for t, (ten, tpt) in TOOL_NAMES.items():
            put(f"item.starfall.{mat}_{t}", (f"{men} {ten}", f"{tpt} de {mpt}" if t not in ("chestplate",) else f"{tpt} de {mpt}"))
    for e, v in ENTITY_NAMES.items():
        put(f"entity.starfall.{e}", v)
        put(f"item.starfall.{e}_spawn_egg", (f"{v[0]} Spawn Egg", f"Ovo de Criação: {v[1]}"))
    for realm, lines in LORE.items():
        for i, (a, b) in enumerate(lines):
            put(f"lore.starfall.{realm}.{i}", (a, b))
    for k, v in NPC.items():
        put(f"npc.starfall.{k}", v)
    put("npc.starfall.say", ("<%s> %s", "<%s> %s"))
    for k, v in {**MSG, **TIPS}.items():
        put(k, v)
    for k, (te, de, tp, dp) in ADV.items():
        put(f"advancement.starfall.{k}.title", (te, tp))
        put(f"advancement.starfall.{k}.desc", (de, dp))
    A("lang/en_us.json", en)
    A("lang/pt_br.json", pt)


def run():
    block_assets()
    item_assets()
    lang()
