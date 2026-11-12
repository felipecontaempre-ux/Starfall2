package com.starfall.registry;

import com.starfall.Starfall;
import com.starfall.entity.*;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public class ModEntities {
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(ForgeRegistries.ENTITY_TYPES, Starfall.MOD_ID);

    private static <T extends Entity> RegistryObject<EntityType<T>> reg(
            String name, EntityType.EntityFactory<T> factory, MobCategory cat, float w, float h, boolean fireImmune, int track) {
        return ENTITIES.register(name, () -> {
            EntityType.Builder<T> b = EntityType.Builder.of(factory, cat).sized(w, h).clientTrackingRange(track);
            if (fireImmune) b.fireImmune();
            return b.build(Starfall.id(name).toString());
        });
    }

    // Bosses
    public static final RegistryObject<EntityType<ThornMatriarchEntity>> THORN_MATRIARCH =
            reg("thorn_matriarch", ThornMatriarchEntity::new, MobCategory.MONSTER, 2.6F, 4.6F, true, 12);
    public static final RegistryObject<EntityType<StormSovereignEntity>> STORM_SOVEREIGN =
            reg("storm_sovereign", StormSovereignEntity::new, MobCategory.MONSTER, 2.4F, 2.6F, true, 16);
    public static final RegistryObject<EntityType<GloomKingEntity>> GLOOM_KING =
            reg("gloom_king", GloomKingEntity::new, MobCategory.MONSTER, 2.0F, 3.6F, true, 12);
    public static final RegistryObject<EntityType<AurelionEntity>> AURELION =
            reg("aurelion", AurelionEntity::new, MobCategory.MONSTER, 2.0F, 3.8F, true, 16);

    // Monstros
    public static final RegistryObject<EntityType<ThornbackEntity>> THORNBACK =
            reg("thornback", ThornbackEntity::new, MobCategory.MONSTER, 0.9F, 1.1F, false, 8);
    public static final RegistryObject<EntityType<StormwispEntity>> STORMWISP =
            reg("stormwisp", StormwispEntity::new, MobCategory.MONSTER, 0.7F, 0.9F, true, 8);
    public static final RegistryObject<EntityType<GloomCrawlerEntity>> GLOOM_CRAWLER =
            reg("gloom_crawler", GloomCrawlerEntity::new, MobCategory.MONSTER, 1.2F, 0.8F, false, 8);

    // Animais e NPC
    public static final RegistryObject<EntityType<LumistagEntity>> LUMISTAG =
            reg("lumistag", LumistagEntity::new, MobCategory.CREATURE, 1.0F, 1.6F, false, 10);
    public static final RegistryObject<EntityType<CloudPuffEntity>> CLOUD_PUFF =
            reg("cloud_puff", CloudPuffEntity::new, MobCategory.CREATURE, 0.9F, 0.8F, false, 10);
    public static final RegistryObject<EntityType<MosslingEntity>> MOSSLING =
            reg("mossling", MosslingEntity::new, MobCategory.CREATURE, 0.7F, 0.6F, false, 8);
    public static final RegistryObject<EntityType<LorekeeperEntity>> LOREKEEPER =
            reg("lorekeeper", LorekeeperEntity::new, MobCategory.CREATURE, 0.6F, 1.95F, false, 10);
}
