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
         <template #title> Sale {{ isEditMode ? 'Update' : 'Entry' }}</template>

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
                     <div class="sm:col-span-2">
                        <!-- <InputeComponent label="Item Name" placeholder="Enter item name" id="name" name="name"
                           type="text" v-model="formData.name" :error="formErrors.name" required /> -->
                     </div>

                     <!-- Brand -->
                     <!-- <CustomMultiSelect label="Brand" v-model="formData.brand_id" :options="brandChoices"
                        label-key="label" value-key="value" placeholder="Select company" :error="formErrors.brand_id"
                        :multiple="false" required /> -->
                  </div>
               </div>

               <!-- Card Footer -->
               <div
                  class="px-3 py-2 sm:px-6 sm:py-3 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/40">
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
import { SalesApiURL, SalesPageURL, CategoryApiURL } from '../../routes';

// ===================================================================
// =========================== 1. INJECTIONS =========================
// ===================================================================
const toast = inject('toast');
const axios = inject('axios');

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
// ------------------- Data comes from Django template ---------------
const page = window.__PAGE__;
const brandChoices = ref(page.brands)
// -------------------------------------------------------------------
const loadingStates = reactive({
   loading: false,
   back: false,
   draft: false,
   save: false,
});
const error = ref(null);

const formData = ref({

});

const isInitializing = ref(false);

const formErrors = reactive({

});

const formSubmitted = ref(false);

// ===================================================================
// =========================== 4. COMPUTED ============================
// ===================================================================
const isEditMode = computed(() => !!props.itemId && props.itemId !== 'null');

// ===================================================================
// =========================== 5. METHODS ===========================
// ===================================================================
const fetchDetails = async () => {
   if (!props.itemId || props.itemId === 'null') return;

   loadingStates.loading = true;
   isInitializing.value = true;
};

// ------------------------- Navigation ------------------------------
const handleBack = () => {
   loadingStates.back = true;
   window.location.href = SalesPageURL.List;
   setTimeout(() => (loadingStates.back = false), 500);
};

// ---------------------------- Validation ----------------------------
const clearErrors = () => {
   Object.keys(formErrors).forEach((key) => (formErrors[key] = ''));

   // Clear any dynamic variant errors
   Object.keys(formErrors).forEach(key => {
      if (key.startsWith('variants_')) {
         delete formErrors[key];
      }
   });
};

const validateFormData = () => {
   let isValid = true;
   clearErrors();

   // Validate basic required fields
   const required = ['name', 'brand_id', 'category_id'];
   required.forEach((field) => {
      if (!formData.value[field] && formData.value[field] !== 0) {
         formErrors[field] = `${field.replace(/_/g, ' ')} is required`;
         isValid = false;
      }
   });

   // Validate variants
   formData.value.variants.forEach((variant, index) => {
      if (!variant.color_id) {
         formErrors[`variants_${index}_color_id`] = 'Colour is required';
         isValid = false;
      }
      if (!variant.size_id) {
         formErrors[`variants_${index}_size_id`] = 'Size is required';
         isValid = false;
      }
      if (!variant.unit_id) {
         formErrors[`variants_${index}_unit_id`] = 'Unit is required';
         isValid = false;
      }
      if (!variant.quantity || variant.quantity <= 0) {
         formErrors[`variants_${index}_quantity`] = 'Valid quantity is required';
         isValid = false;
      }
      if (!variant.selling_price || variant.selling_price <= 0) {
         formErrors[`variants_${index}_selling_price`] = 'Valid price is required';
         isValid = false;
      }
   });

   return isValid;
};

// -------------------------------- Form Actions ---------------------
const resetForm = () => {
   formData.value = {

   };
   categoryLevels.value = [];
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

   };

   // loadingStates.save = false;
   // console.log("========================");
   // console.log(payload);
   // console.log("========================");

   // try {
   //    let response;
   //    if (isEditMode.value) {
   //       response = await axios.put(`${SalesApiURL.Update}/${props.itemId}/`, payload);
   //    } else {
   //       response = await axios.post(`${SalesApiURL.Create}/`, payload);
   //    }

   //    if (response.data.success) {
   //       toast.success(isEditMode.value ? 'successfully updated' : 'successfully created');
   //       // setTimeout(() => {
   //       //    window.location.href = `${SalesPageURL.Details}/${response.data.results.id}/`;
   //       // }, 2000);
   //    } else {
   //       toast.error(response.data.message || 'Failed to save!');
   //       console.error(response.data.message || 'Failed to save!');
   //    }
   // } catch (err) {
   //    toast.error(err.response?.data?.message || 'Something went wrong. Please try again.');
   //    console.log(err.response?.data?.errors?.[0]);
   //    if (err.response?.data?.errors?.[0]) {
   //       toast.error(err.response?.data?.errors?.[0]);
   //    }
   //    if (err.response?.data?.errors) {
   //       mapApiErrorsToForm(err.response.data.errors);
   //    }
   // } finally {
   //    loadingStates.save = false;
   // }
};

const mapApiErrorsToForm = (errors) => {
   if (!errors) return;
   Object.keys(errors).forEach((key) => {
      const value = errors[key];
      if (key.includes('variants')) {
         // Handle variant errors (you may need to parse the index from the error key)
         formErrors[key] = Array.isArray(value) ? value[0] : value;
      } else if (formErrors[key] !== undefined) {
         formErrors[key] = Array.isArray(value) ? value[0] : value;
      }
   });
};

// ===================================================================
// =========================== 6. WATCHERS ============================
// ===================================================================
watch(() => props.itemId, (newVal) => {
   if (newVal && newVal !== 'null') {
      fetchDetails();
   }
}, { immediate: true });


</script>

<style scoped>

</style>