package com.starfall.entity;

import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.util.Mth;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.*;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.AbstractArrow;
import net.minecraft.world.entity.projectile.Arrow;
import net.minecraft.world.entity.projectile.LargeFireball;
import net.minecraft.world.entity.projectile.WitherSkull;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.registries.ForgeRegistries;

import javax.annotation.Nullable;
import java.util.List;

/**
 * Base de todos os bosses: barra de vida, fases por % de vida, invulnerabilidade na
 * transicao e uma biblioteca de ataques reutilizaveis (pisao, empurrao, raios, meteoros...).
 */
public abstract class BaseBoss extends Monster {
    private static final EntityDataAccessor<Integer> DATA_PHASE =
            SynchedEntityData.defineId(BaseBoss.class, EntityDataSerializers.INT);

    protected final ServerBossEvent bossBar;
    protected int attackTimer = 0;
    protected int transitionTicks = 0;
    protected int riftTicks = 0;

    protected BaseBoss(EntityType<? extends Monster> type, Level level, BossEvent.BossBarColor color, int xp) {
        super(type, level);
        this.bossBar = new ServerBossEvent(type.getDescription(), color, BossEvent.BossBarOverlay.NOTCHED_10);
        this.xpReward = xp;
        this.setPersistenceRequired();
    }

