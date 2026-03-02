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
         <template #title> Supplier {{ isEditMode ? 'Update' : 'Create' }}</template>

         <!-- Header Right Side -->
         <template #header-right>
            <span class="text-xs text-gray-500 dark:text-gray-400 italic">
               All (<strong class="text-red-600 text-lg">*</strong>) fields are
               required
            </span>
         </template>

         <template #body>
            <form @submit="handleSubmit" enctype="multipart/form-data">
               <!-- Card Body -->
               <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-6 sm:py-6 space-y-3">
                  <!-- Basic Information -->
                  <h4 class="text-blue-600 font-bold text-lg flex items-center gap-2">
                     <i class="fa-solid fa-info-circle"></i>
                     Basic Information
                  </h4>
                  <div class="responsive-grid gap-md">
                     <!-- Name -->
                     <InputeComponent label="Supplier Name" placeholder="Enter supplier name" id="name" name="name"
                        type="text" v-model="formData.name" :error="formErrors.name"/>

                     <!-- Contact Person -->
                     <InputeComponent label="Contact Person Name" placeholder="Enter contact person name" id="contact"
                        name="contact" type="text" v-model="formData.contact" :error="formErrors.contact"/>

                     <!-- Email -->
                     <InputeComponent label="Email" placeholder="Enter email" id="email" name="email" type="email"
                        v-model="formData.email" :error="formErrors.email" />

                     <!-- Phone -->
                     <InputeComponent label="Phone" placeholder="+8801000000000" id="phone" name="phone" type="text"
                        v-model="formData.phone" :error="formErrors.phone"/>

                     <!-- Is Active -->
                     <div>
                        <label for="is_active" class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
                           Active
                        </label>
                        <Checkbox label="Is active ?" v-model="formData.is_active" />
                     </div>
                  </div>
                  <div>
                     <!-- Address -->
                     <TextAreaComponent label="Address" placeholder="Write address..." v-model="formData.address"
                        :rows="4" helpText="You can write up to 500 characters." />
                  </div>
               </div>

               <!-- Card Footer -->
               <div
                  class="px-3 py-2 sm:px-6 sm:py-3 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/40">
                  <!-- Back Button -->
                  <ActionButton action="back" @click="handleBack" variant="outline-secondary" size="sm" label="Back" />

                  <!-- Save Button -->
                  <ActionButton :action="isEditMode ? 'edit' : 'create'" :loading="loadingStates.save" size="sm"
                     :label="isEditMode ? 'Update' : 'Create'" type="submit" />
               </div>
            </form>
         </template>
      </MainContentCard>
   </MasterCardLayout>
</template>

<script setup>
import { inject, ref, onMounted, computed, reactive, watch } from 'vue';
import { SupplierApiURL, SupplierPageURL } from '../../routes';

// ===================================================================
// =========================== 1. INJECTIONS =========================
// ===================================================================
const toast = inject('toast');
const axios = inject('axios');

// Global from window (Django template থেকে আসে)
const accessToken = ref(window.accessToken);
const userId = ref(window.user_id);

// ===================================================================
// =========================== 2. PROPS =============================
// ===================================================================
const props = defineProps({
   itemId: {
      type: [Number, String],
      default: null
   }
});

// ===================================================================
// =========================== 3. DATA ===============================
// ===================================================================
const loadingStates = reactive({
   loading: false,
   back: false,
   draft: false,
   save: false,
});
const error = ref(null);

const formData = ref({
   name: null,
   contact: null,
   email: null,
   phone: null,
   address: null,
   is_active: true,
});

const formErrors = reactive({
   name: '',
   contact: '',
   email: '',
   phone: '',
   address: '',
   is_active: '',
});
const formSubmitted = ref(false);
// ===================================================================
// =========================== 4. COMPUTED ============================
// ===================================================================
const isEditMode = computed(() => !!props.itemId && props.itemId !== 'null');

