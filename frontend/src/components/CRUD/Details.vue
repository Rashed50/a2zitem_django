<template>
   <div class="flex flex-col h-full w-full space-y-2">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-20">
         <i class="fa-solid fa-spinner fa-spin text-3xl text-blue-500"></i>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-10 text-red-600">
         <p>{{ error }}</p>
      </div>

      <!-- Main Content -->
      <div v-else
         class="flex-1 bg-white dark:bg-gray-800 rounded-md shadow-md border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden">
         <!-- Header -->
         <div
            class="px-3 py-1 sm:px-6 sm:py-3 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
            <h4 class="text-lg font-semibold text-gray-800 dark:text-gray-100 flex items-center gap-2">
               <i class="fa-regular fa-building text-yellow-500"></i>
               {{ detailsData.name }}
            </h4>
         </div>

         <!-- Body -->
         <div class="flex-1 overflow-y-auto px-6 py-6 space-y-8">
            <!-- Basic Information -->
            <div>
               <h4 class="text-blue-600 font-bold text-lg mb-4 flex items-center gap-2">
                  <i class="fa-solid fa-info-circle"></i>
                  Basic Information
               </h4>
               <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  <InfoCard label="Company Name" :value="detailsData.name" />
                  <InfoCard label="Company Short Name" :value="detailsData.short_name" />
                  <InfoCard label="Company Code Number" :value="detailsData.code_no" />
                  <InfoCard label="Company Type" :value="makeTitle(detailsData.company_type)" />
                  <InfoCard label="Email" :value="detailsData.email" icon="fa-solid fa-at" />
                  <InfoCard label="Phone" :value="detailsData.phone" icon="fa-solid fa-phone" />
                  <InfoCard label="Website" :value="detailsData.website" icon="fa-solid fa-globe" />
                  <InfoCard label="Established At" :value="detailsData.established_at" icon="fa-solid fa-calendar" />
                  <InfoCard label="Govt. License" :value="detailsData.gov_license" icon="fa-solid fa-id-card" />
                  <InfoCard label="Created At" :value="detailsData.created_time" icon="fa-solid fa-calendar" />
                  <InfoCard label="Updated At" :value="detailsData.updated_time" icon="fa-solid fa-calendar" />
                  <InfoCard label="Is Active" :value="detailsData.is_active" icon="fa-solid fa-toggle-on" />
                  <InfoCard label="Currency" :value="detailsData?.settings?.currency || ''"
                     icon="fa-solid fa-bangladeshi-taka-sign" />
                  <InfoCard label="Timezone" :value="detailsData?.settings?.timezone || ''" icon="fa-solid fa-clock" />
                  <InfoCard label="Invoice Prefix" :value="detailsData?.settings?.invoice_prefix || ''"
                     icon="fa-solid fa-hashtag" />
                  <InfoCard label="Language" :value="makeTitle(detailsData?.settings?.language || '')"
                     icon="fa-solid fa-language" />
                  <InfoCard label="Company Logo" :value="detailsData.logo" icon="fa-image" />
                  <InfoCard label="Address" :value="detailsData.address" icon="fa-location-dot"
                     col-span="col-span-full md:col-span-2 lg:col-span-3" extra-class="whitespace-pre-wrap" />


               </div>
            </div>

            <!-- Owner / Company Admin Information -->
            <div>
               <div class="flex items-center justify-between mb-4">
                  <h4 class="text-blue-600 dark:text-blue-400 font-bold text-lg flex items-center gap-2">
                     <i class="fa-solid fa-user-tie"></i>
                     Company Owners / Admins
                  </h4>

                  <!-- Add Owner Button -->
                  <ActionButton @click="showAddOwnerModal = true" action="create" size="sm" label="Add Owner"/>
               </div>

               <!-- Multiple Owners Table -->
               <div class="relative overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
                  <table class="w-full text-sm text-left text-gray-700 dark:text-gray-300">
                     <thead
                        class="text-xs uppercase bg-gray-100 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-700">
                        <tr>
                           <th scope="col" class="px-6 py-3 font-semibold text-gray-600 dark:text-gray-300">
                              Name
                           </th>
                           <th scope="col" class="px-6 py-3 font-semibold text-gray-600 dark:text-gray-300">
                              Email
                           </th>
                           <th scope="col" class="px-6 py-3 font-semibold text-gray-600 dark:text-gray-300">
                              Phone
                           </th>
                           <th scope="col" class="px-6 py-3 font-semibold text-gray-600 dark:text-gray-300">
                              Role / Designation
                           </th>
                           <th scope="col" class="px-6 py-3 font-semibold text-gray-600 dark:text-gray-300">
                              Joined
                           </th>
                        </tr>
                     </thead>

                     <tbody class="divide-y divide-gray-100 dark:divide-gray-700/60">
                        <tr v-for="(owner, index) in detailsData?.owners || []" :key="index"
                           class="bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700/40 transition-colors">
                           <th scope="row"
                              class="px-6 py-4 font-medium text-gray-900 dark:text-gray-100 whitespace-nowrap">
                              {{ owner.full_name || owner.name || '—' }}
                           </th>
                           <td class="px-6 py-4">
                              <a v-if="owner.email" :href="`mailto:${owner.email}`"
                                 class="text-blue-600 dark:text-blue-400 hover:underline">
                                 {{ owner.email }}
                              </a>
                              <span v-else>—</span>
                           </td>
                           <td class="px-6 py-4">
                              {{ owner.phone || '—' }}
                           </td>
                           <td class="px-6 py-4">
                              {{ owner.designation || owner.role || 'Owner / Admin' }}
                           </td>
                           <td class="px-6 py-4 text-gray-500 dark:text-gray-400">
                              {{ owner.created_at || owner.joined_at || '—' }}
                           </td>
                        </tr>

                        <tr v-if="!detailsData?.owners || detailsData.owners.length === 0">
                           <td colspan="5" class="text-center py-12 text-gray-500 dark:text-gray-400 italic">
                              <div class="flex flex-col items-center gap-2">
                                 <i class="fa-solid fa-users-slash text-4xl text-gray-400 dark:text-gray-500"></i>
                                 <p>No owners / admins added yet</p>
                              </div>
                           </td>
                        </tr>
                     </tbody>
                  </table>
               </div>
            </div>

            <!-- Subscription Information -->
            <div>
               <h4 class="text-blue-600 font-bold text-lg mb-4 flex items-center gap-2">
                  <i class="fa-solid fa-info-circle"></i>
                  Subscription Information
               </h4>
               <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  <InfoCard label="Plan Name" :value="detailsData?.current_subscription?.plan_name || ''"
                     icon="fa-solid fa-tag" />
                  <InfoCard label="Plan Type" :value="makeTitle(detailsData?.current_subscription?.plan_type || '')"
                     icon="fa-solid fa-layer-group" />
                  <InfoCard label="Billing Cycle"
                     :value="makeCapital(detailsData?.current_subscription?.billing_cycle || '')"
                     icon="fa-solid fa-calendar-alt" />
                  <InfoCard label="Price" :value="detailsData?.current_subscription?.price"
                     icon="fa-solid fa-bangladeshi-taka-sign" />
                  <InfoCard label="Duration" :value="getDurationLabel(detailsData?.current_subscription || '')"
                     icon="fa-solid fa-clock" />
                  <InfoCard label="Max Shops" :value="detailsData?.current_subscription?.max_shops || ''"
                     icon="fa-solid fa-cart-shopping" />
                  <InfoCard label="Max Employees" :value="detailsData?.current_subscription?.max_users || ''"
                     icon="fa-solid fa-users" />
                  <InfoCard label="Subscription Status"
                     :value="makeTitle(detailsData?.current_subscription?.status || '')" icon="fa-solid fa-toggle-on" />
                  <InfoCard label="Start Date" :value="detailsData?.current_subscription?.start_time || ''"
                     icon="fa-solid fa-calendar" />
                  <InfoCard label="End Date" :value="detailsData?.current_subscription?.end_time || ''"
                     icon="fa-solid fa-calendar" />
                  <InfoCard label="Days Remaining" :value="detailsData?.current_subscription?.days_remaining || ''"
                     icon="fa-solid fa-calendar" />

               </div>
            </div>

            <!-- Documents -->
            <div>
               <h4 class="text-blue-600 font-bold text-lg mb-4 flex items-center gap-2">
                  <i class="fa-solid fa-list-check"></i>
                  Documents ({{ detailsData.documents.length }})
               </h4>

               <div v-if="detailsData.documents.length === 0"
                  class="text-center py-8 text-gray-500 dark:text-gray-400 italic border-2 border-dashed rounded-lg">
                  No documents uploaded yet.
               </div>

               <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div v-for="(doc, index) in detailsData.documents" :key="index"
                     class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-all overflow-hidden flex flex-col">

                     <!-- Preview Section -->
                     <div
                        class="relative h-48 bg-gray-50 dark:bg-gray-700 flex items-center justify-center overflow-hidden border-b border-gray-200 dark:border-gray-600">
                        <!-- Image Preview -->
                        <img v-if="isImage(doc.document)" :src="doc.document" alt="Document preview"
                           class="max-h-full max-w-full object-contain" loading="lazy"
                           @error="handlePreviewError($event, doc)" />

                        <!-- PDF or Other File - Simple Icon in Center -->
                        <div v-else class="flex flex-col items-center justify-center text-center">
                           <!-- PDF Icon -->
                           <i v-if="isPdf(doc.document)" class="fa-solid fa-file-pdf text-red-500 text-8xl mb-4"></i>

                           <!-- Other File Icon -->
                           <i v-else class="fa-solid fa-file text-8xl text-gray-400 dark:text-gray-500 mb-4"></i>

                           <!-- File Name -->
                           <p class="text-sm font-medium text-gray-800 dark:text-gray-200 truncate max-w-[90%]">
                              {{ getFileName(doc.document) || 'Unnamed File' }}
                           </p>

                           <!-- Extension & Hint -->
                           <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
                              {{ getFileExtension(doc.document).toUpperCase() }} • Click View to open
                           </p>
                        </div>
                     </div>

                     <!-- Info & Action -->
                     <div class="p-3 flex flex-col flex-1">
                        <h5 class="font-medium text-gray-800 dark:text-gray-100 mb-1 truncate">
                           {{ doc.name || 'Unnamed Document' }}
                        </h5>

                        <div class="mt-auto flex justify-end">
                           <button @click="viewDocument(doc.document, doc.name)"
                              class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm rounded-md transition-colors shadow-sm">
                              <i class="fa-solid fa-eye mr-2"></i>
                              View
                           </button>
                        </div>
                     </div>
                  </div>
               </div>
            </div>

            <!-- Created Info -->
            <!-- <div class="border-t pt-4 text-sm text-gray-500 dark:text-gray-400">
               <p>
                  Created by:
                  <strong></strong> 
               </p>
               <p>
                  Created on: <strong></strong>
               </p>
               <p>
                  Status: <span class="text-green-600 font-medium">Active</span>
               </p>
            </div> -->
         </div>
      </div>



      <!-- ========= [ MODAL ] ============ -->
      <CustomModal :isOpen="showAddOwnerModal" @update:isOpen="showAddOwnerModal = $event"
         title="Add New Company Owner / Admin" size="md">
         <template #body>
            <form @submit.prevent="handleAddOwner" class="space-y-5">
               <div class="grid grid-cols-1 gap-5 @sm:grid-cols-2 @xl:grid-cols-2 @3xl:grid-cols-4">

                  <!-- First Name -->
                  <InputeComponent label="First Name" id="first_name" name="first_name" label-for="first_name"
                     placeholder="First Name" v-model="ownerForm.first_name" :error="ownerFormErrors.first_name" />

                  <!-- Last Name -->
                  <InputeComponent label="Last Name" id="last_name" name="last_name" label-for="last_name"
                     placeholder="Last Name" v-model="ownerForm.last_name" :error="ownerFormErrors.last_name" />

                  <!-- Email -->
                  <InputeComponent label="Email" placeholder="Enter email" id="email" name="email" type="email"
                     v-model="ownerForm.email" :error="ownerFormErrors.email" />

                  <!-- Phone -->
                  <InputeComponent label="Phone" placeholder="Enter phone" id="phone" name="phone" type="text"
                     v-model="ownerForm.phone" :error="ownerFormErrors.phone" />

                  <!-- Password -->
                  <InputeComponent label="Password" placeholder="Enter password" id="password" name="password"
                     type="password" v-model="ownerForm.password" :error="ownerFormErrors.password" />

                  <!-- Confirm Password -->
                  <InputeComponent label="Confirm Password" placeholder="Confirm password" id="password_confirmation"
                     name="password_confirmation" type="password" v-model="ownerForm.password_confirmation"
                     :error="ownerFormErrors.password_confirmation" />
               </div>

               <!-- Footer Buttons -->
               <div class="flex justify-end border-t border-default space-x-3 pt-2 md:pt-5">
                  <ActionButton action="cancel" @click="showAddOwnerModal = false" size="sm" label="Cancel" />
                  <ActionButton action="save" size="sm" label="Save" type="submit" />
               </div>
            </form>
         </template>
      </CustomModal>
   </div>
