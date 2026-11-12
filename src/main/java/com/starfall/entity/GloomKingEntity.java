package com.starfall.entity;

import com.starfall.registry.ModEntities;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.BossEvent;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/** Rei Umbrio - guardiao do Reino Umbrio. Escuridao, drenagem de almas e fendas do vazio. */
public class GloomKingEntity extends BaseBoss {
    public GloomKingEntity(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.PURPLE, 700);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return bossAttributes(560.0D, 0.26D, 18.0D, 12.0D);
    }

    @Override
    protected int maxPhase() {
        return 3;
    }

    @Override
    protected void onPhase(int phase, ServerLevel sl) {
        if (phase == 3) bossBar.setDarkenScreen(true);
    }

    @Override
    protected void abilities(int phase, LivingEntity target, ServerLevel sl) {
        if (every(70)) darkPulse(sl);
        if (every(90) && this.distanceToSqr(target) < 144.0D) cleave(sl);
        if (every(130)) soulDrain(sl, target);
        if (phase >= 2) {
            if (every(200)) summon(sl, ModEntities.GLOOM_CRAWLER.get(), 4, 8);
            if (every(150)) blink(sl, target);
        }
        if (phase >= 3) {
            if (every(240) && riftTicks == 0) riftTicks = 70;
            if (every(80)) shootSkulls(target, 3, 0.35D);
        }
    }

    private void darkPulse(ServerLevel sl) {
        for (Player p : playersNear(sl, 14.0D)) {
            p.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 80, 0));
            p.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0));
            p.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0));
        }
        ring(sl, ParticleTypes.SQUID_INK, 3.0D);
        ring(sl, ParticleTypes.SQUID_INK, 7.0D);
        ring(sl, ParticleTypes.SQUID_INK, 11.0D);
    }

    /** Golpe em arco a frente. */
    private void cleave(ServerLevel sl) {
        Vec3 look = this.getLookAngle();
        for (Player p : playersNear(sl, 6.0D)) {
            Vec3 to = p.position().subtract(this.position()).normalize();
            if (look.dot(to) > 0.0D) {
                p.hurt(this.damageSources().mobAttack(this), 16.0F);
                p.setDeltaMovement(to.x * 1.0D, 0.5D, to.z * 1.0D);
                p.hurtMarked = true;
            }
        }
        sl.sendParticles(ParticleTypes.SWEEP_ATTACK, getX() + look.x * 3.0D, getY() + 1.5D, getZ() + look.z * 3.0D, 6, 1.5, 0.5, 1.5, 0.0);
    }

    /** Drena a alma do alvo e se cura. */
    private void soulDrain(ServerLevel sl, LivingEntity t) {
        if (this.distanceToSqr(t) > 400.0D) return;
        t.hurt(this.damageSources().magic(), 8.0F);
        this.heal(15.0F);
        for (int i = 0; i <= 20; i++) {
            double f = i / 20.0D;
            sl.sendParticles(ParticleTypes.SOUL, t.getX() + (getX() - t.getX()) * f, t.getY(0.5D) + (getY(0.6D) - t.getY(0.5D)) * f,
                    t.getZ() + (getZ() - t.getZ()) * f, 1, 0, 0, 0, 0.0);
        }
    }
}
