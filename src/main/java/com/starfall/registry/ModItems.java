package com.starfall.registry;

import com.starfall.Starfall;
import com.starfall.item.*;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.function.Supplier;

public class ModItems {
    public static final DeferredRegister<Item> ITEMS =
            DeferredRegister.create(ForgeRegistries.ITEMS, Starfall.MOD_ID);

    private static RegistryObject<Item> simple(String name) {
        return ITEMS.register(name, () -> new Item(new Item.Properties()));
    }

    private static RegistryObject<Item> shard(String name, String tip) {
        return ITEMS.register(name, () -> new TooltipItem(new Item.Properties().rarity(Rarity.EPIC).fireResistant(), tip, true));
    }

    private static RegistryObject<Item> sigil(String name) {
        return ITEMS.register(name, () -> new TooltipItem(new Item.Properties().rarity(Rarity.RARE).stacksTo(16),
                "tooltip.starfall." + name, false));
    }

    // ------------------------------------------------ materiais
    public static final RegistryObject<Item> VERDITE_GEM = simple("verdite_gem");
    public static final RegistryObject<Item> AERITE_GEM = simple("aerite_gem");
    public static final RegistryObject<Item> UMBRAL_GEM = simple("umbral_gem");
    public static final RegistryObject<Item> CLOUD_FLUFF = simple("cloud_fluff");

    // ------------------------------------------------ fragmentos da estrela (historia)
    public static final RegistryObject<Item> VERDANT_SHARD = shard("verdant_shard", "tooltip.starfall.shard");
    public static final RegistryObject<Item> TEMPEST_SHARD = shard("tempest_shard", "tooltip.starfall.shard");
    public static final RegistryObject<Item> UMBRAL_SHARD = shard("umbral_shard", "tooltip.starfall.shard");
    public static final RegistryObject<Item> STAR_FRAGMENT = shard("star_fragment", "tooltip.starfall.star_fragment");
    public static final RegistryObject<Item> STAR_MEDAL = shard("star_medal", "tooltip.starfall.star_medal");

    // ------------------------------------------------ sigilos / invocacao
    public static final RegistryObject<Item> THORN_SIGIL = sigil("thorn_sigil");
    public static final RegistryObject<Item> STORM_SIGIL = sigil("storm_sigil");
    public static final RegistryObject<Item> GLOOM_SIGIL = sigil("gloom_sigil");
    public static final RegistryObject<Item> STARHEART = ITEMS.register("starheart",
            () -> new StarheartItem(new Item.Properties().rarity(Rarity.EPIC).stacksTo(1).fireResistant()));

    // ------------------------------------------------ comidas
    public static final RegistryObject<Item> GLOW_FRUIT = ITEMS.register("glow_fruit", () -> new Item(new Item.Properties()
            .food(new FoodProperties.Builder().nutrition(4).saturationMod(0.4F)
                    .effect(() -> new MobEffectInstance(MobEffects.NIGHT_VISION, 400), 1.0F).build())));
    public static final RegistryObject<Item> LUMI_VENISON = ITEMS.register("lumi_venison", () -> new Item(new Item.Properties()
            .food(new FoodProperties.Builder().nutrition(3).saturationMod(0.3F).meat().build())));
    public static final RegistryObject<Item> COOKED_LUMI_VENISON = ITEMS.register("cooked_lumi_venison", () -> new Item(new Item.Properties()
            .food(new FoodProperties.Builder().nutrition(8).saturationMod(0.8F).meat().build())));
    public static final RegistryObject<Item> SKY_PIE = ITEMS.register("sky_pie", () -> new Item(new Item.Properties()
            .food(new FoodProperties.Builder().nutrition(8).saturationMod(0.6F)
                    .effect(() -> new MobEffectInstance(MobEffects.SLOW_FALLING, 1200), 1.0F)
                    .effect(() -> new MobEffectInstance(MobEffects.JUMP, 1200, 1), 1.0F).alwaysEat().build())));

