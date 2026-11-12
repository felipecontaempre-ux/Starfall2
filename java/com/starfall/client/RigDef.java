package com.starfall.client;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.starfall.Starfall;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Definicao de um modelo 3D lida de assets/starfall/rigs/NOME.json.
 * O mesmo JSON (gerado por tools/gen) tambem gera a textura, entao modelo e UV nunca desencontram.
 */
public final class RigDef {
    public static final class Anim {
        public String type = "";
        public String axis = "x";
        public final Map<String, Double> n = new HashMap<>();

        public double get(String key, double def) {
            Double v = n.get(key);
            return v == null ? def : v;
        }
    }

    public static final class Part {
        public String name;
        public String parent;
        public final float[] pivot = new float[3];
        public final float[] rot = new float[3];
        public final float[] box = new float[6];
        public int u, v;
        public float grow;
        public boolean mirror;
        public final List<Anim> anims = new ArrayList<>();
        public String[] path;
    }

    public final List<Part> parts = new ArrayList<>();
    public int texW = 64;
    public int texH = 64;
    public boolean hasGlow;

    private static final Map<String, RigDef> CACHE = new HashMap<>();

    public static synchronized RigDef get(String name) {
        RigDef d = CACHE.get(name);
        if (d == null) {
            d = load(name);
            CACHE.put(name, d);
        }
        return d;
    }

    private static void floats(JsonArray a, float[] out) {
        for (int i = 0; i < out.length && i < a.size(); i++) out[i] = a.get(i).getAsFloat();
    }

    private static RigDef load(String name) {
        String path = "/assets/" + Starfall.MOD_ID + "/rigs/" + name + ".json";
        try (InputStream in = RigDef.class.getResourceAsStream(path)) {
            if (in == null) throw new IllegalStateException("Rig nao encontrado: " + path);
            JsonObject o = JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
            RigDef def = new RigDef();
            def.texW = o.get("texW").getAsInt();
            def.texH = o.get("texH").getAsInt();
            def.hasGlow = o.has("glow") && o.get("glow").getAsBoolean();
            Map<String, Part> byName = new HashMap<>();
            for (JsonElement el : o.getAsJsonArray("parts")) {
                JsonObject po = el.getAsJsonObject();
                Part p = new Part();
                p.name = po.get("name").getAsString();
                p.parent = po.has("parent") && !po.get("parent").isJsonNull() ? po.get("parent").getAsString() : null;
                floats(po.getAsJsonArray("pivot"), p.pivot);
                if (po.has("rot")) floats(po.getAsJsonArray("rot"), p.rot);
                floats(po.getAsJsonArray("box"), p.box);
                JsonArray tex = po.getAsJsonArray("tex");
                p.u = tex.get(0).getAsInt();
                p.v = tex.get(1).getAsInt();
                p.grow = po.has("grow") ? po.get("grow").getAsFloat() : 0.0F;
                p.mirror = po.has("mirror") && po.get("mirror").getAsBoolean();
                if (po.has("anim")) {
                    for (JsonElement ae : po.getAsJsonArray("anim")) {
                        JsonObject ao = ae.getAsJsonObject();
                        Anim a = new Anim();
                        for (Map.Entry<String, JsonElement> e : ao.entrySet()) {
                            switch (e.getKey()) {
                                case "type" -> a.type = e.getValue().getAsString();
                                case "axis" -> a.axis = e.getValue().getAsString();
                                default -> {
                                    JsonElement v = e.getValue();
                                    if (v.getAsJsonPrimitive().isBoolean()) a.n.put(e.getKey(), v.getAsBoolean() ? 1.0D : 0.0D);
                                    else a.n.put(e.getKey(), v.getAsDouble());
                                }
                            }
                        }
                        p.anims.add(a);
                    }
                }
                Part parent = p.parent == null ? null : byName.get(p.parent);
                if (p.parent != null && parent == null) {
                    throw new IllegalStateException("Pai '" + p.parent + "' de '" + p.name + "' nao definido antes em " + name);
                }
                if (parent == null) {
                    p.path = new String[]{p.name};
                } else {
                    p.path = new String[parent.path.length + 1];
                    System.arraycopy(parent.path, 0, p.path, 0, parent.path.length);
                    p.path[parent.path.length] = p.name;
                }
                byName.put(p.name, p);
                def.parts.add(p);
            }
            return def;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
