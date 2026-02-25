<template>
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
            <i class="fa-solid fa-shield-alt text-blue-500 dark:text-blue-400"></i>
         </template>

         <!-- Header Title -->
         <template #title>
            {{ isEditMode ? 'Update Role' : 'Create New Role' }}
         </template>

         <!-- Header Right Side -->
         <template #header-right>
            <ActionButton action="save" size="sm" @click="submitForm" class="px-8"
               :label="isEditMode ? 'Update' : 'Save'" :loading="loadingStates.save" />
            <ActionButton action="back" size="sm" @click="goBack" class="px-8 ml-2" label="Back" />
         </template>

         <template #body>
            <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-6 sm:py-6">
               <!-- Role Name Input -->
               <div class="mb-3 bg-white dark:bg-gray-700 rounded-lg px-4 py-2 shadow">
                  <div class="w-full md:w-2/3 lg:w-1/2 xl:w-1/3">
                     <InputeComponent label="Role Name" placeholder="Enter role name" id="name" name="name" type="text"
                        v-model="formData.name" :error="formErrors.name" required />
                  </div>
               </div>

               <!-- Permissions Section -->
               <div class="bg-white dark:bg-gray-700 rounded-lg shadow">
                  <!-- <div class="px-4 py-2 border-b">
                     <h3 class="text-lg font-semibold text-gray-800 dark:text-white flex items-center gap-2">
                        <i class="fa-solid fa-lock"></i>
                        All Permissions
                     </h3>
                     <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Select permissions for this role</p>
                  </div> -->

                  <!-- Search and Select All -->
                  <div class="px-4 py-1.5 border-b bg-gray-50 dark:bg-gray-700">
                     <div class="flex flex-wrap gap-4 items-center justify-between">
                        <h3 class="text-lg font-semibold text-gray-800 dark:text-white flex items-center gap-2">
                           <i class="fa-solid fa-lock"></i>
                           All Permissions
                        </h3>

                        <div class="flex items-center gap-4">
                           <label class="flex items-center gap-2">
                              <input type="checkbox" v-model="selectAll" @change="toggleSelectAll"
                                 class="rounded border-gray-300 text-blue-600 dark:text-gray-600 focus:ring-blue-500 dark:focus:ring-gray-600" />
                              <span class="text-sm font-medium">Select All</span>
                           </label>
                           <span class="text-sm text-gray-500">
                              Selected: {{ selectedPermissions.length }} / {{ totalPermissions }}
                           </span>
                        </div>
                        <div class="relative w-80">
                           <InputeComponent placeholder="Search permissions..." id="search" name="search" type="search"
                              v-model="searchQuery" size="lg" />
                        </div>
                     </div>
                  </div>

                  <!-- Permissions Grid Grouped by Module -->
                  <div class="p-4 space-y-6 max-h-[600px] overflow-y-auto">
                     <div v-for="(permissions, module) in filteredGroupedPermissions" :key="module"
                        class="border rounded-lg overflow-hidden">
                        <!-- Module Header -->
                        <div
                           class="bg-gray-100 dark:bg-gray-800 px-4 py-3 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
                           <h4 class="font-semibold text-gray-700 dark:text-gray-200 flex items-center gap-2">
                              <i class="fa-solid fa-folder-open text-blue-500 dark:text-blue-400"></i>
                              {{ makeCapital(module) }}
                              <span class="text-sm text-gray-500 dark:text-gray-400">({{ permissions.length
                              }})</span>
                           </h4>
                           <label class="flex items-center gap-2 text-sm">
                              <input type="checkbox" :checked="isModuleSelected(module)" @change="toggleModule(module)"
                                 class="rounded border-gray-300 text-blue-600 dark:text-gray-600 focus:ring-blue-500 dark:focus:ring-gray-600" />
                              Select All in {{ makeCapital(module) }}
                           </label>
                        </div>

                        <!-- Module Permissions -->
                        <!-- <div class="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                           <div v-for="permission in permissions" :key="permission.id"
                              class="flex items-start gap-2 p-2 hover:bg-gray-50 rounded dark:hover:bg-gray-600">
                              <input type="checkbox" :id="'perm_' + permission.id" :value="permission.id"
                                 v-model="selectedPermissions"
                                 class="mt-1 rounded border-gray-300 text-blue-600 dark:text-blue-400 focus:ring-blue-500 dark:focus:ring-blue-400" />
                              <label :for="'perm_' + permission.id"
                                 class="text-sm text-gray-700 dark:text-gray-200 cursor-pointer">
                                 {{ permission.name }}
                              </label>
                           </div>
                        </div> -->

                        <!-- Module Permissions -->
                        <div class="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                           <div v-for="permission in permissions" :key="permission.id"
                              class="flex items-start gap-2 p-2 rounded transition-all duration-200 cursor-pointer"
                              :class="[
                                 isPermissionSelected(permission.id)
                                    ? 'bg-green-500 dark:bg-gray-500 text-white shadow-md hover:bg-green-700 dark:hover:bg-gray-600'
                                    : 'hover:bg-gray-100 dark:hover:bg-gray-600 border border-transparent hover:border-gray-200'
                              ]" @click="togglePermission(permission.id)">

                              <div class="relative flex items-start gap-2 w-full">
                                 <input type="checkbox" :id="'perm_' + permission.id" :value="permission.id"
                                    v-model="selectedPermissions"
                                    class="mt-1 rounded border-gray-300 focus:ring-green-700 dark:focus:ring-gray-700"
                                    :class="[
                                       isPermissionSelected(permission.id)
                                          ? 'bg-white border-white text-green-700 dark:text-gray-700 hover:text-green-500 dark:hover:text-gray-800'
                                          : 'text-green-700 dark:text-gray-700 hover:text-green-500 dark:hover:text-gray-800'
                                    ]" @click.stop />

                                 <label :for="'perm_' + permission.id" class="text-sm cursor-pointer flex-1 select-none"
                                    :class="isPermissionSelected(permission.id) ? 'text-white font-medium' : 'text-gray-700 dark:text-gray-200'"
                                    @click.stop>
                                    {{ permission.name }}
                                 </label>

                                 <!-- Optional: Selected indicator icon -->
                                 <i v-if="isPermissionSelected(permission.id)"
                                    class="fa-solid fa-check-circle absolute right-2 top-1/2 -translate-y-1/2 text-white text-xs"></i>
                              </div>
                           </div>
                        </div>
                     </div>

                     <!-- No Results -->
                     <div v-if="Object.keys(filteredGroupedPermissions).length === 0"
                        class="text-center py-10 text-gray-500">
                        <i class="fa-solid fa-search text-4xl mb-3"></i>
                        <p>No permissions found matching "{{ searchQuery }}"</p>
                     </div>
                  </div>
               </div>
            </div>
         </template>
      </MainContentCard>
   </MasterCardLayout>
