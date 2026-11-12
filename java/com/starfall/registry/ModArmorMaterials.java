package com.starfall.registry;

import com.starfall.Starfall;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.crafting.Ingredient;

import java.util.function.Supplier;

public enum ModArmorMaterials implements ArmorMaterial {
    // protecao na ordem: helmet, chestplate, leggings, boots
    VERDITE("verdite", 24, new int[]{3, 7, 5, 2}, 16, 1.0F, 0.0F, () -> Ingredient.of(ModItems.VERDITE_GEM.get())),
    AERITE("aerite", 30, new int[]{3, 8, 6, 3}, 18, 1.5F, 0.0F, () -> Ingredient.of(ModItems.AERITE_GEM.get())),
    UMBRAL("umbral", 36, new int[]{3, 8, 6, 3}, 14, 2.5F, 0.1F, () -> Ingredient.of(ModItems.UMBRAL_GEM.get()));

    private static final int[] BASE_DURABILITY = {11, 16, 15, 13}; // helmet, chest, legs, boots
    private final String name;
    private final int durabilityMultiplier;
    private final int[] protection;
    private final int enchantability;
    private final float toughness;
    private final float knockbackResistance;
    private final Supplier<Ingredient> repair;

    ModArmorMaterials(String name, int mult, int[] prot, int ench, float tough, float kb, Supplier<Ingredient> repair) {
        this.name = name;
        this.durabilityMultiplier = mult;
        this.protection = prot;
        this.enchantability = ench;
        this.toughness = tough;
        this.knockbackResistance = kb;
        this.repair = repair;
    }

    private static int idx(ArmorItem.Type type) {
        return switch (type) {
            case HELMET -> 0;
            case CHESTPLATE -> 1;
            case LEGGINGS -> 2;
            case BOOTS -> 3;
        };
    }

    @Override public int getDurabilityForType(ArmorItem.Type type) { return BASE_DURABILITY[idx(type)] * durabilityMultiplier; }
    @Override public int getDefenseForType(ArmorItem.Type type) { return protection[idx(type)]; }
    @Override public int getEnchantmentValue() { return enchantability; }
    @Override public SoundEvent getEquipSound() { return SoundEvents.ARMOR_EQUIP_DIAMOND; }
    @Override public Ingredient getRepairIngredient() { return repair.get(); }
    @Override public String getName() { return Starfall.MOD_ID + ":" + name; }
    @Override public float getToughness() { return toughness; }
    @Override public float getKnockbackResistance() { return knockbackResistance; }
}
