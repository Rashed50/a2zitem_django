<template>
   <div class="flex flex-col h-full w-full space-y-2">
      <!-- Form Card -->
      <div
         class="flex-1 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden">
         <!-- Card Header -->
         <div
            class="px-3 py-1 sm:px-6 sm:py-3 border-b border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-900/20">
            <h4 class="text-xl font-bold text-gray-800 dark:text-gray-100 flex items-center gap-3">
               <i class="fa-solid fa-cart-shopping text-blue-600 dark:text-white"></i>
               <span class="text-lg sm:text-xl">Product Item List</span>
            </h4>
            <ActionButton action="add" size="sm" @click="goToAddPage" class="px-8" />
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
                     <div class="space-y-1">
                        <!-- Product Name -->
                        <div class="font-semibold text-gray-900 dark:text-white">
                           {{ row.name }}
                        </div>

                        <!-- Brand -->
                        <div class="text-xs text-blue-600 dark:text-blue-400">
                           {{ row.brand?.name }}
                        </div>

                        <!-- Category -->
                        <div class="text-xs text-gray-500 dark:text-gray-400">
                           {{ row.category_path }}
                        </div>

                        <!-- Code -->
                        <div class="text-[11px] text-gray-400">
                           Code: {{ row.code }}
                        </div>
                     </div>
                  </template>

                  <!-- Contact Information -->
                  <template #cell-variants="{ row }">
                     <div class="flex flex-col gap-1">
                        <div v-for="variant in row.variants" :key="variant.id"
                           class="flex items-center justify-between text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                           <span class="font-medium">
                             Colour:  {{ variant.color?.name }} 
                               <!-- {{ variant.size?.name }} -->
                           </span>

                           <span class="text-gray-500">
                             Stock: {{ variant.stock }}
                              <!-- {{ variant.unit?.symbol }} -->
                           </span>

                           <span class="text-green-600 font-semibold">
                              ৳{{ variant.selling_price }}/-
                           </span>
                        </div>
                     </div>
                  </template>
                  <!-- <template #cell-variants="{ row }">
                     <div class="space-y-2">
                        <div v-for="variant in row.variants" :key="variant.id"
                           class="text-xs border rounded-md px-2 py-1 bg-gray-50 dark:bg-gray-700 border-gray-200 dark:border-gray-600">
                           <div class="font-medium text-gray-800 dark:text-gray-200">
                              {{ variant.color?.name }} | {{ variant.size?.name }}
                           </div>

                           <div class="text-gray-500 dark:text-gray-400">
                              {{ variant.unit?.symbol }}
                              • Stock: {{ variant.stock }}
                           </div>

                           <div class="text-green-600 font-medium">
                              ৳ {{ variant.selling_price }}
                           </div>
                        </div>
                     </div>
                  </template> -->

                  <!-- Created Dates -->
                  <template #cell-created="{ row }">
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
                  <template #cell-updated="{ row }">
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
                        <button @click="goToDetailsPage(row)"
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
import { ProductApiURL, ProductPageURL } from '../../routes';
import { useDelete } from '@/composables/useDelete';
import DataTableTopControls from '@/components/data-table/DataTableTopControls.vue';
import DataTablePagination from '@/components/data-table/DataTablePagination.vue';
import DataTablePcBody from '@/components/data-table/DataTablePcBody.vue'
import { formatLocalDateTimeExtended } from '@/utils/dateFormatter';
import { truncateText, needsTruncation, getTruncatedWithFull } from '@/utils/textFormatter';
import {
   ref,
   computed,
   onMounted,
   watch,
   inject,
   getCurrentInstance,
} from 'vue';

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
// =========================== 2. DATA ================================
// ===================================================================
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
   { field: 'name', title: 'Product Info.', width: '20%', sticky: true, sortable: true },
   { field: 'variants', title: 'variants Info.', width: '20%', sticky: true, sortable: false },
   { field: 'created', title: 'Created At', width: '20%', sortable: false },
   { field: 'updated', title: 'Updated At', width: '20%', sortable: false },
   { field: 'status', title: 'Status', width: '10%', sticky: true, sortable: false },
]


// ===================================================================
// =========================== 3. COMPUTED ============================
// ===================================================================
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

const getTruncatedAddress = (address) => {
   return truncateText(address, 50);
};

// ===================================================================
// =========================== 4. METHODS ============================
// ===================================================================
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
      const response = await axios.get(ProductApiURL.List, { params });
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
const goToAddPage = () => {
   // console.log('Add item');
   window.location = ProductPageURL.Create;
};
const editItem = (item) => {
   // console.log('Edit item:', item);
   window.location = `${ProductPageURL.Update}/${item.id}`;
};

const goToDetailsPage = (item) => {
   console.log('View item:', item.id);
   window.location = `${ProductPageURL.Details}/${item.id}/`;
};

const handleDelete = (id) => {
   deleteItem({
      url: `${ProductApiURL.Delete}`,
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
</style>
