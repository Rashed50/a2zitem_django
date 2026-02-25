<template>
   <div class="w-full space-y-2">
      <!-- Label -->
      <label
         v-if="label"
         class="block text-sm font-semibold text-gray-700 dark:text-gray-200"
      >
         {{ label }}
         <span v-if="required" class="text-red-500 ml-1">*</span>
      </label>

      <!-- Main Container -->
      <div
         ref="container"
         class="flex flex-col md:flex-row gap-3 p-2 bg-white dark:bg-gray-800 rounded-sm border dark:border-gray-700 transition-all duration-200 focus-within:border-indigo-500 dark:focus-within:border-gray-300 focus-within:ring-1 focus-within:ring-indigo-500 dark:focus-within:ring-gray-300 overflow-hidden"
         :class="{
            'border-red-500 ring-2 ring-red-500': hasError,
            'opacity-60 pointer-events-none bg-gray-50 dark:bg-gray-800':
               disabled,
            'h-80': isKeyboardOpen && isMobile,
         }"
         @click="handleContainerClick"
      >
         <!-- Available Items -->
         <div class="flex-1 flex flex-col min-w-0 order-1 md:order-1">
            <div
               class="flex items-center justify-between pb-2 border-b border-gray-300 dark:border-gray-700 gap-2 flex-wrap md:flex-nowrap"
            >
               <span
                  class="text-xs font-semibold text-gray-600 dark:text-gray-300 whitespace-nowrap"
               >
                  Available ({{ filteredAvailable.length }})
               </span>

               <!-- Search -->
               <div class="relative flex-1 w-full md:max-w-[220px]">
                  <input
                     v-model="availableSearch"
                     type="text"
                     placeholder="Search available..."
                     class="w-full pl-10 pr-3 py-2 text-sm rounded-md border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-indigo-500 
                     dark:ring-gray-300 focus:border-indigo-500 dark:focus:border-gray-300 transition"
                     :disabled="disabled"
                     @focus="onSearchFocus"
                     @blur="onSearchBlur"
                     @input="handleSearchInput"
                     ref="availableSearchInput"
                  />
                  <i
                     class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"
                  ></i>
               </div>
            </div>

            <!-- Scrollable List -->
            <div
               ref="availableContainer"
               class="flex-1 mt-2 bg-gray-50 dark:bg-gray-800/50 rounded-md border border-gray-300 dark:border-gray-700 overflow-y-auto p-1.5 min-h-0 custom-scrollbar"
               :style="{ maxHeight: listMaxHeight }"
            >
               <div
                  v-if="loading"
                  class="flex items-center justify-center py-4 text-sm text-gray-500 dark:text-gray-400"
               >
                  <i class="fas fa-spinner fa-spin mr-2"></i> Loading...
               </div>

               <div
                  v-else-if="filteredAvailable.length === 0"
                  class="text-center py-6 text-sm text-gray-500 dark:text-gray-400 italic"
               >
                  {{
                     availableSearch ? 'No items found' : 'No available items'
                  }}
               </div>

               <div v-else class="space-y-1">
                  <label
                     v-for="item in filteredAvailable"
                     :key="getItemKey(item)"
                     class="flex items-start gap-2 p-2 rounded-md cursor-pointer transition-all group min-h-[48px] border border-gray-200 dark:border-gray-700"
                     :class="{
                        'bg-indigo-100 dark:bg-gray-900 ring-1 ring-indigo-500 dark:ring-gray-300':
                           isAvailableSelected(item),
                        'hover:bg-gray-100 dark:hover:bg-gray-700':
                           !isAvailableSelected(item),
                     }"
                     @click="toggleAvailableSelection(item)"
                  >
                     <!-- Checkbox -->
                     <input
                        type="checkbox"
                        :checked="isAvailableSelected(item)"
                        @click.stop="toggleAvailableSelection(item)"
                        class="w-4 h-4 mt-0.5 text-indigo-600 dark:text-gray-600 rounded border-gray-300 dark:border-gray-600 focus:ring-indigo-500 dark:focus:ring-gray-300"
                     />

                     <!-- Option Name -->
                     <span
                        class="flex-1 text-sm font-medium text-gray-800 dark:text-gray-200 break-words whitespace-normal"
                     >
                        {{ getItemDisplay(item) }}
                     </span>

                     <!-- Add Button -->
                     <button
                        @click.stop="moveToChosen(item)"
                        class="w-7 h-7 mt-0.5 rounded-full bg-green-100 dark:bg-green-900/40 text-green-600 dark:text-green-400 flex items-center justify-center hover:bg-green-200 dark:hover:bg-green-800/60 transition opacity-0 group-hover:opacity-100"
                        :disabled="disabled"
                     >
                        <i class="fas fa-plus text-sm"></i>
                     </button>
                  </label>
               </div>
            </div>
         </div>

         <!-- Control Buttons -->
         <div
            class="flex flex-row md:flex-col justify-center items-center gap-2 order-2 md:order-2 py-2 md:py-0"
         >
            <button
               @click="moveSelectedToChosen"
               :disabled="disabled || availableSelected.length === 0"
               class="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400 flex items-center justify-center hover:bg-indigo-200 dark:hover:bg-indigo-800/60 disabled:opacity-50 transition transform hover:scale-110 text-sm"
               title="Move selected"
            >
               <i class="fas fa-chevron-right"></i>
            </button>
            <button
               @click="moveAllToChosen"
               :disabled="disabled || filteredAvailable.length === 0"
               class="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/40 text-indigo-600 dark:text-indigo-400 flex items-center justify-center hover:bg-indigo-200 dark:hover:bg-indigo-800/60 disabled:opacity-50 transition transform hover:scale-110 text-sm"
               title="Move all"
            >
               <i class="fas fa-angle-double-right"></i>
            </button>
            <button
               @click="moveAllToAvailable"
               :disabled="disabled || selectedItems.length === 0"
               class="w-10 h-10 rounded-full bg-red-100 dark:bg-red-900/40 text-red-600 dark:text-red-400 flex items-center justify-center hover:bg-red-200 dark:hover:bg-red-800/60 disabled:opacity-50 transition transform hover:scale-110 text-sm"
               title="Remove all"
            >
               <i class="fas fa-angle-double-left"></i>
            </button>
            <button
               @click="moveSelectedToAvailable"
               :disabled="disabled || chosenSelected.length === 0"
               class="w-10 h-10 rounded-full bg-red-100 dark:bg-red-900/40 text-red-600 dark:text-red-400 flex items-center justify-center hover:bg-red-200 dark:hover:bg-red-800/60 disabled:opacity-50 transition transform hover:scale-110 text-sm"
               title="Remove selected"
            >
               <i class="fas fa-chevron-left"></i>
            </button>
         </div>

         <!-- Selected Items -->
         <div class="flex-1 flex flex-col min-w-0 order-3">
            <div
               class="flex items-center justify-between pb-2 border-b border-gray-300 dark:border-gray-700 gap-2 flex-wrap md:flex-nowrap"
            >
               <span
                  class="text-xs font-semibold text-gray-600 dark:text-gray-300 whitespace-nowrap"
               >
                  Selected ({{ selectedItems.length }})
               </span>

               <!-- Search -->
               <div class="relative flex-1 w-full md:max-w-[220px]">
                  <input
                     v-model="selectedSearch"
                     type="text"
                     placeholder="Search selected..."
                     class="w-full pl-10 pr-3 py-2 text-sm rounded-md border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-indigo-500 
                     dark:ring-gray-300 focus:border-indigo-500 dark:focus:border-gray-300 transition"
                     :disabled="disabled"
                     @focus="onSearchFocus"
                     @blur="onSearchBlur"
                     @input="handleSearchInput"
                     ref="selectedSearchInput"
                  />
                  <i
                     class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"
                  ></i>
               </div>
            </div>

            <!-- Scrollable List -->
            <div
               ref="selectedContainer"
               class="flex-1 mt-2 bg-gray-50 dark:bg-gray-800/50 rounded-md border border-gray-300 dark:border-gray-700 overflow-y-auto p-2 min-h-0 custom-scrollbar"
               :style="{ maxHeight: listMaxHeight }"
            >
               <div
                  v-if="selectedItems.length === 0"
                  class="text-center py-6 text-sm text-gray-500 dark:text-gray-400 italic"
               >
                  No items selected
               </div>
               <div v-else class="space-y-1">
                  <label
                     v-for="item in filteredSelected"
                     :key="getItemKey(item)"
                     class="flex items-start gap-2 p-2 rounded-md cursor-pointer transition-all group min-h-[48px] border border-gray-200 dark:border-gray-700"
                     :class="{
                        'bg-indigo-100 dark:bg-gray-900 ring-2 ring-indigo-500 dark:ring-gray-300':
                           isChosenSelected(item),
                        'hover:bg-gray-100 dark:hover:bg-gray-700':
                           !isChosenSelected(item),
                     }"
                     @click="toggleChosenSelection(item)"
                  >
                     <!-- Checkbox -->
                     <input
                        type="checkbox"
                        :checked="isChosenSelected(item)"
                        @click.stop="toggleChosenSelection(item)"
                        class="w-4 h-4 mt-0.5 text-indigo-600 dark:text-gray-600 rounded border-gray-300 dark:border-gray-600 focus:ring-indigo-500 dark:focus:ring-gray-300"
                     />
                     <span
                        class="flex-1 text-sm font-medium text-gray-800 dark:text-gray-200 line-clamp-2 break-words"
                     >
                        {{ getItemDisplay(item) }}
                     </span>
                     <button
                        @click.stop="moveToAvailable(item)"
                        class="w-7 h-7 mt-0.5 rounded-full bg-red-100 dark:bg-red-900/40 text-red-600 dark:text-red-400 flex items-center justify-center hover:bg-red-200 dark:hover:bg-red-800/60 transition opacity-0 group-hover:opacity-100"
                        :disabled="disabled"
                     >
                        <i class="fas fa-xmark text-sm"></i>
                     </button>
                  </label>
               </div>
            </div>
         </div>
      </div>

      <!-- Validation Message -->
      <p
         v-if="hasError"
         class="mt-1 text-sm text-red-600 dark:text-red-400 font-medium"
      >
         {{ errorMessage || 'This field is required' }}
      </p>
   </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue';

