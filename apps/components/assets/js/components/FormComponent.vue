<template>
   <div class="flex flex-col h-full w-full space-y-2">
      <!-- Form Card -->
      <div
         class="flex-1 bg-white dark:bg-gray-800 rounded-md shadow-md border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden"
      >
         <!-- Card Header -->
         <div
            class="px-3 py-1 sm:px-6 sm:py-3 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center bg-gray-50 dark:bg-gray-900/40"
         >
            <h4
               class="text-lg font-semibold text-gray-800 dark:text-gray-100 flex items-center gap-2"
            >
               <i class="fa-solid fa-pen-to-square text-blue-500"></i>
               Component Testing Lab
            </h4>
            <span class="text-xs text-gray-500 dark:text-gray-400 italic"
               >All fields are just for testing</span
            >
         </div>

         <form @submit.prevent="handleSubmit()">
            <!-- Card Body -->
            <div
               class="flex-1 overflow-y-auto px-6 py-6 space-y-10 scrollbar-thin scrollbar-thumb-gray-400"
            >
               <!-- ====================== ১. Basic Inputs ====================== -->
               <div
                  class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
               >
                  <InputeComponent
                     label="Full Name"
                     placeholder="Enter full name"
                     v-model="form.name"
                  />
                  <InputeComponent
                     label="Email Address"
                     placeholder="example@mail.com"
                     type="email"
                     v-model="form.email"
                  />
                  <CustomMultiSelect
                     label="Country"
                     v-model="form.country"
                     :options="countries"
                     :multiple="false"
                     placeholder="Select country"
                     size="sm"
                  />
                  <CustomMultiSelect
                     label="Skills"
                     v-model="form.skills"
                     :options="skills"
                     :multiple="true"
                     placeholder="Select skills"
                     size="sm"
                  />
                  <InputeComponent
                     label="Phone Number"
                     placeholder="+8801XXXXXXXXX"
                     v-model="form.phone"
                  />
                  <InputeComponent
                     label="Subject"
                     placeholder="Enter subject"
                     v-model="form.subject"
                  />
                  <MultiselectComponent
                     label="Favorite Fruit"
                     v-model="form.fruit"
                     :options="fruits"
                     placeholder="Select a fruit"
                  />
                  <MultiselectComponent
                     label="Hobbies"
                     v-model="form.hobbies"
                     :options="hobbies"
                     multiple
                     placeholder="Select your hobbies"
                  />
                  <div class="sm:col-span-2">
                     <TextAreaComponent
                        label="Message"
                        placeholder="Write your message..."
                        v-model="form.message"
                        :rows="5"
                        helpText="You can write up to 500 characters."
                     />
                  </div>
               </div>

               <!-- ====================== ২. Checkbox & Switch ====================== -->
               <div class="space-y-6">
                  <!-- Single Checkbox -->
                  <div
                     class="bg-gray-50 dark:bg-gray-700/50 p-5 rounded-lg border"
                  >
                     <h5 class="font-semibold mb-4 text-blue-600">
                        1. Single Checkbox
                     </h5>
                     <Checkbox
                        label="I agree to terms and conditions"
                        v-model="form.agree_terms"
                        :error="errors.agree_terms"
                        required
                     />
                  </div>

                  <!-- Switch -->
                  <div
                     class="bg-gray-50 dark:bg-gray-700/50 p-5 rounded-lg border"
                  >
                     <h5 class="font-semibold mb-4 text-blue-600">
                        2. Switch / Toggle
                     </h5>
                     <div class="space-y-3">
                        <SwitchComponent
                           label="Enable Notifications"
                           v-model="form.notifications"
                        />
                        <SwitchComponent
                           label="Dark Mode (Disabled Example)"
                           v-model="form.dark_mode"
                           disabled
                        />
                     </div>
                  </div>

                  <!-- Checkbox Group -->
                  <div
                     class="bg-gray-50 dark:bg-gray-700/50 p-5 rounded-lg border"
                  >
                     <h5 class="font-semibold mb-4 text-blue-600">
                        3. Checkbox Group (Multiple)
                     </h5>
                     <CheckboxGroup
                        label="Select Your Interests"
                        v-model="form.interests"
                        :options="interestsOptions"
                        :error="errors.interests"
                        required
                     />
                  </div>

                  <!-- Alternative Checkbox Group -->
                  <div
                     class="bg-gray-50 dark:bg-gray-700/50 p-5 rounded-lg border"
                  >
                     <h5 class="font-semibold mb-4 text-blue-600">
                        4. MultipleCheckboxGroup (Alternative)
                     </h5>
                     <MultipleCheckboxGroup
                        label="Select Permissions (Alternative)"
                        v-model="form.permissions_alt"
                        :options="permissionsOptions"
                     />
                  </div>
               </div>

               <!-- ====================== ৩. Django Style Multiselect ====================== -->
               <div
                  class="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 p-6 rounded-lg border"
               >
                  <DjangoStyleMultiselect
                     v-model="form.permissions"
                     :options="permissions"
                     label="Select Permissions"
                     track-by="id"
                     display-by="name"
                     :required="true"
                     :loading="loading"
                  />
                  <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                     Selected:
                     <strong>{{ form.permissions.length }}</strong> permissions
                  </p>
               </div>

               <!-- ====================== ৪. Real World Example ====================== -->
               <div
                  class="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-gray-800 dark:to-gray-900 p-6 rounded-lg border border-indigo-200 dark:border-indigo-900"
               >
                  <h5
                     class="font-bold text-lg mb-5 text-indigo-700 dark:text-indigo-300"
                  >
                     Real World Example
                  </h5>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                     <InputeComponent
                        label="Username"
                        v-model="form.username"
                        placeholder="Enter username"
                        required
                     />
                     <CustomMultiSelect
                        label="User Role"
                        v-model="form.role"
                        :options="roles"
                        :multiple="false"
                        placeholder="Select role"
                     />
                     <SwitchComponent
                        label="Account Active"
                        v-model="form.is_active"
                     />
                     <SwitchComponent
                        label="Two-Factor Authentication"
                        v-model="form.tfa_enabled"
                     />
                     <div class="md:col-span-2">
                        <CheckboxGroup
                           label="Assign Modules"
                           v-model="form.modules"
                           :options="modulesOptions"
                        />
                     </div>
                     <div class="md:col-span-2">
                        <Checkbox
                           label="I have read and accept the privacy policy"
                           v-model="form.privacy_accepted"
                           required
                           :error="
                              form.privacy_accepted
                                 ? ''
                                 : 'You must accept the privacy policy'
                           "
                        />
                     </div>
                  </div>
               </div>
            </div>

            <!-- Card Footer -->
            <div
               class="px-3 py-2 sm:px-6 sm:py-3 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/40"
            >
               <button
                  type="button"
                  class="px-5 py-2 rounded-md bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
               >
                  Cancel
               </button>
               <button
                  type="submit"
                  class="px-5 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition"
               >
                  Submit
               </button>
            </div>
         </form>
      </div>
   </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Reactive Form
