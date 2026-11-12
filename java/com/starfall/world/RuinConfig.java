package com.starfall.world;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.configurations.FeatureConfiguration;

public record RuinConfig(BlockState wall, BlockState floor, BlockState tablet, ResourceLocation loot, int radius)
        implements FeatureConfiguration {
    public static final Codec<RuinConfig> CODEC = RecordCodecBuilder.create(i -> i.group(
            BlockState.CODEC.fieldOf("wall").forGetter(RuinConfig::wall),
            BlockState.CODEC.fieldOf("floor").forGetter(RuinConfig::floor),
            BlockState.CODEC.fieldOf("tablet").forGetter(RuinConfig::tablet),
            ResourceLocation.CODEC.fieldOf("loot").forGetter(RuinConfig::loot),
            Codec.intRange(3, 10).fieldOf("radius").forGetter(RuinConfig::radius)
    ).apply(i, RuinConfig::new));
}
