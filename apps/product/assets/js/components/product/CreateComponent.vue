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
         <template #title> Product {{ isEditMode ? 'Update' : 'Create' }}</template>

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

                  

                  <!-- Category -->
                  <h4 class="text-blue-600 font-bold text-lg flex items-center gap-2">
                     <i class="fa-regular fa-rectangle-list"></i>
                     Category
                  </h4>
                  <div class="responsive-grid gap-md">
                     <!-- Category (Level 1 - Root) -->
                     <CustomMultiSelect label="Category" v-model="formData.category_id" :options="categoryChoices"
                        label-key="label" value-key="value" placeholder="Select category"
                        :error="formErrors.category_id" :multiple="false" required />

                     <!-- Dynamic Children (Sub-Category, Sub-sub-category, etc.) -->
                     <div v-for="(level, index) in categoryLevels" :key="index">
                        <CustomMultiSelect :label="getCategoryLevelLabel(index)" v-model="formData.children[index]"
                           :options="level" label-key="label" value-key="value"
                           :placeholder="`Select ${getCategoryLevelName(index + 1)}`" :error="formErrors.children"
                           :multiple="false"
                           :disabled="index === 0 ? !formData.category_id : !formData.children[index - 1]"
                           @update:modelValue="(val) => handleChildSelection(val, index)" />
                     </div>
                  </div>

                  <div class="responsive-grid gap-md">
                     <!-- Name -->
                     <div class="sm:col-span-2">
                        <InputeComponent label="Item Name" placeholder="Enter item name" id="name" name="name"
                           type="text" v-model="formData.name" :error="formErrors.name" required />
                     </div>

                     <!-- Brand -->
                     <CustomMultiSelect label="Brand" v-model="formData.brand_id" :options="brandChoices"
                        label-key="label" value-key="value" placeholder="Select company" :error="formErrors.brand_id"
                        :multiple="false" required />

                     <!-- Is Active -->
                     <div>
                        <label for="is_active" class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
                           Active
                        </label>
                        <Checkbox label="Is active ?" v-model="formData.is_active" />
                     </div>
                  </div>

                  <!-- Variants Information -->
                  <h4 class="text-blue-600 font-bold text-lg flex items-center gap-2">
                     <i class="fa-solid fa-info-circle"></i>
                     Variants Information
                  </h4>

                  <!-- Variants Table -->
                  <div class="overflow-x-auto border rounded-lg">
                     <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead class="bg-gray-50 dark:bg-gray-800">
                           <tr>
                              <th width="20%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Colour</th>
                              <!-- <th width="15%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Size </th>
                              <th width="15%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Unit</th> -->
                              <th width="10%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Qty</th>
                              <th
                                 width="15%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Purchase Price</th>
                              <th
                                 width="15%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Sell Price</th>
                              <th
                                 width="20%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Total Value</th>
                              <th
                                 width="10%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Actions</th>
                           </tr>
                        </thead>
                        <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                           <tr v-for="(variant, index) in formData.variants" :key="index"
                              class="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                              <td class="px-4 py-2">
                                 <CustomMultiSelect v-model="variant.color_id" :options="colorChoices"
                                    label-key="label" value-key="value" placeholder="Select Colour"
                                    :error="formErrors[`variants_${index}_color_id`]" :multiple="false" required />
                              </td>
                              <td class="px-4 py-2" v-show="false">
                                 <CustomMultiSelect v-model="variant.size_id" :options="sizeChoices" label-key="label"
                                    value-key="value" placeholder="Select Size"
                                    :error="formErrors[`variants_${index}_size_id`]" :multiple="false" required />
                              </td>
                              <td class="px-4 py-2" v-show="false">
                                 <CustomMultiSelect v-model="variant.unit_id" :options="unitChoices" label-key="label"
                                    value-key="value" placeholder="Select Unit"
                                    :error="formErrors[`variants_${index}_unit_id`]" :multiple="false" required />
                              </td>
                              <td class="px-4 py-2">
                                 <InputeComponent type="number" v-model="variant.quantity" placeholder="Qty"
                                    :error="formErrors[`variants_${index}_quantity`]"
                                    @update:modelValue="calculateTotal(index)" min="0" />
                              </td>

                              <td class="px-4 py-2">
                                 <InputeComponent type="number" v-model="variant.purchase_price" placeholder="Price"
                                    :error="formErrors[`variants_${index}_purchase_price`]"
                                    @update:modelValue="calculateTotal(index)" min="0" />
                              </td>
                               <td class="px-4 py-2">
                                 <InputeComponent type="number" v-model="variant.selling_price" placeholder="Price"
                                    :error="formErrors[`variants_${index}_selling_price`]"
                                   min="0" />
                              </td>
                              <td class="px-4 py-2 text-right font-medium">
                                 {{ formatCurrency(variant.total_value || 0) }}
                              </td>
                              <td class="px-4 py-2">
                                 <div class="flex justify-center items-center gap-2">
                                    <button type="button" @click="removeVariant(index)"
                                       class="text-red-500 hover:text-red-700 disabled:opacity-50"
                                       :disabled="formData.variants.length <= 1">
                                       <i class="fa-solid fa-trash"></i>
                                    </button>
                                    <button type="button" @click="addVariant"
                                       class="text-green-500 hover:text-green-700">
                                       <i class="fa-solid fa-plus"></i>
                                    </button>
                                 </div>
                              </td>
                           </tr>
                        </tbody>
                        <tfoot class="bg-gray-50 dark:bg-gray-800 font-semibold">
                           <tr>
                              <td colspan="5" class="px-4 py-3 text-right">Grand Total:</td>
                              <td class="px-4 py-3 text-right">{{ formatCurrency(grandTotal) }}</td>
                              <td></td>
                           </tr>
                        </tfoot>
                     </table>
                  </div>

                  <!-- Description -->
                  <h4 class="text-blue-600 font-bold text-lg flex items-center gap-2">
                     <i class="fa-regular fa-newspaper"></i>
                     Description
                  </h4>
                  <div>
                     <TextAreaComponent label="Description" placeholder="Write description..."
                        v-model="formData.description" :rows="4" helpText="You can write up to 500 characters." />
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
import { ProductApiURL, ProductPageURL, CategoryApiURL } from '../../routes';

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
const colorChoices = ref(page.colors)
const sizeChoices = ref(page.sizes)
const unitChoices = ref(page.units)
const categoryChoices = ref(page.categories)
const statusChoices = ref(page.statuses)
// -------------------------------------------------------------------
const loadingStates = reactive({
   loading: false,
   back: false,
   draft: false,
   save: false,
});
const error = ref(null);

