<template>
   <!-- MasterCardLayout -->
   <MasterCardLayout :is-loading="loadingStates.loading">
      <!-- Loading -->
      <template #loading>
         <div class="flex items-center justify-center py-20">
            <i class="fa-solid fa-spinner fa-spin text-3xl text-blue-500"></i>
         </div>
      </template>

      <!-- Main Content Card -->
      <MainContentCard :error="error">
         <!-- Header Icon -->
         <template #icon>
            <i class="fa-solid fa-table-list text-blue-500"></i>
         </template>

         <!-- Header Title -->
         <template #title>
            Category List
         </template>

         <!-- Header Right Side -->
         <template #header-right>
            <!-- Add Button -->
            <ActionButton action="add" size="sm" @click="addItemPage" class="px-8" />

            <!-- Filter Button -->
            <Button type="button" variant="primary" size="sm" @click="showFilter = !showFilter" class="px-8"
               :label="showFilter ? 'Filter Close' : 'Filter Open'"
               :icon-right="showFilter ? 'fa-solid fa-xmark' : 'fa-solid fa-filter'" />
         </template>

         <!-- Card Body -->
         <template #body>
            <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-5 sm:py-3 space-y-4 sm:space-y-2">
               <!-- Filter Section -->
               <transition enter-active-class="transition duration-300 ease-out"
                  enter-from-class="transform opacity-0 -translate-y-2"
                  enter-to-class="transform opacity-100 translate-y-0"
                  leave-active-class="transition duration-200 ease-in"
                  leave-from-class="transform opacity-100 translate-y-0"
                  leave-to-class="transform opacity-0 -translate-y-2">
                  <div v-if="showFilter"
                     class="flex flex-col gap-4 p-3 sm:p-2 bg-gray-50 dark:bg-gray-900/30 rounded-lg border border-gray-200 dark:border-gray-700">
                     <div class="responsive-grid gap-sm">
                        <CustomMultiSelect label="Root Category" v-model="filterForm.parent" :options="categoryChoices"
                           label-key="label" value-key="value" placeholder="Select category" />

                        <CustomMultiSelect label="Status" v-model="filterForm.status" :options="statusChoices"
                           label-key="label" value-key="value" placeholder="Select status" />
                     </div>

                     <!-- Filter Action Buttons -->
                     <div class="flex justify-end gap-2 mt-4">
                        <ActionButton action="export" size="sm" @click="exportData" label="Export" />

                        <Button type="button" variant="outline-danger" size="sm" @click="resetFilters"
                           icon-left="fa-solid fa-filter-circle-xmark">
                           Reset
                        </Button>

                        <ActionButton action="filter" size="sm" @click="applyFilters" label="Apply Filter" />
                     </div>
                  </div>
               </transition>

               <!-- Top Controls -->
               <DataTableTopControls :entries-per-page="entriesPerPage"
                  @update:entries-per-page="entriesPerPage = $event" :search-query="searchQuery"
                  @update:search-query="searchQuery = $event" :bulk-action="bulkAction"
                  @update:bulk-action="bulkAction = $event" :selected-rows="selectedRows"
                  :search-placeholder="'Search subscription plans...'" @entries-change="fetchData"
                  @search-input="onSearchInput" @clear-search="clearSearch" @bulk-apply="executeBulkAction" />

               <!-- Data Table -->
               <div class="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-lg">
                  <DataTablePcBody :items="apiData?.results || []" :columns="tableColumns"
                     :pagination="apiData?.pagination" :loading="loadingStates.loadingTable" :sort-column="sortColumn"
                     :sort-direction="sortDirection" :selected-rows="selectedRows"
                     @update:selected-rows="val => (selectedRows = val)" :select-all="selectAll"
                     @update:select-all="val => (selectAll = val)" :sticky-columns="['name']" :show-checkbox="false"
                     @sort="sortTable" :footer-data="tableFooterData">

                     <!-- Name (Sticky) -->
                     <template #cell-name="{ row }">
                        <div class="font-medium text-gray-900 dark:text-white">
                           {{ row.name || '' }}
                        </div>
                     </template>

                     <!-- Parent Name -->
                     <template #cell-parent="{ row }">
                        <div class="text-gray-500 dark:text-gray-400">
                           {{ row.parent?.name || '' }}
                        </div>
                     </template>

                     <!-- Logo -->
                     <template #cell-logo="{ row }">
                        <div class="flex items-center space-x-2 ms-2">
                           <div v-if="row.logo">
                              <img :src="row.logo" class="w-24 h-24 rounded-md" alt="Logo" />
                           </div>
                           <div v-else
                              class="w-24 h-24 flex items-center justify-center font-bold text-gray-500 dark:text-gray-400">
                              <i class="fa-regular fa-image me-2"></i>
                              <span>Not Uploaded</span>
                           </div>
                        </div>
                     </template>

                     <!-- Created Dates -->
                     <template #cell-created_at="{ row }">
                        <div class="space-y-2 text-xs">
                           <div>
                              <div class="font-medium text-gray-700 dark:text-gray-300">Created By</div>
                              <div class="text-gray-500 dark:text-gray-400">
                                 <span v-if="row.created_by">{{ row.created_by?.name || '' }}</span>
                                 <span v-else>-</span>
                              </div>
                           </div>
                           <div>
                              <div class="font-medium text-gray-700 dark:text-gray-300">Created At</div>
                              <div class="text-gray-500 dark:text-gray-400">
                                 {{ formatLocalDateTimeExtended(row.created_at).formattedDate }}
                              </div>
                              <div class="text-gray-400 dark:text-gray-500">
                                 {{ formatLocalDateTimeExtended(row.created_at).formattedTime }}
                              </div>
                           </div>
                        </div>
                     </template>

                     <!-- Updated Dates -->
                     <template #cell-updated_at="{ row }">
                        <div class="space-y-2 text-xs">
                           <div>
                              <div class="font-medium text-gray-700 dark:text-gray-300">Updated By</div>
                              <div class="text-gray-500 dark:text-gray-400">
                                 <span v-if="row.updated_by">{{ row.updated_by?.name || '' }}</span>
                                 <span v-else>-</span>
                              </div>
                           </div>
                           <div>
                              <div class="font-medium text-gray-700 dark:text-gray-300">Updated At</div>
                              <div class="text-gray-500 dark:text-gray-400">
                                 {{ formatLocalDateTimeExtended(row.updated_at).formattedDate }}
                              </div>
                              <div class="text-gray-400 dark:text-gray-500">
                                 {{ formatLocalDateTimeExtended(row.updated_at).formattedTime }}
                              </div>
                           </div>
                        </div>
                     </template>

                     <!-- Status -->
                     <template #cell-status="{ row }">
                        <ActionBadge :status="row.is_active ? 'active' : 'inactive'" size="sm" rounded="full" />
                     </template>

                     <!-- Action Column (Custom) -->
                     <template #cell-action="{ row }">
                        <div class="flex flex-col items-center gap-1">
                           <button @click="viewItem(row)"
                              class="p-1 text-green-600 hover:bg-green-100 dark:hover:bg-green-900/30 rounded-lg transition-colors"
                              title="View">
                              <i class="fa-solid fa-eye text-lg"></i>
                           </button>
                           <button @click="editItem(row)"
                              class="p-1 text-blue-600 hover:bg-blue-100 dark:hover:bg-blue-900/30 rounded-lg transition-colors"
                              title="Edit">
                              <i class="fa-solid fa-pen-to-square text-lg"></i>
                           </button>
                           <button @click="handleDelete(row.id)"
                              class="p-1 text-red-600 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-lg transition-colors"
                              title="Delete">
                              <i class="fa-solid fa-trash text-lg"></i>
                           </button>
                        </div>
                     </template>

                  </DataTablePcBody>
               </div>

               <!-- Table Info and Pagination -->
               <DataTablePagination :current-page="currentPage" :pagination="apiData?.pagination"
                  :total-items="apiData?.total_items" :selected-count="selectedRows.length" @page-change="goToPage" />
            </div>

            <!-- Card Footer -->
            <div
               class="px-3 py-2 sm:px-4 sm:py-3 border-t border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row justify-between items-center gap-2 bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-900/20">
            </div>

         </template>
      </MainContentCard>
   </MasterCardLayout>