// ===================================================================
// =========================== 5. ON MOUNTED ========================
// ===================================================================
// onMounted(() => {
//    if (formData.value.documents.length === 0) {
//       addDocument();
//    }
// });

// ===================================================================
// =========================== 6. METHODS ===========================
// ===================================================================
const fetchDetails = async () => {
   if (!props.itemId || props.itemId === 'null') return;

   loadingStates.loading = true;
   try {
      const response = await axios.get(`${SupplierApiURL.Details}/${props.itemId}/`);
      if (response.data.success) {
         console.log(response.data.results);
         const detailsData = response.data.results;
         formData.value.name = detailsData.name;
         formData.value.contact = detailsData.contact;
         formData.value.email = detailsData.email;
         formData.value.phone = detailsData.phone;
         formData.value.address = detailsData.address;
         formData.value.is_active = detailsData.is_active;
      }
   } catch (err) {
      console.error(err);
      // toast.error('Failed to load details');
   } finally {
      loadingStates.loading = false;
   }
};
// ------------------------- Navigation ------------------------------
const handleBack = () => {
   loadingStates.back = true;
   // window.history.back();
   window.location.href = SupplierPageURL.List;
   setTimeout(() => (loadingStates.back = false), 500);
};

// ---------------------------- Validation ----------------------------
const clearErrors = () => {
   Object.keys(formErrors).forEach((key) => (formErrors[key] = ''));
};

const validateFormData = () => {
   let isValid = true;
   clearErrors();

   const required = ['name', 'contact', 'phone'];
   required.forEach((field) => {
      if (!formData.value[field] && formData.value[field] !== 0) {
         formErrors[field] = `${field.replace(/_/g, ' ')} is required`;
         isValid = false;
      }
   });

   return isValid;
};

// -------------------------------- Form Actions ---------------------
const resetForm = () => {
   formData.value = {
      name: null,
      contact: null,
      email: null,
      phone: null,
      address: null,
      is_active: true,
   };
   formSubmitted.value = false;
   clearErrors();
};

const handleSubmit = async (e) => {
   e.preventDefault();
   loadingStates.save = true;

   clearErrors();
   if (!validateFormData()) {
      loadingStates.save = false;
      return;
   }

   const payload = {
      name: formData.value.name,
      contact: formData.value.contact,
      email: formData.value.email,
      phone: formData.value.phone,
      address: formData.value.address,
      is_active: formData.value.is_active,
   };

   //================== [API Call] ==================//
   try {
      let response;
      if (isEditMode.value) {
         response = await axios.put(`${SupplierApiURL.Update}/${props.itemId}/`, payload);
      } else {
         response = await axios.post(`${SupplierApiURL.Create}/`, payload);
      }

      if (response.data.success) {
         toast.success(isEditMode.value ? 'successfully updated' : 'successfully created');
         setTimeout(() => {
            // goBack();
            window.location.href = `${SupplierPageURL.Details}/${response.data.results.id}/`;
         }, 2000);

      } else {
         toast.error(response.data.message || 'Failed to save!');
         console.error(response.data.message || 'Failed to save!');
      }
   } catch (err) {
      console.log(err.response.data.errors.name[0]);
      toast.error(err.response.data.message || 'Something went wrong. Please try again.');
      mapApiErrorsToForm(err.response.data.errors);
   } finally {
      loadingStates.save = false;
   }
};

const mapApiErrorsToForm = (errors) => {
   if (!errors) return;
   Object.keys(errors).forEach((key) => {
      const value = errors[key];
      // ===== Normal field errors =====
      if (formErrors[key] !== undefined) {
         formErrors[key] = Array.isArray(value) ? value[0] : value;
      }
   });
};

// ===================================================================
// =========================== 7. WATCHERS ============================
// ===================================================================
watch(() => props.itemId, (newVal) => {
   if (newVal && newVal !== 'null') {
      fetchDetails();
   }
}, { immediate: true });
</script>
<style scoped></style>