    public static AttributeSupplier.Builder bossAttributes(double hp, double speed, double damage, double armor) {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, hp)
                .add(Attributes.MOVEMENT_SPEED, speed)
                .add(Attributes.ATTACK_DAMAGE, damage)
                .add(Attributes.FOLLOW_RANGE, 64.0D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0D)
                .add(Attributes.ARMOR, armor);
    }

    // ------------------------------------------------------------------ fases
    protected abstract int maxPhase();

    protected abstract void abilities(int phase, LivingEntity target, ServerLevel sl);

    protected void onPhase(int phase, ServerLevel sl) {}

    protected void tickBoss(ServerLevel sl) {}

    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        this.entityData.define(DATA_PHASE, 1);
    }

    public int getPhase() {
        return this.entityData.get(DATA_PHASE);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.0D, true));
        this.goalSelector.addGoal(5, new WaterAvoidingRandomStrollGoal(this, 0.8D));
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 16.0F));
        this.goalSelector.addGoal(7, new RandomLookAroundGoal(this));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        ServerLevel sl = (ServerLevel) this.level();
        bossBar.setProgress(this.getHealth() / this.getMaxHealth());

        int wanted = Mth.clamp(1 + (int) ((1.0F - this.getHealth() / this.getMaxHealth()) * maxPhase()), 1, maxPhase());
        if (wanted > getPhase()) enterPhase(wanted, sl);

        tickBoss(sl);

        if (riftTicks > 0) {
            riftTicks--;
            pull(sl, 22.0D, 0.10D);
            sl.sendParticles(ParticleTypes.PORTAL, getX(), getY() + 1.5D, getZ(), 30, 2.0, 1.5, 2.0, 0.5);
            if (riftTicks == 0) slam(sl, 9.0D, 16.0F);
        }

        if (transitionTicks > 0) {
            transitionTicks--;
            sl.sendParticles(ParticleTypes.END_ROD, getX(), getY() + 2.0D, getZ(), 12, 1.2, 1.8, 1.2, 0.05);
            return;
        }
        LivingEntity target = this.getTarget();
        if (target == null || !target.isAlive()) {
            attackTimer = 0;
            return;
        }
        attackTimer++;
        abilities(getPhase(), target, sl);
    }

    protected boolean every(int n) {
        return attackTimer % n == 0;
    }

    private void enterPhase(int p, ServerLevel sl) {
        this.entityData.set(DATA_PHASE, p);
        this.transitionTicks = 50;
        this.attackTimer = 0;
        this.playSound(SoundEvents.ENDER_DRAGON_GROWL, 5.0F, 0.5F);
        if (p == 2) bossBar.setColor(BossEvent.BossBarColor.PINK);
        else if (p == 3) bossBar.setColor(BossEvent.BossBarColor.RED);
        else if (p >= 4) bossBar.setColor(BossEvent.BossBarColor.WHITE);

        String id = ForgeRegistries.ENTITY_TYPES.getKey(this.getType()).getPath();
        Component msg = Component.translatable("message.starfall.phase." + id + "." + p);
        for (ServerPlayer pl : bossBar.getPlayers()) {
            pl.displayClientMessage(msg, true);
        }
        sl.sendParticles(ParticleTypes.EXPLOSION_EMITTER, getX(), getY() + 2.0D, getZ(), 1, 0, 0, 0, 0);
        onPhase(p, sl);
    }

    // ------------------------------------------------------------------ biblioteca de ataques
    protected List<Player> playersNear(ServerLevel sl, double r) {
        return sl.getEntitiesOfClass(Player.class, getBoundingBox().inflate(r, r / 2.0D, r),
                p -> p.isAlive() && !p.isSpectator());
    }

    protected void ring(ServerLevel sl, ParticleOptions particle, double r) {
        for (int i = 0; i < 36; i++) {
            double a = i * Math.PI / 18.0D;
            sl.sendParticles(particle, getX() + Math.cos(a) * r, getY() + 0.3D, getZ() + Math.sin(a) * r,
                    1, 0.0D, 0.05D, 0.0D, 0.01D);
        }
    }

    /** Pisao: dano e arremesso em quem estiver perto. */
    protected void slam(ServerLevel sl, double radius, float damage) {
        sl.playSound(null, blockPosition(), SoundEvents.GENERIC_EXPLODE, SoundSource.HOSTILE, 2.0F, 0.6F);
        for (Player p : playersNear(sl, radius)) {
            p.hurt(this.damageSources().mobAttack(this), damage);
            Vec3 away = p.position().subtract(this.position()).normalize();
            p.setDeltaMovement(away.x * 1.2D, 0.9D, away.z * 1.2D);
            p.hurtMarked = true;
        }
        for (double r = 1.5D; r <= radius; r += 1.5D) ring(sl, ParticleTypes.CLOUD, r);
    }

    /** Onda de vento: empurra longe, com dano opcional. */
    protected void push(ServerLevel sl, double r, double strength, float dmg) {
        sl.playSound(null, blockPosition(), SoundEvents.PHANTOM_FLAP, SoundSource.HOSTILE, 3.0F, 0.5F);
        for (Player p : playersNear(sl, r)) {
            Vec3 d = p.position().subtract(this.position()).normalize();
            p.setDeltaMovement(d.x * strength, 0.6D, d.z * strength);
            p.hurtMarked = true;
            if (dmg > 0.0F) p.hurt(this.damageSources().mobAttack(this), dmg);
        }
        ring(sl, ParticleTypes.CLOUD, 2.0D);
        ring(sl, ParticleTypes.CLOUD, 5.0D);
    }

    /** Puxa jogadores para o boss (usado a cada tick durante a fenda). */
    protected void pull(ServerLevel sl, double r, double strength) {
        for (Player p : playersNear(sl, r)) {
            Vec3 d = this.position().subtract(p.position()).normalize();
            p.setDeltaMovement(p.getDeltaMovement().add(d.scale(strength)));
            p.hurtMarked = true;
        }
    }

    /** Leque de caveiras de Wither. */
    protected void shootSkulls(LivingEntity target, int count, double spread) {
        this.playSound(SoundEvents.WITHER_SHOOT, 2.0F, 0.7F);
        double dx = target.getX() - getX();
        double dz = target.getZ() - getZ();
        double len = Math.sqrt(dx * dx + dz * dz) + 1.0E-4D;
        for (int i = 0; i < count; i++) {
            double a = (i - (count - 1) / 2.0D) * spread;
            double rx = dx * Math.cos(a) - dz * Math.sin(a);
            double rz = dx * Math.sin(a) + dz * Math.cos(a);
            double sy = getEyeY() - 0.3D;
            double dy = target.getY(0.5D) - sy;
            WitherSkull skull = new WitherSkull(this.level(), this, rx, dy, rz);
            skull.setPos(getX() + rx / len * 1.8D, sy, getZ() + rz / len * 1.8D);
            this.level().addFreshEntity(skull);
        }
    }

    /** Bolas de fogo caindo do ceu ao redor do alvo. */
    protected void meteors(ServerLevel sl, LivingEntity target, int count) {
        this.playSound(SoundEvents.BLAZE_SHOOT, 3.0F, 0.5F);
        for (int i = 0; i < count; i++) {
            double x = target.getX() + (this.random.nextDouble() - 0.5D) * 14.0D;
            double z = target.getZ() + (this.random.nextDouble() - 0.5D) * 14.0D;
            LargeFireball f = new LargeFireball(sl, this, 0.0D, -1.0D, 0.0D, 2);
            f.setPos(x, target.getY() + 22.0D + this.random.nextInt(6), z);
            f.setDeltaMovement(0.0D, -0.8D, 0.0D);
            sl.addFreshEntity(f);
        }
    }

    protected void lightningAt(ServerLevel sl, Vec3 pos) {
        LightningBolt bolt = EntityType.LIGHTNING_BOLT.create(sl);
        if (bolt != null) {
            bolt.moveTo(pos);
            sl.addFreshEntity(bolt);
        }
    }

    /** Anel de flechas espalhadas para todos os lados. */
    protected void arrowRing(ServerLevel sl, int n, float damage) {
        this.playSound(SoundEvents.CROSSBOW_SHOOT, 3.0F, 0.6F);
        for (int i = 0; i < n; i++) {
            double a = i * Math.PI * 2.0D / n;
            Arrow arrow = new Arrow(sl, getX(), getY() + 1.2D, getZ());
            arrow.setOwner(this);
            arrow.setBaseDamage(damage / 2.0D);
            arrow.shoot(Math.cos(a), 0.05D, Math.sin(a), 1.1F, 0.0F);
            arrow.pickup = AbstractArrow.Pickup.DISALLOWED;
            sl.addFreshEntity(arrow);
        }
    }

    /** Teleporta para perto do alvo. */
    protected void blink(ServerLevel sl, LivingEntity target) {
        sl.sendParticles(ParticleTypes.REVERSE_PORTAL, getX(), getY() + 2.0D, getZ(), 60, 0.8, 1.5, 0.8, 0.2);
        double ang = this.random.nextDouble() * Math.PI * 2.0D;
        this.randomTeleport(target.getX() + Math.cos(ang) * 5.0D, target.getY(), target.getZ() + Math.sin(ang) * 5.0D, true);
        sl.sendParticles(ParticleTypes.REVERSE_PORTAL, getX(), getY() + 2.0D, getZ(), 60, 0.8, 1.5, 0.8, 0.2);
    }

    /** Invoca lacaios (respeitando um limite). */
    protected <T extends Mob> void summon(ServerLevel sl, EntityType<T> type, int count, int cap) {
        int existing = sl.getEntities(type, getBoundingBox().inflate(40.0D), e -> true).size();
        if (existing >= cap) return;
        this.playSound(SoundEvents.EVOKER_PREPARE_SUMMON, 3.0F, 0.6F);
        for (int i = 0; i < count; i++) {
            T m = type.create(sl);
            if (m == null) continue;
            double ang = i * (Math.PI * 2.0D / count) + this.random.nextDouble();
            m.moveTo(getX() + Math.cos(ang) * 4.0D, getY(), getZ() + Math.sin(ang) * 4.0D, this.random.nextFloat() * 360.0F, 0.0F);
            m.finalizeSpawn(sl, sl.getCurrentDifficultyAt(blockPosition()), MobSpawnType.MOB_SUMMONED, null, null);
            m.setTarget(this.getTarget());
            sl.addFreshEntity(m);
            sl.sendParticles(ParticleTypes.LARGE_SMOKE, m.getX(), m.getY() + 1.0D, m.getZ(), 20, 0.3, 0.8, 0.3, 0.02);
        }
    }

    // ------------------------------------------------------------------ combate
    protected boolean immuneTo(DamageSource source) {
        return source.is(DamageTypeTags.IS_EXPLOSION);
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (transitionTicks > 0 && !source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) return false;
        if (immuneTo(source)) return false;
        return super.hurt(source, Math.min(amount, 40.0F));
    }

    @Override
    public boolean canBeAffected(MobEffectInstance effect) {
        return effect.getEffect() != MobEffects.WITHER && super.canBeAffected(effect);
    }

    @Override
    protected boolean isImmobile() {
        return super.isImmobile() || transitionTicks > 0;
    }

    @Override
    public boolean canChangeDimensions() {
        return false;
    }

    @Override
    public boolean removeWhenFarAway(double distance) {
        return false;
    }

    // ------------------------------------------------------------------ barra de vida / NBT
    @Override
    public void startSeenByPlayer(ServerPlayer player) {
        super.startSeenByPlayer(player);
        bossBar.addPlayer(player);
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        bossBar.removePlayer(player);
    }

    @Override
    public void setCustomName(@Nullable Component name) {
        super.setCustomName(name);
        bossBar.setName(this.getDisplayName());
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("Phase", getPhase());
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        if (tag.contains("Phase")) this.entityData.set(DATA_PHASE, tag.getInt("Phase"));
        if (this.hasCustomName()) bossBar.setName(this.getDisplayName());
    }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.RAVAGER_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.RAVAGER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.RAVAGER_DEATH; }
}
