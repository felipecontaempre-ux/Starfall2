package com.starfall.block;

import com.starfall.world.RealmTeleporter;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;

/** Portal em forma de bloco. Entre nele: vai para o reino; dentro do reino, volta ao Overworld. */
public class RiftGateBlock extends Block {
    private final ResourceKey<Level> realm;

    public RiftGateBlock(Properties props, ResourceKey<Level> realm) {
        super(props);
        this.realm = realm;
    }

    @Override
    public void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
        if (level.isClientSide || !(entity instanceof ServerPlayer sp)) return;
        MinecraftServer server = level.getServer();
        if (server == null) return;

        CompoundTag pd = sp.getPersistentData();
        long now = level.getGameTime();
        if (now - pd.getLong("starfall_gate_cd") < 100L) return;
        pd.putLong("starfall_gate_cd", now);

        if (level.dimension() == realm) {
            ServerLevel overworld = server.overworld();
            BlockPos ret = StoryData.getReturn(sp, realm);
            if (ret == null) {
                ret = overworld.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING, overworld.getSharedSpawnPos());
            }
            sp.changeDimension(overworld, RealmTeleporter.toPos(ret));
        } else {
            ServerLevel dest = server.getLevel(realm);
            if (dest == null) return;
            if (level.dimension() == Level.OVERWORLD) StoryData.setReturn(sp, realm, pos);
            sp.changeDimension(dest, RealmTeleporter.toRealm(realm));
        }
        sp.displayClientMessage(Component.translatable("message.starfall.gate." + realm.location().getPath()), true);
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource r) {
        for (int i = 0; i < 2; i++) {
            level.addParticle(ParticleTypes.PORTAL, pos.getX() + r.nextDouble(), pos.getY() + r.nextDouble(),
                    pos.getZ() + r.nextDouble(), 0.0D, 0.05D, 0.0D);
        }
    }
}
