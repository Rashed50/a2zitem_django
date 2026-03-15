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
            <i class="fa-solid fa-box-open text-blue-500"></i>
         </template>

         <!-- Header Title -->
         <template #title>
            <span class="me-2">{{ detailsData.name }}</span>
            <ActionBadge :status="detailsData.is_active ? 'active' : 'inactive'" size="md" rounded="md" />
         </template>

         <!-- Header Right Side -->
         <template #header-right>
            <ActionButton action="edit" size="sm" @click="goUpdatePage" class="px-8" label="Update" />
         </template>

         <template #body>
            <!-- Card Body -->
            <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-6 sm:py-6 space-y-3">
               <!-- Product Information -->
               <div>
                  <h4 class="text-blue-600 font-bold text-lg mb-4 flex items-center gap-2">
                     <i class="fa-solid fa-box"></i>
                     Product Information
                  </h4>

                  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">

                     <InfoCard label="Product Name" :value="detailsData.name" icon="fa-solid fa-box" />

                     <InfoCard label="Product Code" :value="detailsData.code" icon="fa-solid fa-barcode" />

                     <InfoCard label="Brand" :value="detailsData.brand?.name" icon="fa-solid fa-tag" />

                     <InfoCard label="Category" :value="detailsData.category?.name" icon="fa-solid fa-layer-group" />

                     <InfoCard label="Category Path" :value="detailsData.category_path" icon="fa-solid fa-sitemap"
                        col-span="md:col-span-2" />

                     <InfoCard label="Featured Product" :value="detailsData.is_featured ? 'Yes' : 'No'"
                        icon="fa-solid fa-star" />

                  </div>
               </div>

               <div v-if="detailsData.description">
                  <h4 class="text-blue-600 font-bold text-lg mb-3 flex items-center gap-2">
                     <i class="fa-solid fa-align-left"></i>
                     Description
                  </h4>

                  <div
                     class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg text-gray-700 dark:text-gray-200 text-sm leading-relaxed">
                     {{ detailsData.description }}
                  </div>
               </div>

               <div>
                  <h4 class="text-blue-600 font-bold text-lg mb-4 flex items-center gap-2">
                     <i class="fa-solid fa-boxes-stacked"></i>
                     Product Variants
                  </h4>

                  <div class="overflow-x-auto border rounded-lg">
                     <table class="min-w-full text-sm">
                        <thead class="bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200">
                           <tr>
                              <th class="px-3 py-2 text-left">SKU</th>
                              <th class="px-3 py-2 text-left">Color</th>
                              <th class="px-3 py-2 text-left">Size</th>
                              <th class="px-3 py-2 text-left">Unit</th>
                              <th class="px-3 py-2 text-left">Stock</th>
                              <th class="px-3 py-2 text-left">Price</th>
                           </tr>
                        </thead>

                        <tbody>
                           <tr v-for="variant in detailsData.variants" :key="variant.id"
                              class="border-t dark:border-gray-700">
                              <td class="px-3 py-2 font-medium">
                                 {{ variant.sku }}
                              </td>

                              <td class="px-3 py-2">
                                 {{ variant.color?.name }}
                              </td>

                              <td class="px-3 py-2">
                                 {{ variant.size?.name }}
                              </td>

                              <td class="px-3 py-2">
                                 {{ variant.unit?.symbol }}
                              </td>

                              <td class="px-3 py-2">
                                 {{ variant.stock }}
                              </td>

                              <td class="px-3 py-2 text-green-600 font-semibold">
                                 ৳ {{ variant.selling_price }}
                              </td>
                           </tr>
                        </tbody>
                     </table>
                  </div>
               </div>

               <!-- Audit Information - Enhanced Design -->
               <AuditInfoCard 
                  :created-by="detailsData?.created_by?.name"
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
import { ProductApiURL, ProductPageURL } from '../../routes';
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
         `${ProductApiURL.Details}/${props.itemId}/`
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

const goUpdatePage = () => {
   window.location.href = `${ProductPageURL.Update}/${props.itemId}/`;
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