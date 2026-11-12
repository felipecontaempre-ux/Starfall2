package com.starfall.client;

import com.starfall.Starfall;
import net.minecraft.client.model.geom.ModelLayerLocation;

import java.util.List;

public final class RigLayers {
    public static final List<String> NAMES = List.of(
            "thorn_matriarch", "storm_sovereign", "gloom_king", "aurelion",
            "thornback", "stormwisp", "gloom_crawler", "lumistag", "cloud_puff", "mossling");

    private RigLayers() {}

    public static ModelLayerLocation layer(String name) {
        return new ModelLayerLocation(Starfall.id(name), "main");
    }
}
