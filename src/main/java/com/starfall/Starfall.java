package com.starfall;

import com.starfall.entity.*;
import com.starfall.registry.*;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnPlacements;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.event.entity.SpawnPlacementRegisterEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(Starfall.MOD_ID)
public class Starfall {
    public static final String MOD_ID = "starfall";

    public static final ResourceKey<Level> WHISPERWOOD = dim("whisperwood");
    public static final ResourceKey<Level> SKYREACH = dim("skyreach");
    public static final ResourceKey<Level> UMBRAL = dim("umbral");

    private static ResourceKey<Level> dim(String name) {
        return ResourceKey.create(Registries.DIMENSION, id(name));
    }

    public static ResourceLocation id(String path) {
        return new ResourceLocation(MOD_ID, path);
    }

    public Starfall() {
        IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        ModBlocks.BLOCKS.register(bus);
        ModItems.ITEMS.register(bus);
        ModEntities.ENTITIES.register(bus);
        ModFeatures.FEATURES.register(bus);
        ModTabs.TABS.register(bus);
        bus.addListener(this::attributes);
        bus.addListener(this::spawns);
    }

    private void attributes(EntityAttributeCreationEvent e) {
        e.put(ModEntities.THORN_MATRIARCH.get(), ThornMatriarchEntity.createAttributes().build());
        e.put(ModEntities.STORM_SOVEREIGN.get(), StormSovereignEntity.createAttributes().build());
        e.put(ModEntities.GLOOM_KING.get(), GloomKingEntity.createAttributes().build());
        e.put(ModEntities.AURELION.get(), AurelionEntity.createAttributes().build());
        e.put(ModEntities.THORNBACK.get(), ThornbackEntity.createAttributes().build());
        e.put(ModEntities.STORMWISP.get(), StormwispEntity.createAttributes().build());
        e.put(ModEntities.GLOOM_CRAWLER.get(), GloomCrawlerEntity.createAttributes().build());
        e.put(ModEntities.LUMISTAG.get(), LumistagEntity.createAttributes().build());
        e.put(ModEntities.CLOUD_PUFF.get(), CloudPuffEntity.createAttributes().build());
        e.put(ModEntities.MOSSLING.get(), MosslingEntity.createAttributes().build());
        e.put(ModEntities.LOREKEEPER.get(), LorekeeperEntity.createAttributes().build());
    }

    /** Spawn simples: precisa de um bloco solido embaixo (nao depende de luz nem de grama). */
    private static <T extends Mob> boolean ground(EntityType<T> type, ServerLevelAccessor level,
                                                  MobSpawnType reason, BlockPos pos, RandomSource random) {
        return level.getBlockState(pos.below()).isValidSpawn(level, pos.below(), type);
    }

    private void spawns(SpawnPlacementRegisterEvent e) {
        SpawnPlacementRegisterEvent.Operation op = SpawnPlacementRegisterEvent.Operation.OR;
        e.register(ModEntities.THORNBACK.get(), SpawnPlacements.Type.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkAnyLightMonsterSpawnRules, op);
        e.register(ModEntities.GLOOM_CRAWLER.get(), SpawnPlacements.Type.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Monster::checkAnyLightMonsterSpawnRules, op);
        e.register(ModEntities.STORMWISP.get(), SpawnPlacements.Type.NO_RESTRICTIONS,
                Heightmap.Types.MOTION_BLOCKING, Monster::checkAnyLightMonsterSpawnRules, op);
        e.register(ModEntities.LUMISTAG.get(), SpawnPlacements.Type.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Starfall::ground, op);
        e.register(ModEntities.MOSSLING.get(), SpawnPlacements.Type.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Starfall::ground, op);
        e.register(ModEntities.LOREKEEPER.get(), SpawnPlacements.Type.ON_GROUND,
                Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, Starfall::ground, op);
        e.register(ModEntities.CLOUD_PUFF.get(), SpawnPlacements.Type.NO_RESTRICTIONS,
                Heightmap.Types.MOTION_BLOCKING, Mob::checkMobSpawnRules, op);
    }
}
