<!-- src/components/data-table/DataTablePcBody.vue -->
<template>
  <div class="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-lg">
    <table class="w-full min-w-max table-auto text-left">
      <!-- Header -->
      <thead class="sticky top-0 z-50 bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-800 dark:to-blue-900/20">
        <tr>
          <!-- S/N - Always Sticky -->
          <th class="sticky-left-col left-0 z-65 px-4 py-4 text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase w-12 text-center">
            S/N
          </th>

          <!-- Checkbox - Sticky only on Desktop -->
          <th
            v-if="showCheckbox"
            :class="[
              'px-4 py-4 w-12 text-center',
              isDesktop ? 'sticky-left-col z-65' : ''
            ]"
            :style="isDesktop ? { left: '48px' } : {}"
          >
            <input
              type="checkbox"
              v-model="selectAll"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
          </th>

          <!-- Dynamic Columns -->
          <th
            v-for="(col, idx) in columns"
            :key="col.field"
            :class="[
              'px-4 py-4 text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider',
              col.sortable ? 'cursor-pointer hover:text-gray-900 dark:hover:text-gray-200 transition-colors duration-200' : '',
              isColumnSticky(col) ? 'sticky-left-col z-65' : ''
            ]"
            :style="isColumnSticky(col) ? { left: columnLeft(idx) } : {}"
            @click="col.sortable && sortTable(col.field)"
          >
            <div class="flex items-center gap-2">
              {{ col.title }}
              <i
                v-if="col.sortable"
                class="fa-solid text-xs"
                :class="sortColumn === col.field
                  ? sortDirection === 'asc' ? 'fa-arrow-up text-blue-500' : 'fa-arrow-down text-blue-500'
                  : 'fa-sort text-gray-400'"
              ></i>
            </div>
          </th>

          <th class="px-4 py-4 text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase w-32">
            Actions
          </th>
        </tr>
      </thead>

      <!-- Body -->
      <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
        <tr v-if="loading">
          <td :colspan="totalCols" class="px-6 py-8 text-center">
            <i class="fa-solid fa-spinner fa-spin text-blue-500 text-2xl"></i>
          </td>
        </tr>
        <tr v-else-if="!items?.length">
          <td :colspan="totalCols" class="px-6 py-8 text-center text-gray-500">No data found</td>
        </tr>

        <tr
          v-for="(item, index) in items"
          :key="item.id"
          class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        >
          <!-- S/N - Always Sticky -->
          <td
            class="sticky-left-col left-0 z-55 px-2 py-2 text-sm text-center font-medium"
            :class="rowBg(index, item.id)"
          >
            {{ pagination?.showing_from + index }}
          </td>

          <!-- Checkbox - Sticky only on Desktop -->
          <td
            v-if="showCheckbox"
            :class="[
              'px-2 py-2 text-center',
              isDesktop ? 'sticky-left-col z-55' : '',
              rowBg(index, item.id)
            ]"
            :style="isDesktop ? { left: '48px' } : {}"
          >
            <input
              type="checkbox"
              :value="item.id"
              v-model="selectedRows"
              class="w-4 h-4 text-blue-600 rounded"
            />
          </td>

          <!-- Dynamic Cells -->
          <td
            v-for="(col, idx) in columns"
            :key="col.field"
            class="px-2 py-2 text-sm"
            :class="[
              isColumnSticky(col) ? 'sticky-left-col z-55' : '',
              rowBg(index, item.id)
            ]"
            :style="isColumnSticky(col) ? { left: columnLeft(idx) } : {}"
          >
            <slot :name="`cell-${col.field}`" :row="item" :index="index">
              {{ item[col.field] }}
            </slot>
          </td>

          <td class="px-2 py-2 text-sm" :class="rowBg(index, item.id)">
            <slot name="cell-action" :row="item"></slot>
          </td>
        </tr>
      </tbody>

      <tfoot v-if="hasFooter" class="bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <tr>
          <!-- S/N Footer -->
          <td class="sticky-left-col left-0 z-50 px-2 py-3 text-sm font-semibold text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-900"></td>

          <!-- Checkbox Footer (খালি রাখবো) -->
          <td v-if="showCheckbox" :class="['px-2 py-3', isDesktop ? 'sticky-left-col z-50' : '']" :style="isDesktop ? { left: '48px' } : {}" class="bg-gray-100 dark:bg-gray-900"></td>

          <!-- Dynamic Footer Cells -->
          <td
            v-for="(col, idx) in columns"
            :key="col.field"
            class="px-2 py-3 text-sm font-semibold text-gray-700 dark:text-gray-300 text-right"
            :class="[isColumnSticky(col) ? 'sticky-left-col z-50 bg-gray-100 dark:bg-gray-900' : '']"
            :style="isColumnSticky(col) ? { left: columnLeft(idx) } : {}"
          >
            <slot :name="`footer-${col.field}`" :data="footerData">
              {{ footerData[col.field] ?? '' }}
            </slot>
          </td>

          <!-- Actions Footer (খালি) -->
          <td class="px-2 py-3 bg-gray-100 dark:bg-gray-900"></td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  columns: { type: Array, required: true },
  pagination: Object,
  loading: Boolean,
  sortColumn: String,
  sortDirection: { type: String, default: 'asc' },
  selectedRows: Array,
  selectAll: Boolean,
  showCheckbox: { type: Boolean, default: true },
  stickyColumns: { type: Array, default: () => ['name'] },
  footerData: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['update:selectedRows', 'update:selectAll', 'sort'])