// Create a default variant structure
const createDefaultVariant = () => ({
   color_id: null,
   size_id: 1,
   unit_id: 1,
   quantity: 0,
   purchase_price: 0,
   selling_price: 0,
   total_value: 0
});

const formData = ref({
   name: null,
   title: null,
   description: null,
   brand_id: null,
   category_id: null,
   children: [],
   is_featured: false,
   is_active: true,

   // Multiple variants array
   variants: [createDefaultVariant()]
});

const isInitializing = ref(false);

const formErrors = reactive({
   name: '',
   title: '',
   description: '',
   brand_id: '',
   category_id: '',
   children: '',
   is_featured: '',
   is_active: '',

   // We'll handle variant errors dynamically
});

const formSubmitted = ref(false);

// Dynamic category levels
const categoryLevels = ref([]);

// ===================================================================
// =========================== 4. COMPUTED ============================
// ===================================================================
const isEditMode = computed(() => !!props.itemId && props.itemId !== 'null');

// Calculate grand total of all variants
const grandTotal = computed(() => {
   return formData.value.variants.reduce((total, variant) => {
      return total + (variant.total_value || 0);
   }, 0);
});

// Get the last selected category ID (deepest child)
const getLastCategoryId = computed(() => {
   if (formData.value.children.length > 0) {
      for (let i = formData.value.children.length - 1; i >= 0; i--) {
         if (formData.value.children[i]) {
            return formData.value.children[i];
         }
      }
   }
   return formData.value.category_id || null;
});

// ===================================================================
// =========================== 5. METHODS ===========================
// ===================================================================
const formatCurrency = (value) => {
   return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'BDT',
      minimumFractionDigits: 2
   }).format(value);
};

const calculateTotal = (index) => {
   const variant = formData.value.variants[index];
   const quantity = parseFloat(variant.quantity) || 0;
   const price = parseFloat(variant.purchase_price) || 0;
   variant.total_value = quantity * price;
};

const addVariant = () => {
   formData.value.variants.push(createDefaultVariant());
};

const removeVariant = (index) => {
   if (formData.value.variants.length > 1) {
      formData.value.variants.splice(index, 1);
   }
};

