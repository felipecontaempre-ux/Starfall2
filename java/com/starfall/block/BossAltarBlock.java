package com.starfall.block;

import com.starfall.entity.BaseBoss;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

import java.util.function.Supplier;

/** Altar de desafio: clique com o sigilo certo para invocar o guardiao do reino. */
public class BossAltarBlock extends Block {
    private static final VoxelShape SHAPE = Block.box(1.0D, 0.0D, 1.0D, 15.0D, 12.0D, 15.0D);
    private final Supplier<? extends EntityType<? extends BaseBoss>> boss;
    private final Supplier<? extends Item> sigil;

    public BossAltarBlock(Properties props, Supplier<? extends EntityType<? extends BaseBoss>> boss,
                          Supplier<? extends Item> sigil) {
        super(props);
        this.boss = boss;
        this.sigil = sigil;
    }

    @Override
    public VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
        return SHAPE;
    }

    @Override
    public InteractionResult use(BlockState state, Level level, BlockPos pos, Player player,
                                 InteractionHand hand, BlockHitResult hit) {
        if (level.isClientSide) return InteractionResult.SUCCESS;
        ServerLevel sl = (ServerLevel) level;
        ItemStack stack = player.getItemInHand(hand);

        if (!stack.is(sigil.get())) {
            player.displayClientMessage(Component.translatable("message.starfall.altar.need", sigil.get().getDescription()), true);
            return InteractionResult.CONSUME;
        }
        if (!sl.getEntitiesOfClass(BaseBoss.class, new AABB(pos).inflate(64.0D)).isEmpty()) {
            player.displayClientMessage(Component.translatable("message.starfall.boss_exists"), true);
            return InteractionResult.CONSUME;
        }
        BaseBoss b = boss.get().create(sl);
        if (b == null) return InteractionResult.FAIL;
        b.moveTo(pos.getX() + 0.5D, pos.getY() + 1.0D, pos.getZ() + 0.5D, player.getYRot() + 180.0F, 0.0F);
        b.finalizeSpawn(sl, sl.getCurrentDifficultyAt(pos), MobSpawnType.MOB_SUMMONED, null, null);
        sl.addFreshEntity(b);

        LightningBolt bolt = EntityType.LIGHTNING_BOLT.create(sl);
        if (bolt != null) {
            bolt.moveTo(pos.getX() + 0.5D, pos.getY() + 1.0D, pos.getZ() + 0.5D);
            bolt.setVisualOnly(true);
            sl.addFreshEntity(bolt);
        }
        sl.playSound(null, pos, SoundEvents.WITHER_SPAWN, SoundSource.HOSTILE, 2.0F, 0.7F);
        if (!player.getAbilities().instabuild) stack.shrink(1);
        return InteractionResult.CONSUME;
    }
}
