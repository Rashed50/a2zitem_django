<template>
  <div class="w-full">
    <!-- Label -->
    <label
      v-if="label"
      :for="computedId"
      class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200"
    >
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1" aria-hidden="true">*</span>
    </label>

    <!-- Textarea -->
    <div
      :class="[
        'relative rounded-sm shadow-sm transition-all duration-200',
        disabled ? 'opacity-60 pointer-events-none' : '',
        focused
            ? 'ring-1 ring-indigo-600 dark:ring-gray-300 ring-offset-1 ring-offset-white dark:ring-offset-gray-800'
            : ''
      ]"
    >
      <textarea
        :id="computedId"
        :name="name"
        :rows="rows"
        :placeholder="placeholder"
        :disabled="disabled"
        :value="modelValue"
        @input="onInput"
        @focus="onFocus"
        @blur="onBlur"
        class="block w-full rounded-sm border-[0.5px] bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border-gray-300 dark:border-gray-700 focus:outline-none focus:border-indigo-600 dark:focus:border-gray-300 text-sm px-3 py-2 resize-y min-h-[6rem] transition"

        :aria-invalid="error ? 'true' : 'false'"
        :aria-describedby="error ? computedId + '-error' : helpText ? computedId + '-help' : null"
      ></textarea>
    </div>

    <!-- Help / Error text -->
    <p
      v-if="error"
      :id="computedId + '-error'"
      class="mt-1 text-xs text-red-600 dark:text-red-400"
    >
      {{ error }}
    </p>
    <p
      v-else-if="helpText"
      :id="computedId + '-help'"
      class="mt-1 text-xs text-gray-500 dark:text-gray-400"
    >
      {{ helpText }}
    </p>
  </div>
</template>

<script>
export default {
  name: "TextAreaComponent",
  props: {
    modelValue: { type: [String, Number], default: "" },
    label: { type: String, default: "" },
    placeholder: { type: String, default: "" },
    rows: { type: Number, default: 4 },
    error: { type: [String, Boolean], default: "" },
    helpText: { type: String, default: "" },
    disabled: { type: Boolean, default: false },
    required: { type: Boolean, default: false },
    name: { type: String, default: "" },
    id: { type: String, default: "" },
  },
  emits: ["update:modelValue", "focus", "blur"],
  data() {
    return {
      focused: false,
    };
  },
  computed: {
    computedId() {
      return this.id || this.name || `textarea-${this._uid}`;
    },
  },
  methods: {
    onInput(e) {
      this.$emit("update:modelValue", e.target.value);
    },
    onFocus() {
      this.focused = true;
      this.$emit("focus");
    },
    onBlur(e) {
      this.focused = false;
      this.$emit("blur", e);
    },
  },
};
</script>

<style scoped>
textarea:disabled {
  cursor: not-allowed;
}
</style>
