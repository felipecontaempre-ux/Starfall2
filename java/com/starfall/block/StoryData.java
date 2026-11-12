package com.starfall.block;

import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/** Progresso da historia guardado no jogador (sobrevive a morte via PlayerEvents). */
public final class StoryData {
    private static final String ROOT = "PlayerPersisted";

    private StoryData() {}

    public static CompoundTag tag(Player p) {
        CompoundTag data = p.getPersistentData();
        if (!data.contains(ROOT, 10)) data.put(ROOT, new CompoundTag());
        return data.getCompound(ROOT);
    }

    public static int chapter(Player p) { return tag(p).getInt("starfall_chapter"); }
    public static void setChapter(Player p, int c) { tag(p).putInt("starfall_chapter", c); }

    public static int claimed(Player p) { return tag(p).getInt("starfall_claimed"); }
    public static void setClaimed(Player p, int c) { tag(p).putInt("starfall_claimed", c); }

    public static int tabletsRead(Player p) { return tag(p).getLongArray("starfall_tablets").length; }

    /** @return true se for uma tabua nova. */
    public static boolean readTablet(Player p, BlockPos pos) {
        CompoundTag t = tag(p);
        long[] a = t.getLongArray("starfall_tablets");
        long key = pos.asLong();
        for (long l : a) if (l == key) return false;
        long[] n = new long[a.length + 1];
        System.arraycopy(a, 0, n, 0, a.length);
        n[a.length] = key;
        t.putLongArray("starfall_tablets", n);
        return true;
    }

    public static void setReturn(Player p, ResourceKey<Level> realm, BlockPos pos) {
        tag(p).putLong("starfall_ret_" + realm.location().getPath(), pos.asLong());
    }

    public static BlockPos getReturn(Player p, ResourceKey<Level> realm) {
        String k = "starfall_ret_" + realm.location().getPath();
        CompoundTag t = tag(p);
        return t.contains(k) ? BlockPos.of(t.getLong(k)) : null;
    }
}
