package com.starfall.client;

import com.starfall.Starfall;
import com.starfall.entity.LorekeeperEntity;
import net.minecraft.client.model.VillagerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;

/** O NPC reaproveita o modelo de aldeao com uma pele propria. */
public class LorekeeperRenderer extends MobRenderer<LorekeeperEntity, VillagerModel<LorekeeperEntity>> {
    private static final ResourceLocation TEXTURE = Starfall.id("textures/entity/lorekeeper.png");

    public LorekeeperRenderer(EntityRendererProvider.Context ctx) {
        super(ctx, new VillagerModel<>(ctx.bakeLayer(ModelLayers.VILLAGER)), 0.5F);
    }

    @Override
    public ResourceLocation getTextureLocation(LorekeeperEntity entity) {
        return TEXTURE;
    }
}
