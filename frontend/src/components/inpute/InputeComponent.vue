<!-- frontend\src\components\inpute\InputeComponent.vue -->
<template>
  <div class="w-full" :class="customClass">
    <!-- label -->
    <label v-if="label" :for="computedId" class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1" aria-hidden="true">*</span>
    </label>

    <!-- input wrapper (handles prefix/suffix) -->
    <div :class="[
      'relative rounded-sm shadow-sm flex items-center',
      sizeClasses.wrapper,
      disabled ? 'opacity-60 pointer-events-none' : ''
    ]">
      <!-- ================================== -->
      <!-- prefix slot (icon etc) Start -->
      <!-- ================================== -->
      <span class="absolute left-0 pl-3 flex items-center"
        :class="{ 'pointer-events-none': !isSearch && !$slots.prefix }">
        <!-- search type হলে icon দেখাবে -->
        <i v-if="isSearch" class="fa-solid fa-magnifying-glass text-gray-500 dark:text-gray-300"></i>
        <!-- normal prefix slot (যখন search না) -->
        <slot v-else name="prefix"></slot>
      </span>
      <!-- ================================== -->
      <!-- prefix slot (icon etc) End -->
      <!-- ================================== -->


      <!-- input / textarea -->
      <component :is="isTextarea ? 'textarea' : 'input'" :id="computedId" :name="name" :type="inputType"
        :placeholder="placeholder" :disabled="disabled" :required="required" :rows="isTextarea ? rows : undefined"
        :value="modelValue" @input="onInput" @blur="onBlur" @focus="$emit('focus')" :class="[
          'block w-full rounded-sm bg-white dark:bg-gray-800 border transition-all duration-200 focus:outline-none',
          sizeClasses.input,
          hasPrefix ? 'pl-10' : 'pl-3',
          hasSuffix ? 'pr-10' : 'pr-3',
          error
            ? 'border-red-500 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:shadow-[0_0_0_3px_rgba(239,68,68,0.25)]'
            : 'border-gray-300 dark:border-gray-700 focus:border-indigo-700 dark:focus:border-gray-300 focus:ring-1 focus:ring-indigo-600 dark:focus:ring-gray-300 focus:shadow-[0_0_0_3px_rgba(79,70,229,0.25)] dark:focus:shadow-none',
          'text-sm text-gray-900 dark:text-gray-100'
        ]" :aria-invalid="error ? 'true' : 'false'"
        :aria-describedby="error ? computedId + '-error' : helpText ? computedId + '-help' : null"
        :aria-required="required ? 'true' : 'false'"></component>

      <!-- =============================== -->
      <!-- suffix slot (icon etc) Start -->
      <!-- =============================== -->
      <span v-if="isPassword" class="absolute right-0 pr-3 flex items-center pointer-events-auto">
        <button type="button" @click="togglePassword"
          class="text-gray-500 hover:text-gray-700 dark:text-gray-300 focus:outline-none" tabindex="-1">
          <i v-if="showPassword" class="fa-solid fa-eye-slash"></i>
          <i v-else class="fa-solid fa-eye"></i>
        </button>
      </span>

      <!-- normal suffix slot (only when NOT password) -->
      <span v-else-if="$slots.suffix" class="absolute right-0 pr-3 flex items-center pointer-events-auto">
        <slot name="suffix"></slot>
      </span>

      <!-- clear button -->
      <button v-if="showClear" @click.prevent="clear" type="button" class="absolute right-0 pr-3" aria-label="Clear">
        <svg class="h-4 w-4 text-gray-500 hover:text-gray-700 dark:text-gray-300" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Search Clear Button -->
      <button v-if="showClearSearch" @click.prevent="clearSearch" type="button"
        class="absolute right-0 pr-3 flex items-center text-gray-500 hover:text-gray-700 dark:text-gray-300 focus:outline-none"
        aria-label="Clear search">
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- help / error text -->
    <p v-if="error" :id="computedId + '-error'" class="mt-1 text-xs text-red-600 dark:text-red-400">
      <i class="fa-solid fa-triangle-exclamation"></i>
      {{ error }}
    </p>
    <p v-else-if="helpText" :id="computedId + '-help'" class="mt-1 text-xs text-gray-500 dark:text-gray-400">
      <i class="fa-solid fa-info"></i>
      {{ helpText }}
    </p>
  </div>
</template>

<script>
export default {
  name: "InputeComponent",
  props: {
    modelValue: { type: [String, Number], default: "" },
    label: { type: String, default: "" },
    type: { type: String, default: "text" },
    placeholder: { type: String, default: "" },
    error: { type: [String, Boolean], default: "" },
    helpText: { type: String, default: "" },
    disabled: { type: Boolean, default: false },
    required: { type: Boolean, default: false },
    name: { type: String, default: "" },
    id: { type: String, default: "" },
    size: { type: String, default: "md" },
    rows: { type: Number, default: 3 },
    maxRows: { type: Number, default: 5 },
    clearable: { type: Boolean, default: false },
    customClass: { type: String, default: "" },
  },
  data() {
    return {
      showPassword: false,
    };
  },
  emits: ["update:modelValue", "blur", "input", "focus"],
  computed: {
    computedId() {
      return this.id || this.name || `input-${this._uid}`;
    },
    inputType() {
      if (this.type === "search") return "text";
      if (this.type === "textarea") return undefined;
      if (this.type === "password") {
        return this.showPassword ? "text" : "password";
      }
      return this.type;
    },
    isSearch() {
      return this.type === "search";
    },
    isPassword() {
      return this.type === "password";
    },
    isTextarea() {
      return this.type === "textarea";
    },
    hasPrefix() {
      // return !!this.$slots.prefix;
      return !!this.$slots.prefix || this.isSearch;
    },
    hasSuffix() {
      // return !!this.$slots.suffix || this.showClear;
      return !!this.$slots.suffix || this.showClear || this.showClearSearch;
    },
    showClear() {
      return this.clearable && !this.disabled && (this.modelValue !== "" && this.modelValue !== null && this.modelValue !== undefined);
    },
    showClearSearch() {
      return this.isSearch && !this.disabled && this.modelValue && this.modelValue.toString().length > 0;
    },
    sizeClasses() {
      const map = {
        sm: {
          wrapper: "h-8",
          input: "py-1.5 px-2 text-sm",
        },
        md: {
          wrapper: "h-10",
          input: "py-2 px-3 text-sm",
        },
        lg: {
          wrapper: "h-12",
          input: "py-3 px-4 text-base",
        },
      };
      return map[this.size] || map.md;
    },
    textareaStyle() {
      return {
        minHeight: `${this.rows * 24}px`,
        maxHeight: `${this.maxRows * 24}px`,
      };
    },
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    onInput(e) {
      const v = e.target.value;
      this.$emit("update:modelValue", v);
      this.$emit("input", v);
    },
    onBlur(e) {
      this.$emit("blur", e);
    },
    clear() {
      this.$emit("update:modelValue", "");
      this.$emit("input", "");
      // this.$refs && this.$refs.input && (this.$refs.input.value = "");
      this.$nextTick(() => {
        const input = this.$el.querySelector('input, textarea');
        if (input) input.focus();
      });
    },
    clearSearch() {
      this.$emit("update:modelValue", "");
      this.$emit("input", "");
      // search field এ clear করার পর automatically focus
      this.$nextTick(() => {
        const input = this.$el.querySelector('input');
        if (input) input.focus();
      });
    },
  },
};
</script>