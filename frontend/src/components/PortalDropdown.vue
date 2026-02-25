<!-- src/components/PortalDropdown.vue -->
<template>
   <teleport to="body">
      <div v-if="open" :style="style" class="fixed z-[9999]">
         <slot></slot>
      </div>
   </teleport>
</template>

<script setup>
defineProps({
   open: Boolean,
   style: Object,
});
</script>