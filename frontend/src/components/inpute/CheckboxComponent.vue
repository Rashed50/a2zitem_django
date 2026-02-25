<!-- frontend/src/components/inpute/CheckboxComponent.vue -->
<template>
   <div>
      <div class="flex items-center">
         <input
            :id="computedId"
            :name="name"
            type="checkbox"
            :checked="modelValue"
            @change="$emit('update:modelValue', $event.target.checked)"
            :disabled="disabled"
            class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600 dark:bg-gray-700 dark:border-gray-600"
         />
         <label
            v-if="label"
            :for="computedId"
            class="ml-3 block text-sm font-medium text-gray-700 dark:text-gray-200 cursor-pointer"
         >
            {{ label }}
            <span v-if="required" class="text-red-500 ml-1">*</span>
         </label>
      </div>
      <p v-if="error" class="mt-1 text-xs text-red-600 dark:text-red-400">
         {{ error }}
      </p>
   </div>
</template>

<script setup>
import { computed, ref } from 'vue';

// একই কাউন্টার ব্যবহার করলাম (গ্লোবাল হিসেবে কাজ করবে)
const idCounter = ref(0);
const generateId = () => `checkbox-${++idCounter.value}`;

const props = defineProps({
   modelValue: Boolean,
   label: String,
   name: String,
   id: String,
   disabled: Boolean,
   required: Boolean,
   error: String,
});

const computedId = computed(() => props.id || props.name || generateId());
</script>
