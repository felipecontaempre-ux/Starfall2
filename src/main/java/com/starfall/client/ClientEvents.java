package com.starfall.client;

import com.starfall.Starfall;
import com.starfall.registry.ModEntities;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.registries.RegistryObject;

@Mod.EventBusSubscriber(modid = Starfall.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public class ClientEvents {

    @SubscribeEvent
    public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions event) {
        for (String name : RigLayers.NAMES) {
            event.registerLayerDefinition(RigLayers.layer(name), () -> RigModel.createLayer(RigDef.get(name)));
        }
    }

    private static <T extends Mob> void rig(EntityRenderersEvent.RegisterRenderers e,
                                            RegistryObject<EntityType<T>> type, String name, float shadow, float scale) {
        e.registerEntityRenderer(type.get(), ctx -> new RigRenderer<T>(ctx, name, shadow, scale));
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers e) {
        rig(e, ModEntities.THORN_MATRIARCH, "thorn_matriarch", 1.6F, 1.4F);
        rig(e, ModEntities.STORM_SOVEREIGN, "storm_sovereign", 1.4F, 1.5F);
        rig(e, ModEntities.GLOOM_KING, "gloom_king", 1.2F, 1.4F);
        rig(e, ModEntities.AURELION, "aurelion", 1.2F, 1.45F);
        rig(e, ModEntities.THORNBACK, "thornback", 0.6F, 1.0F);
        rig(e, ModEntities.STORMWISP, "stormwisp", 0.3F, 1.0F);
        rig(e, ModEntities.GLOOM_CRAWLER, "gloom_crawler", 0.7F, 1.0F);
        rig(e, ModEntities.LUMISTAG, "lumistag", 0.6F, 1.0F);
        rig(e, ModEntities.CLOUD_PUFF, "cloud_puff", 0.4F, 1.0F);
        rig(e, ModEntities.MOSSLING, "mossling", 0.4F, 1.0F);
        e.registerEntityRenderer(ModEntities.LOREKEEPER.get(), LorekeeperRenderer::new);
    }
}
