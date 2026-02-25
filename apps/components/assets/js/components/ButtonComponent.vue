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
               Button Component
            </h4>
            <span class="text-xs text-gray-500 dark:text-gray-400 italic"
               >All button example</span
            >
         </div>

         <!-- Card Body -->
         <div
            class="flex-1 overflow-y-auto px-3 py-3 sm:px-6 sm:py-6 p-8 space-y-12"
         >
            <!-- Solid Buttons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Solid Buttons
               </h2>
               <div class="flex flex-wrap gap-4 items-center">
                  <Button variant="primary" @click="showToast('Primary')">
                     Primary
                  </Button>
                  <Button variant="secondary"> Secondary </Button>
                  <Button variant="success"> Success </Button>
                  <Button variant="danger"> Danger </Button>
                  <Button variant="warning"> Warning </Button>
                  <Button variant="info"> Info </Button>
                  <Button variant="light"> Light </Button>
                  <Button variant="dark"> Dark </Button>
               </div>
            </section>

            <!-- Outline Buttons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Outline Buttons
               </h2>
               <div class="flex flex-wrap gap-4 items-center">
                  <Button variant="outline-primary"> Outline Primary </Button>
                  <Button variant="outline-success"> Outline Success </Button>
                  <Button variant="outline-danger"> Outline Danger </Button>
                  <Button variant="outline-warning"> Outline Warning </Button>
                  <Button variant="outline-info"> Outline Info </Button>
                  <Button variant="outline-dark"> Outline Dark </Button>
               </div>
            </section>

            <!-- Gradient Buttons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Gradient Buttons
               </h2>
               <div class="flex flex-wrap gap-4 items-center">
                  <Button variant="gradient-primary"> Gradient Primary </Button>
                  <Button variant="gradient-success"> Gradient Success </Button>
                  <Button variant="gradient-danger"> Gradient Danger </Button>
               </div>
            </section>

            <!-- Sizes -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Button Sizes
               </h2>
               <div class="flex flex-wrap items-center gap-4">
                  <Button variant="primary" size="xs"> Extra Small </Button>
                  <Button variant="primary" size="sm"> Small </Button>
                  <Button variant="primary" size="md"> Medium </Button>
                  <Button variant="primary" size="lg"> Large </Button>
                  <Button variant="primary" size="xl"> Extra Large </Button>
               </div>
            </section>

            <!-- With Icons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Buttons with Icons
               </h2>
               <div class="flex flex-wrap gap-4 items-center">
                  <Button variant="success" icon-left="fas fa-download">
                     Download
                  </Button>
                  <Button variant="danger" icon-right="fas fa-trash">
                     Delete
                  </Button>
                  <Button
                     variant="info"
                     icon-left="fas fa-envelope"
                     icon-right="fas fa-arrow-right"
                  >
                     Send Message
                  </Button>
                  <Button variant="outline-primary" icon-left="fas fa-star">
                     Favorite
                  </Button>
               </div>
            </section>

            <!-- Loading States -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Loading States
               </h2>
               <div class="flex flex-wrap gap-4 items-center">
                  <Button variant="primary" :loading="true">
                     Loading...
                  </Button>
                  <Button variant="success" :loading="true" hide-text-on-load>
                     Submit
                  </Button>
                  <Button
                     variant="danger"
                     :loading="loading"
                     @click="toggleLoading"
                  >
                     {{ loading ? 'Processing' : 'Click to Load' }}
                  </Button>
               </div>
            </section>

            <!-- Rounded Styles -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Rounded Styles
               </h2>
               <div class="flex flex-wrap gap-4 items-center">
                  <Button variant="primary" rounded="none"> Square </Button>
                  <Button variant="success" rounded="sm">
                     Small Rounded
                  </Button>
                  <Button variant="info" rounded="md"> Medium Rounded </Button>
                  <Button variant="warning" rounded="lg">
                     Large Rounded
                  </Button>
                  <Button variant="danger" rounded="full">
                     Fully Rounded
                  </Button>
                  <Button variant="primary" rounded="pill"> Pill Style </Button>
               </div>
            </section>

            <!-- Special Effects -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Special Effects
               </h2>
               <div class="flex flex-wrap gap-4 items-center">
                  <Button variant="primary" shadow> With Shadow </Button>
                  <Button variant="success" shadow block> Block Button </Button>
                  <Button variant="danger" :ripple="false"> No Ripple </Button>
                  <Button variant="info" disabled> Disabled </Button>
               </div>
            </section>

            <!-- Action Buttons - CRUD Operations -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  CRUD Action Buttons
               </h2>
               <div
                  class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
               >
                  <ActionButton
                     action="create"
                     @click="handleAction('create')"
                  />
                  <ActionButton action="view" @click="handleAction('view')" />
                  <ActionButton action="edit" @click="handleAction('edit')" />
                  <ActionButton
                     action="delete"
                     @click="handleAction('delete')"
                  />
                  <ActionButton action="save" @click="handleAction('save')" />
                  <ActionButton
                     action="cancel"
                     @click="handleAction('cancel')"
                  />
               </div>
            </section>

            <!-- Data Management Actions -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Data Management Actions
               </h2>
               <div
                  class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
               >
                  <ActionButton
                     action="download"
                     @click="handleAction('download')"
                  />
                  <ActionButton
                     action="upload"
                     @click="handleAction('upload')"
                  />
                  <ActionButton
                     action="export"
                     @click="handleAction('export')"
                  />
                  <ActionButton
                     action="import"
                     @click="handleAction('import')"
                  />
                  <ActionButton action="copy" @click="handleAction('copy')" />
                  <ActionButton action="print" @click="handleAction('print')" />
               </div>
            </section>

            <!-- Form Actions -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Form Actions
               </h2>
               <div
                  class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
               >
                  <ActionButton
                     action="submit"
                     @click="handleAction('submit')"
                  />
                  <ActionButton action="reset" @click="handleAction('reset')" />
                  <ActionButton
                     action="confirm"
                     @click="handleAction('confirm')"
                  />
                  <ActionButton
                     action="approve"
                     @click="handleAction('approve')"
                  />
                  <ActionButton
                     action="reject"
                     @click="handleAction('reject')"
                  />
                  <ActionButton action="send" @click="handleAction('send')" />
               </div>
            </section>

            <!-- Search & Filter Actions -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Search & Filter Actions
               </h2>
               <div
                  class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
               >
                  <ActionButton
                     action="search"
                     @click="handleAction('search')"
                  />
                  <ActionButton
                     action="filter"
                     @click="handleAction('filter')"
                  />
                  <ActionButton
                     action="refresh"
                     @click="handleAction('refresh')"
                  />
                  <ActionButton
                     action="preview"
                     @click="handleAction('preview')"
                  />
               </div>
            </section>

            <!-- Action Button Sizes -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Action Button Sizes
               </h2>
               <div class="flex flex-wrap items-center gap-4">
                  <ActionButton action="add" size="xs" />
                  <ActionButton action="edit" size="sm" />
                  <ActionButton action="delete" size="md" />
                  <ActionButton action="download" size="lg" />
                  <ActionButton action="upload" size="xl" />
               </div>
            </section>

            <!-- Action Buttons with Custom Labels -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Action Buttons with Custom Labels
               </h2>
               <div
                  class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
               >
                  <ActionButton action="create" label="New Project" />
                  <ActionButton action="download" label="Download PDF" />
                  <ActionButton action="delete" label="Remove Item" />
                  <ActionButton action="send" label="Send Message" />
                  <ActionButton action="export" label="Export Data" />
                  <ActionButton action="import" label="Import File" />
               </div>
            </section>

            <!-- Loading Action Buttons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Loading Action Buttons
               </h2>
               <div
                  class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
               >
                  <ActionButton action="save" :loading="true" />
                  <ActionButton
                     action="submit"
                     :loading="actionLoading"
                     @click="simulateActionLoad"
                  />
                  <ActionButton
                     action="download"
                     :loading="actionLoading"
                     label="Processing..."
                  />
               </div>
            </section>

            <!-- Disabled Action Buttons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Disabled Action Buttons
               </h2>
               <div
                  class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
               >
                  <ActionButton action="edit" disabled />
                  <ActionButton action="delete" disabled />
                  <ActionButton action="approve" disabled />
                  <ActionButton action="reject" disabled />
               </div>
            </section>

            <!-- Block Action Buttons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Block Action Buttons
               </h2>
               <div class="space-y-4 max-w-2xl">
                  <ActionButton action="create" block label="Create New Item" />
                  <ActionButton action="submit" block label="Submit Form" />
                  <ActionButton
                     action="delete"
                     block
                     variant="outline-danger"
                     label="Delete All Items"
                  />
               </div>
            </section>

            <!-- Real World Examples with Action Buttons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Real World Examples
               </h2>
               <div class="space-y-6 p-6 bg-white rounded-lg shadow-md">
                  <!-- Toolbar Example -->
                  <div
                     class="flex flex-wrap gap-3 items-center p-4 bg-gray-50 rounded"
                  >
                     <ActionButton action="create" size="sm" label="New" />
                     <ActionButton action="edit" size="sm" />
                     <ActionButton action="delete" size="sm" />
                     <ActionButton action="download" size="sm" />
                     <ActionButton action="print" size="sm" />
                     <div class="flex-1"></div>
                     <ActionButton action="search" size="sm" />
                     <ActionButton action="filter" size="sm" />
                  </div>

                  <!-- Form Actions Example -->
                  <div class="flex gap-3 justify-end p-4 border-t">
                     <ActionButton action="cancel" size="sm" />
                     <ActionButton action="save" size="sm" />
                     <ActionButton action="submit" size="sm" />
                  </div>

                  <!-- Data Grid Actions Example -->
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                     <div class="p-4 border rounded-lg">
                        <h3 class="font-semibold mb-3">User Management</h3>
                        <div class="flex gap-2 flex-wrap">
                           <ActionButton action="add" size="xs" />
                           <ActionButton action="edit" size="xs" />
                           <ActionButton action="delete" size="xs" />
                           <ActionButton action="view" size="xs" />
                        </div>
                     </div>
                     <div class="p-4 border rounded-lg">
                        <h3 class="font-semibold mb-3">File Operations</h3>
                        <div class="flex gap-2 flex-wrap">
                           <ActionButton action="upload" size="xs" />
                           <ActionButton action="download" size="xs" />
                           <ActionButton action="export" size="xs" />
                           <ActionButton action="print" size="xs" />
                        </div>
                     </div>
                  </div>
               </div>
            </section>

            <!-- Real World Examples with Submit Buttons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Real World Submit Button Examples
               </h2>

               <!-- Example 1: Blog Post Editor -->
               <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                  <h3 class="text-xl font-semibold mb-4 text-gray-700">
                     1. Blog Post Editor
                  </h3>
                  <form @submit.prevent="handleBlogSubmit">
                     <div class="space-y-4 mb-6">
                        <input
                           v-model="blogData.title"
                           type="text"
                           placeholder="Post Title"
                           class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                           required
                        />
                        <textarea
                           v-model="blogData.content"
                           placeholder="Write your post content here..."
                           class="border border-gray-300 p-3 rounded w-full h-32 focus:outline-none focus:ring-2 focus:ring-blue-500"
                           required
                        ></textarea>
                        <select
                           v-model="blogData.category"
                           class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                           <option value="">Select Category</option>
                           <option value="technology">Technology</option>
                           <option value="lifestyle">Lifestyle</option>
                           <option value="business">Business</option>
                        </select>
                     </div>

                     <!-- Multiple Submit Options -->
                     <div class="flex flex-wrap gap-3">
                        <Button
                           type="submit"
                           variant="outline-secondary"
                           name="blogAction"
                           value="save"
                           @click="blogAction = 'save'"
                           :loading="blogLoading"
                           icon-left="fas fa-save"
                        >
                           Save Draft
                        </Button>

                        <Button
                           type="submit"
                           variant="primary"
                           name="blogAction"
                           value="publish"
                           @click="blogAction = 'publish'"
                           :loading="blogLoading"
                           icon-left="fas fa-rocket"
                        >
                           Publish Now
                        </Button>

                        <ActionButton
                           action="submit"
                           type="submit"
                           name="blogAction"
                           value="schedule"
                           @click="blogAction = 'schedule'"
                           variant="info"
                           :loading="blogLoading"
                        >
                           Schedule
                        </ActionButton>

                        <Button
                           type="button"
                           variant="outline-danger"
                           @click="resetBlogForm"
                           icon-left="fas fa-times"
                        >
                           Cancel
                        </Button>
                     </div>
                  </form>
               </div>

               <!-- Example 2: User Registration Form -->
               <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                  <h3 class="text-xl font-semibold mb-4 text-gray-700">
                     2. User Registration Form
                  </h3>
                  <form @submit.prevent="handleUserSubmit">
                     <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                        <input
                           v-model="userData.firstName"
                           type="text"
                           placeholder="First Name"
                           class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                           required
                        />
                        <input
                           v-model="userData.lastName"
                           type="text"
                           placeholder="Last Name"
                           class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                           required
                        />
                        <input
                           v-model="userData.email"
                           type="email"
                           placeholder="Email Address"
                           class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                           required
                        />
                        <input
                           v-model="userData.phone"
                           type="tel"
                           placeholder="Phone Number"
                           class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                     </div>

                     <div class="flex flex-wrap gap-3 justify-between">
                        <div class="flex gap-3">
                           <Button
                              type="reset"
                              variant="outline-secondary"
                              @click="resetUserForm"
                              icon-left="fas fa-undo"
                           >
                              Reset
                           </Button>

                           <Button
                              type="button"
                              variant="outline-danger"
                              @click="cancelUserForm"
                              icon-left="fas fa-times"
                           >
                              Cancel
                           </Button>
                        </div>

                        <Button
                           type="submit"
                           variant="success"
                           :loading="userLoading"
                           icon-left="fas fa-user-plus"
                           block
                           class="min-w-32"
                        >
                           Register User
                        </Button>
                     </div>
                  </form>
               </div>

               <!-- Example 3: Product Order Form -->
               <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                  <h3 class="text-xl font-semibold mb-4 text-gray-700">
                     3. Product Order Form
                  </h3>
                  <form @submit.prevent="handleOrderSubmit">
                     <div class="space-y-4 mb-6">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                           <input
                              v-model="orderData.product"
                              type="text"
                              placeholder="Product Name"
                              class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                              required
                           />
                           <input
                              v-model="orderData.quantity"
                              type="number"
                              placeholder="Quantity"
                              min="1"
                              class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                              required
                           />
                           <input
                              v-model="orderData.price"
                              type="number"
                              placeholder="Unit Price"
                              step="0.01"
                              class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                              required
                           />
                        </div>

                        <div class="flex items-center gap-2">
                           <input
                              v-model="orderData.urgent"
                              type="checkbox"
                              id="urgentOrder"
                              class="w-4 h-4 text-blue-600 focus:ring-blue-500"
                           />
                           <label
                              for="urgentOrder"
                              class="text-sm text-gray-700"
                              >Urgent Delivery</label
                           >
                        </div>
                     </div>

                     <div class="flex flex-wrap gap-3 justify-end">
                        <ActionButton
                           action="submit"
                           type="submit"
                           variant="warning"
                           :loading="orderLoading"
                           icon-left="fas fa-shopping-cart"
                        >
                           Add to Cart
                        </ActionButton>

                        <Button
                           type="submit"
                           variant="success"
                           :loading="orderLoading"
                           icon-left="fas fa-credit-card"
                           @click="orderType = 'buy_now'"
                        >
                           Buy Now
                        </Button>

                        <ActionButton
                           action="save"
                           type="button"
                           variant="outline-primary"
                           @click="saveOrderDraft"
                           icon-left="fas fa-bookmark"
                        >
                           Save for Later
                        </ActionButton>
                     </div>
                  </form>
               </div>

               <!-- Example 4: Support Ticket Form -->
               <div class="bg-white rounded-lg shadow-md p-6">
                  <h3 class="text-xl font-semibold mb-4 text-gray-700">
                     4. Support Ticket System
                  </h3>
                  <form @submit.prevent="handleTicketSubmit">
                     <div class="space-y-4 mb-6">
                        <select
                           v-model="ticketData.priority"
                           class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                           required
                        >
                           <option value="">Select Priority</option>
                           <option value="low">Low</option>
                           <option value="medium">Medium</option>
                           <option value="high">High</option>
                           <option value="urgent">Urgent</option>
                        </select>

                        <input
                           v-model="ticketData.subject"
                           type="text"
                           placeholder="Ticket Subject"
                           class="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                           required
                        />

                        <textarea
                           v-model="ticketData.description"
                           placeholder="Describe your issue in detail..."
                           class="border border-gray-300 p-3 rounded w-full h-24 focus:outline-none focus:ring-2 focus:ring-blue-500"
                           required
                        ></textarea>

                        <div class="flex items-center gap-2">
                           <input
                              v-model="ticketData.attachFiles"
                              type="checkbox"
                              id="attachFiles"
                              class="w-4 h-4 text-blue-600 focus:ring-blue-500"
                           />
                           <label
                              for="attachFiles"
                              class="text-sm text-gray-700"
                              >Attach relevant files</label
                           >
                        </div>
                     </div>

                     <div class="flex flex-wrap gap-3">
                        <Button
                           type="submit"
                           variant="danger"
                           :loading="ticketLoading"
                           icon-left="fas fa-exclamation-triangle"
                           @click="ticketPriority = 'high'"
                        >
                           Submit Urgent Ticket
                        </Button>

                        <ActionButton
                           action="submit"
                           type="submit"
                           variant="info"
                           :loading="ticketLoading"
                           icon-left="fas fa-paper-plane"
                           @click="ticketPriority = 'normal'"
                        >
                           Submit Normal Ticket
                        </ActionButton>

                        <Button
                           type="button"
                           variant="outline-secondary"
                           @click="saveTicketDraft"
                           icon-left="fas fa-save"
                        >
                           Save as Draft
                        </Button>

                        <ActionButton
                           action="cancel"
                           type="button"
                           @click="cancelTicket"
                           variant="outline-danger"
                        >
                           Cancel
                        </ActionButton>
                     </div>
                  </form>
               </div>
            </section>
         </div>
         <!-- Card Footer -->
         <div
            class="px-3 py-2 sm:px-6 sm:py-3 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50 dark:bg-gray-900/40"
         ></div>
      </div>
   </div>