const fetchDetails = async () => {
   if (!props.itemId || props.itemId === 'null') return;

   loadingStates.loading = true;
   isInitializing.value = true;

   try {
      const response = await axios.get(`${ProductApiURL.Details}/${props.itemId}/`);

      if (response.data.success) {
         const detailsData = response.data.results;

         formData.value.name = detailsData.name;
         formData.value.is_active = detailsData.is_active;
         formData.value.brand_id = detailsData.brand?.id;
         formData.value.title = detailsData.title;
         formData.value.description = detailsData.description;
         
         // Load variants if available
         if (detailsData.variants && detailsData.variants.length > 0) {
            formData.value.variants = detailsData.variants.map(v => ({
               id: v.id,
               color_id: v.color?.id,
               size_id:  v.size?.id,
               unit_id: v.unit?.id,
               quantity: v.stock || 0,
               purchase_price: v.purchase_price || 0,
               selling_price: v.selling_price || 0,
               total_value: (v.stock || 0) * (v.selling_price || 0)
            }));
         } else {
            formData.value.variants = [createDefaultVariant()];
         }

         const categoryChain = detailsData.category_hierarchy || [];

         if (categoryChain.length > 0) {
            formData.value.category_id = categoryChain[0].id;

            for (let i = 0; i < categoryChain.length; i++) {
               const parentId = categoryChain[i].id;

               const res = await axios.get(`${CategoryApiURL.MiniList}?parent_id=${parentId}`);

               if (res.data.success) {
                  const options = mapOptions(res.data.results);
                  categoryLevels.value[i] = options;
                  formData.value.children[i] = categoryChain[i + 1]?.id || null;
               }
            }
         }
      }
   } catch (err) {
      console.error(err);
   } finally {
      isInitializing.value = false;
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
   const isValidParent = parentId && !(Array.isArray(parentId) && parentId.length === 0);

   if (!isValidParent) {
      categoryLevels.value = categoryLevels.value.slice(0, levelIndex);
      formData.value.children = formData.value.children.slice(0, levelIndex);

      if (levelIndex > 0) {
         formData.value.children[levelIndex - 1] = null;
      }
      return;
   }

   const actualParentId = Array.isArray(parentId) && parentId.length === 1
      ? parentId[0]
      : parentId;

   try {
      const response = await axios.get(`${CategoryApiURL.MiniList}?parent_id=${actualParentId}`);
      if (response.data.success) {
         const options = mapOptions(response.data.results);
         if (options.length > 0) {
            categoryLevels.value[levelIndex] = options;
            categoryLevels.value = categoryLevels.value.slice(0, levelIndex + 1);
            formData.value.children = formData.value.children.slice(0, levelIndex);
         } else {
            categoryLevels.value = categoryLevels.value.slice(0, levelIndex);
            formData.value.children = formData.value.children.slice(0, levelIndex);
         }
      }
   } catch (err) {
      console.error('Error fetching children:', err);
   }
};

const getCategoryLevelLabel = (index) => {
   const levelNames = ['Sub-Category', 'Sub-Sub-Category', 'Level 4', 'Level 5', 'Level 6'];
   return levelNames[index] || `Level ${index + 2}`;
};

const getCategoryLevelName = (level) => {
   const levelNames = ['Category', 'Sub-Category', 'Sub-Sub-Category', 'Level 4', 'Level 5', 'Level 6'];
   return levelNames[level - 1] || `Level ${level}`;
};

const handleChildSelection = async (val, index) => {
   formData.value.children[index] = val;
   formData.value.children = formData.value.children.slice(0, index + 1);
   categoryLevels.value = categoryLevels.value.slice(0, index + 1);
   if (val) {
      await fetchChildren(val, index + 1);
   }
};

// ------------------------- Navigation ------------------------------
const handleBack = () => {
   loadingStates.back = true;
   window.location.href = ProductPageURL.List;
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
      name: null,
      title: null,
      description: null,
      brand_id: null,
      category_id: null,
      children: [],
      is_featured: true,
      is_active: true,
      variants: [createDefaultVariant()]
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
      name: formData.value.name,
      title: formData.value.title,
      description: formData.value.description,
      brand_id: formData.value.brand_id,
      category_id: getLastCategoryId.value,
      is_active: formData.value.is_active,
      is_featured: formData.value.is_featured,
      variants: formData.value.variants.map(v => ({
         ...(v.id && { id: v.id }),
         color_id: v.color_id,
         size_id: v.size_id,
         unit_id: v.unit_id,
         stock: v.quantity,
         purchase_price: v.purchase_price,
         selling_price: v.selling_price
      }))
   };

   // loadingStates.save = false;
   // console.log("========================");
   // console.log(payload);
   // console.log("========================");

   try {
      let response;
      if (isEditMode.value) {
         response = await axios.put(`${ProductApiURL.Update}/${props.itemId}/`, payload);
      } else {
         response = await axios.post(`${ProductApiURL.Create}/`, payload);
      }

      if (response.data.success) {
         toast.success(isEditMode.value ? 'successfully updated' : 'successfully created');
         // setTimeout(() => {
         //    window.location.href = `${ProductPageURL.Details}/${response.data.results.id}/`;
         // }, 2000);
      } else {
         toast.error(response.data.message || 'Failed to save!');
         console.error(response.data.message || 'Failed to save!');
      }
   } catch (err) {
      toast.error(err.response?.data?.message || 'Something went wrong. Please try again.');
      console.log(err.response?.data?.errors?.[0]);
      if (err.response?.data?.errors?.[0]) {
         toast.error(err.response?.data?.errors?.[0]);
      }
      if (err.response?.data?.errors) {
         mapApiErrorsToForm(err.response.data.errors);
      }
   } finally {
      loadingStates.save = false;
   }
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

// Watch category_id (root) - fetch first level children
watch(() => formData.value.category_id, async (newVal, oldVal) => {
   if (isInitializing.value) return;
   if (newVal === oldVal) return;

   formData.value.children = [];
   categoryLevels.value = [];

   const isValid = newVal && !(Array.isArray(newVal) && newVal.length === 0);

   if (!isValid) {
      formData.value.category_id = null;
      return;
   }

   const actualId = Array.isArray(newVal) && newVal.length === 1 ? newVal[0] : newVal;
   formData.value.category_id = actualId;
   await fetchChildren(actualId, 0);
}, { deep: true });
</script>

<style scoped>
/* Optional: Add some styling for the table */
/* .responsive-grid {
   display: grid;
   grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
   gap: 1rem;
} */
</style>