const form = ref({
   name: '',
   email: '',
   phone: '',
   subject: '',
   fruit: null,
   hobbies: [],
   country: null,
   skills: [],
   message: '',
   permissions: [2, 5], // প্রি-সিলেক্ট

   // For Checkbox
   agree_terms: false,
   notifications: true,
   dark_mode: false,
   interests: ['gaming', 'traveling'],
   permissions_alt: [1, 3],
   username: '',
   role: 'admin',
   is_active: true,
   modules: ['pos', 'inventory'],
   tfa_enabled: false,
   privacy_accepted: false,
});

const errors = ref({});
const submitting = ref(false);

const loading = ref(true);
const permissions = ref([]);

// Single Select Options
const fruits = [
   { label: 'Apple', value: 'apple' },
   { label: 'Banana', value: 'banana' },
   { label: 'Orange', value: 'orange' },
   { label: 'Pineapple', value: 'pineapple' },
   { label: 'Watermelon', value: 'watermelon' },
   { label: 'Mango', value: 'mango' },
   { label: 'Strawberry', value: 'strawberry' },
   { label: 'Grapes', value: 'grapes' },
   { label: 'Kiwi', value: 'kiwi' },
   { label: 'Papaya', value: 'papaya' },
];

// Multi Select Options
const hobbies = [
   { label: 'Reading', value: 'reading' },
   { label: 'Traveling', value: 'traveling' },
   { label: 'Gaming', value: 'gaming' },
   { label: 'Cooking', value: 'cooking' },
   { label: 'Photography', value: 'photography' },
   { label: 'Drawing', value: 'drawing' },
   { label: 'Dancing', value: 'dancing' },
   { label: 'Singing', value: 'singing' },
   { label: 'Swimming', value: 'swimming' },
   { label: 'Cycling', value: 'cycling' },
   { label: 'Running', value: 'running' },
   { label: 'Yoga', value: 'yoga' },
   { label: 'Meditation', value: 'meditation' },
   { label: 'Gardening', value: 'gardening' },
   { label: 'Fishing', value: 'fishing' },
];