const props = defineProps({
   modelValue: { type: Array, default: () => [] },
   options: { type: Array, required: true },
   label: String,
   trackBy: { type: String, default: 'id' },
   displayBy: { type: String, default: 'name' },
   required: Boolean,
   disabled: Boolean,
   errorMessage: String,
   loading: Boolean,
   validateOnMount: Boolean,
});

const emit = defineEmits(['update:modelValue', 'validation']);

const availableSearch = ref('');
const selectedSearch = ref('');
const availableSelected = ref([]);
const chosenSelected = ref([]);
const isTouched = ref(false);
const isKeyboardOpen = ref(false);
const keyboardCheckInterval = ref(null);
const originalHeight = ref(window.innerHeight);
const screenWidth = ref(window.innerWidth);

const container = ref(null);
const availableContainer = ref(null);
const selectedContainer = ref(null);

// Computed
const isMobile = computed(() => screenWidth.value < 768);

const listMaxHeight = computed(() => {
   return isMobile.value ? '180px' : '220px';
});

const hasError = computed(() => {
   return (
      props.errorMessage ||
      (isTouched.value && props.required && props.modelValue.length === 0)
   );
});

const selectedItems = computed(() => {
   return props.modelValue
      .map((value) =>
         typeof value === 'object'
            ? value
            : props.options.find(
                 (opt) =>
                    (typeof opt === 'object' ? opt[props.trackBy] : opt) ===
                    value
              )
      )
      .filter(Boolean);
});

