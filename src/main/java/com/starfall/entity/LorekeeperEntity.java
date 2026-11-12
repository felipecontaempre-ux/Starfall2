package com.starfall.entity;

import com.starfall.block.StoryData;
import com.starfall.registry.ModBlocks;
import com.starfall.registry.ModItems;
import net.minecraft.network.chat.Component;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;

/**
 * O Guardiao das Historias: NPC que narra a lenda da Estrela Partida e guia o jogador
 * por capitulos. Mostre a ele o fragmento do capitulo (segurando na mao) para avancar.
 */
public class LorekeeperEntity extends PathfinderMob {
    public LorekeeperEntity(EntityType<? extends PathfinderMob> type, Level level) {
        super(type, level);
        this.setPersistenceRequired();
    }

    public static AttributeSupplier.Builder createAttributes() {
        return PathfinderMob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 40.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.22D);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(1, new LookAtPlayerGoal(this, Player.class, 8.0F));
        this.goalSelector.addGoal(2, new WaterAvoidingRandomStrollGoal(this, 0.5D));
        this.goalSelector.addGoal(3, new RandomLookAroundGoal(this));
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) return super.hurt(source, amount);
        return false;
    }

    @Override
    public boolean removeWhenFarAway(double distance) {
        return false;
    }

    private void say(Player p, String key) {
        p.sendSystemMessage(Component.translatable("npc.starfall.say", this.getDisplayName(), Component.translatable(key)));
    }

    private static void give(Player p, ItemStack stack) {
        if (!p.getInventory().add(stack)) p.drop(stack, false);
    }

    private static boolean holding(Player p, Item item) {
        return p.getMainHandItem().is(item);
    }

    @Override
    protected InteractionResult mobInteract(Player player, InteractionHand hand) {
        if (hand != InteractionHand.MAIN_HAND) return InteractionResult.PASS;
        if (this.level().isClientSide) return InteractionResult.SUCCESS;

        int ch = StoryData.chapter(player);

        // recompensa por tabuas lidas (3 novas = presente)
        if (ch >= 1 && StoryData.tabletsRead(player) - StoryData.claimed(player) * 3 >= 3) {
            StoryData.setClaimed(player, StoryData.claimed(player) + 1);
            say(player, "npc.starfall.tablets");
            give(player, new ItemStack(ModItems.GLOW_FRUIT.get(), 6));
            give(player, new ItemStack(Items.EMERALD, 4));
            return InteractionResult.CONSUME;
        }

        switch (ch) {
            case 0 -> {
                say(player, "npc.starfall.0");
                give(player, new ItemStack(ModBlocks.WHISPER_GATE.get().asItem(), 2));
                StoryData.setChapter(player, 1);
            }
            case 1 -> {
                if (holding(player, ModItems.VERDANT_SHARD.get())) {
                    say(player, "npc.starfall.1b");
                    give(player, new ItemStack(ModBlocks.SKY_GATE.get().asItem(), 2));
                    StoryData.setChapter(player, 2);
                } else say(player, "npc.starfall.1");
            }
            case 2 -> {
                if (holding(player, ModItems.TEMPEST_SHARD.get())) {
                    say(player, "npc.starfall.2b");
                    give(player, new ItemStack(ModBlocks.UMBRAL_GATE.get().asItem(), 2));
                    StoryData.setChapter(player, 3);
                } else say(player, "npc.starfall.2");
            }
            case 3 -> {
                if (holding(player, ModItems.UMBRAL_SHARD.get())) {
                    say(player, "npc.starfall.3b");
                    StoryData.setChapter(player, 4);
                } else say(player, "npc.starfall.3");
            }
            case 4 -> {
                if (holding(player, ModItems.STAR_FRAGMENT.get())) {
                    say(player, "npc.starfall.4b");
                    give(player, new ItemStack(ModItems.STAR_MEDAL.get(), 1));
                    give(player, new ItemStack(Items.DIAMOND, 16));
                    StoryData.setChapter(player, 5);
                } else say(player, "npc.starfall.4");
            }
            default -> say(player, "npc.starfall.5");
        }
        return InteractionResult.CONSUME;
    }
}
