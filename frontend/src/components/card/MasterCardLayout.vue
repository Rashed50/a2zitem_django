<!-- frontend/src/components/card/MasterCardLayout.vue -->
<template>
   <div class="flex flex-col h-full w-full space-y-2">
      <!-- Loading State -->
      <div
         v-if="isLoading"
         class="flex flex-col items-center justify-center h-full py-20"
      >
         <slot name="loading">
            <i class="fa-solid fa-spinner fa-spin text-4xl text-blue-500"></i>
            <p class="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
         </slot>
      </div>

      <!-- Main Content -->
      <div
         v-else
         class="flex-1 bg-white dark:bg-gray-800 rounded-md shadow-md border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden"
      >
         <slot></slot>
      </div>
   </div>
</template>

<script setup>
defineProps({
   isLoading: {
      type: Boolean,
      default: false,
   },
});
</script>
