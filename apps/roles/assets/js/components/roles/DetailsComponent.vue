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
            {{ detailsData.name }}
         </template>

         <!-- Header Right Side -->
         <template #header-right>
            <ActionButton action="edit" size="sm" @click="goUpdatePage" class="px-8" label="Update" />
         </template>

         <template #body>
            <!-- Card Body -->
            <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-6 sm:py-6 space-y-6">
               <!-- Permissions Grouped by Module -->
               <div v-for="(permissions, module) in groupedPermissions" :key="module"
                  class="border rounded-lg p-4 bg-gray-50 dark:bg-gray-800">
                  <!-- Module Title -->
                  <h4
                     class="text-blue-600 dark:text-white font-bold text-lg mb-4 flex items-center gap-2 border-b pb-2">
                     <i class="fa-solid fa-shield-alt"></i>
                     {{ makeCapital(module) }}
                  </h4>

                  <!-- Permissions Grid -->
                  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                     <div v-for="permission in permissions" :key="permission.id"
                        class="flex items-center gap-2 p-2 bg-white dark:bg-gray-700 rounded shadow-sm hover:shadow transition">
                        <i class="fa-solid fa-check-circle text-green-500 text-sm"></i>
                        <span class="text-sm text-gray-700 dark:text-gray-200">{{ permission.name }}</span>
                     </div>
                  </div>
               </div>
            </div>
         </template>
      </MainContentCard>
   </MasterCardLayout>
</template>

<script setup>
import { ref, onMounted, reactive, inject, computed } from 'vue';
import { RoleApiURL, RolePageURL, EmployeeApiURL, EmployeePageURL } from '../../routes';
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
         `${RoleApiURL.Details}/${props.itemId}/`
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
   window.location.href = `${EmployeePageURL.Update}/${props.itemId}/`;
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