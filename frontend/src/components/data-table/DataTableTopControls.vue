<!-- src/components/data-table/DataTableTopControls.vue -->
<template>
  <div class="flex flex-col gap-4 p-3 sm:p-2 bg-gray-50 dark:bg-gray-900/30 rounded-lg border border-gray-200 dark:border-gray-700">
    <!-- Desktop Layout (lg and above) -->
    <div class="hidden lg:flex items-center justify-between gap-4">
      <!-- Show Entries -->
      <div class="flex items-center gap-2 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
        <i class="fa-solid fa-list-ol text-blue-500 text-sm"></i>
        <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Show</label>
        <select
          :value="entriesPerPage"
          @change="updateEntriesPerPage($event.target.value)"
          class="min-w-[60px] border-0 bg-transparent px-2 py-1 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 dark:focus:ring-gray-300 rounded"
        >
          <option value="2">2</option>
          <option value="10">10</option>
          <option value="25">25</option>
          <option value="50">50</option>
          <option value="100">100</option>
        </select>
        <span class="text-sm text-gray-500 dark:text-gray-400">Entries</span>
      </div>

      <!-- Bulk Actions -->
      <div
        v-if="selectedRows.length > 0"
        class="flex items-center gap-3 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm"
      >
        <i class="fa-solid fa-layer-group text-green-500 text-sm"></i>
        <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
          {{ selectedRows.length }} selected
        </span>
        <select
          :value="bulkAction"
          @change="updateBulkAction($event.target.value)"
          class="border-0 bg-transparent px-2 py-1 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 rounded min-w-32"
        >
          <option value="">Bulk Actions</option>
          <option value="activate">Activate</option>
          <option value="deactivate">Deactivate</option>
          <option value="delete">Delete</option>
          <option value="export">Export</option>
        </select>
        <button
          @click="$emit('bulk-apply')"
          class="px-3 py-1 bg-green-500 hover:bg-green-600 text-white text-sm rounded-lg transition-colors duration-200 flex items-center gap-1"
        >
          <i class="fa-solid fa-play text-xs"></i>
          Apply
        </button>
      </div>

      <!-- Search -->
      <div class="relative flex-1 max-w-md">
        <input
          type="text"
          :value="searchQuery"
          @input="updateSearchQuery($event.target.value)"
          :placeholder="searchPlaceholder"
          class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 dark:focus:ring-gray-300 focus:border-transparent shadow-sm transition-all duration-200 text-sm"
        />
        <i class="fa-solid fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm"></i>
        <i
          v-if="searchQuery"
          @click="clearSearch"
          class="fa-solid fa-times absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 cursor-pointer text-sm"
        ></i>
      </div>
    </div>

    <!-- Mobile & Tablet Layout -->
    <div class="flex flex-col gap-3 lg:hidden">
      <!-- Search -->
      <div class="relative">
        <input
          type="text"
          :value="searchQuery"
          @input="updateSearchQuery($event.target.value)"
          :placeholder="searchPlaceholder"
          class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 dark:focus:ring-gray-300 focus:border-transparent shadow-sm transition-all duration-200 text-sm"
        />

        <i class="fa-solid fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm"></i>
        <i
          v-if="searchQuery"
          @click="clearSearch"
          class="fa-solid fa-times absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 cursor-pointer text-sm"
        ></i>
      </div>

      <!-- Entries + Bulk Actions -->
      <div class="flex flex-col sm:flex-row gap-3 justify-between">
        <!-- Show Entries -->
        <div class="flex items-center gap-2 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm w-full sm:w-auto">
          <i class="fa-solid fa-list-ol text-blue-500 text-sm"></i>
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Show</label>
          <select
            :value="entriesPerPage"
            @change="updateEntriesPerPage($event.target.value)"
            class="min-w-[60px] border-0 bg-transparent px-2 py-1 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded flex-1 sm:flex-none"
          >
            <option value="2">2</option>
            <option value="10">10</option>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
          <span class="text-sm text-gray-500 dark:text-gray-400 hidden sm:block">Entries</span>
        </div>

        <!-- Bulk Actions Mobile -->
        <div
          v-if="selectedRows.length > 0"
          class="flex items-center gap-2 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm w-full sm:w-auto"
        >
          <i class="fa-solid fa-layer-group text-green-500 text-sm"></i>
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ selectedRows.length }}</span>
          <select
            :value="bulkAction"
            @change="updateBulkAction($event.target.value)"
            class="border-0 bg-transparent px-2 py-1 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 rounded flex-1 sm:flex-none min-w-24"
          >
            <option value="">Actions</option>
            <option value="activate">Activate</option>
            <option value="deactivate">Deactivate</option>
            <option value="delete">Delete</option>
            <option value="export">Export</option>
          </select>
          <button
            @click="$emit('bulk-apply')"
            class="px-3 py-1 bg-green-500 hover:bg-green-600 text-white text-sm rounded-lg transition-colors duration-200 flex items-center gap-1"
          >
            <i class="fa-solid fa-play text-xs"></i>
            <span class="hidden sm:block">Apply</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  entriesPerPage: { type: [String, Number], required: true },
  searchQuery: { type: String, default: '' },
  bulkAction: { type: String, default: '' },
  selectedRows: { type: Array, default: () => [] },
  searchPlaceholder: { type: String, default: 'Search...' }
})

const emit = defineEmits([
  'update:entriesPerPage',
  'update:searchQuery',
  'update:bulkAction',
  'entries-change',
  'search-input',
  'clear-search',
  'bulk-apply'
])

// Entries Per Page
const updateEntriesPerPage = (value) => {
  const num = Number(value)
  emit('update:entriesPerPage', num)
  emit('entries-change', num)
}

// Search Query
const updateSearchQuery = (value) => {
  emit('update:searchQuery', value)
  emit('search-input', value)
}

const clearSearch = () => {
  emit('update:searchQuery', '')
  emit('clear-search')
}

// Bulk Action
const updateBulkAction = (value) => {
  emit('update:bulkAction', value)
}
</script>