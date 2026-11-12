package com.starfall.entity;

import com.starfall.registry.ModEntities;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.BossEvent;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.AreaEffectCloud;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/** Matriarca dos Espinhos - guardia do Bosque Sussurrante. Raizes, esporos e espinhos. */
public class ThornMatriarchEntity extends BaseBoss {
    public ThornMatriarchEntity(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.GREEN, 600);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return bossAttributes(520.0D, 0.24D, 16.0D, 8.0D);
    }

    @Override
    protected int maxPhase() {
        return 3;
    }

    @Override
    protected void tickBoss(ServerLevel sl) {
        if (getPhase() >= 3 && this.tickCount % 20 == 0) this.heal(2.0F); // Supercrescimento
    }

    @Override
    protected void abilities(int phase, LivingEntity target, ServerLevel sl) {
        if (every(80)) rootSnare(sl);
        if (every(100)) sporeCloud(sl, target);
        if (phase >= 2) {
            if (every(110)) slam(sl, 6.0D, 10.0F);
            if (every(200)) summon(sl, ModEntities.THORNBACK.get(), 3, 7);
        }
        if (phase >= 3) {
            if (every(140)) arrowRing(sl, 14, 6.0F);
        }
    }

    /** Raizes prendem e machucam quem estiver por perto. */
    private void rootSnare(ServerLevel sl) {
        for (Player p : playersNear(sl, 10.0D)) {
            p.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 3));
            p.hurt(this.damageSources().mobAttack(this), 4.0F);
            sl.sendParticles(ParticleTypes.HAPPY_VILLAGER, p.getX(), p.getY() + 0.2D, p.getZ(), 20, 0.4, 0.1, 0.4, 0.05);
        }
        ring(sl, ParticleTypes.HAPPY_VILLAGER, 4.0D);
    }

    private void sporeCloud(ServerLevel sl, LivingEntity t) {
        AreaEffectCloud c = new AreaEffectCloud(sl, t.getX(), t.getY(), t.getZ());
        c.setOwner(this);
        c.setRadius(3.5F);
        c.setDuration(140);
        c.addEffect(new MobEffectInstance(MobEffects.POISON, 100, 1));
        c.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 100, 0));
        c.setParticle(ParticleTypes.SPORE_BLOSSOM_AIR);
        sl.addFreshEntity(c);
    }
}
