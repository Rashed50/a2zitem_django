<template>
  <div>
    <label v-if="label" class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-200">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    <div class="space-y-3">
      <Checkbox
        v-for="option in options"
        :key="option.value"
        :label="option.label"
        :model-value="modelValue.includes(option.value)"
        @update:model-value="toggleOption(option.value)"
      />
    </div>
    <p v-if="error" class="mt-1 text-xs text-red-600">{{ error }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  options: { type: Array, required: true }, // [{ label: "Shop", value: "shop" }]
  label: String,
  required: Boolean,
  error: String
});

const emit = defineEmits(['update:modelValue']);

const toggleOption = (value) => {
  const arr = [...props.modelValue];
  if (arr.includes(value)) {
    arr.splice(arr.indexOf(value), 1);
  } else {
    arr.push(value);
  }
  emit('update:modelValue', arr);
};
</script>