package com.starfall.world;

import com.mojang.serialization.Codec;
import com.starfall.registry.ModBlocks;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;

/**
 * As ilhas de Skyreach saem do gerador "floating_islands" feitas de pedra do End.
 * Esta feature pinta o chunk: grama no topo, terra embaixo e pedra do ceu no resto.
 */
public class SkyPaintFeature extends Feature<NoneFeatureConfiguration> {
    public SkyPaintFeature(Codec<NoneFeatureConfiguration> codec) {
        super(codec);
    }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> ctx) {
        WorldGenLevel level = ctx.level();
        BlockPos o = ctx.origin();
        int x0 = (o.getX() >> 4) << 4;
        int z0 = (o.getZ() >> 4) << 4;
        BlockState stone = ModBlocks.SKYSTONE.get().defaultBlockState();
        BlockState grass = Blocks.GRASS_BLOCK.defaultBlockState();
        BlockState dirt = Blocks.DIRT.defaultBlockState();
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();

        for (int x = 0; x < 16; x++) {
            for (int z = 0; z < 16; z++) {
                int run = 0; // blocos solidos desde o ultimo ar
                for (int y = 255; y >= 0; y--) {
                    p.set(x0 + x, y, z0 + z);
                    BlockState s = level.getBlockState(p);
                    if (s.isAir()) {
                        run = 0;
                    } else if (s.is(Blocks.END_STONE)) {
                        level.setBlock(p, run == 0 ? grass : run < 3 ? dirt : stone, 2);
                        run++;
                    } else {
                        run = 99;
                    }
                }
            }
        }
        return true;
    }
}