</template>

<script setup>
import { ref, onMounted, reactive, inject } from 'vue';
import { CompanyApiURL, SuscriptionApiURL, SuscriptionPageURL } from '../../routes';
import CustomModal from '@/components/modal/CustomModal.vue';

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
const loading = ref(true);
const error = ref(null);
const detailsData = ref({});

// Owner Modal Data
const showAddOwnerModal = ref(false)
const ownerForm = ref({
   first_name: '',
   last_name: '',
   email: '',
   phone: '',
   password: '',
   password_confirmation: ''
})
const ownerFormErrors = ref({});

// ===================================================================
// =========================== 4. MOUNTED ============================
// ===================================================================
onMounted(() => {
   if (props.itemId && props.itemId !== 'null') {
      fetchPlanDetails();
   } else {
      error.value = 'Invalid plan ID';
      loading.value = false;
   }
});

// ===================================================================
// =========================== 5. METHODS ============================
// ===================================================================
const fetchPlanDetails = async () => {
   loading.value = true;
   error.value = null;

   try {
      const response = await axios.get(
         `${CompanyApiURL.Details}/${props.itemId}/`
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
      loading.value = false;
   }
};

const handleAddOwner = () => {
   ownerFormErrors.value = {}   

   const requiredFields = [
      'first_name',
      'last_name',
      'email',
      'phone',
      'password',
      'password_confirmation',
   ];

   let hasError = false;

   requiredFields.forEach((field) => {
      if (!ownerForm.value[field]) {
         ownerFormErrors.value[field] = `${field.replace(/_/g, ' ')} is required`;
         hasError = true;
      }
   });

   if (hasError) {
      toast.error('Required fields must be entry');
      return;
   }

   // Password match check (optional but recommended)
   if (ownerForm.value.password !== ownerForm.value.password_confirmation) {
      ownerFormErrors.value.password_confirmation = 'Passwords do not match';
      toast.error('Password confirmation mismatch');
      return;
   }

   console.log('New owner data:', ownerForm.value);

   // TODO: API call এখানে দিবে

   // Form Close & Reset
   showAddOwnerModal.value = false;
   ownerForm.value = {
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      password: '',
      password_confirmation: '',
   };
};


// Helper Labels
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

const getDurationLabel = (duration) => {
   if (duration) {
      const durationLabel = `${duration.duration} ${duration.duration_type}`;
      return durationLabel;
   }
   return '';
};

// ====== Helper Functions For File Type ======
const isImage = (url) => {
   if (!url) return false;
   const ext = (url.split('?')[0].split('.').pop() || '').toLowerCase();
   return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'].includes(ext);
};

const isPdf = (url) => {
   if (!url) return false;
   return (url.split('?')[0].split('.').pop() || '').toLowerCase() === 'pdf';
};

const getFileName = (url) => {
   if (!url) return 'Unknown';
   let name = url.split('/').pop().split('?')[0];
   return decodeURIComponent(name);
};

const getFileExtension = (url) => {
   if (!url) return '';
   return (url.split('?')[0].split('.').pop() || '').toLowerCase();
};

const viewDocument = (url, name = 'Document') => {
   if (!url) {
      toast.error('No file available');
      return;
   }
   const newWindow = window.open(url, '_blank');

   if (!newWindow) {
      toast.warning('Popup blocked. Please allow popups or right-click → Open in new tab');
   }
};

const handlePreviewError = (event, doc) => {
   console.warn('Preview failed for:', doc.document);

};
</script>
