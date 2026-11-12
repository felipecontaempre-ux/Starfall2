package com.starfall.registry;

import com.starfall.Starfall;
import com.starfall.world.*;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public class ModFeatures {
    public static final DeferredRegister<Feature<?>> FEATURES =
            DeferredRegister.create(ForgeRegistries.FEATURES, Starfall.MOD_ID);

    public static final RegistryObject<Feature<RuinConfig>> RUIN =
            FEATURES.register("ruin", () -> new RuinFeature(RuinConfig.CODEC));
    public static final RegistryObject<Feature<ArenaConfig>> ARENA =
            FEATURES.register("arena", () -> new ArenaFeature(ArenaConfig.CODEC));
    public static final RegistryObject<Feature<NoneFeatureConfiguration>> SKY_PAINT =
            FEATURES.register("sky_paint", () -> new SkyPaintFeature(NoneFeatureConfiguration.CODEC));
}
