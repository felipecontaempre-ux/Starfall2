package com.starfall.world;

import com.mojang.serialization.Codec;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.RandomizableContainerBlockEntity;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;

/** Ruina circular com muros quebrados, pilares, tabua de lore e bau de loot. */
public class RuinFeature extends Feature<RuinConfig> {
    public RuinFeature(Codec<RuinConfig> codec) {
        super(codec);
    }

    @Override
    public boolean place(FeaturePlaceContext<RuinConfig> ctx) {
        WorldGenLevel level = ctx.level();
        BlockPos o = ctx.origin();
        RandomSource r = ctx.random();
        RuinConfig c = ctx.config();
        int rad = c.radius();

        for (int dx = -rad; dx <= rad; dx++) {
            for (int dz = -rad; dz <= rad; dz++) {
                double d = Math.sqrt(dx * dx + dz * dz);
                if (d > rad) continue;
                level.setBlock(o.offset(dx, -1, dz), c.floor(), 2);
                for (int y = 0; y <= 5; y++) {
                    BlockPos p = o.offset(dx, y, dz);
                    if (!level.getBlockState(p).isAir()) level.setBlock(p, Blocks.AIR.defaultBlockState(), 2);
                }
                if (d > rad - 1.2D && r.nextFloat() < 0.65F) {
                    int h = 1 + r.nextInt(3);
                    for (int y = 0; y < h; y++) level.setBlock(o.offset(dx, y, dz), c.wall(), 2);
                }
            }
        }
        int pr = rad - 1;
        int[][] corners = {{pr, pr}, {-pr, pr}, {pr, -pr}, {-pr, -pr}};
        for (int[] k : corners) {
            int h = 4 + r.nextInt(2);
            for (int y = 0; y < h; y++) level.setBlock(o.offset(k[0], y, k[1]), c.wall(), 2);
        }
        level.setBlock(o, c.tablet(), 2);
        BlockPos chest = o.offset(2, 0, 0);
        level.setBlock(chest, Blocks.CHEST.defaultBlockState(), 2);
        RandomizableContainerBlockEntity.setLootTable(level, r, chest, c.loot());
        return true;
    }
}
