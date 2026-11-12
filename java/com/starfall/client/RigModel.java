package com.starfall.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.starfall.entity.BaseBoss;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;

import java.util.HashMap;
import java.util.Map;

/**
 * Modelo generico dirigido por dados (RigDef). Animacoes por parte:
 * look, walk, arm, flap, orbit, spin, sway, bob.
 */
public class RigModel<T extends LivingEntity> extends EntityModel<T> {
    private static final float DEG = (float) Math.PI / 180.0F;
    private static final float PI = (float) Math.PI;

    private final ModelPart root;
    private final RigDef def;
    private final ModelPart[] parts;

    public RigModel(ModelPart root, RigDef def) {
        this.root = root;
        this.def = def;
        this.parts = new ModelPart[def.parts.size()];
        for (int i = 0; i < parts.length; i++) {
            ModelPart mp = root;
            for (String seg : def.parts.get(i).path) mp = mp.getChild(seg);
            parts[i] = mp;
        }
    }

    public static LayerDefinition createLayer(RigDef def) {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition rootDef = mesh.getRoot();
        Map<String, PartDefinition> defs = new HashMap<>();
        for (RigDef.Part p : def.parts) {
            PartDefinition parent = p.parent == null ? rootDef : defs.get(p.parent);
            CubeListBuilder b = CubeListBuilder.create().texOffs(p.u, p.v).mirror(p.mirror)
                    .addBox(p.box[0], p.box[1], p.box[2], p.box[3], p.box[4], p.box[5], new CubeDeformation(p.grow));
            PartPose pose = PartPose.offsetAndRotation(p.pivot[0], p.pivot[1], p.pivot[2], p.rot[0], p.rot[1], p.rot[2]);
            defs.put(p.name, parent.addOrReplaceChild(p.name, b, pose));
        }
        return LayerDefinition.create(mesh, def.texW, def.texH);
    }

    private static void addRot(ModelPart mp, String axis, float v) {
        switch (axis) {
            case "y" -> mp.yRot += v;
            case "z" -> mp.zRot += v;
            default -> mp.xRot += v;
        }
    }

    @Override
    public void setupAnim(T e, float limbSwing, float limbSwingAmount, float age, float yaw, float pitch) {
        float phaseBoost = 1.0F;
        if (e instanceof BaseBoss b) phaseBoost = 1.0F + 0.5F * (b.getPhase() - 1);

        for (int i = 0; i < parts.length; i++) {
            RigDef.Part pd = def.parts.get(i);
            if (pd.anims.isEmpty()) continue;
            ModelPart mp = parts[i];
            mp.resetPose();
            for (RigDef.Anim a : pd.anims) {
                switch (a.type) {
                    case "look" -> {
                        float f = (float) a.get("f", 1.0D);
                        mp.yRot += yaw * DEG * f;
                        mp.xRot += pitch * DEG * f;
                    }
                    case "walk" -> {
                        float v = Mth.cos(limbSwing * (float) a.get("speed", 0.6662D) + (float) a.get("phase", 0.0D) * PI)
                                * (float) a.get("amp", 1.2D) * limbSwingAmount;
                        addRot(mp, a.axis, v);
                    }
                    case "arm" -> {
                        float side = (float) a.get("side", 1.0D);
                        float v = Mth.cos(limbSwing * 0.6662F + (float) a.get("phase", 0.0D) * PI)
                                * (float) a.get("amp", 0.9D) * limbSwingAmount;
                        mp.xRot += v;
                        if (e instanceof Mob m && m.isAggressive()) mp.xRot -= (float) a.get("raise", 0.5D);
                        if (e.attackAnim > 0.0F) mp.xRot -= Mth.sin(e.attackAnim * PI) * (float) a.get("swing", 2.0D);
                        mp.zRot += side * (0.06F + Mth.cos(age * 0.09F) * 0.05F);
                    }
                    case "flap" -> {
                        float s = (float) a.get("speed", 0.2D) * (a.get("ps", 0.0D) > 0.0D ? phaseBoost : 1.0F);
                        addRot(mp, a.axis, Mth.sin(age * s + (float) a.get("phase", 0.0D)) * (float) a.get("amp", 0.5D)
                                + (float) a.get("bias", 0.0D));
                    }
                    case "sway" -> addRot(mp, a.axis, Mth.sin(age * (float) a.get("speed", 0.08D) + (float) a.get("phase", 0.0D))
                            * (float) a.get("amp", 0.1D));
                    case "spin" -> addRot(mp, a.axis, age * (float) a.get("speed", 0.1D));
                    case "bob" -> mp.y += Mth.sin(age * (float) a.get("speed", 0.1D) + (float) a.get("phase", 0.0D))
                            * (float) a.get("amp", 1.0D);
                    case "orbit" -> {
                        float speed = (float) a.get("speed", 0.05D) * (a.get("ps", 0.0D) > 0.0D ? phaseBoost : 1.0F);
                        float count = (float) a.get("count", 1.0D);
                        float ang = age * speed + (float) a.get("idx", 0.0D) * (PI * 2.0F / count);
                        float r = (float) a.get("radius", 10.0D);
                        mp.x = pd.pivot[0] + Mth.cos(ang) * r;
                        mp.z = pd.pivot[2] + Mth.sin(ang) * r;
                        mp.y = pd.pivot[1] + Mth.sin(age * 0.1F + (float) a.get("idx", 0.0D)) * (float) a.get("hover", 2.0D);
                        mp.yRot = -ang;
                    }
                    default -> { }
                }
            }
        }
    }

    @Override
    public void renderToBuffer(PoseStack ps, VertexConsumer vc, int light, int overlay,
                               float r, float g, float b, float a) {
        root.render(ps, vc, light, overlay, r, g, b, a);
    }
}