const countries = [
   { label: 'Bangladesh', value: 'bd' },
   { label: 'India', value: 'in' },
   { label: 'United States', value: 'us' },
   { label: 'United Kingdom', value: 'uk' },
   { label: 'Canada', value: 'ca' },
   { label: 'Australia', value: 'au' },
   { label: 'Germany', value: 'de' },
   { label: 'France', value: 'fr' },
   { label: 'Italy', value: 'it' },
   { label: 'Spain', value: 'es' },
   { label: 'Brazil', value: 'br' },
   { label: 'Mexico', value: 'mx' },
   { label: 'Argentina', value: 'ar' },
   { label: 'Japan', value: 'jp' },
   { label: 'South Korea', value: 'kr' },
   { label: 'China', value: 'cn' },
   { label: 'Russia', value: 'ru' },
   { label: 'Turkey', value: 'tr' },
   { label: 'Egypt', value: 'eg' },
   { label: 'South Africa', value: 'za' },
   { label: 'Nigeria', value: 'ng' },
   { label: 'Kenya', value: 'ke' },
   { label: 'Thailand', value: 'th' },
   { label: 'Vietnam', value: 'vn' },
   { label: 'Indonesia', value: 'id' },
   { label: 'Malaysia', value: 'my' },
   { label: 'Singapore', value: 'sg' },
   { label: 'New Zealand', value: 'nz' },
   { label: 'Sweden', value: 'se' },
   { label: 'Norway', value: 'no' },
];

const skills = [
   // Programming
   { label: 'JavaScript', value: 'javascript' },
   { label: 'TypeScript', value: 'typescript' },
   { label: 'Python', value: 'python' },
   { label: 'Java', value: 'java' },
   { label: 'C++', value: 'cpp' },
   { label: 'C#', value: 'csharp' },
   { label: 'PHP', value: 'php' },
   { label: 'Ruby', value: 'ruby' },
   { label: 'Go', value: 'go' },
   { label: 'Rust', value: 'rust' },

   // Frameworks
   { label: 'Vue.js', value: 'vue' },
   { label: 'React', value: 'react' },
   { label: 'Angular', value: 'angular' },
   { label: 'Svelte', value: 'svelte' },
   { label: 'Django', value: 'django' },
   { label: 'Flask', value: 'flask' },
   { label: 'Laravel', value: 'laravel' },
   { label: 'Spring Boot', value: 'spring' },
   { label: 'Express.js', value: 'express' },
   { label: 'NestJS', value: 'nestjs' },

   // Frontend
   { label: 'HTML', value: 'html' },
   { label: 'CSS', value: 'css' },
   { label: 'Tailwind CSS', value: 'tailwind' },
   { label: 'Bootstrap', value: 'bootstrap' },
   { label: 'Sass', value: 'sass' },
   { label: 'Figma', value: 'figma' },
   { label: 'Sketch', value: 'sketch' },
   { label: 'Adobe XD', value: 'adobe_xd' },

   // Backend & DevOps
   { label: 'Node.js', value: 'nodejs' },
   { label: 'Docker', value: 'docker' },
   { label: 'Kubernetes', value: 'kubernetes' },
   { label: 'AWS', value: 'aws' },
   { label: 'Azure', value: 'azure' },
   { label: 'Google Cloud', value: 'gcp' },
   { label: 'Git', value: 'git' },
   { label: 'GitHub', value: 'github' },
   { label: 'CI/CD', value: 'cicd' },

   // Design & Video
   { label: 'Photoshop', value: 'photoshop' },
   { label: 'Illustrator', value: 'illustrator' },
   { label: 'Premiere Pro', value: 'premiere' },
   { label: 'After Effects', value: 'after-effects' },
   { label: 'Lightroom', value: 'lightroom' },
   { label: 'InDesign', value: 'indesign' },
   { label: 'Canva', value: 'canva' },
   { label: 'Blender', value: 'blender' },

   // Testing & Others
   { label: 'Jest', value: 'jest' },
   { label: 'Cypress', value: 'cypress' },
   { label: 'Postman', value: 'postman' },
   { label: 'SQL', value: 'sql' },
   { label: 'MongoDB', value: 'mongodb' },
   { label: 'Firebase', value: 'firebase' },

   // Sample Keywords
   { label: 'Sample Data', value: 'sample' },
   { label: 'PP Sample', value: 'pp_sample' },
   { label: 'Kid Sample', value: 'kid_sample' },
   { label: 'Complete Garments Sample', value: 'compleate_garments_sample' },
   { label: 'Sample Test 1', value: 'sample_test_1' },
   { label: 'Sample Test 2', value: 'sample_test_2' },
   { label: 'Sample Test 3', value: 'sample_test_3' },
   { label: 'Sample Test 4', value: 'sample_test_4' },
   { label: 'Sample Test 5', value: 'sample_test_5' },
   { label: 'Sample Test 6', value: 'sample_test_6' },
   { label: 'Sample Test 7', value: 'sample_test_7' },
   { label: 'Sample Test 8', value: 'sample_test_8' },
   { label: 'Sample Test 9', value: 'sample_test_9' },
   { label: 'Sample Test 10', value: 'sample_test_10' },
];

