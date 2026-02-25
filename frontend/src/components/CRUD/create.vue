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
         <template #title> Employee Create </template>

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
                     <!-- First Name -->
                     <InputeComponent label="First Name" placeholder="Enter first name" id="first_name"
                        name="first_name" type="text" v-model="formData.first_name" :error="formErrors.first_name"
                        required />

                     <!-- Last Name -->
                     <InputeComponent label="Last Name" placeholder="Enter last name" id="last_name" name="last_name"
                        type="text" v-model="formData.last_name" :error="formErrors.last_name" required />

                     <!-- email -->
                     <InputeComponent label="Email" placeholder="Enter email" id="email" name="email" type="email"
                        v-model="formData.email" :error="formErrors.email" required />

                     <!-- phone -->
                     <InputeComponent label="Phone" placeholder="Enter phone" id="phone" name="phone" type="text"
                        v-model="formData.phone" :error="formErrors.phone" required />

                     <!-- Gender -->
                     <CustomMultiSelect label="Gender" v-model="formData.gender" :options="genderChoices"
                        label-key="label" value-key="value" placeholder="Select gender" :error="formErrors.gender"
                        :multiple="false" required />

                     <!-- Date of Birth -->
                     <InputeComponent label="Date of Birth (Age 18+ required)" placeholder="Enter date of birth"
                        id="dob" name="dob" type="date" v-model="formData.dob" :error="formErrors.dob" required />

                     <!-- Religion -->
                     <CustomMultiSelect label="Religion" v-model="formData.religion_id" :options="religionChoices"
                        label-key="label" value-key="value" placeholder="Select religion"
                        :error="formErrors.religion_id" :multiple="false" required />

                     <!-- Blood Group -->
                     <CustomMultiSelect label="Blood Group" v-model="formData.blood_group" :options="bloodGroupChoices"
                        label-key="label" value-key="value" placeholder="Select blood group"
                        :error="formErrors.blood_group" :multiple="false" />

                     <!-- NID -->
                     <InputeComponent label="NID (10 or 17 digits)" placeholder="Enter NID" id="nid" name="nid"
                        type="text" v-model="formData.nid" :error="formErrors.nid" />

                     <!-- Passport No -->
                     <InputeComponent label="Passport No (Ex: A00000001)" placeholder="Enter passport no"
                        id="passport_no" name="passport_no" type="text" v-model="formData.passport_no"
                        :error="formErrors.passport_no" />


                     <!-- Roles -->
                     <CustomMultiSelect label="Roles" v-model="formData.role_ids" :options="roleChoices"
                        label-key="label" value-key="value" placeholder="Select roles" :error="formErrors.role_ids"
                        :multiple="true" required />

                     <!-- Password -->
                     <InputeComponent label="Password" placeholder="Enter password" id="password" name="password"
                        type="password" v-model="formData.password" :error="formErrors.password" required />

                     <!-- Confirm Password -->
                     <InputeComponent label="Confirm Password" placeholder="Enter confirm password"
                        id="confirm_password" name="confirm_password" type="password"
                        v-model="formData.confirm_password" :error="formErrors.confirm_password" required />

                     <!-- Is Active -->
                     <div>
                        <label for="is_active" class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
                           Active
                        </label>
                        <Checkbox label="Is active ?" v-model="formData.is_active" />
                     </div>
                  </div>

                  <!-- Employee Information -->
                  <h4 class="text-blue-600 font-bold text-lg flex items-center gap-2">
                     <i class="fa-solid fa-info-circle"></i>
                     Employee Information
                  </h4>
                  <div class="responsive-grid gap-md">
                     <!-- Company -->
                     <CustomMultiSelect label="Company" v-model="formData.company_id" :options="companyChoices"
                        label-key="label" value-key="value" placeholder="Select company" :error="formErrors.company_id"
                        :multiple="false" required />

                     <!-- Employee ID -->
                     <InputeComponent label="Employee ID" placeholder="Enter employee id" id="employee_id"
                        name="employee_id" type="text" v-model="formData.employee_id" :error="formErrors.employee_id"
                        required />

                     <!-- Designation -->
                     <CustomMultiSelect label="Designation" v-model="formData.designation_id"
                        :options="designationChoices" label-key="label" value-key="value"
                        placeholder="Select designation" :error="formErrors.designation_id" :multiple="false" />

                     <!-- Department -->
                     <CustomMultiSelect label="Department" v-model="formData.department_id" :options="departmentChoices"
                        label-key="label" value-key="value" placeholder="Select department"
                        :error="formErrors.department_id" :multiple="false" />

                     <!-- Joining Date -->
                     <InputeComponent label="Joining Date" placeholder="Enter joining date" id="joining_date"
                        name="joining_date" type="date" v-model="formData.joining_date" :error="formErrors.joining_date"
                        required />

                     <!-- Employee Status -->
                     <CustomMultiSelect label="Employee Status" v-model="formData.status" :options="empStatusChoices"
                        label-key="label" value-key="value" placeholder="Select employee status"
                        :error="formErrors.status" :multiple="false" required />

                     <!-- Employee Notes -->
                     <!-- <InputeComponent label="Employee Notes" placeholder="Enter notes" id="notes" name="notes" type="text"
                        v-model="formData.notes" :error="formErrors.notes" /> -->
                     <div class="grid-col-span-2">
                        <TextAreaComponent label="Employee Notes" placeholder="Write employee notes..."
                           v-model="formData.notes" :rows="4" helpText="You can write up to 500 characters." />
                     </div>

                     <!-- Address -->
                     <div class="grid-col-span-2">
                        <TextAreaComponent label="Address" placeholder="Write your address..."
                           v-model="formData.address" :rows="4" helpText="You can write up to 500 characters." />
                     </div>

                     <!-- Image -->
                     <FileInputComponent label="Profile Image" v-model="formData.profile_img"
                        :current-image-url="formData?.profile_img" :error="formErrors.profile_img" :accept="['image/*']"
                        help-text="Square logo (1:1 ratio)" :max-size="2 * 1024 * 1024" />
                  </div>
               </div>

               <!-- Card Footer -->
               <div
                  class="px-3 py-2 sm:px-6 sm:py-3 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/40">
                  <!-- Back Button -->
                  <ActionButton action="back" @click="handleBack" variant="outline-secondary" size="sm" label="Back" />

                  <!-- Save Button -->
                  <ActionButton action="create" :loading="loadingStates.save" size="sm" label="Create company"
                     type="submit" />
               </div>
            </form>
         </template>
      </MainContentCard>
   </MasterCardLayout>
