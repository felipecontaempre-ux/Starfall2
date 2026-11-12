package com.starfall.world;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.configurations.FeatureConfiguration;

public record ArenaConfig(BlockState floor, BlockState pillar, BlockState lamp, BlockState altar, int radius)
        implements FeatureConfiguration {
    public static final Codec<ArenaConfig> CODEC = RecordCodecBuilder.create(i -> i.group(
            BlockState.CODEC.fieldOf("floor").forGetter(ArenaConfig::floor),
            BlockState.CODEC.fieldOf("pillar").forGetter(ArenaConfig::pillar),
            BlockState.CODEC.fieldOf("lamp").forGetter(ArenaConfig::lamp),
            BlockState.CODEC.fieldOf("altar").forGetter(ArenaConfig::altar),
            Codec.intRange(6, 13).fieldOf("radius").forGetter(ArenaConfig::radius)
    ).apply(i, ArenaConfig::new));
}