const availableItems = computed(() => {
   const selectedIds = selectedItems.value.map((i) =>
      typeof i === 'object' ? i[props.trackBy] : i
   );
   return props.options.filter((opt) => {
      const id = typeof opt === 'object' ? opt[props.trackBy] : opt;
      return !selectedIds.includes(id);
   });
});

const filteredAvailable = computed(() =>
   filterItems(availableItems.value, availableSearch.value)
);
const filteredSelected = computed(() =>
   filterItems(selectedItems.value, selectedSearch.value)
);

const filterItems = (items, query) => {
   if (!query?.trim()) return items;
   const words = query.toLowerCase().trim().split(/\s+/).filter(Boolean);
   return items.filter((item) => {
      const text = (
         typeof item === 'object'
            ? item[props.displayBy] || item[props.trackBy]
            : item
      )
         ?.toString()
         .toLowerCase();
      return words.every((word) => text.includes(word));
   });
};

const getItemKey = (item) =>
   typeof item === 'object' ? item[props.trackBy] : item;
const getItemDisplay = (item) =>
   typeof item === 'object'
      ? item[props.displayBy] || item[props.trackBy]
      : item;

const isAvailableSelected = (item) =>
   availableSelected.value.some((s) => getItemKey(s) === getItemKey(item));
const isChosenSelected = (item) =>
   chosenSelected.value.some((s) => getItemKey(s) === getItemKey(item));