</template>

<script setup>
import { ref, onMounted, reactive, inject } from 'vue';
import { validateForm } from '@/utils/validation.js'
import { createEmployeeValidationRules } from '../../validation/employee.js'
import { EmployeeApiURL } from '../../routes';

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
   genderChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
   bloodGroupChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
   religionChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
   departmentChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
   designationChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
   empStatusChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
   roleChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
   companyChoices: {
      type: Array,
      required: true,
      default: () => [],
   },
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

// const formData = ref({
//    first_name: null,
//    last_name: null,
//    email: null,
//    phone: null,
//    gender: null,
//    dob: null,
//    blood_group: null,
//    nid: null,
//    passport_no: null,
//    religion_id: null,
//    password: null,
//    confirm_password: null,
//    is_active: true,
//    employee_id: null,
//    department_id: null,
//    designation_id: null,
//    joining_date: null,
//    status: null,
//    notes: null,
//    address: null,
//    profile_img: null,
//    role_ids: [],
// });

const formData = ref({
   first_name: "Mr Korim",
   last_name: "Uddin",
   email: "korim@gmail.com",
   phone: "+8801500000011",
   gender: "male",
   dob: "1999-01-01",
   blood_group: "AB+",
   nid: "1000000001",
   passport_no: "A00000001",
   religion_id: 1,
   password: "123456Ra",
   confirm_password: "123456Ra",
   timezone: "Asia/Dhaka",
   language_preference: "en",
   is_active: true,
   company_id: 1,
   employee_id: "EMP10001",
   department_id: null,
   designation_id: null,
   joining_date: "2023-01-01",
   status: 'active',
   notes: null,
   address: null,
   profile_img: null,
   role_ids: [2],
});

const formErrors = reactive({
   first_name: '',
   last_name: '',
   email: '',
   phone: '',
   gender: '',
   dob: '',
   blood_group: '',
   nid: '',
   passport_no: '',
   religion_id: '',
   password: null,
   confirm_password: null,
   is_active: '',
   company_id: '',
   employee_id: '',
   department_id: '',
   designation_id: '',
   joining_date: '',
   status: '',
   notes: '',
   address: '',
   profile_img: '',
   role_ids: '',
});
const formSubmitted = ref(false);

// ===================================================================
// =========================== 4. WATCH =============================
// ===================================================================
// ************* Here haven't any watchers *********

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

// ------------------------- Navigation ------------------------------
const handleBack = () => {
   loadingStates.back = true;
   window.history.back();
   setTimeout(() => (loadingStates.back = false), 500);
};

const handleCancel = () => {
   if (confirm('Are you sure? All unsaved changes will be lost.')) {
      resetForm();
   }
};

// ---------------------------- Validation ----------------------------
const validationRules = createEmployeeValidationRules({
   genderChoices: props.genderChoices,
   bloodGroupChoices: props.bloodGroupChoices,
   religionChoices: props.religionChoices,
   departmentChoices: props.departmentChoices,
   designationChoices: props.designationChoices,
   empStatusChoices: props.empStatusChoices,
   roleChoices: props.roleChoices,
});

const validateFormData = () => {
   return validateForm(formData.value, validationRules, formErrors);
};

