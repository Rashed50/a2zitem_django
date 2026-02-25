<template>
  <div class="w-full">
    <!-- Label -->
    <label v-if="label" :for="computedId" class="block text-sm font-medium mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>

    <!-- Multiselect -->
    <Multiselect
      :id="computedId"
      v-model="internalValue"
      :options="props.options"
      :multiple="props.multiple"
      :searchable="true"
      :clear-on-select="!props.multiple"
      :close-on-select="!props.multiple"
      track-by="value"
      label="label"
      :placeholder="props.placeholder"
      @focus="onFocus"
      @blur="onBlur"
      input-class="border-gray-300 focus:border-purple-600 focus:ring-1 focus:ring-purple-600"
    />

    <!-- Help / Error -->
    <p v-if="props.error" class="mt-1 text-xs text-red-600">
      <i class="fa-solid fa-triangle-exclamation"></i>
      {{ props.error }}
    </p>
    <p v-else-if="props.helpText" class="mt-1 text-xs text-gray-500">
      <i class="fa-solid fa-triangle-exclamation"></i>
      {{ props.helpText }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import Multiselect from 'vue-multiselect';
import 'vue-multiselect/dist/vue-multiselect.css';

const props = defineProps({
  modelValue: { type: [Array, Object, String, Number], default: () => [] },
  options: { type: Array, default: () => [] },
  label: { type: String, default: '' },
  placeholder: { type: String, default: 'Select...' },
  error: { type: [String, Boolean], default: '' },
  helpText: { type: String, default: '' },
  required: { type: Boolean, default: false },
  multiple: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  id: { type: String, default: '' }
});

const emit = defineEmits(['update:modelValue', 'focus', 'blur']);

const internalValue = ref(props.modelValue);

watch(internalValue, (val) => emit('update:modelValue', val));
watch(() => props.modelValue, (val) => internalValue.value = val);

const computedId = computed(() => props.id || `multiselect-${Math.floor(Math.random() * 10000)}`);

function onFocus() {
  emit('focus');
}

function onBlur() {
  emit('blur');
}
</script>

<style scoped>
/* .multiselect__input:focus {
    outline: none !important;
    box-shadow: none !important;
    border-color: transparent !important;
} */
</style>
