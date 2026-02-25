<template>
  <div class="flex items-center">
    <input
      :id="computedId"
      :name="groupName"
      type="radio"
      :value="value"
      :checked="modelValue === value"
      @change="$emit('update:modelValue', value)"
      :disabled="disabled"
      class="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-600 dark:bg-gray-700"
    />
    <label
      :for="computedId"
      class="ml-3 block text-sm font-medium text-gray-700 dark:text-gray-200"
    >
      {{ label }}
    </label>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: [String, Number, Boolean],
  value: [String, Number, Boolean],
  label: String,
  groupName: String,
  disabled: Boolean
});

const computedId = computed(() => `radio-${props.value}-${useId()}`);
</script>