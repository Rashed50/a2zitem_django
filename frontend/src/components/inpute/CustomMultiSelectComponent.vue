<!-- src/components/inpute/CustomMultiSelectComponent.vue -->
<template>
   <div class="w-full">
      <!-- Label -->
      <label v-if="label" :for="computedId" class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
         {{ label }}
         <span v-if="required" class="text-red-500 ml-1" aria-hidden="true">*</span>
      </label>

      <!-- Field Wrapper -->
      <div ref="selectWrapper" class="relative">
         <!-- Input Field -->
         <div
            ref="selectRef"
            :class="['relative rounded-sm shadow-sm flex items-start min-h-[40px]', disabled ? 'opacity-60 pointer-events-none' : '']"
            @click.stop="toggleDropdown"
         >
            <!-- Prefix -->
            <span v-if="$slots.prefix" class="absolute left-0 pl-3 flex items-center pointer-events-none top-2">
               <slot name="prefix"></slot>
            </span>

            <!-- Inner Field -->
            <div
               :id="computedId"
               :class="[
                  'flex flex-wrap items-center gap-1.5 w-full bg-white dark:bg-gray-800 border transition-all duration-200 cursor-pointer rounded-sm focus:outline-none',
                  sizeClasses.input,
                  hasPrefix ? 'pl-10' : 'pl-3',
                  hasSuffix ? 'pr-10' : 'pr-3',
                  error
                     ? 'border-red-500 focus:border-red-500 focus:ring-1 focus:ring-red-500 focus:shadow-[0_0_0_3px_rgba(239,68,68,0.25)]'
                     : 'border-gray-300 dark:border-gray-700 focus:border-indigo-700 dark:focus:border-gray-300 focus:ring-1 focus:ring-indigo-600 dark:focus:ring-gray-300 focus:shadow-[0_0_0_3px_rgba(79,70,229,0.25)] dark:focus:shadow-none',
                  isOpen ? 'ring-1 ring-indigo-600 dark:ring-gray-300 shadow-[0_0_0_3px_rgba(79,70,229,0.25)] dark:shadow-none' : '',
               ]"
               tabindex="0"
               @focus="onFocus"
               @blur="onBlur"
            >
               <!-- Selected Tags -->
               <span
                  v-for="item in safeModelValue"
                  :key="getValue(item)"
                  class="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200 mt-1"
               >
                  {{ getLabel(item) }}
                  <button v-if="!disabled" @click.stop="removeItem(item)" class="ml-1 focus:outline-none">
                     <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                     </svg>
                  </button>
               </span>

               <!-- Search Input (IME safe + force re-render) -->
               <input
                  v-if="searchable && isOpen"
                  :value="searchQuery"
                  @input="handleSearchInput"
                  @compositionstart="isComposing = true"
                  @compositionend="isComposing = false; handleSearchInput($event)"
                  @keydown.down.prevent="focusNext"
                  @keydown.up.prevent="focusPrev"
                  @keydown.enter.prevent="selectFocused"
                  @keydown.esc="closeDropdown"
                  type="text"
                  :placeholder="safeModelValue.length === 0 ? placeholder : ''"
                  class="flex-1 min-w-[120px] text-sm text-gray-900 dark:text-gray-100 bg-transparent outline-none border-0 ring-0 shadow-none px-0 py-0 focus:outline-none focus:border-0 focus:ring-0 focus:shadow-none mt-1"
                  ref="searchInput"
                  @focus.stop
               />

               <!-- Placeholder -->
               <span v-else-if="safeModelValue.length === 0" class="text-gray-500 dark:text-gray-400 text-sm mt-1">
                  {{ placeholder }}
               </span>
            </div>

            <!-- Clear Button -->
            <button v-if="showClear" @click.prevent="clear" type="button" class="absolute right-10 top-1/2 -translate-y-1/2" aria-label="Clear">
               <svg class="h-4 w-4 text-gray-500 hover:text-gray-700 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
               </svg>
            </button>

            <!-- Arrow -->
            <i :class="['fa-solid fa-caret-down absolute right-3 top-3 text-xs text-gray-500 transition-transform', showClear ? 'right-10' : 'right-3', isOpen ? 'rotate-180' : '']"></i>
         </div>

         <!-- Mobile Dropdown -->
         <div
            v-if="isMobile"
            ref="dropdownRef"
            class="absolute z-50 left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-sm shadow-lg max-h-60 overflow-auto"
            :style="{ width: dropdownWidth + 'px' }"
            v-show="isOpen"
            @touchmove="handleTouchMove"
         >
            <div
               v-for="(option, index) in filteredOptions"
               :key="getUniqueKey(option)"
               @click="toggleSelection(option)"
               class="px-3 py-2 cursor-pointer flex items-center justify-between text-sm transition-colors"
               :class="{
                  'bg-green-100 dark:bg-green-900/40 text-green-800 dark:text-green-200 hover:bg-red-100 dark:hover:bg-red-900/30': isSelected(option),
                  'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-900 dark:text-gray-100': !isSelected(option),
                  'bg-gray-50 dark:bg-gray-700': focusedIndex === index,
               }"
            >
               <span class="text-gray-900 dark:text-gray-100">{{ getLabel(option) }}</span>
               <svg v-if="isSelected(option)" class="w-4 h-4 text-indigo-600 dark:text-indigo-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
               </svg>
            </div>
            <div v-if="!filteredOptions.length" class="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">
               No options found
            </div>
         </div>

         <!-- PC Dropdown (teleport) -->
         <teleport to="body" v-else>
            <div
               v-show="isOpen"
               ref="dropdownRef"
               class="fixed bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-sm shadow-lg max-h-60 overflow-auto z-[9999]"
               :style="dropdownStyle"
            >
               <div
                  v-for="(option, index) in filteredOptions"
                  :key="getUniqueKey(option)"
                  @click="toggleSelection(option)"
                  class="px-3 py-2 cursor-pointer flex items-center justify-between text-sm transition-colors"
                  :class="{
                     'bg-green-100 dark:bg-green-900/40 text-green-800 dark:text-green-200 hover:bg-red-100 dark:hover:bg-red-900/30': isSelected(option),
                     'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-900 dark:text-gray-100': !isSelected(option),
                     'bg-gray-50 dark:bg-gray-700': focusedIndex === index,
                  }"
               >
                  <span class="text-gray-900 dark:text-gray-100">{{ getLabel(option) }}</span>
                  <svg v-if="isSelected(option)" class="w-4 h-4 text-indigo-600 dark:text-indigo-400" fill="currentColor" viewBox="0 0 20 20">
                     <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                  </svg>
               </div>
               <div v-if="!filteredOptions.length" class="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">
                  No options found
               </div>
            </div>
         </teleport>
      </div>

      <!-- Error / Help -->
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
   name: 'CustomMultiSelectComponent',
   props: {
      modelValue: { type: [Array, null], default: null },
      options: { type: Array, required: true },
      labelKey: { type: String, default: 'label' },
      valueKey: { type: String, default: 'value' },
      label: { type: String, default: '' },
      placeholder: { type: String, default: 'Select...' },
      multiple: { type: Boolean, default: false },
      searchable: { type: Boolean, default: true },
      disabled: { type: Boolean, default: false },
      required: { type: Boolean, default: false },
      error: { type: [String, Boolean], default: '' },
      helpText: { type: String, default: '' },
      size: { type: String, default: 'sm' },
      id: { type: String, default: '' },
      name: { type: String, default: '' },
      clearable: { type: Boolean, default: false },
      validated: { type: Boolean, default: false },
      returnObject: { type: Boolean, default: false },
   },
   emits: ['update:modelValue', 'change', 'focus', 'blur'],

   data() {
      return {
         isOpen: false,
         searchQuery: '',
         isComposing: false,
         focusedIndex: -1,
         dropdownWidth: 0,
         dropdownStyle: {},
         isMobile: window.innerWidth <= 768,
         forceRender: 0,
      };
   },

   computed: {
      computedId() {
         return this.id || this.name || `multiselect-${Math.random().toString(36).substr(2, 9)}`;
      },

      safeModelValue() {
         const raw = this.multiple
            ? Array.isArray(this.modelValue) ? this.modelValue : []
            : this.modelValue != null ? [this.modelValue] : [];
         return raw.filter(item => this.getLabel(item)?.trim());
      },

      filteredOptions() {
         this.forceRender; // force re-compute
         const query = this.searchQuery.trim().toLowerCase();
         if (!query) return this.options;

         const words = query.split(/\s+/).filter(Boolean);
         return this.options.filter(opt => {
            const label = this.getLabel(opt).toLowerCase();
            return words.every(word => label.includes(word));
         });
      },

      hasPrefix() {
         return !!this.$slots?.prefix;
      },

      hasSuffix() {
         return !!this.$slots?.suffix || this.showClear;
      },

      showClear() {
         return this.clearable && !this.disabled && (this.multiple ? this.safeModelValue.length > 0 : this.safeModelValue[0] != null);
      },

      sizeClasses() {
         const map = {
            sm: { input: 'py-1.5 px-2 text-sm' },
            md: { input: 'py-2 px-3 text-sm' },
            lg: { input: 'py-3 px-4 text-base' }
         };
         return map[this.size] || map.sm;
      },
   },

   methods: {
      getLabel(opt) {
         if (!opt) return '';
         if (typeof opt === 'string' || typeof opt === 'number') {
            const found = this.options.find(o => this.getValue(o) === opt);
            return found ? found[this.labelKey] : opt;
         }
         return opt[this.labelKey] != null ? String(opt[this.labelKey]) : '';
      },

      getValue(opt) {
         if (!opt) return null;
         return typeof opt === 'object' && opt[this.valueKey] != null ? opt[this.valueKey] : opt;
      },

      getUniqueKey(opt) {
         return `${this.getValue(opt)}-${this.getLabel(opt)}`;
      },

      isSelected(opt) {
         const val = this.getValue(opt);
         if (this.multiple) {
            const selectedVals = this.safeModelValue.map(item => this.returnObject ? this.getValue(item) : item);
            return selectedVals.includes(val);
         }
         const current = this.safeModelValue[0];
         return current != null && (this.returnObject ? this.getValue(current) : current) === val;
      },

      toggleSelection(opt) {
         if (this.disabled) return;
         const item = this.returnObject ? opt : this.getValue(opt);
         let newVal;

         if (!this.multiple) {
            newVal = item;
            this.closeDropdown();
         } else {
            const vals = this.safeModelValue.map(i => this.returnObject ? this.getValue(i) : i);
            const v = this.getValue(opt);
            newVal = vals.includes(v)
               ? this.safeModelValue.filter(i => (this.returnObject ? this.getValue(i) : i) !== v)
               : [...this.safeModelValue, item];
         }

         this.$emit('update:modelValue', newVal);
         this.$emit('change', newVal);
      },

      removeItem(opt) {
         const v = this.returnObject ? this.getValue(opt) : opt;
         const newVal = this.safeModelValue.filter(i => (this.returnObject ? this.getValue(i) : i) !== v);
         this.$emit('update:modelValue', newVal);
         this.$emit('change', newVal);
      },

      clear() {
         this.$emit('update:modelValue', this.multiple ? [] : null);
         this.$emit('change', this.multiple ? [] : null);
      },

      toggleDropdown() {
         if (this.disabled) return;
         document.dispatchEvent(new CustomEvent('close-other-dropdowns', { detail: this.computedId }));
         this.isOpen = !this.isOpen;

         if (this.isOpen && this.searchable) {
            this.$nextTick(() => {
               this.$refs.searchInput?.focus();
            });
         }

         this.updateDropdownWidth();
         if (this.isOpen && !this.isMobile) this.updatePosition();
      },

      closeDropdown() {
         this.isOpen = false;
         this.searchQuery = '';
         this.focusedIndex = -1;
         this.forceRender++;
      },

      onFocus() {
         this.$emit('focus');
      },

      onBlur(e) {
         if (!this.$refs.selectWrapper?.contains(e.relatedTarget)) {
            this.closeDropdown();
            this.$emit('blur', e);
         }
      },

      focusNext() {
         if (!this.filteredOptions.length) return;
         this.focusedIndex = (this.focusedIndex + 1) % this.filteredOptions.length;
      },

      focusPrev() {
         if (!this.filteredOptions.length) return;
         this.focusedIndex = this.focusedIndex <= 0 ? this.filteredOptions.length - 1 : this.focusedIndex - 1;
      },

      selectFocused() {
         if (this.focusedIndex >= 0) {
            this.toggleSelection(this.filteredOptions[this.focusedIndex]);
         }
      },

      updateDropdownWidth() {
         this.$nextTick(() => {
            if (this.$refs.selectRef) {
               this.dropdownWidth = this.$refs.selectRef.offsetWidth;
            }
         });
      },

      updatePosition() {
         if (!this.$refs.selectRef || !this.isOpen || this.isMobile) return;

         this.$nextTick(() => {
            requestAnimationFrame(() => {
               const rect = this.$refs.selectRef.getBoundingClientRect();
               this.dropdownStyle = {
                  position: 'absolute',
                  top: `${rect.top + rect.height + window.pageYOffset}px`,
                  left: `${rect.left + window.pageXOffset}px`,
                  width: `${rect.width}px`,
               };
            });
         });
      },

      handleSearchInput(e) {
         this.searchQuery = e.target.value;
         if (this.isComposing) return;
         this.focusedIndex = -1;
         this.forceRender++; // force filteredOptions recompute
         this.$nextTick(() => {
            if (!this.isMobile && this.isOpen) this.updatePosition();
         });
      },

      handleClickOutside(e) {
         if (this.$refs.selectWrapper && !this.$refs.selectWrapper.contains(e.target)) {
            this.closeDropdown();
         }
      },

      handleTouchMove(e) {
         e.stopPropagation();
         const dropdown = this.$refs.dropdownRef;
         if (dropdown && dropdown.contains(e.target)) {
            return;
         }
         e.preventDefault();
      },
   },

   watch: {
      focusedIndex(idx) {
         this.$nextTick(() => {
            const el = this.$refs.dropdownRef?.children[idx];
            if (el) el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
         });
      },

      isOpen() {
         this.updateDropdownWidth();
         if (this.isOpen && !this.isMobile) this.updatePosition();
      },
   },

   mounted() {
      document.addEventListener('click', this.handleClickOutside);
      window.addEventListener('resize', () => {
         this.isMobile = window.innerWidth <= 768;
         this.updateDropdownWidth();
         if (this.isOpen && !this.isMobile) this.updatePosition();
      });
      window.addEventListener('scroll', this.updatePosition, true);
      if ('visualViewport' in window) {
         window.visualViewport.addEventListener('resize', this.updatePosition);
         window.visualViewport.addEventListener('scroll', this.updatePosition);
      }
      document.addEventListener('close-other-dropdowns', (e) => {
         if (e.detail !== this.computedId) this.closeDropdown();
      });
      this.updateDropdownWidth();
   },

   beforeUnmount() {
      document.removeEventListener('click', this.handleClickOutside);
      window.removeEventListener('resize', this.updatePosition);
      window.removeEventListener('scroll', this.updatePosition, true);
      if ('visualViewport' in window) {
         window.visualViewport.removeEventListener('resize', this.updatePosition);
         window.visualViewport.removeEventListener('scroll', this.updatePosition);
      }
      document.removeEventListener('close-other-dropdowns', () => {});
   },

   updated() {
      this.updateDropdownWidth();
   },
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.15s, transform 0.15s; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-4px); }
</style>