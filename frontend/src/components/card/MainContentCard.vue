<!-- frontend/src/components/card/MainContentCard.vue -->
<template>
   <div>
      <!-- Card Header -->
      <!-- <div
         class="px-3 py-1 sm:px-6 sm:py-3 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800"
      >
         <div>
            <h4 class="text-lg font-semibold text-gray-800 dark:text-gray-100 flex items-center gap-2">
               <slot name="icon">
                  <i class="fa-solid fa-info-circle text-blue-500 text-xl"></i>
               </slot>
               <slot name="title">Default Title</slot>
            </h4>
         </div>
         <div>
            <slot name="header-right"></slot>
         </div>
      </div> -->

      <div
         class="px-3 py-2 sm:px-6 sm:py-3 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
         <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
            <!-- Title section - 60% on large devices -->
            <!-- <div class="w-full lg:w-3/5"> -->
            <div class="w-full lg:w-1/2">
               <h4 class="text-base sm:text-lg font-semibold text-gray-800 dark:text-gray-100 flex items-center gap-2">
                  <slot name="icon">
                     <i class="fa-solid fa-info-circle text-blue-500 text-lg sm:text-xl"></i>
                  </slot>
                  <span class="truncate">
                     <slot name="title">Default Title</slot>
                  </span>
               </h4>
            </div>

            <!-- Header right section - 40% on large devices -->
            <!-- <div v-if="$slots['header-right']"
               class="w-full lg:w-2/5 pt-2 sm:pt-0 border-t sm:border-0 border-gray-200 dark:border-gray-700"> -->
            <div v-if="$slots['header-right']"
               class="w-full lg:w-1/2 pt-2 sm:pt-0 border-t sm:border-0 border-gray-200 dark:border-gray-700">
               <!-- Content right aligned on desktop -->
               <div class="flex flex-wrap items-center gap-2 justify-start lg:justify-end">
                  <slot name="header-right"></slot>
               </div>
            </div>
         </div>
      </div>

      <!-- Error State -->
      <div v-if="error">
         <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong class="font-bold">Error: </strong>
            <span class="block sm:inline">{{ error }}</span>
         </div>
      </div>

      <!-- Card Body -->
      <slot name="body"></slot>
   </div>
</template>

<script setup>
defineProps({
   error: {
      type: String,
      default: '',
   },
});
</script>
<style scoped>
/* @media (max-width: 640px) {
   .header-right-content {
      display: flex;
      justify-content: flex-start; 
      width: 100%;
   }
} */
</style>