</template>

<script setup>
import { ref, inject } from 'vue';

const toast = inject('toast');
const loading = ref(false);
const actionLoading = ref(false);

const showToast = (type) => {
   toast.success(`${type} button clicked!`);
};

const toggleLoading = () => {
   loading.value = true;
   setTimeout(() => {
      loading.value = false;
      toast.info('Process completed!');
   }, 2000);
};

const handleAction = (action) => {
   const messages = {
      create: 'Creating new item...',
      edit: 'Editing item...',
      delete: 'Deleting item...',
      save: 'Changes saved successfully!',
      download: 'Download started...',
      upload: 'Uploading file...',
      view: 'Viewing details...',
      search: 'Searching...',
      submit: 'Form submitted!',
      confirm: 'Action confirmed!',
      approve: 'Request approved!',
      reject: 'Request rejected!',
      export: 'Exporting data...',
      import: 'Importing file...',
      copy: 'Copied to clipboard!',
      print: 'Printing...',
      refresh: 'Refreshing data...',
      reset: 'Form reset!',
      cancel: 'Action cancelled!',
      send: 'Message sent!',
      filter: 'Filter applied!',
      preview: 'Preview opened!',
   };

   const message = messages[action] || `${action} action performed!`;

   if (action === 'delete' || action === 'remove') {
      toast.error(message);
   } else if (
      action === 'save' ||
      action === 'submit' ||
      action === 'confirm'
   ) {
      toast.success(message);
   } else {
      toast.info(message);
   }
};

