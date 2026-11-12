package com.starfall.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.starfall.Starfall;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.EyesLayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.Mob;

/** Renderer generico: modelo RigModel + textura + camada que brilha no escuro. */
public class RigRenderer<T extends Mob> extends MobRenderer<T, RigModel<T>> {
    private final ResourceLocation texture;
    private final float scale;

    public RigRenderer(EntityRendererProvider.Context ctx, String name, float shadow, float scale) {
        super(ctx, new RigModel<T>(ctx.bakeLayer(RigLayers.layer(name)), RigDef.get(name)), shadow * scale);
        this.texture = Starfall.id("textures/entity/" + name + ".png");
        this.scale = scale;
        if (RigDef.get(name).hasGlow) {
            final ResourceLocation glow = Starfall.id("textures/entity/" + name + "_glow.png");
            this.addLayer(new EyesLayer<T, RigModel<T>>(this) {
                @Override
                public RenderType renderType() {
                    return RenderType.eyes(glow);
                }
            });
        }
    }

    @Override
    protected void scale(T entity, PoseStack ps, float partialTick) {
        float s = scale * (entity.isBaby() ? 0.55F : 1.0F);
        ps.scale(s, s, s);
    }

    @Override
    public ResourceLocation getTextureLocation(T entity) {
        return texture;
    }
}
