package com.starfall.block;

import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/** Nuvem solida: anula dano de queda e faz quicar (agache para nao quicar). */
public class CloudBlock extends Block {
    public CloudBlock(Properties props) {
        super(props);
    }

    @Override
    public void fallOn(Level level, BlockState state, BlockPos pos, Entity entity, float fallDistance) {
        entity.causeFallDamage(fallDistance, 0.0F, level.damageSources().fall());
    }

    @Override
    public void updateEntityAfterFallOn(BlockGetter level, Entity entity) {
        Vec3 v = entity.getDeltaMovement();
        if (v.y < 0.0D && !entity.isSuppressingBounce()) {
            entity.setDeltaMovement(v.x, -v.y * 0.9D, v.z);
        } else {
            super.updateEntityAfterFallOn(level, entity);
        }
    }
}