// Footer আছে কিনা চেক
const hasFooter = computed(() => {
  return Object.keys(props.footerData).length > 0
})

const isMobile = ref(window.innerWidth <= 640)
const handleResize = () => {
  isMobile.value = window.innerWidth <= 640
}
onMounted(() => window.addEventListener('resize', handleResize))
onUnmounted(() => window.removeEventListener('resize', handleResize))

const isDesktop = computed(() => !isMobile.value)

const selectedRows = computed({
  get: () => props.selectedRows || [],
  set: val => emit('update:selectedRows', val)
})

const selectAll = computed({
  get: () => props.selectAll,
  set: val => {
    emit('update:selectAll', val)
    emit('update:selectedRows', val ? props.items.map(i => i.id) : [])
  }
})

const sortTable = field => emit('sort', field)
const totalCols = computed(() => props.columns.length + (props.showCheckbox ? 2 : 1) + 1)

const isColumnSticky = col => isDesktop.value && props.stickyColumns.includes(col.field)

const columnLeft = idx => {
  if (!isDesktop.value) return null
  const base = props.showCheckbox ? 96 : 48
  const stickyIndex = props.stickyColumns.indexOf(props.columns[idx]?.field)
  if (stickyIndex === -1) return null
  return `${base + stickyIndex * 192}px`
}

const rowBg = (index, id) => {
  const selected = selectedRows.value.includes(id)
  const even = index % 2 === 0
  return {
    'bg-white dark:bg-gray-800': even && !selected,
    'bg-gray-100 dark:bg-gray-700': !even && !selected,
    'bg-blue-50 dark:bg-blue-900/20': selected
  }
}
</script>

<style scoped>
.sticky-left-col {
  position: sticky !important;
  background-color: #ffffff !important;
  background-clip: padding-box !important;
  z-index: 55 !important;
  box-shadow: 3px 0 6px -2px rgba(0, 0, 0, 0.1) !important;
  border-right: 1px solid #e5e7eb !important;
}

.dark .sticky-left-col {
  background-color: #1f2937 !important;
  box-shadow: 3px 0 6px -2px rgba(0, 0, 0, 0.3) !important;
  border-right: 1px solid #374151 !important;
}

.sticky-left-col.bg-white { background-color: #ffffff !important; }
.dark .sticky-left-col.bg-white { background-color: #1f2937 !important; }
.sticky-left-col.bg-gray-100 { background-color: #f3f4f6 !important; }
.dark .sticky-left-col.bg-gray-100 { background-color: #374151 !important; }
.sticky-left-col.bg-blue-50 { background-color: #eff6ff !important; }
.dark .sticky-left-col.bg-blue-50 { background-color: #1e40af !important; }

thead .sticky-left-col { z-index: 65 !important; }

table { table-layout: auto !important; width: 100%; min-width: 600px; border-collapse: separate; border-spacing: 0; }
table td, table th { min-width: 80px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.overflow-x-auto {
  overflow-x: auto !important;
  -webkit-overflow-scrolling: touch;
  background-color: #ffffff;
  border-radius: 0.75rem;
  width: 100%;
}
.dark .overflow-x-auto { background-color: #1f2937; }

@media (max-width: 640px) {
  th, td { padding: 0.5rem 0.375rem !important; font-size: 0.8rem; }
}

/* তোমার আগের সব স্টাইল + ফুটারের জন্য একটু অ্যাডজাস্ট */
tfoot .sticky-left-col {
  background-color: #f3f4f6 !important;
  z-index: 50 !important;
}
.dark tfoot .sticky-left-col {
  background-color: #1f2937 !important;
}
</style>