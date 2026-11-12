package com.starfall.event;

import com.starfall.Starfall;
import com.starfall.block.StoryData;
import com.starfall.registry.ModArmorMaterials;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraftforge.event.entity.living.LivingEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/** Bonus de conjunto completo + preservacao do progresso da historia ao morrer. */
@Mod.EventBusSubscriber(modid = Starfall.MOD_ID)
public class PlayerEvents {

    private static boolean fullSet(Player p, ArmorMaterial mat) {
        for (EquipmentSlot slot : new EquipmentSlot[]{EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET}) {
            if (!(p.getItemBySlot(slot).getItem() instanceof ArmorItem a) || a.getMaterial() != mat) return false;
        }
        return true;
    }

    @SubscribeEvent
    public static void onTick(LivingEvent.LivingTickEvent event) {
        if (!(event.getEntity() instanceof Player p) || p.level().isClientSide || p.tickCount % 40 != 0) return;

        if (fullSet(p, ModArmorMaterials.VERDITE)) {
            p.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 100, 0, true, false, true));
        }
        if (fullSet(p, ModArmorMaterials.AERITE)) {
            p.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING, 100, 0, true, false, true));
            p.addEffect(new MobEffectInstance(MobEffects.JUMP, 100, 1, true, false, true));
        }
        if (fullSet(p, ModArmorMaterials.UMBRAL)) {
            p.addEffect(new MobEffectInstance(MobEffects.NIGHT_VISION, 420, 0, true, false, true));
            p.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 100, 0, true, false, true));
        }
    }

    @SubscribeEvent
    public static void onClone(PlayerEvent.Clone event) {
        StoryData.tag(event.getEntity()).merge(StoryData.tag(event.getOriginal()));
    }
}
