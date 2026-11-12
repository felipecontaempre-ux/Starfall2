package com.starfall.registry;

import com.starfall.Starfall;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public class ModTabs {
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, Starfall.MOD_ID);

    public static final RegistryObject<CreativeModeTab> MAIN = TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.starfall.tab"))
                    .icon(() -> new ItemStack(ModItems.STARHEART.get()))
                    .displayItems((params, out) ->
                            ModItems.ITEMS.getEntries().forEach(i -> out.accept(i.get())))
                    .build());
}