</template>

<script setup>
import { ref, onMounted, reactive, inject, computed, watch } from 'vue';
import { RoleApiURL, RolePageURL, PermissionApiURL } from '../../routes';

// ===================================================================
// =========================== 1. INJECTIONS =========================
// ===================================================================
const toast = inject('toast');
const axios = inject('axios');

// ===================================================================
// =========================== 2. PROPS ==============================
// ===================================================================
const props = defineProps({
   itemId: {
      type: [Number, String],
      default: null
   }
});

// ===================================================================
// =========================== 3. DATA ================================
// ===================================================================
const loadingStates = reactive({
   loading: false,
   save: false
});
const error = ref(null);
const permissionsList = ref([]);
const selectedPermissions = ref([]);
const searchQuery = ref('');
const formData = ref({
   name: ''
});
const formErrors = reactive({
   name: '',
   permissions: ''
});
const errors = ref({});

// ===================================================================
// =========================== 4. COMPUTED ============================
// ===================================================================
const isEditMode = computed(() => !!props.itemId && props.itemId !== 'null');

const groupedPermissions = computed(() => {
   const groups = {};
   permissionsList.value.forEach(permission => {
      const module = permission.module || 'other';
      if (!groups[module]) {
         groups[module] = [];
      }
      groups[module].push(permission);
   });

   // Sort permissions by name in each group
   Object.keys(groups).forEach(module => {
      groups[module].sort((a, b) => a.name.localeCompare(b.name));
   });

   return groups;
});

const filteredGroupedPermissions = computed(() => {
   if (!searchQuery.value) return groupedPermissions.value;

   const query = searchQuery.value.toLowerCase();
   const filtered = {};

   Object.entries(groupedPermissions.value).forEach(([module, permissions]) => {
      const matchedPermissions = permissions.filter(p =>
         p.name.toLowerCase().includes(query) ||
         p.codename.toLowerCase().includes(query) ||
         module.toLowerCase().includes(query)
      );

      if (matchedPermissions.length > 0) {
         filtered[module] = matchedPermissions;
      }
   });

   return filtered;
});

const totalPermissions = computed(() => permissionsList.value.length);

