<template>
   <div class="w-full md:w-1/2">
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
            <template #title> Category {{ isEditMode ? 'Update' : 'Create' }}</template>

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
                        Category Information
                     </h4>
                     <div class="space-y-3">
                        <!-- Name -->
                        <InputeComponent label="Category Name" placeholder="Enter category name" id="name" name="name"
                           type="text" v-model="formData.name" :error="formErrors.name" />

                        <!-- Root Parent -->
                        <CustomMultiSelect label="Root Category" v-model="formData.parent"
                           :options="rootCategoryChoices" label-key="label" value-key="value"
                           placeholder="Select root category" :error="formErrors.parent" />

                        <!-- Dynamic Children -->
                        <div v-for="(level, index) in categoryLevels" :key="index">
                           <CustomMultiSelect :label="`Child Level ${index + 1}`" v-model="formData.children[index]"
                              :options="level" label-key="label" value-key="value" placeholder="Select category"
                              @update:modelValue="(val) => fetchChildren(val, index)" />
                        </div>

                        <!-- Logo -->
                        <FileInputComponent label="Category Logo" v-model="formData.logo"
                           :current-image-url="formData?.logo" :error="formErrors.logo" :accept="['image/*']"
                           help-text="Square logo (1:1 ratio)" :max-size="2 * 1024 * 1024" />

                        <!-- Is Active -->
                        <div>
                           <label for="is_active"
                              class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
                              Active
                           </label>
                           <Checkbox label="Is active ?" v-model="formData.is_active" />
                        </div>
                     </div>
                  </div>

                  <!-- Card Footer -->
                  <div
                     class="px-3 py-2 sm:px-6 sm:py-3 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/40">
                     <!-- Back Button -->
                     <ActionButton action="back" @click="handleBack" variant="outline-secondary" size="sm"
                        label="Back" />

                     <!-- Save Button -->
                     <ActionButton :action="isEditMode ? 'edit' : 'create'" :loading="loadingStates.save" size="sm"
                        :label="isEditMode ? 'Update' : 'Create'" type="submit" />
                  </div>
               </form>
            </template>
         </MainContentCard>
      </MasterCardLayout>
   </div>
</template>

<script setup>
import { inject, ref, onMounted, computed, reactive, watch } from 'vue';
import { CategoryApiURL, CategoryPageURL } from '../../routes';

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
   },
   rootCategoryChoices: {
      type: Array,
      required: true,
      default: () => [],
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
   parent: null,
   children: [],
   logo: null,
   is_active: true,
});

const formErrors = reactive({
   name: '',
   parent: '',
   children: '',
   logo: '',
   is_active: '',
});
const formSubmitted = ref(false);
const categoryLevels = ref([]);
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
      const response = await axios.get(`${CategoryApiURL.Details}/${props.itemId}/`);
      if (response.data.success) {
         const data = response.data.results;
         formData.value.name = data.name;
         const chain = data.parent_chain || [];
         if (chain.length) {
            // first parent
            formData.value.parent = chain[0].id;

            // load children
            for (let i = 0; i < chain.length; i++) {
               const parentId = chain[i].id;
               const res = await axios.get(`${CategoryApiURL.List}?parent_id=${parentId}`);
               if (res.data.success) {
                  const options = mapOptions(res.data.results);
                  categoryLevels.value[i] = options;
                  formData.value.children[i] = chain[i + 1]?.id || null;
               }
            }
         }
      }
   } catch (err) {
      console.error(err);
   } finally {
      loadingStates.loading = false;
   }
};

const mapOptions = (data) => {
   return data.map(item => ({
      value: item.id,
      label: item.name
   }));
};

const fetchChildren = async (parentId, levelIndex = 0) => {
   if (!parentId) return;
   try {
      const response = await axios.get(`${CategoryApiURL.List}?parent_id=${parentId}`);
      if (response.data.success) {
         const options = mapOptions(response.data.results);
         if (options.length) {
            categoryLevels.value[levelIndex + 1] = options;
         }
         // remove deeper levels if parent changed
         categoryLevels.value = categoryLevels.value.slice(0, levelIndex + 2);
      }
   } catch (err) {
      console.error(err);
   }
};

// ------------------------- Navigation ------------------------------
const handleBack = () => {
   loadingStates.back = true;
   // window.history.back();
   window.location.href = CategoryPageURL.List;
   setTimeout(() => (loadingStates.back = false), 500);
};

// ---------------------------- Validation ----------------------------
const clearErrors = () => {
   Object.keys(formErrors).forEach((key) => (formErrors[key] = ''));
};

const validateFormData = () => {
   let isValid = true;
   clearErrors();

   const required = ['name'];
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
      parent: null,
      children: [],
      logo: null,
      is_active: true,
   };
   formSubmitted.value = false;
   clearErrors();
};

const handleSubmit = async (e) => {
   e.preventDefault();
   loadingStates.save = true;

   // clearErrors();
   // if (!validateFormData()) {
   //    loadingStates.save = false;
   //    return;
   // }

   const formDataToSend = new FormData();
   formDataToSend.append('name', formData.value.name || '');
   formDataToSend.append('is_active', formData.value.is_active);
   if (getParentId()) {
      formDataToSend.append('parent_id', getParentId());
   }
   if (formData.value.logo) {
      formDataToSend.append('logo', formData.value.logo);
   }

   //================== [API Call] ==================//
   try {
      let response;
      if (isEditMode.value) {
         response = await axios.put(`${CategoryApiURL.Update}/${props.itemId}/`, formDataToSend, {});
      } else {
         response = await axios.post(`${CategoryApiURL.Create}/`, formDataToSend, {});
      }

      if (response.data.success) {
         toast.success(isEditMode.value ? 'successfully updated' : 'successfully created');
         if (!isEditMode.value) {
            resetForm();
         }
         clearErrors();
         setTimeout(() => {
            // goBack();
            // window.location.href = `${CategoryPageURL.Details}/${response.data.results.id}/`;
            window.location.reload(); // Reload page
         }, 2000);
      } else {
         toast.error(response.data.message || 'Failed to save!');
         mapApiErrorsToForm(response.data.errors);
      }
   } catch (err) {
      console.log(err.response.data.errors);
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
      // console.log("====================")
      // console.log(key, value);
      // console.log("====================")
      // ===== Normal field errors =====
      if (formErrors[key] !== undefined) {
         formErrors[key] = Array.isArray(value) ? value[0] : value;
      }
   });
};

const getParentId = () => {
   // children array reverse করে প্রথম non-null value নাও
   const lastChild = [...formData.value.children].reverse().find(v => v);
   if (lastChild) {
      return lastChild;
   }
   return formData.value.parent || null;
};

// ===================================================================
// =========================== 7. WATCHERS ============================
// ===================================================================
watch(() => props.itemId, (newVal) => {
   if (newVal && newVal !== 'null') {
      fetchDetails();
   }
}, { immediate: true });

watch(() => formData.value.parent, async (newParent) => {
   formData.value.children = [];
   categoryLevels.value = [];
   if (!newParent) return;
   try {
      const response = await axios.get(`${CategoryApiURL.List}?parent_id=${newParent}`);
      if (response.data.success) {
         categoryLevels.value[0] = mapOptions(response.data.results);
         // console.log("========================");
         // console.log(response.data.results);
         // console.log("========================");
      }
   } catch (err) {
      console.error(err);
   }
});
</script>
<style scoped></style>