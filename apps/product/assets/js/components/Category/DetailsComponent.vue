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
            <span class="me-2">{{ detailsData.name }}</span>
            <ActionBadge :status="detailsData.is_active ? 'active' : 'inactive'" size="md" rounded="md" />
         </template>

         <!-- Header Right Side -->
         <template #header-right>
            <ActionButton action="back" @click="goToBack" variant="outline-secondary" size="sm" label="Back" />
            <ActionButton action="edit" size="sm" @click="goUpdatePage" class="px-8" label="Update" />
         </template>

         <template #body>
            <!-- Card Body -->
            <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-6 sm:py-6 space-y-3">
               <div>
                  <h4 class="text-blue-600 font-bold text-lg mb-4 flex items-center gap-2">
                     <i class="fa-solid fa-info-circle"></i>
                     Category Information
                  </h4>
                  <div v-if="detailsData" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                     <InfoCard label="Category Name" :value="detailsData.name" icon="fa-solid fa-layer-group" />
                     <InfoCard label="Category Immediate Parent" :value="detailsData.parent?.name"
                        icon="fa-solid fa-layer-group" />
                  </div>
               </div>

               <!-- Parent Chain - Modern Breadcrumb -->
               <div v-if="detailsData.parent_chain?.length"
                  class="bg-white dark:bg-gray-800/50 rounded-xl p-5 border border-gray-200 dark:border-gray-700">
                  <h5 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-4 flex items-center gap-2">
                     <i class="fa-solid fa-diagram-project text-blue-500"></i>
                     Hierarchy Path
                  </h5>

                  <!-- Animated breadcrumb -->
                  <div class="flex flex-wrap items-center gap-2">
                     <template v-for="(cat, index) in detailsData.parent_chain" :key="cat.id">
                        <div class="flex items-center">
                           <div class="group relative">
                              <span
                                 class="px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg text-sm font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 cursor-default">
                                 {{ cat.name }}
                                 <span
                                    class="absolute -top-2 -right-2 w-5 h-5 bg-gray-200 dark:bg-blue-500 rounded-full text-xs flex items-center justify-center border-2  border-gray-600 dark:border-white">
                                    <span class="text-black dark:text-white">{{ index + 1 }}</span>
                                 </span>
                              </span>
                           </div>
                           <i v-if="index < detailsData.parent_chain.length - 1"
                              class="fa-solid fa-arrow-right-long text-gray-400 mx-3 text-xl"></i>
                        </div>
                     </template>

                     <!-- Current item -->
                     <div class="flex items-center">
                        <i class="fa-solid fa-arrow-right-long text-gray-400 mx-3 text-xl"></i>
                        <span
                           class="px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg text-sm font-bold shadow-lg">
                           {{ detailsData.name }}
                           <span class="ml-2 text-xs bg-white/20 px-2 py-0.5 rounded-full">Current</span>
                        </span>
                     </div>
                  </div>

                  <!-- Mini tree view alternative -->
                  <div class="mt-4 flex items-center text-xs text-gray-500 dark:text-gray-400">
                     <i class="fa-regular fa-clock mr-1 text-gray-400"></i>
                     Last updated: {{ formatLocalDateTimeExtended(detailsData.updated_at).fullDateTime }}
                  </div>
               </div>

               <!-- Children Categories - Card Grid -->
               <div v-if="detailsData.children_chain?.length"
                  class="bg-white dark:bg-gray-800/50 rounded-xl p-5 border border-gray-200 dark:border-gray-700">
                  <div class="flex items-center justify-between mb-4">
                     <h5 class="text-sm font-semibold text-gray-500 dark:text-gray-400 flex items-center gap-2">
                        <i class="fa-solid fa-folder-tree text-green-500"></i>
                        Subcategories ({{ detailsData.children_chain.length }})
                     </h5>

                     <!-- View toggle -->
                     <button @click="childView = childView === 'grid' ? 'list' : 'grid'"
                        class="text-xs px-3 py-1.5 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition flex items-center gap-2">
                        <i :class="childView === 'grid' ? 'fa-solid fa-list' : 'fa-solid fa-grid-2'"></i>
                        {{ childView === 'grid' ? 'List View' : 'Grid View' }}
                     </button>
                  </div>

                  <!-- Grid View -->
                  <div v-if="childView === 'grid'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                     <div v-for="child in detailsData.children_chain" :key="child.id"
                        class="group relative bg-white dark:bg-gray-800 rounded-xl p-4 border-2 border-transparent hover:border-green-400 dark:hover:border-green-600 shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer"
                        @click="viewCategory(child.id)">

                        <!-- Decorative corner -->
                        <!-- <div class="absolute top-0 right-0 w-12 h-12 overflow-hidden">
                           <div
                              class="absolute transform rotate-45 bg-green-400 text-white text-xs py-1 right-[-35px] top-[15px] w-[85px] text-center font-semibold">
                              NEW
                           </div>
                        </div> -->

                        <div class="flex items-start gap-3">
                           <div
                              class="w-10 h-10 bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition">
                              <i class="fa-solid fa-folder-open"></i>
                           </div>
                           <div class="flex-1">
                              <h6 class="font-bold text-gray-900 dark:text-white">{{ child.name }}</h6>
                              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">ID: {{ child.id }}</p>
                              <div class="flex items-center gap-2 mt-2 text-xs text-gray-400">
                                 <i class="fa-regular fa-calendar"></i>
                                 {{ formatLocalDateTimeExtended(child.created_at).fullDateTime }}
                              </div>
                           </div>
                        </div>

                        <!-- Hover effect indicator -->
                        <!-- <div class="absolute bottom-2 right-2 opacity-0 group-hover:opacity-100 transition">
                           <i class="fa-solid fa-arrow-right text-green-500"></i>
                        </div> -->
                     </div>
                  </div>

                  <!-- List View -->
                  <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
                     <div v-for="child in detailsData.children_chain" :key="child.id"
                        class="flex items-center justify-between py-3 px-2 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg transition cursor-pointer group"
                        @click="viewCategory(child.id)">
                        <div class="flex items-center gap-3">
                           <div
                              class="w-6 h-6 bg-green-100 dark:bg-green-900/30 rounded flex items-center justify-center">
                              <i class="fa-solid fa-folder text-green-600 dark:text-green-400 text-xs"></i>
                           </div>
                           <span class="font-medium text-gray-900 dark:text-white">{{ child.name }}</span>
                           <span class="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full">
                              #{{ child.id }}
                           </span>
                        </div>
                        <div class="flex items-center gap-4">
                           <span class="text-xs text-gray-400">{{
                              formatLocalDateTimeExtended(child.created_at).fullDateTime
                           }}</span>
                           <i class="fa-solid fa-chevron-right text-gray-300 group-hover:text-green-500 transition"></i>
                        </div>
                     </div>
                  </div>
               </div>

               <!-- No Children Message -->
               <div v-else
                  class="bg-white dark:bg-gray-800/50 rounded-xl p-8 border border-gray-200 dark:border-gray-700 text-center">
                  <div
                     class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-3">
                     <i class="fa-solid fa-folder-open text-2xl text-gray-400"></i>
                  </div>
                  <h6 class="text-gray-500 dark:text-gray-400 font-medium">No Subcategories</h6>
                  <p class="text-xs text-gray-400 mt-1">This category has no child categories yet</p>
               </div>

               <!-- Audit Information - Enhanced Design -->
               <AuditInfoCard :created-by="detailsData?.created_by?.name"
                  :created-at="formatLocalDateTimeExtended(detailsData.created_at).fullDateTime"
                  :updated-by="detailsData?.updated_by?.name"
                  :updated-at="formatLocalDateTimeExtended(detailsData.updated_at).fullDateTime" />
            </div>
         </template>
      </MainContentCard>
   </MasterCardLayout>