// -------------------------------- Form Actions ---------------------
const resetForm = () => {
   formData.value = {
      first_name: null,
      last_name: null,
      email: null,
      phone: null,
      gender: null,
      dob: null,
      blood_group: null,
      nid: null,
      passport_no: null,
      religion_id: null,
      password: null,
      confirm_password: null,
      is_active: true,
      company_id: null,
      employee_id: null,
      department_id: null,
      designation_id: null,
      joining_date: null,
      status: null,
      notes: null,
      address: null,
      profile_img: null,
      role_ids: [],
   };
   formSubmitted.value = false;
   clearErrors();
};

const clearErrors = () => {
   Object.keys(formErrors).forEach((key) => (formErrors[key] = ''));
};

const handleSubmit = async (e) => {
   e.preventDefault();
   loadingStates.save = true;
   clearErrors();

   if (!validateFormData()) {
      loadingStates.save = false;
      return;
   }

   const formDataToSend = new FormData();

   // Basic information
   formDataToSend.append('first_name', formData.value.first_name);
   formDataToSend.append('last_name', formData.value.last_name);
   formDataToSend.append('email', formData.value.email);
   formDataToSend.append('phone', formData.value.phone);
   formDataToSend.append('gender', formData.value.gender);
   formDataToSend.append('dob', formData.value.dob);
   formDataToSend.append('blood_group', formData.value.blood_group);
   formDataToSend.append('nid', formData.value.nid);
   formDataToSend.append('passport_no', formData.value.passport_no);
   formDataToSend.append('religion_id', formData.value.religion_id || '');
   formDataToSend.append('is_active', formData.value.is_active);
   formDataToSend.append('address', formData.value.address);
   formDataToSend.append('timezone', formData.value.timezone);
   formDataToSend.append('language_preference', formData.value.language_preference);

   // Passwords
   if (formData.value.password) {
      formDataToSend.append('password', formData.value.password);
      formDataToSend.append('confirm_password', formData.value.confirm_password);
   }

   // Roles 
   if (formData.value.role_ids && formData.value.role_ids.length > 0) {
      formData.value.role_ids.forEach((roleId, index) => {
         formDataToSend.append(`role_ids[${index}]`, roleId);
      });
   }

   // Employee Information
   if (formData.value.employee_id) {
      formDataToSend.append('employee.employee_id', formData.value.employee_id || '');
      formDataToSend.append('employee.company_id', formData.value.company_id || '');
      formDataToSend.append('employee.department_id', formData.value.department_id || '');
      formDataToSend.append('employee.designation_id', formData.value.designation_id || '');
      formDataToSend.append('employee.joining_date', formData.value.joining_date);
      formDataToSend.append('employee.status', formData.value.status || '');
      formDataToSend.append('employee.notes', formData.value.notes || '');
   }

   // console.log("FormData entries:");
   // for (let [key, value] of formDataToSend.entries()) {
   //    console.log(key, value instanceof File ? `${value.name} (File)` : value + " Type: " + typeof value);
   // }

   // Profile Image (single file)
   if (formData.value.profile_img instanceof File) {
      formDataToSend.append('profile_img', formData.value.profile_img);
   }

   //================== [API Call] ==================//
   try {
      const result = await createApiCall(formDataToSend);

      if (result.success) {
         toast.success(result.message || 'Successfully created!');
         resetForm();
      } else {
         toast.error(result.message || 'Something went wrong. Please try again.');
         mapApiErrorsToForm(result.errors);
      }
   } catch (err) {
      console.error('Unexpected exception:', err);
      toast.error('Something went wrong. Please try again.');
   } finally {
      loadingStates.save = false;
   }
};

const createApiCall = async (formDataToSend) => {
   try {
      const res = await axios.post(
         `${EmployeeApiURL.Create}/`,
         formDataToSend,
         {}
      );
      if (res.status >= 200 && res.status < 300) {
         return {
            success: true,
            message: res.data.message || 'Successfully created!',
            data: res.data.results || res.data,
         };
      } else {
         return {
            success: false,
            message: res.data.message || 'Request failed',
            errors: res.data.errors || res.data.error || res.data,
         };
      }
   } catch (error) {
      // console.error('API Error:', error);

      let errorMessage = 'Unexpected error occurred';
      let errors = {};

      if (error.response) {
         errorMessage = error.response.data.message || 'Validation failed';
         errors = error.response.data.errors || error.response.data.error || error.response.data;
      } else if (error.request) {
         errorMessage = 'No response from server';
      }

      return {
         success: false,
         message: errorMessage,
         errors,
      };
   }
};


const mapApiErrorsToForm = (errors) => {
   if (!errors) return;

   Object.keys(errors).forEach((key) => {
      const value = errors[key];

      // ===== Nested employee errors =====
      if (key === 'employee' && typeof value === 'object') {
         Object.keys(value).forEach((nestedKey) => {
            if (formErrors[nestedKey] !== undefined) {
               formErrors[nestedKey] = Array.isArray(value[nestedKey])
                  ? value[nestedKey][0]
                  : value[nestedKey];
            }
         });
      }

      // ===== Normal field errors =====
      else {
         if (formErrors[key] !== undefined) {
            formErrors[key] = Array.isArray(value) ? value[0] : value;
         }
      }
   });
};

</script>
<style scoped></style>