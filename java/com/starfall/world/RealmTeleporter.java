package com.starfall.world;

import com.starfall.Starfall;
import com.starfall.registry.ModBlocks;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.portal.PortalInfo;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.common.util.ITeleporter;

import java.util.function.Function;

/** Teleporta direto para uma posicao; ao chegar num reino, constroi o patio com o portal de volta. */
public class RealmTeleporter implements ITeleporter {
    private final ResourceKey<Level> realm;
    private BlockPos pos;

    private RealmTeleporter(ResourceKey<Level> realm, BlockPos pos) {
        this.realm = realm;
        this.pos = pos;
    }

    public static RealmTeleporter toRealm(ResourceKey<Level> realm) {
        return new RealmTeleporter(realm, null);
    }

    public static RealmTeleporter toPos(BlockPos pos) {
        return new RealmTeleporter(null, pos);
    }

    @Override
    public PortalInfo getPortalInfo(Entity entity, ServerLevel dest, Function<ServerLevel, PortalInfo> defaultInfo) {
        BlockPos c = target(dest);
        return new PortalInfo(new Vec3(c.getX() + 0.5D, c.getY(), c.getZ() + 0.5D), Vec3.ZERO,
                entity.getYRot(), entity.getXRot());
    }

    @Override
    public Entity placeEntity(Entity entity, ServerLevel from, ServerLevel to, float yaw,
                              Function<Boolean, Entity> reposition) {
        target(to);
        return reposition.apply(false);
    }

    private BlockPos target(ServerLevel dest) {
        if (pos != null) return pos;
        BlockPos c = realm == Starfall.SKYREACH
                ? new BlockPos(0, 100, 0)
                : dest.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING, BlockPos.ZERO);
        buildPad(dest, c);
        pos = c;
        return c;
    }

    private void buildPad(ServerLevel level, BlockPos c) {
        Block bricks;
        Block gate;
        if (realm == Starfall.WHISPERWOOD) {
            bricks = ModBlocks.WHISPER_BRICKS.get();
            gate = ModBlocks.WHISPER_GATE.get();
        } else if (realm == Starfall.SKYREACH) {
            bricks = ModBlocks.SKY_BRICKS.get();
            gate = ModBlocks.SKY_GATE.get();
        } else {
            bricks = ModBlocks.GLOOM_BRICKS.get();
            gate = ModBlocks.UMBRAL_GATE.get();
        }
        if (level.getBlockState(c.below()).is(bricks)) return; // ja existe

        for (int dx = -4; dx <= 4; dx++) {
            for (int dz = -4; dz <= 4; dz++) {
                if (dx * dx + dz * dz > 17) continue;
                level.setBlockAndUpdate(c.offset(dx, -1, dz), bricks.defaultBlockState());
                for (int dy = 0; dy <= 4; dy++) {
                    level.setBlockAndUpdate(c.offset(dx, dy, dz), Blocks.AIR.defaultBlockState());
                }
            }
        }
        // arco do portal de volta
        for (int dz = -1; dz <= 1; dz++) {
            for (int dy = 0; dy <= 2; dy++) {
                level.setBlockAndUpdate(c.offset(3, dy, dz), bricks.defaultBlockState());
            }
        }
        level.setBlockAndUpdate(c.offset(3, 0, 0), gate.defaultBlockState());
        level.setBlockAndUpdate(c.offset(3, 1, 0), gate.defaultBlockState());
    }
}
