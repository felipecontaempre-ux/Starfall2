package com.starfall.registry;

import com.starfall.Starfall;
import com.starfall.block.*;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.grower.AbstractTreeGrower;
import net.minecraft.world.level.material.MapColor;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.function.Supplier;

public class ModBlocks {
    public static final DeferredRegister<Block> BLOCKS =
            DeferredRegister.create(ForgeRegistries.BLOCKS, Starfall.MOD_ID);

    private static RegistryObject<Block> reg(String name, Supplier<Block> s) {
        return BLOCKS.register(name, s);
    }

    // ------------------------------------------------ fabricas
    private static Block log(MapColor c) {
        return new RotatedPillarBlock(BlockBehaviour.Properties.copy(Blocks.OAK_LOG).mapColor(c));
    }
    private static Block planks(MapColor c) {
        return new Block(BlockBehaviour.Properties.copy(Blocks.OAK_PLANKS).mapColor(c));
    }
    private static Block slab(MapColor c) {
        return new SlabBlock(BlockBehaviour.Properties.copy(Blocks.OAK_SLAB).mapColor(c));
    }
    private static Block leaves(MapColor c) {
        return new LeavesBlock(BlockBehaviour.Properties.copy(Blocks.OAK_LEAVES).mapColor(c));
    }
    private static Block sapling(String tree) {
        AbstractTreeGrower grower = new RealmTreeGrower(ResourceKey.create(Registries.CONFIGURED_FEATURE, Starfall.id(tree)));
        return new SaplingBlock(grower, BlockBehaviour.Properties.copy(Blocks.OAK_SAPLING));
    }
    private static Block flower(MobEffect effect, int seconds, int light) {
        return new FlowerBlock(effect, seconds, BlockBehaviour.Properties.copy(Blocks.DANDELION).lightLevel(s -> light));
    }
    private static Block ore() {
        return new DropExperienceBlock(BlockBehaviour.Properties.copy(Blocks.IRON_ORE), UniformInt.of(2, 6));
    }
    private static Block gemBlock() {
        return new Block(BlockBehaviour.Properties.copy(Blocks.DIAMOND_BLOCK));
    }
    private static Block bricks() {
        return new Block(BlockBehaviour.Properties.copy(Blocks.STONE_BRICKS));
    }
    private static Block tablet(String realm) {
        return new LoreTabletBlock(realm, BlockBehaviour.Properties.copy(Blocks.STONE_BRICKS).strength(2.5F).noOcclusion());
    }
    private static Block gate(ResourceKey<Level> realm) {
        return new RiftGateBlock(BlockBehaviour.Properties.of().noCollission().noOcclusion().strength(0.6F)
                .lightLevel(s -> 13).sound(SoundType.GLASS).mapColor(MapColor.COLOR_PURPLE), realm);
    }
    private static BlockBehaviour.Properties altarProps() {
        return BlockBehaviour.Properties.copy(Blocks.OBSIDIAN).strength(-1.0F, 3600000.0F).noLootTable().lightLevel(s -> 8);
    }

    // ------------------------------------------------ BOSQUE SUSSURRANTE
    public static final RegistryObject<Block> WHISPER_LOG = reg("whisper_log", () -> log(MapColor.COLOR_PURPLE));
    public static final RegistryObject<Block> WHISPER_PLANKS = reg("whisper_planks", () -> planks(MapColor.COLOR_PURPLE));
    public static final RegistryObject<Block> WHISPER_SLAB = reg("whisper_slab", () -> slab(MapColor.COLOR_PURPLE));
    public static final RegistryObject<Block> WHISPER_LEAVES = reg("whisper_leaves", () -> leaves(MapColor.COLOR_CYAN));
    public static final RegistryObject<Block> WHISPER_SAPLING = reg("whisper_sapling", () -> sapling("whisper_tree"));
    public static final RegistryObject<Block> LUMIBLOOM = reg("lumibloom", () -> flower(MobEffects.NIGHT_VISION, 8, 9));
    public static final RegistryObject<Block> GLOWCAP_BLOCK = reg("glowcap_block", () ->
            new Block(BlockBehaviour.Properties.copy(Blocks.BROWN_MUSHROOM_BLOCK).lightLevel(s -> 13)));
    public static final RegistryObject<Block> VERDITE_ORE = reg("verdite_ore", ModBlocks::ore);
    public static final RegistryObject<Block> VERDITE_BLOCK = reg("verdite_block", ModBlocks::gemBlock);
    public static final RegistryObject<Block> WHISPER_BRICKS = reg("whisper_bricks", ModBlocks::bricks);
    public static final RegistryObject<Block> WHISPER_TABLET = reg("whisper_tablet", () -> tablet("whisper"));
    public static final RegistryObject<Block> WHISPER_ALTAR = reg("whisper_altar", () ->
            new BossAltarBlock(altarProps(), () -> ModEntities.THORN_MATRIARCH.get(), () -> ModItems.THORN_SIGIL.get()));
    public static final RegistryObject<Block> WHISPER_GATE = reg("whisper_gate", () -> gate(Starfall.WHISPERWOOD));