</template>

<script setup>
import { CategoryApiURL, CategoryPageURL } from '../../routes';
import { useDelete } from '@/composables/useDelete';
import DataTableTopControls from '@/components/data-table/DataTableTopControls.vue';
import DataTablePagination from '@/components/data-table/DataTablePagination.vue';
import DataTablePcBody from '@/components/data-table/DataTablePcBody.vue'
import { formatLocalDateTimeExtended } from '@/utils/dateFormatter';
import { truncateText } from '@/utils/textFormatter';
import CustomModal from '@/components/modal/CustomModal.vue';
import {
   ref,
   reactive,
   computed,
   onMounted,
   watch,
   inject,
   getCurrentInstance,
} from 'vue';
import { h } from 'vue';

// ===================================================================
// =========================== 1. INJECTIONS =========================
// ===================================================================
const toast = inject('toast');
const axios = inject('axios');
const swal = inject('swal');
const { deleteItem } = useDelete();
const today = new Date().toISOString().split('T')[0];
const { proxy } = getCurrentInstance();

// ===================================================================
// =========================== 2. PROPS =============================
// ===================================================================
const props = defineProps({
   categoryChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
   statusChoices: {
      type: Array,
      required: true,
      default: () => [],
   }
});

// ===================================================================
// =========================== 2. DATA ================================
// ===================================================================
const accessToken = ref(window.accessToken);
const userId = ref(window.user_id);
const loadingStates = reactive({
   loading: false,
   loadingTable: false,
   back: false,
   draft: false,
   save: false,
});

