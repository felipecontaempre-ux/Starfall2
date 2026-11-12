package com.starfall.item;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

import javax.annotation.Nullable;
import java.util.List;

/** Item simples com uma linha de tooltip (e brilho opcional). */
public class TooltipItem extends Item {
    private final String key;
    private final boolean foil;

    public TooltipItem(Properties props, String key, boolean foil) {
        super(props);
        this.key = key;
        this.foil = foil;
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return foil || super.isFoil(stack);
    }

    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tips, TooltipFlag flag) {
        tips.add(Component.translatable(key).withStyle(ChatFormatting.GRAY));
    }
}
