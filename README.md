# ✨ Starfall: Shattered Realms (Forge 1.20.1)

> Há muito tempo uma **Estrela** velava pelo mundo, guardada por **Aurelion**. Ela se partiu em três
> fragmentos, que caíram em três reinos e corromperam seus guardiões. Reforje a **Coração Estelar**.

## 🛠️ Como compilar (jeito mais fácil: GitHub faz por você)
1. Crie conta grátis no github.com e um repositório novo.
2. Suba o conteúdo desta pasta (botão *Add file → Upload files*).
3. **Importante:** a pasta oculta `.github` costuma NÃO subir no arrastar-e-soltar. Se a aba *Actions* ficar vazia:
   *Add file → Create new file*, nome `.github/workflows/build.yml`, e cole o conteúdo do arquivo `build.yml.txt` deste zip. Commit.
4. Aba **Actions** → espere ficar verde (~5 min) → baixe **starfall-jar** em *Artifacts*.
5. Coloque o `.jar` em `mods/` (Minecraft **1.20.1** + **Forge 47.x**).

Compilando local: JDK 17 + Forge MDK 1.20.1 (copie `gradlew` e `gradle/` dele pra cá) → `./gradlew build`.

## 🗺️ História e progressão
1. Ache o **Guardião das Histórias** (NPC de manto roxo, aparece raro no Overworld; tem spawn egg). Clique nele.
   Ele dá **2 Portais do Bosque Sussurrante** (receita alternativa: 4 esmeraldas + 4 obsidianas + pérola do Ender).
2. **Portais** são blocos: coloque e entre. Na chegada surge um pátio com o portal de volta.
3. Em cada reino ache **ruínas** (baú de loot + **Tábua** de lore: clique pra ler a história) e a **arena** do boss (altar no centro).
4. Minere o minério do reino → gemas → forje **Sigilo** → ofereça no altar → boss.
5. Cada boss solta um **Fragmento**. Segure-o e clique no NPC pra avançar o capítulo e ganhar o portal do próximo reino.
6. Com os 3 fragmentos + Estrela do Nether → **Coração Estelar** → use no chão → **Aurelion** (4 fases!).
7. Mostre o **Fragmento Estelar** ao NPC: final da história.

| Reino | Terreno | Boss | Sigilo |
|---|---|---|---|
| 🌲 Bosque Sussurrante | floresta crepuscular, cogumelos luminosos | **Matriarca dos Espinhos** | 4 verdita, 4 ouro, 1 esmeralda |
| ☁️ Cumes do Céu | ilhas flutuantes, nuvens que fazem quicar | **Soberano da Tempestade** (voa) | 4 aerita, 4 algodão de nuvem, 1 diamante |
| 🌑 Reino Umbrio | terra de eterna meia-noite, cristais | **Rei Umbrio** | 4 umbria, 4 pérolas, 1 diamante |

## ⚔️ Mecânicas
- **Bosses** com barra de vida, fases por % de vida, invulnerabilidade ao mudar de fase e ataques próprios
  (raízes, esporos, raios, ventania, mergulho, drenar alma, fenda do vazio que puxa, meteoros, invocações...).
- **Armaduras de 3 materiais + bônus de conjunto completo:** Verdita = Regeneração · Aerita = Queda lenta + Pulo · Umbria = Visão noturna + Resistência.
- **Armas especiais:** Cajado Verdejante (cura aliados/pets), Cajado do Vento (salto + empurrão), Foice Umbria (Passo Sombrio), Lâmina Estelar (incendeia + arremessa estrelas).
- **Mossling:** pet domesticável com Fruta Luminosa (clique pra sentar/seguir), dá Regeneração ao dono.
- **Nuvem:** anula dano de queda e quica (agache pra não quicar).
- A cada **3 tábuas lidas** o NPC te dá um presente. O progresso sobrevive à morte.
- 10 **conquistas** (aba de avançamentos) acompanham a história.
- Tudo em **inglês e português (pt_br)**.

## 🧰 Para quem quer modificar
`python3 tools/generate_assets.py` regenera texturas, modelos, receitas, dimensões e traduções.
Os modelos das criaturas ficam em `tools/gen/rigs.py` (um arquivo gera o modelo 3D **e** a textura juntos).
`python3 tools/validate.py` confere se nada ficou faltando.
