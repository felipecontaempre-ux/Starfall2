package com.starfall.entity;

import com.starfall.registry.ModEntities;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.BossEvent;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;

/** Aurelion, o Guardiao Caido - chefe final em 4 fases, usa o arsenal de todos os reinos. */
public class AurelionEntity extends BaseBoss {
    public AurelionEntity(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.YELLOW, 1500);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return bossAttributes(900.0D, 0.30D, 20.0D, 14.0D);
    }

    @Override
    protected int maxPhase() {
        return 4;
    }

    @Override
    protected void onPhase(int phase, ServerLevel sl) {
        if (phase >= 3) bossBar.setDarkenScreen(true);
    }

    @Override
    protected void abilities(int phase, LivingEntity target, ServerLevel sl) {
        if (every(60)) shootSkulls(target, 5, 0.25D);
        if (every(100)) slam(sl, 7.0D, 12.0F);
        if (phase >= 2) {
            if (every(140)) blink(sl, target);
            if (every(120)) lightningAt(sl, target.position());
        }
        if (phase >= 3) {
            if (every(120)) meteors(sl, target, 6);
            if (every(220)) {
                summon(sl, ModEntities.STORMWISP.get(), 2, 5);
                summon(sl, ModEntities.GLOOM_CRAWLER.get(), 3, 7);
            }
        }
        if (phase >= 4) {
            if (every(40)) shootSkulls(target, 3, 0.4D);
            if (every(260) && riftTicks == 0) riftTicks = 60;
            if (every(90)) push(sl, 14.0D, 1.4D, 8.0F);
        }
    }
}
