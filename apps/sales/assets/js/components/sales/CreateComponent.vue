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
                     Customer Information
                  </h4>
                  <div class="responsive-grid gap-md">
                     <!-- Name -->
                     <InputeComponent label="Name" placeholder="Enter customer name" id="name" name="name" type="text"
                        v-model="formData.c_name" :error="formErrors.c_name" required />

                     <!-- Email -->
                     <InputeComponent label="Email" placeholder="Enter customer email" id="email" name="email"
                        type="email" v-model="formData.c_email" :error="formErrors.c_email" />

                     <!-- Phone -->
                     <InputeComponent label="Phone" placeholder="Enter customer phone" id="phone" name="phone"
                        type="text" v-model="formData.c_phone" :error="formErrors.c_phone" required />

                     <!-- Address -->
                     <div class="sm:col-span-2">
                        <InputeComponent label="Address" placeholder="Enter customer address" id="address"
                           name="address" type="text" v-model="formData.c_address" :error="formErrors.c_address" />
                     </div>

                     <!-- Brand -->
                     <!-- <CustomMultiSelect label="Brand" v-model="formData.brand_id" :options="brandChoices"
                        label-key="label" value-key="value" placeholder="Select company" :error="formErrors.brand_id"
                        :multiple="false" required /> -->
                  </div>

                  <!-- Variants Information -->
                  <h4 class="text-blue-600 font-bold text-lg flex items-center gap-2">
                     <i class="fa-solid fa-info-circle"></i>
                     Product Information
                  </h4>

                  <!-- Variants Table -->
                  <div class="overflow-x-auto border rounded-lg">
                     <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                        <thead class="bg-gray-50 dark:bg-gray-800">
                           <tr>
                              <th width="50%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Product
                              </th>
                              <th width="15%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Unit Price
                              </th>
                              <th width="10%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Quantity
                              </th>
                              <th width="15%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Total Value
                              </th>
                              <th width="10%"
                                 class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                 Actions
                              </th>
                           </tr>
                        </thead>
                        <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                           <tr v-for="(variant, index) in formData.variants" :key="index"
                              class="hover:bg-gray-50 dark:hover:bg-gray-800/50">

                              <!-- Product -->
                              <td class="px-4 py-2">
                                 <CustomMultiSelect
                                    v-model="formData.variants[index].variant_id"
                                    :options="productVariantLists[formData.variants[index].search_key] || []"
                                    label-key="label"
                                    value-key="value"
                                    placeholder="Search Product Variant"
                                    :multiple="false"
                                    @search="(query) => fetchProductVariants(query, formData.variants[index].search_key)" />
                                 <!-- Product Info -->
                                 <div v-if="formData.variants[index].variant_id" class="mt-2 text-xs text-gray-600 dark:text-gray-400">
                                    <div class="flex flex-wrap gap-x-3 gap-y-1">
                                       <span v-if="getSelectedVariant(index)?.product_name" class="font-medium">
                                          {{ getSelectedVariant(index)?.product_name }}
                                       </span>
                                       <span v-if="getSelectedVariant(index)?.product_code">
                                          Code: {{ getSelectedVariant(index)?.product_code }}
                                       </span>
                                       <span v-if="getSelectedVariant(index)?.sku">
                                          SKU: {{ getSelectedVariant(index)?.sku }}
                                       </span>
                                       <span v-if="getSelectedVariant(index)?.color_name">
                                          Color: {{ getSelectedVariant(index)?.color_name }}
                                       </span>
                                       <!-- <span v-if="getSelectedVariant(index)?.size_name">
                                          Size: {{ getSelectedVariant(index)?.size_name }}
                                       </span>
                                       <span v-if="getSelectedVariant(index)?.unit_name">
                                          Unit: {{ getSelectedVariant(index)?.unit_name }}
                                       </span> -->
                                        <span v-if="formData.variants[index].selling_price">Selling Price: {{ formData.variants[index].selling_price.toFixed(2) }}</span>
                                       <span v-if="getSelectedVariant(index)?.stock !== undefined" 
                                          :class="getSelectedVariant(index)?.stock <= 0 ? 'text-red-500 font-semibold' : 'text-green-600'">
                                          Stock: {{ getSelectedVariant(index)?.stock }}
                                       </span>
                                      
                                    </div>
                                 </div>
                              </td>
                              <!-- sell Price -->                             
                              <td class="px-4 py-2">
                                 <InputeComponent type="number" v-model="formData.variants[index].unit_price" placeholder="Sell Price" />
                              </td>

                              <!-- Quantity -->
                              <td class="px-4 py-2">
                                 <InputeComponent type="number" v-model="formData.variants[index].quantity" placeholder="Qty" />
                              </td>

                              <!-- Total Value -->
                              <td class="px-4 py-2">
                                 {{ (variant.unit_price * variant.quantity).toFixed(2) }}
                              </td>

                              <!-- Actions -->
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
                              <td colspan="3" class="px-4 py-3 text-right">Grand Total:</td>
                              <td class="px-4 py-3 text-right">৳ {{ grandTotal }}</td>
                              <td></td>
                           </tr>
                        </tfoot>
                     </table>
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
import { SalesApiURL, SalesPageURL, ProductVariationListApiURL } from '../../routes';

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
   c_name: null,
   c_email: null,
   c_phone: null,
   c_address: null,
   variants: [],
});