</template>

<script setup>
import { ref, onMounted, reactive, inject, computed } from 'vue';
import { CategoryApiURL, CategoryPageURL } from '../../routes';
import { formatLocalDateTimeExtended } from '@/utils/dateFormatter';
import AuditInfoCard from '@/components/card/AuditTrailCard.vue';

// ===================================================================
// =========================== 1. INJECTIONS =========================
// ===================================================================
const toast = inject('toast');
const axios = inject('axios');

// Global from window (Django template থেকে আসে)
const accessToken = ref(window.accessToken);
const userId = ref(window.user_id);

// ===================================================================
// =========================== 1. PROPS ===============================
// ===================================================================
const props = defineProps({
   itemId: {
      type: [Number, String],
      required: true,
   },
});

// ===================================================================
// =========================== 3. DATA ================================
// ===================================================================
const loadingStates = reactive({
   loading: false,
   back: false,
   draft: false,
   save: false,
});
const error = ref(null);
const detailsData = ref({});
const childView = ref('List View');
// ===================================================================
// =========================== 4. COMPUTED ============================
// ===================================================================
const groupedPermissions = computed(() => {
   if (!detailsData.value.permissions) return {};

   return detailsData.value.permissions.reduce((groups, permission) => {
      const module = permission.module || 'other';
      if (!groups[module]) {
         groups[module] = [];
      }
      groups[module].push(permission);
      return groups;
   }, {});
});

// ===================================================================
// =========================== 5. MOUNTED ============================
// ===================================================================
onMounted(() => {
   if (props.itemId && props.itemId !== 'null') {
      fetchDetailsData();
   } else {
      error.value = 'Invalid plan ID';
      loadingStates.loading = false;
   }
});

// ===================================================================
// =========================== 6. METHODS ============================
// ===================================================================
const fetchDetailsData = async () => {
   loadingStates.loading = true;
   error.value = null;

   try {
      const response = await axios.get(
         `${CategoryApiURL.Details}/${props.itemId}/`
      );

      if (response.data.success) {
         detailsData.value = response.data.results;
      } else {
         error.value = response.data.message || 'Failed to load plan details';
      }
   } catch (err) {
      console.error(err);
      error.value = 'Something went wrong. Please try again.';
      toast.error('Failed to load plan details');
   } finally {
      loadingStates.loading = false;
   }
};

const goToBack = () => {
   loadingStates.back = true;
   window.location.href = CategoryPageURL.List;
   setTimeout(() => (loadingStates.back = false), 500);
};

const goUpdatePage = () => {
   window.location.href = `${CategoryPageURL.Update}/${props.itemId}/`;
}

// Helper Labels ----------------------------------------------------
const makeCapital = (v) => {
   if (v) {
      return v.charAt(0).toUpperCase() + v.slice(1);
   }
   return '';
};

const makeTitle = (v) => {
   if (v) {
      return v.toUpperCase();
   }
   return '';
};
</script>

<style scoped>
/* Optional: Add some custom styles if needed */
</style>