const error = ref(null);
const apiData = ref(null);

// Table configuration
const entriesPerPage = ref(10);
const currentPage = ref(1);
const searchQuery = ref('');
const selectedRows = ref([]);
const selectAll = ref(false);
const bulkAction = ref('');
const sortColumn = ref('name');
const sortDirection = ref('asc');

// Filter configuration
const showFilter = ref(false);
const categories = ref([]);
const filterForm = ref({
   parent: null,
   status: null,
});

// Table columns configuration for subscription plans
const tableColumns = [
   { field: 'name', title: 'Name', width: '20%', sticky: true, sortable: true },
   { field: 'parent', title: 'Parent Name', width: '20%', sticky: false, sortable: false },
   { field: 'logo', title: 'Logo', width: '20%', sticky: false, sortable: false },
   { field: 'created_at', title: 'Created At', width: '20%', sortable: true },
   { field: 'updated_at', title: 'Updated At', width: '20%', sortable: false },
   { field: 'status', title: 'Status', width: '10%', sticky: true, sortable: false },
]

// ===================================================================
// =========================== 3. COMPUTED ============================
// ===================================================================
const tableFooterData = computed(() => {
   // if (!apiData.value?.results?.length) {
   //    return {}
   // }
   // const items = apiData.value.results
   // const totalPrice = items.reduce((sum, item) => sum + Number(item.price || 0), 0)
   // const activeCount = items.filter(item => item.is_active).length
   // return {
   //    total_price: totalPrice.toFixed(2),
   //    active_count: activeCount,
   // }
})