const formErrors = reactive({

});

const formSubmitted = ref(false);

// Product Variants - Map to store variant lists for each row
const productVariantLists = reactive({}); // { [searchKey]: [...] }
const productVariantLoading = ref(false);

// ===================================================================
// =========================== 4. COMPUTED ============================
// ===================================================================
const isEditMode = computed(() => !!props.itemId && props.itemId !== 'null');

const grandTotal = computed(() => {
   return formData.value.variants.reduce((total, variant) => {
      const price = parseFloat(variant.unit_price) || 0;
      const qty = parseInt(variant.quantity) || 0;
      return total + (price * qty);
   }, 0).toFixed(2);
});

// ===================================================================
// =========================== 5. METHODS ===========================
// ===================================================================
const fetchDetails = async () => {
   if (!props.itemId || props.itemId === 'null') return;

   loadingStates.loading = true;
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
   const required = ['c_name', 'c_phone'];
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


// ------------------------ Product Variants ------------------------
const createDefaultVariant = () => ({
   variant_id: null,
   unit_price: 0,
   selling_price: 0,
   quantity: 1,
   total: 0,
   search_key: Date.now() + Math.random(), // Unique key for each row's search
});

const fetchProductVariants = async (search = '', searchKey = null) => {
   console.log("========================");
   console.log("Search Query:", search);
   console.log("Search Key:", searchKey);
   console.log("========================");

   if (!searchKey) {
      console.warn("No search key provided!");
      return;
   }

   try {
      productVariantLoading.value = true;

      const params = {};
      if (search && search.trim()) {
         params.search = search.trim();
      }

      const response = await axios.get(ProductVariationListApiURL, { params });

      if (response.data.success) {
         productVariantLists[searchKey] = response.data.results.map(item => ({
            value: item.id,
            label: `${item.product.name} - ${item.product.code} - ${item.color?.name || 'N/A'} - ${item.size?.name || 'N/A'} - ${item.unit?.name || 'N/A'}`,
            price: parseFloat(item.selling_price) || 0,
            stock: item.stock || 0,
            sku: item.sku || '',
            product_code: item.product.code || '',
            product_name: item.product.name || '',
            color_name: item.color?.name || 'N/A',
            size_name: item.size?.name || 'N/A',
            unit_name: item.unit?.name || 'N/A',
         }));
      }

   } catch (err) {
      console.error(err);
   } finally {
      productVariantLoading.value = false;
   }
};

const addVariant = () => {
   formData.value.variants.push(createDefaultVariant());
};

const removeVariant = (index) => {
   if (formData.value.variants.length > 1) {
      formData.value.variants.splice(index, 1);
   }
};

const getSelectedVariant = (index) => {
   const variant = formData.value.variants[index];
   if (!variant?.variant_id || !variant?.search_key) return null;
   const list = productVariantLists[variant.search_key];
   if (!list) return null;
   return list.find(p => p.value === variant.variant_id) || null;
};
// ===================================================================
// =========================== 6. WATCHERS ============================
// ===================================================================
watch(() => props.itemId, (newVal) => {
   if (newVal && newVal !== 'null') {
      fetchDetails();
   }
}, { immediate: true });

watch(
   () => formData.value.variants,
   (variants) => {
      variants.forEach((variant) => {
         if (!variant.search_key || !variant.variant_id) return;
         
         const list = productVariantLists[variant.search_key];
         if (!list) return;
         
         const selected = list.find(p => p.value === variant.variant_id);

         if (selected) {
            variant.selling_price = selected.price;
         }

         variant.total = variant.unit_price * variant.quantity;
      });
   },
   { deep: true }
);
// ===================================================================
// =========================== 7. MOUNTED ============================
// ===================================================================
onMounted(() => {
   if (!formData.value.variants.length) {
      formData.value.variants.push(createDefaultVariant());
   }
});

</script>

<style scoped></style>