    // ------------------------------------------------ CUMES DO CEU
    public static final RegistryObject<Block> SKYROOT_LOG = reg("skyroot_log", () -> log(MapColor.SNOW));
    public static final RegistryObject<Block> SKYROOT_PLANKS = reg("skyroot_planks", () -> planks(MapColor.SNOW));
    public static final RegistryObject<Block> SKYROOT_SLAB = reg("skyroot_slab", () -> slab(MapColor.SNOW));
    public static final RegistryObject<Block> SKYROOT_LEAVES = reg("skyroot_leaves", () -> leaves(MapColor.COLOR_LIGHT_BLUE));
    public static final RegistryObject<Block> SKYROOT_SAPLING = reg("skyroot_sapling", () -> sapling("skyroot_tree"));
    public static final RegistryObject<Block> SUNBLOOM = reg("sunbloom", () -> flower(MobEffects.JUMP, 6, 7));
    public static final RegistryObject<Block> CLOUD_BLOCK = reg("cloud_block", () ->
            new CloudBlock(BlockBehaviour.Properties.of().mapColor(MapColor.SNOW).strength(0.4F).sound(SoundType.WOOL)));
    public static final RegistryObject<Block> SKYSTONE = reg("skystone", () ->
            new Block(BlockBehaviour.Properties.copy(Blocks.STONE)));
    public static final RegistryObject<Block> AERITE_ORE = reg("aerite_ore", ModBlocks::ore);
    public static final RegistryObject<Block> AERITE_BLOCK = reg("aerite_block", ModBlocks::gemBlock);
    public static final RegistryObject<Block> SKY_BRICKS = reg("sky_bricks", ModBlocks::bricks);
    public static final RegistryObject<Block> SKY_TABLET = reg("sky_tablet", () -> tablet("sky"));
    public static final RegistryObject<Block> SKY_ALTAR = reg("sky_altar", () ->
            new BossAltarBlock(altarProps(), () -> ModEntities.STORM_SOVEREIGN.get(), () -> ModItems.STORM_SIGIL.get()));
    public static final RegistryObject<Block> SKY_GATE = reg("sky_gate", () -> gate(Starfall.SKYREACH));

    // ------------------------------------------------ REINO UMBRIO
    public static final RegistryObject<Block> GLOOM_LOG = reg("gloom_log", () -> log(MapColor.COLOR_BLACK));
    public static final RegistryObject<Block> GLOOM_PLANKS = reg("gloom_planks", () -> planks(MapColor.COLOR_BLACK));
    public static final RegistryObject<Block> GLOOM_SLAB = reg("gloom_slab", () -> slab(MapColor.COLOR_BLACK));
    public static final RegistryObject<Block> GLOOM_LEAVES = reg("gloom_leaves", () -> leaves(MapColor.COLOR_MAGENTA));
    public static final RegistryObject<Block> GLOOM_SAPLING = reg("gloom_sapling", () -> sapling("gloom_tree"));
    public static final RegistryObject<Block> GLOOMCAP = reg("gloomcap", () -> flower(MobEffects.DAMAGE_RESISTANCE, 6, 6));
    public static final RegistryObject<Block> UMBRAL_CRYSTAL = reg("umbral_crystal", () ->
            new Block(BlockBehaviour.Properties.copy(Blocks.AMETHYST_BLOCK).lightLevel(s -> 12)));
    public static final RegistryObject<Block> UMBRAL_ORE = reg("umbral_ore", ModBlocks::ore);
    public static final RegistryObject<Block> UMBRAL_BLOCK = reg("umbral_block", ModBlocks::gemBlock);
    public static final RegistryObject<Block> GLOOM_BRICKS = reg("gloom_bricks", ModBlocks::bricks);
    public static final RegistryObject<Block> UMBRAL_TABLET = reg("umbral_tablet", () -> tablet("umbral"));
    public static final RegistryObject<Block> UMBRAL_ALTAR = reg("umbral_altar", () ->
            new BossAltarBlock(altarProps(), () -> ModEntities.GLOOM_KING.get(), () -> ModItems.GLOOM_SIGIL.get()));
    public static final RegistryObject<Block> UMBRAL_GATE = reg("umbral_gate", () -> gate(Starfall.UMBRAL));
}
