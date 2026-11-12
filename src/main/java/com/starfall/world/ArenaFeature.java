package com.starfall.world;

import com.mojang.serialization.Codec;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;

/** Arena de boss: plataforma plana, 8 pilares iluminados e o altar de invocacao no centro. */
public class ArenaFeature extends Feature<ArenaConfig> {
    public ArenaFeature(Codec<ArenaConfig> codec) {
        super(codec);
    }

    @Override
    public boolean place(FeaturePlaceContext<ArenaConfig> ctx) {
        WorldGenLevel level = ctx.level();
        BlockPos o = ctx.origin();
        ArenaConfig c = ctx.config();
        int R = c.radius();
        BlockState air = Blocks.AIR.defaultBlockState();

        for (int dx = -R; dx <= R; dx++) {
            for (int dz = -R; dz <= R; dz++) {
                double d = Math.sqrt(dx * dx + dz * dz);
                if (d > R) continue;
                for (int y = -4; y <= -1; y++) level.setBlock(o.offset(dx, y, dz), c.floor(), 2);
                for (int y = 0; y <= 14; y++) {
                    BlockPos p = o.offset(dx, y, dz);
                    if (!level.getBlockState(p).isAir()) level.setBlock(p, air, 2);
                }
                if (d > R - 1.5D) level.setBlock(o.offset(dx, 0, dz), c.pillar(), 2);
            }
        }
        for (int i = 0; i < 8; i++) {
            double a = i * Math.PI / 4.0D;
            int px = (int) Math.round(Math.cos(a) * (R - 1));
            int pz = (int) Math.round(Math.sin(a) * (R - 1));
            for (int y = 0; y < 7; y++) level.setBlock(o.offset(px, y, pz), c.pillar(), 2);
            level.setBlock(o.offset(px, 7, pz), c.lamp(), 2);
        }
        level.setBlock(o, c.altar(), 2);
        int[][] around = {{2, 0}, {-2, 0}, {0, 2}, {0, -2}};
        for (int[] k : around) level.setBlock(o.offset(k[0], 0, k[1]), c.pillar(), 2);
        return true;
    }
}