const selectAll = computed({
   get: () => selectedPermissions.value.length === totalPermissions.value,
   set: (value) => { }
});

// ===================================================================
// =========================== 5. MOUNTED ============================
// ===================================================================
onMounted(() => {
   fetchPermissions();
});

// ===================================================================
// =========================== 6. METHODS ============================
// ===================================================================
const fetchPermissions = async () => {
   loadingStates.loading = true;
   try {
      const response = await axios.get(PermissionApiURL.List);
      if (response.data.success) {
         permissionsList.value = response.data.results;
      }
   } catch (err) {
      console.error(err);
      toast.error('Failed to load permissions');
   } finally {
      loadingStates.loading = false;
   }
};

const fetchRoleDetails = async () => {
   if (!props.itemId || props.itemId === 'null') return;

   loadingStates.loading = true;
   try {
      const response = await axios.get(`${RoleApiURL.Details}/${props.itemId}/`);
      if (response.data.success) {
         const role = response.data.results;
         formData.value.name = role.name;
         selectedPermissions.value = role.permissions.map(p => p.id);
      }
   } catch (err) {
      console.error(err);
      toast.error('Failed to load role details');
   } finally {
      loadingStates.loading = false;
   }
};

// Check if a specific permission is selected
const isPermissionSelected = (permissionId) => {
   return selectedPermissions.value.includes(permissionId);
};

// Optional: Toggle individual permission (যদি div এ click ইভেন্ট ব্যবহার করেন)
const togglePermission = (permissionId) => {
   const index = selectedPermissions.value.indexOf(permissionId);
   if (index === -1) {
      selectedPermissions.value.push(permissionId);
   } else {
      selectedPermissions.value.splice(index, 1);
   }
};

const toggleSelectAll = () => {
   if (selectAll.value) {
      selectedPermissions.value = [];
   } else {
      selectedPermissions.value = permissionsList.value.map(p => p.id);
   }
};

const isModuleSelected = (module) => {
   const modulePermissions = groupedPermissions.value[module] || [];
   const modulePermissionIds = modulePermissions.map(p => p.id);
   return modulePermissions.length > 0 &&
      modulePermissionIds.every(id => selectedPermissions.value.includes(id));
};

const toggleModule = (module) => {
   const modulePermissions = groupedPermissions.value[module] || [];
   const modulePermissionIds = modulePermissions.map(p => p.id);

   if (isModuleSelected(module)) {
      // Deselect all in this module
      selectedPermissions.value = selectedPermissions.value.filter(
         id => !modulePermissionIds.includes(id)
      );
   } else {
      // Select all in this module
      modulePermissionIds.forEach(id => {
         if (!selectedPermissions.value.includes(id)) {
            selectedPermissions.value.push(id);
         }
      });
   }
};

const validateForm = () => {
   let isValid = true;
   formErrors.name = '';
   if (!formData.value.name.trim()) {
      formErrors.name = 'Role name is required';
      isValid = false;
   }
   return isValid;
};

const submitForm = async () => {
   if (!validateForm()) return;

   loadingStates.save = true;

   const payload = {
      name: formData.value.name,
      permissions_ids: selectedPermissions.value
   };

   try {
      let response;
      if (isEditMode.value) {
         response = await axios.put(`${RoleApiURL.Update}/${props.itemId}/`, payload);
      } else {
         response = await axios.post(RoleApiURL.Create, payload);
      }

      if (response.data.success) {
         toast.success(isEditMode.value ? 'Role updated successfully' : 'Role created successfully');
         setTimeout(() => {
            // goBack();
            window.location.href = `${RolePageURL.Details}/${response.data.results.id}/`;
         }, 2000);

      } else {
         toast.error(response.data.message || 'Failed to save role');
      }
   } catch (err) {
      console.error(err.response.data.errors.name[0]);
      if (err.response && err.response.data && err.response.data.errors) {
         const apiErrors = err.response.data.errors;
         formErrors.name = apiErrors.name ? apiErrors.name[0] : '';
      } else {
         toast.error('Something went wrong');
      }
   } finally {
      loadingStates.save = false;
   }
};

const goBack = () => {
   window.location.href = RolePageURL.List;
};

const makeCapital = (v) => {
   if (v) return v.charAt(0).toUpperCase() + v.slice(1);
   return '';
};


// ===================================================================
// =========================== 7. WATCHERS ============================
// ===================================================================
watch(() => props.itemId, (newVal) => {
   if (newVal && newVal !== 'null') {
      fetchRoleDetails();
   }
}, { immediate: true });
</script>