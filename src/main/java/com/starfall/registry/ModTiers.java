package com.starfall.registry;

import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.function.Supplier;

public class ModTiers {
    private static Tier make(int level, int uses, float speed, float dmg, int ench, Supplier<Ingredient> repair) {
        return new Tier() {
            @Override public int getUses() { return uses; }
            @Override public float getSpeed() { return speed; }
            @Override public float getAttackDamageBonus() { return dmg; }
            @Override public int getLevel() { return level; }
            @Override public int getEnchantmentValue() { return ench; }
            @Override public Ingredient getRepairIngredient() { return repair.get(); }
        };
    }

    public static final Tier VERDITE = make(2, 750, 7.0F, 2.5F, 16, () -> Ingredient.of(ModItems.VERDITE_GEM.get()));
    public static final Tier AERITE = make(3, 1150, 8.0F, 3.0F, 18, () -> Ingredient.of(ModItems.AERITE_GEM.get()));
    public static final Tier UMBRAL = make(3, 1650, 8.5F, 3.5F, 14, () -> Ingredient.of(ModItems.UMBRAL_GEM.get()));
    public static final Tier STAR = make(4, 3200, 10.0F, 5.0F, 25, () -> Ingredient.of(ModItems.STAR_FRAGMENT.get()));
}
