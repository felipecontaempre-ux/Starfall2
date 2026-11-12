package com.starfall.item;

import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.LargeFireball;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

import javax.annotation.Nullable;
import java.util.List;

/** Armas especiais com habilidades ativas. */
public final class WeaponItems {
    private WeaponItems() {}

    private static void tip(List<Component> tips, String key, ChatFormatting color) {
        tips.add(Component.translatable(key).withStyle(color));
    }

    /** Cajado Verdante: cura voce, jogadores e pets proximos. */
    public static class VerdantStaff extends Item {
        public VerdantStaff(Properties p) { super(p); }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (level instanceof ServerLevel sl) {
                AABB box = player.getBoundingBox().inflate(8.0D);
                for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, box,
                        x -> x instanceof Player || (x instanceof TamableAnimal t && t.isTame()))) {
                    e.heal(6.0F);
                    e.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 100, 1));
                    sl.sendParticles(ParticleTypes.HAPPY_VILLAGER, e.getX(), e.getY(0.5D), e.getZ(), 12, 0.4, 0.6, 0.4, 0.05);
                }
                sl.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 1.5F, 0.9F);
                stack.hurtAndBreak(1, player, p -> p.broadcastBreakEvent(hand));
            }
            player.getCooldowns().addCooldown(this, 160);
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
        }

        @Override
        public void appendHoverText(ItemStack s, @Nullable Level l, List<Component> tips, TooltipFlag f) {
            tip(tips, "tooltip.starfall.verdant_staff", ChatFormatting.GREEN);
        }
    }

    /** Cajado do Vento: impulso para frente/cima e empurra inimigos. */
    public static class WindStaff extends Item {
        public WindStaff(Properties p) { super(p); }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            Vec3 look = player.getLookAngle();
            player.setDeltaMovement(look.x * 1.1D, 0.9D, look.z * 1.1D);
            player.hurtMarked = true;
            player.fallDistance = 0.0F;
            if (level instanceof ServerLevel sl) {
                AABB box = player.getBoundingBox().inflate(6.0D);
                for (LivingEntity e : sl.getEntitiesOfClass(LivingEntity.class, box, x -> x != player)) {
                    e.setDeltaMovement(look.x * 1.5D, 0.5D, look.z * 1.5D);
                    e.hurtMarked = true;
                }
                sl.sendParticles(ParticleTypes.CLOUD, player.getX(), player.getY(0.3D), player.getZ(), 40, 0.5, 0.2, 0.5, 0.15);
                sl.playSound(null, player.blockPosition(), SoundEvents.PHANTOM_FLAP, SoundSource.PLAYERS, 1.5F, 1.4F);
                stack.hurtAndBreak(1, player, p -> p.broadcastBreakEvent(hand));
            }
            player.getCooldowns().addCooldown(this, 40);
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
        }

        @Override
        public void appendHoverText(ItemStack s, @Nullable Level l, List<Component> tips, TooltipFlag f) {
            tip(tips, "tooltip.starfall.wind_staff", ChatFormatting.AQUA);
        }
    }

    /** Foice Umbria: escuridao + roubo de vida; botao direito = passo sombrio. */
    public static class GloomScythe extends SwordItem {
        public GloomScythe(Tier tier, int dmg, float speed, Properties p) { super(tier, dmg, speed, p); }

        @Override
        public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
            target.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 100, 0), attacker);
            target.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0), attacker);
            attacker.heal(1.5F);
            return super.hurtEnemy(stack, target, attacker);
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (player instanceof ServerPlayer sp) {
                Vec3 eye = sp.getEyePosition();
                Vec3 look = sp.getLookAngle();
                Vec3 end = eye.add(look.scale(10.0D));
                BlockHitResult hit = level.clip(new ClipContext(eye, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, sp));
                Vec3 dest = hit.getType() == HitResult.Type.MISS ? end : hit.getLocation().subtract(look.scale(0.6D));
                ((ServerLevel) level).sendParticles(ParticleTypes.SQUID_INK, sp.getX(), sp.getY(0.5D), sp.getZ(), 25, 0.3, 0.6, 0.3, 0.05);
                sp.connection.teleport(dest.x, dest.y - sp.getEyeHeight(), dest.z, sp.getYRot(), sp.getXRot());
                level.playSound(null, sp.blockPosition(), SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 1.0F, 0.6F);
                stack.hurtAndBreak(3, player, p -> p.broadcastBreakEvent(hand));
            }
            player.getCooldowns().addCooldown(this, 80);
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
        }

        @Override
        public void appendHoverText(ItemStack s, @Nullable Level l, List<Component> tips, TooltipFlag f) {
            tip(tips, "tooltip.starfall.gloom_scythe.hit", ChatFormatting.DARK_PURPLE);
            tip(tips, "tooltip.starfall.gloom_scythe.use", ChatFormatting.LIGHT_PURPLE);
        }
    }

    /** Lamina Estelar: incendeia ao acertar; botao direito dispara uma bola estelar. */
    public static class StarBlade extends SwordItem {
        public StarBlade(Tier tier, int dmg, float speed, Properties p) { super(tier, dmg, speed, p); }

        @Override
        public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
            target.setSecondsOnFire(6);
            if (target.level() instanceof ServerLevel sl) {
                sl.sendParticles(ParticleTypes.END_ROD, target.getX(), target.getY(0.5D), target.getZ(), 16, 0.3, 0.5, 0.3, 0.08);
            }
            return super.hurtEnemy(stack, target, attacker);
        }

        @Override
        public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
            ItemStack stack = player.getItemInHand(hand);
            if (!level.isClientSide) {
                Vec3 look = player.getLookAngle();
                LargeFireball ball = new LargeFireball(level, player, look.x, look.y, look.z, 2);
                ball.setPos(player.getX() + look.x * 1.5D, player.getEyeY() - 0.2D + look.y * 1.5D, player.getZ() + look.z * 1.5D);
                level.addFreshEntity(ball);
                level.playSound(null, player.blockPosition(), SoundEvents.BLAZE_SHOOT, SoundSource.PLAYERS, 1.0F, 1.5F);
                stack.hurtAndBreak(4, player, p -> p.broadcastBreakEvent(hand));
            }
            player.getCooldowns().addCooldown(this, 50);
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
        }

        @Override
        public void appendHoverText(ItemStack s, @Nullable Level l, List<Component> tips, TooltipFlag f) {
            tip(tips, "tooltip.starfall.star_blade.hit", ChatFormatting.GOLD);
            tip(tips, "tooltip.starfall.star_blade.use", ChatFormatting.YELLOW);
        }
    }
}
