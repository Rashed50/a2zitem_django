<template>
   <div class="flex flex-col h-full w-full space-y-2">
      <!-- Form Card -->
      <div
         class="flex-1 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden">
         <!-- Card Header -->
         <div
            class="px-3 py-1 sm:px-6 sm:py-3 border-b border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-900/20">
            <h4 class="text-xl font-bold text-gray-800 dark:text-gray-100 flex items-center gap-3">
               <i class="fa-regular fa-truck text-blue-600"></i>
               <span class="text-lg sm:text-xl">Supplier List</span>
            </h4>
            <ActionButton action="add" size="sm" @click="addItem" class="px-8" />
         </div>

         <!-- Card Body -->
         <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-5 sm:py-3 space-y-4 sm:space-y-2">
            <!-- Top Controls -->
            <DataTableTopControls :entries-per-page="entriesPerPage" @update:entries-per-page="entriesPerPage = $event"
               :search-query="searchQuery" @update:search-query="searchQuery = $event" :bulk-action="bulkAction"
               @update:bulk-action="bulkAction = $event" :selected-rows="selectedRows"
               :search-placeholder="'Search subscription plans...'" @entries-change="fetchData"
               @search-input="onSearchInput" @clear-search="clearSearch" @bulk-apply="executeBulkAction" />

            <!-- Data Table -->
            <div class="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-lg">
               <DataTablePcBody :items="apiData?.results || []" :columns="tableColumns"
                  :pagination="apiData?.pagination" :loading="loading" :sort-column="sortColumn"
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

                  <!-- Contact Information -->
                  <template #cell-contact="{ row }">
                     <div class="font-medium text-gray-900 dark:text-white">
                        {{ row.contact || '' }}
                     </div>
                     <div class="text-xs text-gray-500 dark:text-gray-400">
                        {{ row.email || '' }}
                     </div>
                     <div class="text-xs text-gray-500 dark:text-gray-400">
                        {{ row.phone || '' }}
                     </div>
                  </template>

                  <!-- Address -->
                  <template #cell-address="{ row }">
                     {{ row.address || '' }}
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
      </div>
   </div>
</template>

<script setup>
import { SupplierApiURL, SupplierPageURL } from '../../routes';
import { useDelete } from '@/composables/useDelete';
import DataTableTopControls from '@/components/data-table/DataTableTopControls.vue';
import DataTablePagination from '@/components/data-table/DataTablePagination.vue';
import DataTablePcBody from '@/components/data-table/DataTablePcBody.vue'
import { formatLocalDateTimeExtended } from '@/utils/dateFormatter';
import {
   ref,
   computed,
   onMounted,
   watch,
   inject,
   getCurrentInstance,
} from 'vue';

const toast = inject('toast');
const axios = inject('axios');
const swal = inject('swal');
const { deleteItem } = useDelete();

const today = new Date().toISOString().split('T')[0];
const { proxy } = getCurrentInstance();

const accessToken = ref(window.accessToken);
const userId = ref(window.user_id);
const loading = ref(false);
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

// Table columns configuration for subscription plans
const tableColumns = [
   { field: 'name', title: 'Name', width: '20%', sticky: true, sortable: true },
   { field: 'contact', title: 'Contact Information', width: '20%', sticky: true, sortable: false },
   { field: 'address', title: 'Address', width: '20%', sticky: false, sortable: false },
   { field: 'status', title: 'Status', width: '10%', sticky: true, sortable: false },
]

const tableFooterData = computed(() => {
   if (!apiData.value?.results?.length) {
      return {}
   }
   const items = apiData.value.results
   const totalPrice = items.reduce((sum, item) => sum + Number(item.price || 0), 0)
   const activeCount = items.filter(item => item.is_active).length
   return {
      total_price: totalPrice.toFixed(2),
      active_count: activeCount,
   }
})

// Methods ============================================================================
const fetchData = async () => {
   loading.value = true;
   try {
      const params = {
         page: currentPage.value,
         page_size: entriesPerPage.value,
         ...(searchQuery.value && { search: searchQuery.value }),
         ...(sortColumn.value && {
            ordering:
               sortDirection.value === 'desc'
                  ? `-${sortColumn.value}`
                  : sortColumn.value,
         }),
      };

      // ✅ Relative URL with axios
      const response = await axios.get(SupplierApiURL.List, { params });
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
      loading.value = false;
   }
};

// Actions ------------------------------------------
const addItem = () => {
   // console.log('Add item');
   window.location = SupplierPageURL.Create;
};
const editItem = (item) => {
   // console.log('Edit item:', item);
   window.location = `${SupplierPageURL.Update}/${item.id}`;
};

const viewItem = (item) => {
   console.log('View item:', item.id);
   window.location = `${SupplierPageURL.Details}/${item.id}/`;
};

const handleDelete = (id) => {
   deleteItem({
      url: `${SupplierApiURL.Delete}`,
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

// Watch ===========================================================================
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

// Computed properties ===============================================================
const visiblePages = computed(() => {
   if (!apiData.value?.pagination) return [];

   const totalPages = apiData.value.pagination.total_pages;
   const maxVisible = window.innerWidth < 640 ? 3 : 5;
   let startPage = Math.max(1, currentPage.value - Math.floor(maxVisible / 2));
   let endPage = Math.min(totalPages, startPage + maxVisible - 1);

   if (endPage - startPage + 1 < maxVisible) {
      startPage = Math.max(1, endPage - maxVisible + 1);
   }

   const pages = [];
   for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
   }

   return pages;
});

// Mounted ===========================================================================
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
</style>