const simulateActionLoad = () => {
   actionLoading.value = true;
   setTimeout(() => {
      actionLoading.value = false;
      toast.success('Action completed successfully!');
   }, 2000);
};

// Blog Post Data
const blogData = ref({
   title: '',
   content: '',
   category: '',
});
const blogAction = ref('');
const blogLoading = ref(false);

// User Registration Data
const userData = ref({
   firstName: '',
   lastName: '',
   email: '',
   phone: '',
});
const userLoading = ref(false);

// Product Order Data
const orderData = ref({
   product: '',
   quantity: 1,
   price: 0,
   urgent: false,
});
const orderType = ref('');
const orderLoading = ref(false);

// Support Ticket Data
const ticketData = ref({
   priority: '',
   subject: '',
   description: '',
   attachFiles: false,
});
const ticketPriority = ref('');
const ticketLoading = ref(false);

// Blog Post Handlers
const handleBlogSubmit = async () => {
   blogLoading.value = true;

   try {
      await new Promise((resolve) => setTimeout(resolve, 1500));

      const messages = {
         save: 'Blog post saved as draft!',
         publish: 'Blog post published successfully!',
         schedule: 'Blog post scheduled for publishing!',
      };

      toast.success(messages[blogAction.value] || 'Action completed!');
      resetBlogForm();
   } catch (error) {
      toast.error('Failed to process blog post!');
   } finally {
      blogLoading.value = false;
   }
};

