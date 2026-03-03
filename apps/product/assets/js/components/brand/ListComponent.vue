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
            <i class="fa-brands fa-airbnb text-blue-600 font-bold"></i>
         </template>

         <!-- Header Title -->
         <template #title>
            Brand List
         </template>

         <!-- Header Right Side -->
         <template #header-right>
            <ActionButton action="add" size="sm" @click="showAddItemModal = true" class="px-8" />
         </template>

         <!-- Card Body -->
         <template #body>
            <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-5 sm:py-3 space-y-4 sm:space-y-2">
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

                     <!-- Logo -->
                     <template #cell-logo="{ row }">
                        <div class="flex items-center space-x-2">
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

                     <!-- Activity Dates -->
                     <template #cell-activity_dates="{ row }">
                        <div class="space-y-2 text-xs">
                           <div>
                              <div class="font-medium text-gray-700 dark:text-gray-300">Created</div>
                              <div class="text-gray-500 dark:text-gray-400">
                                 {{ formatLocalDateTimeExtended(row.created_at).formattedDate }}
                              </div>
                              <div class="text-gray-400 dark:text-gray-500">
                                 {{ formatLocalDateTimeExtended(row.created_at).formattedTime }}
                              </div>
                           </div>

                           <div>
                              <div class="font-medium text-gray-700 dark:text-gray-300">Updated</div>
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
                           <!-- <button @click="viewItem(row)"
                              class="p-1 text-green-600 hover:bg-green-100 dark:hover:bg-green-900/30 rounded-lg transition-colors"
                              title="View">
                              <i class="fa-solid fa-eye text-lg"></i>
                           </button> -->
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

            <!-- ========= [ ADD MODAL ] ============ -->
            <CustomModal :isOpen="showAddItemModal" @update:isOpen="showAddItemModal = $event" title="Add New Brand"
               size="sm">
               <template #body>
                  <form @submit.prevent="handleAddItem" class="space-y-5">
                     <div class="space-y-3">
                        <!-- Name -->
                        <InputeComponent label="Brand Name" id="name" name="name" label-for="name"
                           placeholder="Enter Brand Name" v-model="addForm.name" :error="addFormErrors.name" />

                        <!-- Logo -->
                        <FileInputComponent label="Brand Logo" v-model="addForm.logo" :current-image-url="addForm?.logo"
                           :error="addFormErrors.logo" :accept="['image/*']" help-text="Square logo (1:1 ratio)"
                           :max-size="2 * 1024 * 1024" />

                        <!-- Is Active -->
                        <div>
                           <label for="is_active"
                              class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
                              Active
                           </label>
                           <Checkbox label="Is active ?" v-model="addForm.is_active" />
                        </div>

                     </div>
                     <!-- Footer Buttons -->
                     <div class="flex justify-end border-t border-default space-x-3 pt-2 md:pt-5">
                        <ActionButton action="cancel" @click="showAddItemModal = false" size="sm" label="Cancel" />
                        <ActionButton action="save" size="sm" label="Save" type="submit" />
                     </div>
                  </form>
               </template>
            </CustomModal>

            <!-- ========= [ EDIT MODAL ] ============ -->
            <CustomModal :isOpen="showEditItemModal" @update:isOpen="showEditItemModal = $event" title="Edit Brand"
               size="sm">
               <template #body>
                  <form @submit.prevent="handleUpdateItem" class="space-y-5">
                     <div class="space-y-3">
                        <!-- Name -->
                        <InputeComponent label="Brand Name" id="edit_name" name="edit_name" label-for="edit_name"
                           placeholder="Enter Brand Name" v-model="editForm.name" :error="editFormErrors.name" />

                        <!-- Logo -->
                        <FileInputComponent label="Brand Logo" v-model="editForm.logo"
                           :current-image-url="editForm?.current_logo" :error="editFormErrors.logo" :accept="['image/*']"
                           help-text="Square logo (1:1 ratio) - Leave empty to keep current logo"
                           :max-size="2 * 1024 * 1024" />

                        <!-- Is Active -->
                        <div>
                           <label for="edit_is_active"
                              class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
                              Active Status
                           </label>
                           <Checkbox label="Is active ?" v-model="editForm.is_active" />
                        </div>
                     </div>

                     <!-- Footer Buttons -->
                     <div class="flex justify-end border-t border-default space-x-3 pt-2 md:pt-5">
                        <ActionButton action="cancel" @click="showEditItemModal = false" size="sm" label="Cancel" />
                        <ActionButton action="save" size="sm" label="Update" type="submit" />
                     </div>
                  </form>
               </template>
            </CustomModal>
         </template>
      </MainContentCard>
   </MasterCardLayout>
</template>

<script setup>
import { BrandApiURL } from '../../routes';
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