// Methods
const markAsTouched = () => {
   if (!isTouched.value) {
      isTouched.value = true;
      emit('validation', { isValid: !hasError.value, isTouched: true });
   }
};

const handleContainerClick = () => markAsTouched();

const toggleAvailableSelection = (item) => {
   markAsTouched();
   const idx = availableSelected.value.findIndex(
      (i) => getItemKey(i) === getItemKey(item)
   );
   if (idx > -1) {
      availableSelected.value.splice(idx, 1);
   } else {
      availableSelected.value.push(item);
   }
};

const toggleChosenSelection = (item) => {
   markAsTouched();
   const idx = chosenSelected.value.findIndex(
      (i) => getItemKey(i) === getItemKey(item)
   );
   if (idx > -1) {
      chosenSelected.value.splice(idx, 1);
   } else {
      chosenSelected.value.push(item);
   }
};

const moveToChosen = (item) => moveItems([item], true);
const moveToAvailable = (item) => moveItems([item], false);

const moveSelectedToChosen = () => {
   moveItems(availableSelected.value, true);
   availableSelected.value = [];
};

const moveSelectedToAvailable = () => {
   moveItems(chosenSelected.value, false);
   chosenSelected.value = [];
};

const moveAllToChosen = () => {
   moveItems(filteredAvailable.value, true);
   availableSearch.value = '';
};

const moveAllToAvailable = () => {
   moveItems(selectedItems.value, false);
   selectedSearch.value = '';
};

const moveItems = (items, toChosen) => {
   markAsTouched();
   const values = [...props.modelValue];
   items.forEach((item) => {
      const val = typeof item === 'object' ? item[props.trackBy] : item;
      if (toChosen) {
         if (!values.includes(val)) values.push(val);
      } else {
         const idx = values.indexOf(val);
         if (idx > -1) values.splice(idx, 1);
      }
   });
   emit('update:modelValue', values);
};

const handleSearchInput = () => {
   nextTick(() => {
      availableContainer.value?.scrollTo(0, 0);
      selectedContainer.value?.scrollTo(0, 0);
   });
};

const onSearchFocus = () => {
   markAsTouched();
   if (isMobile.value) {
      originalHeight.value = window.innerHeight;
      isKeyboardOpen.value = true;
      startKeyboardMonitoring();
   }
};

const onSearchBlur = () => {
   if (isMobile.value) {
      isKeyboardOpen.value = false;
      stopKeyboardMonitoring();
   }
};

const startKeyboardMonitoring = () => {
   stopKeyboardMonitoring();
   keyboardCheckInterval.value = setInterval(() => {
      const diff = originalHeight.value - window.innerHeight;
      isKeyboardOpen.value = diff > 100;
   }, 150);
};

const stopKeyboardMonitoring = () => {
   if (keyboardCheckInterval.value) clearInterval(keyboardCheckInterval.value);
};

const handleResize = () => {
   screenWidth.value = window.innerWidth;
};

onMounted(() => {
   window.addEventListener('resize', handleResize);
   if (props.validateOnMount) isTouched.value = true;
});

onUnmounted(() => {
   window.removeEventListener('resize', handleResize);
   stopKeyboardMonitoring();
});

watch(availableSearch, () =>
   nextTick(() => availableContainer.value?.scrollTo(0, 0))
);
watch(selectedSearch, () =>
   nextTick(() => selectedContainer.value?.scrollTo(0, 0))
);
</script>

<style scoped>
/* Custom Scrollbar */
.custom-scrollbar {
   -webkit-overflow-scrolling: touch;
}

.custom-scrollbar::-webkit-scrollbar {
   width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
   @apply bg-gray-100 dark:bg-gray-800 rounded-full;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
   @apply bg-gray-400 dark:bg-gray-600 rounded-full border-2 border-solid border-white dark:border-gray-900;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
   @apply bg-gray-500 dark:bg-gray-500;
}

/* Firefox */
* {
   scrollbar-width: thin;
   scrollbar-color: #9ca3af #f3f4f6;
}

.dark * {
   scrollbar-color: #6b7280 #1f2937;
}

/* Text Wrap */
.line-clamp-2 {
   display: -webkit-box;
   -webkit-line-clamp: 2;
   -webkit-box-orient: vertical;
   overflow: hidden;
}

.break-words {
   word-break: break-word;
}
</style>