    // ------------------------------------------------ armas especiais
    public static final RegistryObject<Item> VERDANT_STAFF = ITEMS.register("verdant_staff",
            () -> new WeaponItems.VerdantStaff(new Item.Properties().durability(260).rarity(Rarity.RARE)));
    public static final RegistryObject<Item> WIND_STAFF = ITEMS.register("wind_staff",
            () -> new WeaponItems.WindStaff(new Item.Properties().durability(320).rarity(Rarity.RARE)));
    public static final RegistryObject<Item> GLOOM_SCYTHE = ITEMS.register("gloom_scythe",
            () -> new WeaponItems.GloomScythe(ModTiers.UMBRAL, 4, -2.3F, new Item.Properties().rarity(Rarity.RARE)));
    public static final RegistryObject<Item> STAR_BLADE = ITEMS.register("star_blade",
            () -> new WeaponItems.StarBlade(ModTiers.STAR, 4, -2.2F, new Item.Properties().rarity(Rarity.EPIC).fireResistant()));

    // ------------------------------------------------ conjuntos de ferramentas e armaduras
    private static void toolSet(String m, Tier t) {
        ITEMS.register(m + "_sword", () -> new SwordItem(t, 3, -2.4F, new Item.Properties()));
        ITEMS.register(m + "_pickaxe", () -> new PickaxeItem(t, 1, -2.8F, new Item.Properties()));
        ITEMS.register(m + "_axe", () -> new AxeItem(t, 5.0F, -3.0F, new Item.Properties()));
        ITEMS.register(m + "_shovel", () -> new ShovelItem(t, 1.5F, -3.0F, new Item.Properties()));
        ITEMS.register(m + "_hoe", () -> new HoeItem(t, -2, -1.0F, new Item.Properties()));
    }

    private static void armorSet(String m, ArmorMaterial mat) {
        for (ArmorItem.Type type : ArmorItem.Type.values()) {
            ITEMS.register(m + "_" + type.getName(), () -> new ArmorItem(mat, type, new Item.Properties()));
        }
    }

    static {
        toolSet("verdite", ModTiers.VERDITE);
        toolSet("aerite", ModTiers.AERITE);
        toolSet("umbral", ModTiers.UMBRAL);
        armorSet("verdite", ModArmorMaterials.VERDITE);
        armorSet("aerite", ModArmorMaterials.AERITE);
        armorSet("umbral", ModArmorMaterials.UMBRAL);
        // um BlockItem para cada bloco registrado
        for (RegistryObject<Block> b : ModBlocks.BLOCKS.getEntries()) {
            ITEMS.register(b.getId().getPath(), () -> new BlockItem(b.get(), new Item.Properties()));
        }
    }

    // ------------------------------------------------ spawn eggs
    private static void egg(String name, Supplier<? extends EntityType<? extends Mob>> type, int c1, int c2) {
        ITEMS.register(name + "_spawn_egg", () -> new ForgeSpawnEggItem(type, c1, c2, new Item.Properties()));
    }

    static {
        egg("thorn_matriarch", ModEntities.THORN_MATRIARCH, 0x3C2A1E, 0x7CFF6A);
        egg("storm_sovereign", ModEntities.STORM_SOVEREIGN, 0xD0D8EE, 0xFFE866);
        egg("gloom_king", ModEntities.GLOOM_KING, 0x26203A, 0xAA66FF);
        egg("aurelion", ModEntities.AURELION, 0xEBDDB0, 0xFFC840);
        egg("thornback", ModEntities.THORNBACK, 0x54402A, 0xD8CFA8);
        egg("stormwisp", ModEntities.STORMWISP, 0x96AAF0, 0xFFFFFF);
        egg("gloom_crawler", ModEntities.GLOOM_CRAWLER, 0x1E162D, 0xAA55FF);
        egg("lumistag", ModEntities.LUMISTAG, 0x8A6A4A, 0x7FFFD8);
        egg("cloud_puff", ModEntities.CLOUD_PUFF, 0xFFFFFF, 0xFFB6C8);
        egg("mossling", ModEntities.MOSSLING, 0x4C8C3C, 0xFFE066);
        egg("lorekeeper", ModEntities.LOREKEEPER, 0x5A3E8C, 0xFFD866);
    }
}
