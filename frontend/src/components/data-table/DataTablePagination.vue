<!-- src/components/data-table/DataTablePagination.vue -->
<template>
  <div class="flex flex-col lg:flex-row justify-between items-center gap-3 p-3 sm:p-2 bg-gray-50 dark:bg-gray-900/30 rounded-lg border border-gray-200 dark:border-gray-700">
    
    <!-- Showing Info -->
    <div class="text-xs sm:text-sm text-gray-600 dark:text-gray-400 font-medium text-center sm:text-left">
      Showing {{ pagination?.showing_from || 0 }} to
      {{ pagination?.showing_to || 0 }} of
      {{ totalItems || 0 }}
      <span v-if="selectedCount > 0" class="text-blue-600 dark:text-blue-400">
        ({{ selectedCount }} selected)
      </span>
    </div>

    <!-- Pagination Controls -->
    <div class="flex items-center space-x-1 sm:space-x-2" v-if="pagination">
      <!-- First -->
      <button
        @click="$emit('page-change', 1)"
        :disabled="currentPage === 1"
        class="p-1 sm:p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200"
        title="First Page"
      >
        <i class="fa-solid fa-angles-left text-xs sm:text-sm"></i>
      </button>

      <!-- Prev -->
      <button
        @click="$emit('page-change', currentPage - 1)"
        :disabled="currentPage === 1"
        class="p-1 sm:p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200"
        title="Previous Page"
      >
        <i class="fa-solid fa-angle-left text-xs sm:text-sm"></i>
      </button>

      <!-- Page Numbers -->
      <button
        v-for="page in visiblePages"
        :key="page"
        @click="$emit('page-change', page)"
        :class="[
          'px-2 sm:px-3 py-1 sm:py-2 rounded-lg border text-xs sm:text-sm font-medium transition-all duration-200 min-w-8 sm:min-w-10',
          currentPage === page
            ? 'bg-gradient-to-r from-blue-500 to-blue-600 border-blue-500 text-white shadow-lg shadow-blue-500/25'
            : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600',
        ]"
      >
        {{ page }}
      </button>

      <!-- Next -->
      <button
        @click="$emit('page-change', currentPage + 1)"
        :disabled="currentPage === pagination.total_pages"
        class="p-1 sm:p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200"
        title="Next Page"
      >
        <i class="fa-solid fa-angle-right text-xs sm:text-sm"></i>
      </button>

      <!-- Last -->
      <button
        @click="$emit('page-change', pagination.total_pages)"
        :disabled="currentPage === pagination.total_pages"
        class="p-1 sm:p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200"
        title="Last Page"
      >
        <i class="fa-solid fa-angles-right text-xs sm:text-sm"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, required: true },
  pagination: { type: Object, default: () => ({}) },
  totalItems: { type: Number, default: 0 },
  selectedCount: { type: Number, default: 0 }
})

defineEmits(['page-change'])

// Responsive visible pages
const visiblePages = computed(() => {
  if (!props.pagination?.total_pages) return []

  const total = props.pagination.total_pages
  const current = props.currentPage
  const maxVisible = window.innerWidth < 640 ? 3 : 5

  let start = Math.max(1, current - Math.floor(maxVisible / 2))
  let end = Math.min(total, start + maxVisible - 1)

  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }

  const pages = []
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})
</script>