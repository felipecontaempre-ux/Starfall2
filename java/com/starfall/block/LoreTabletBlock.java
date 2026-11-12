package com.starfall.block;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Tabua antiga: conta um trecho da historia do mundo. */
public class LoreTabletBlock extends Block {
    public static final int LINES = 8;
    private static final VoxelShape SHAPE = Block.box(2.0D, 0.0D, 5.0D, 14.0D, 15.0D, 11.0D);
    private final String realm;

    public LoreTabletBlock(String realm, Properties props) {
        super(props);
        this.realm = realm;
    }

    @Override
    public VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
        return SHAPE;
    }

    @Override
    public InteractionResult use(BlockState state, Level level, BlockPos pos, Player player,
                                 InteractionHand hand, BlockHitResult hit) {
        if (!level.isClientSide) {
            long h = pos.asLong();
            int idx = Math.floorMod((int) (h * 31L + (h >>> 11)), LINES);
            player.sendSystemMessage(Component.translatable("lore.starfall." + realm + "." + idx)
                    .withStyle(ChatFormatting.ITALIC, ChatFormatting.GRAY));
            if (StoryData.readTablet(player, pos)) {
                player.displayClientMessage(Component.translatable("message.starfall.tablet.new",
                        StoryData.tabletsRead(player)), true);
            }
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
}