// Table columns configuration for subscription plans
const tableColumns = [
   { field: 'name', title: 'Name', width: '50%', sticky: true, sortable: true },
   { field: 'logo', title: 'Logo', width: '20%', sticky: false, sortable: false },
   { field: 'activity_dates', title: 'Activity Dates', width: '20%', sortable: false },
   { field: 'status', title: 'Status', width: '10%', sticky: true, sortable: false },
]

// Modal configuration
const showAddItemModal = ref(false);
const showEditItemModal = ref(false);
const addForm = ref({
   name: null,
   logo: null,
   is_active: true
});
const editForm = ref({
   id: null,
   name: null,
   logo: null,
   current_logo: null,
   is_active: true
});
const addFormErrors = ref({});
const editFormErrors = ref({});

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
         ...(searchQuery.value && { search: searchQuery.value }),
         ...(sortColumn.value && {
            ordering:
               sortDirection.value === 'desc'
                  ? `-${sortColumn.value}`
                  : sortColumn.value,
         }),
      };

      // ✅ Relative URL with axios
      const response = await axios.get(`${BrandApiURL.List}/`, { params });
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

// ------------ Start Modals -------------------------
const resetAddFrom = () => {
   addForm.value = {};
   addFormErrors.value = {};
}
const handleAddItem = async () => {
   addFormErrors.value = {}
   const requiredFields = ['name', 'logo'];
   let hasError = false;
   requiredFields.forEach((field) => {
      if (!addForm.value[field]) {
         addFormErrors.value[field] = `${field.replace(/_/g, ' ')} is required`;
         hasError = true;
      }
   });
   if (hasError) {
      toast.error('Required fields must be entry');
      return;
   }

   const formDataToSend = new FormData();
   formDataToSend.append('name', addForm.value.name);
   formDataToSend.append('is_active', addForm.value.is_active);
   if (addForm.value.logo) {
      formDataToSend.append('logo', addForm.value.logo);
   }

   // API call ============
   try {
      const response = await axios.post(
         `${BrandApiURL.Create}/`,
         formDataToSend,
         {}
      );

      if (response.data.success) {
         toast.success('Owner added successfully');
         // Form Close & Reset
         showAddItemModal.value = false;
         resetAddFrom();
         fetchData();
      } else {
         if (response.data.errors) {
            console.log(response.data.errors)
         }
         toast.error(response.data.message || 'Failed to add owner')
      }
   } catch (err) {
      console.log(err.response.data.message);
   }
};

const resetEditForm = () => {
   editForm.value = {
      id: null,
      name: null,
      logo: null,
      is_active: true
   };
   editFormErrors.value = {};
};
const handleUpdateItem = async () => {
   editFormErrors.value = {}
   const requiredFields = ['name']; 
   let hasError = false;

   requiredFields.forEach((field) => {
      if (!editForm.value[field]) {
         editFormErrors.value[field] = `${field.replace(/_/g, ' ')} is required`;
         hasError = true;
      }
   });

   if (hasError) {
      toast.error('Required fields must be entry');
      return;
   }

   const formDataToSend = new FormData();
   formDataToSend.append('name', editForm.value.name);
   formDataToSend.append('is_active', editForm.value.is_active);
   if (editForm.value.logo && typeof editForm.value.logo !== 'string') {
      formDataToSend.append('logo', editForm.value.logo);
   }

   try {
      const response = await axios.put(
         `${BrandApiURL.Update}/${editForm.value.id}/`, 
         formDataToSend,
         {}
      );

      if (response.data.success) {
         toast.success('Brand updated successfully');
         // Modal Close & Reset
         showEditItemModal.value = false;
         resetEditForm();
         fetchData();  // Table reload
      } else {
         if (response.data.errors) {
            editFormErrors.value = response.data.errors;
            console.log(response.data.errors)
         }
         toast.error(response.data.message || 'Failed to update brand')
      }
   } catch (err) {
      console.log(err.response?.data?.message);
      if (err.response?.data?.errors) {
         editFormErrors.value = err.response.data.errors;
      }
      toast.error(err.response?.data?.message || 'Failed to update brand');
   }
};
// --------------- End Modals -----------------------

// Actions ------------------------------------------
const editItem = (item) => {
   // window.location = `${SupplierPageURL.Update}/${item.id}`;
   editForm.value = {
      id: item.id,
      name: item.name,
      logo: null,
      current_logo: item.logo,
      is_active: item.is_active
   };
   showEditItemModal.value = true;
};

const viewItem = (item) => {
   console.log('View item:', item.id);
   // window.location = `${SupplierPageURL.Details}/${item.id}/`;
};

const handleDelete = (id) => {
   deleteItem({
      url: `${BrandApiURL.Delete}`,
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
