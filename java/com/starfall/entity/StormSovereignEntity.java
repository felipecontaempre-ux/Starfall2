package com.starfall.entity;

import com.starfall.registry.ModEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.control.FlyingMoveControl;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.navigation.FlyingPathNavigation;
import net.minecraft.world.entity.ai.navigation.PathNavigation;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/** Soberano da Tempestade - guardiao voador de Skyreach. Raios, ventania e mergulhos. */
public class StormSovereignEntity extends BaseBoss {
    public StormSovereignEntity(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.BLUE, 600);
        this.moveControl = new FlyingMoveControl(this, 20, true);
        this.setNoGravity(true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return bossAttributes(480.0D, 0.30D, 14.0D, 6.0D).add(Attributes.FLYING_SPEED, 0.7D);
    }

    @Override
    protected PathNavigation createNavigation(Level level) {
        FlyingPathNavigation nav = new FlyingPathNavigation(this, level);
        nav.setCanOpenDoors(false);
        nav.setCanFloat(true);
        nav.setCanPassDoors(true);
        return nav;
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.2D, true));
        this.goalSelector.addGoal(5, new WaterAvoidingRandomFlyingGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 16.0F));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) {
        return false;
    }

    @Override
    protected void checkFallDamage(double y, boolean onGround, BlockState state, BlockPos pos) {
    }

    @Override
    protected boolean immuneTo(DamageSource source) {
        return super.immuneTo(source) || source.is(DamageTypeTags.IS_LIGHTNING);
    }

    @Override
    protected int maxPhase() {
        return 3;
    }

    @Override
    protected void abilities(int phase, LivingEntity target, ServerLevel sl) {
        if (every(90)) lightningAt(sl, target.position().add(target.getDeltaMovement().scale(8.0D)));
        if (every(120)) push(sl, 16.0D, 1.5D, 6.0F);
        if (every(170)) dive(target);
        if (phase >= 2) {
            if (every(200)) summon(sl, ModEntities.STORMWISP.get(), 3, 6);
        }
        if (phase >= 3) {
            if (every(50)) {
                double ang = this.random.nextDouble() * Math.PI * 2.0D;
                lightningAt(sl, target.position().add(Math.cos(ang) * 6.0D, 0.0D, Math.sin(ang) * 6.0D));
            }
            if (every(260)) meteors(sl, target, 5);
        }
    }

    private void dive(LivingEntity t) {
        Vec3 d = t.position().add(0.0D, 1.0D, 0.0D).subtract(this.position()).normalize().scale(1.7D);
        this.setDeltaMovement(d);
        this.playSound(net.minecraft.sounds.SoundEvents.PHANTOM_SWOOP, 3.0F, 0.6F);
    }
}