// ===================================================================
// =========================== 4. METHODS ============================
// ===================================================================
const fetchData = async () => {
   loadingStates.loadingTable = true;
   try {
      const params = {
         page: currentPage.value,
         page_size: entriesPerPage.value,

         //!✅ Search Query
         ...(searchQuery.value && { search: searchQuery.value }),

         //!✅ Sort Configuration
         ...(sortColumn.value && {
            ordering:
               sortDirection.value === 'desc'
                  ? `-${sortColumn.value}`
                  : sortColumn.value,
         }),

         //!✅ Filter Configuration
         ...(filterForm.value.parent && { parent_id: filterForm.value.parent }),
         ...(filterForm.value.status && { is_active: filterForm.value.status }),
      };

      // ✅ Relative URL with axios
      const response = await axios.get(`${CategoryApiURL.List}/`, { params });
      apiData.value = response.data;
   } catch (error) {
      console.error('Error fetching data:', error);
      apiData.value = {
         total_items: 0,
         results: [],
         pagination: {
            showing_from: 0,
            showing_to: 0,
            total_pages: 0,
         },
      };
   } finally {
      loadingStates.loadingTable = false;
   }
};

// Actions ------------------------------------------
const addItemPage = () => {
   console.log('Add item');
   window.location = `${CategoryPageURL.Create}`;
}
const editItem = (item) => {
   window.location = `${CategoryPageURL.Update}/${item.id}`;
};

const viewItem = (item) => {
   window.location = `${CategoryPageURL.Details}/${item.id}/`;
};

const handleDelete = (id) => {
   deleteItem({
      url: `${CategoryApiURL.Delete}`,
      id: id,
      name: 'Shop',
      onSuccess: fetchData,
   });
};

// Search -------------------------------------------
const onSearchInput = debounce(() => {
   currentPage.value = 1;
   fetchData();
}, 500);

const clearSearch = () => {
   searchQuery.value = '';
   currentPage.value = 1;
   fetchData();
};

// Pagination --------------------------------------
const goToPage = (page) => {
   if (page >= 1 && page <= (apiData.value?.pagination?.total_pages || 1)) {
      currentPage.value = page;
      fetchData();
   }
};

// Sorting ----------------------------------------
const sortTable = (column) => {
   if (sortColumn.value === column) {
      sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
   } else {
      sortColumn.value = column;
      sortDirection.value = 'asc';
   }
   fetchData();
};

// Bulk actions -------------------------------------
const executeBulkAction = () => {
   if (!bulkAction.value) return;

   console.log(`Executing ${bulkAction.value} on:`, selectedRows.value);

   // Reset after execution
   bulkAction.value = '';
   selectedRows.value = [];
};

// Apply filters ----------------------------------------------------
const exportData = () => {
   // console.log('Exporting data...');
   toast.info('Exporting data...');
}

const applyFilters = () => {
   currentPage.value = 1;
   fetchData();
};

// Reset filters
const resetFilters = () => {
   filterForm.value = {
      parent: null,
      status: null
   };
   currentPage.value = 1;
   fetchData();
};

// Utility functions ================================================================
function debounce(func, wait) {
   let timeout;
   return function executedFunction(...args) {
      const later = () => {
         clearTimeout(timeout);
         func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
   };
}

// ===================================================================
// =========================== 1. WATCH =========================
// ===================================================================
watch(selectAll, (newVal) => {
   if (newVal && apiData.value?.results) {
      selectedRows.value = apiData.value.results.map((item) => item.id);
   } else {
      selectedRows.value = [];
   }
});

// Watch for selectedRows changes
watch(selectedRows, (newVal) => {
   if (apiData.value?.results) {
      selectAll.value =
         newVal.length === apiData.value.results.length &&
         apiData.value.results.length > 0;
   }
});

// ===================================================================
// =========================== 5. MOUNTED ============================
// ===================================================================
onMounted(() => {
   fetchData();
});
</script>

<style scoped>
/* Line clamp utility */
.line-clamp-2 {
   display: -webkit-box;
   -webkit-line-clamp: 2;
   -webkit-box-orient: vertical;
   overflow: hidden;
}

.v-enter-active,
.v-leave-active {
   transition: all 0.3s ease;
}

.v-enter-from,
.v-leave-to {
   opacity: 0;
   transform: translateY(-10px);
}

.v-enter-to,
.v-leave-from {
   opacity: 1;
   transform: translateY(0);
}
</style>