// Generate 50+ Permissions
const generatePermissions = () => {
   const base = [
      'View Dashboard',
      'Edit Profile',
      'Manage Users',
      'Delete Content',
      'Export Data',
      'View Reports',
      'Create Post',
      'Edit Post',
      'Delete Post',
      'Moderate Comments',
      'Manage Categories',
      'Upload Media',
      'View Analytics',
      'Send Notifications',
      'Manage Roles',
      'Access Admin Panel',
      'Change Settings',
      'View Logs',
      'Backup Database',
      'Restore Backup',
      'API Access',
      'Webhook Setup',
      'Email Templates',
      'SMS Gateway',
      'Payment Integration',
      'Invoice Management',
      'Refund Processing',
      'Tax Configuration',
      'Shipping Rules',
      'Inventory Control',
      'Product Management',
      'Order Processing',
      'Customer Support',
      'Ticket System',
      'Live Chat',
      'Knowledge Base',
      'FAQ Management',
      'Survey Builder',
      'Form Builder',
      'Workflow Automation',
      'Task Assignment',
      'Calendar Sync',
      'File Storage',
      'Cloud Integration',
      'Security Audit',
      'Two-Factor Auth',
      'Session Management',
      'IP Whitelisting',
      'Rate Limiting',
      'Captcha Setup',
      'Inbound Courier Buyer Wise Report 1',
      'Inbound Courier Buyer Wise Report 2',
      'Inbound Courier Department Wise Report 3',
      'Inbound Courier Department Wise Report 4 fdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdhdh',
   ];

   return base.map((name, index) => ({
      id: index + 1,
      name: `${name} Permission`,
      group: index < 15 ? 'Core' : index < 30 ? 'Content' : 'Advanced',
   }));
};

// Options
const interestsOptions = [
   { label: 'Reading Books', value: 'reading' },
   { label: 'Traveling', value: 'traveling' },
   { label: 'Gaming', value: 'gaming' },
   { label: 'Cooking', value: 'cooking' },
];

const permissionsOptions = [
   { label: 'View Dashboard', value: 1 },
   { label: 'Manage Users', value: 2 },
   { label: 'Edit Content', value: 3 },
   { label: 'Delete Records', value: 4 },
];

const roles = [
   { label: 'Admin', value: 'admin' },
   { label: 'Manager', value: 'manager' },
   { label: 'User', value: 'user' },
];

const modulesOptions = [
   { label: 'POS System', value: 'pos' },
   { label: 'Inventory', value: 'inventory' },
   { label: 'Accounting', value: 'accounting' },
   { label: 'Reports', value: 'reports' },
];

// Submit Handler
const formSubmitted = ref(false);
const handleSubmit = () => {
   formSubmitted.value = true;
   console.log('Form Submitted:', form.value);
   // alert(`Submitted! Selected ${form.value.permissions.length} permissions.`);
};

// Load Permissions
onMounted(() => {
   loading.value = true;
   setTimeout(() => {
      permissions.value = generatePermissions();
      loading.value = false;
   }, 800);
});
</script>
