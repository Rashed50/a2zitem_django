<!-- frontend/src/components/inpute/SwitchComponent.vue -->
<template>
   <div>
      <div class="flex items-center gap-3">
         <button
            type="button"
            role="switch"
            :aria-checked="modelValue"
            :aria-labelledby="labelId"
            @click="$emit('update:modelValue', !modelValue)"
            :disabled="disabled"
            :class="[
               'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2',
               modelValue ? 'bg-indigo-600' : 'bg-gray-300 dark:bg-gray-600',
               disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer',
            ]"
         >
            <span
               :class="[
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                  modelValue ? 'translate-x-6' : 'translate-x-1',
               ]"
            />
         </button>
         <label
            v-if="label"
            :id="labelId"
            class="text-sm font-medium text-gray-700 dark:text-gray-200 cursor-pointer"
         >
            {{ label }}
            <span v-if="required" class="text-red-500 ml-1">*</span>
         </label>
      </div>
      <p v-if="error" class="mt-1 text-xs text-red-600">{{ error }}</p>
   </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// নিজের ID জেনারেট করার জন্য একটা গ্লোবাল কাউন্টার
const idCounter = ref(0);
const generateId = () => `switch-${++idCounter.value}`;

const props = defineProps({
   modelValue: Boolean,
   label: String,
   disabled: Boolean,
   required: Boolean,
   error: String,
});

// এখানে useId() বাদ দিয়ে নিজের ফাংশন দিলাম
const labelId = computed(() => (props.label ? generateId() : undefined));
</script>