const resetBlogForm = () => {
   blogData.value = { title: '', content: '', category: '' };
   blogAction.value = '';
};

// User Registration Handlers
const handleUserSubmit = async () => {
   userLoading.value = true;

   try {
      await new Promise((resolve) => setTimeout(resolve, 2000));
      toast.success(
         `User ${userData.value.firstName} ${userData.value.lastName} registered successfully!`
      );
      resetUserForm();
   } catch (error) {
      toast.error('User registration failed!');
   } finally {
      userLoading.value = false;
   }
};

const resetUserForm = () => {
   userData.value = { firstName: '', lastName: '', email: '', phone: '' };
};

const cancelUserForm = () => {
   toast.info('User registration cancelled!');
   resetUserForm();
};

// Product Order Handlers
const handleOrderSubmit = async () => {
   orderLoading.value = true;

   try {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      if (orderType.value === 'buy_now') {
         toast.success('Order placed successfully! Processing payment...');
      } else {
         toast.success('Product added to cart!');
      }

      resetOrderForm();
   } catch (error) {
      toast.error('Failed to process order!');
   } finally {
      orderLoading.value = false;
   }
};

const saveOrderDraft = () => {
   toast.info('Order saved for later!');
};

const resetOrderForm = () => {
   orderData.value = { product: '', quantity: 1, price: 0, urgent: false };
   orderType.value = '';
};

// Support Ticket Handlers
const handleTicketSubmit = async () => {
   ticketLoading.value = true;

   try {
      await new Promise((resolve) => setTimeout(resolve, 1800));

      const priorityMessage =
         ticketPriority.value === 'high'
            ? 'Urgent ticket submitted! Our team will respond within 1 hour.'
            : 'Ticket submitted successfully! We will respond within 24 hours.';

      toast.success(priorityMessage);
      resetTicketForm();
   } catch (error) {
      toast.error('Failed to submit ticket!');
   } finally {
      ticketLoading.value = false;
   }
};

const saveTicketDraft = () => {
   toast.info('Ticket saved as draft!');
};

const cancelTicket = () => {
   toast.warning('Ticket creation cancelled!');
   resetTicketForm();
};

const resetTicketForm = () => {
   ticketData.value = {
      priority: '',
      subject: '',
      description: '',
      attachFiles: false,
   };
   ticketPriority.value = '';
};
</script>
