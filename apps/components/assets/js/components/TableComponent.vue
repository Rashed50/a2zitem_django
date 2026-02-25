<!-- apps/components/assets/js/components/FormComponent.vue -->
<template>
   <div class="flex flex-col h-full w-full space-y-2">
      <!-- Form Card -->
      <div
         class="flex-1 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden"
      >
         <!-- Card Header -->
         <div
            class="px-3 py-1 sm:px-6 sm:py-3 border-b border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-900/20"
         >
            <h4
               class="text-xl font-bold text-gray-800 dark:text-gray-100 flex items-center gap-3"
            >
               <i class="fa-solid fa-building text-blue-600"></i>
               <span class="text-lg sm:text-xl">Demo Companies For Testing</span>
            </h4>
            <span
               class="text-xs sm:text-sm text-blue-600 dark:text-blue-400 font-medium bg-blue-100 dark:bg-blue-900/30 px-3 py-1 rounded-full"
            >
               {{ apiData?.total_items || 0 }} Total Records
            </span>
         </div>

         <!-- Card Body -->
         <div
            class="flex-1 overflow-y-auto px-3 py-3 sm:px-5 sm:py-3 space-y-4 sm:space-y-2"
         >
            <!-- Top Controls -->
            <div
               class="flex flex-col gap-4 p-3 sm:p-2 bg-gray-50 dark:bg-gray-900/30 rounded-lg border border-gray-200 dark:border-gray-700"
            >
               <!-- Desktop Layout (PC) -->
               <div class="hidden lg:flex items-center justify-between gap-4">
                  <!-- Left Side: Show Entries -->
                  <div
                     class="flex items-center gap-2 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm"
                  >
                     <i class="fa-solid fa-list-ol text-blue-500 text-sm"></i>
                     <label
                        for="entries"
                        class="text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Show</label
                     >
                     <select
                        id="entries"
                        v-model="entriesPerPage"
                        @change="fetchData"
                        class="min-w-[60px] border-0 bg-transparent px-2 py-1 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
                     >
                        <option value="10">10</option>
                        <option value="25">25</option>
                        <option value="50">50</option>
                        <option value="100">100</option>
                     </select>
                     <span class="text-sm text-gray-500 dark:text-gray-400"
                        >Entries</span
                     >
                  </div>

                  <!-- Middle: Bulk Actions -->
                  <div
                     class="flex items-center gap-3 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm"
                     v-if="selectedRows.length > 0"
                  >
                     <i
                        class="fa-solid fa-layer-group text-green-500 text-sm"
                     ></i>
                     <span
                        class="text-sm font-medium text-gray-700 dark:text-gray-300"
                     >
                        {{ selectedRows.length }} selected
                     </span>
                     <select
                        v-model="bulkAction"
                        class="border-0 bg-transparent px-2 py-1 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 rounded min-w-32"
                     >
                        <option value="">Bulk Actions</option>
                        <option value="activate">Activate</option>
                        <option value="deactivate">Deactivate</option>
                        <option value="delete">Delete</option>
                        <option value="export">Export</option>
                     </select>
                     <button
                        @click="executeBulkAction"
                        class="px-3 py-1 bg-green-500 hover:bg-green-600 text-white text-sm rounded-lg transition-colors duration-200 flex items-center gap-1"
                     >
                        <i class="fa-solid fa-play text-xs"></i>
                        Apply
                     </button>
                  </div>

                  <!-- Right Side: Search -->
                  <div class="relative flex-1 max-w-md">
                     <input
                        type="text"
                        v-model="searchQuery"
                        @input="onSearchInput"
                        placeholder="Search companies..."
                        class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition-all duration-200 text-sm"
                     />
                     <i
                        class="fa-solid fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm"
                     ></i>
                     <i
                        v-if="searchQuery"
                        @click="clearSearch"
                        class="fa-solid fa-times absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 cursor-pointer text-sm"
                     ></i>
                  </div>
               </div>

               <!-- Mobile & Tablet Layout -->
               <div class="flex flex-col gap-3 lg:hidden">
                  <!-- First Row: Search (Full Width) -->
                  <div class="relative">
                     <input
                        type="text"
                        v-model="searchQuery"
                        @input="onSearchInput"
                        placeholder="Search companies..."
                        class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition-all duration-200 text-sm"
                     />
                     <i
                        class="fa-solid fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm"
                     ></i>
                     <i
                        v-if="searchQuery"
                        @click="clearSearch"
                        class="fa-solid fa-times absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 cursor-pointer text-sm"
                     ></i>
                  </div>

                  <!-- Second Row: Controls (Full Width) -->
                  <div
                     class="flex flex-col sm:flex-row items-start sm:items-center gap-3 justify-between"
                  >
                     <!-- Show Entries Selector -->
                     <div
                        class="flex items-center gap-2 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm w-full sm:w-auto"
                     >
                        <i
                           class="fa-solid fa-list-ol text-blue-500 text-sm"
                        ></i>
                        <label
                           for="entries-mobile"
                           class="text-sm font-medium text-gray-700 dark:text-gray-300"
                           >Show</label
                        >
                        <select
                           id="entries-mobile"
                           v-model="entriesPerPage"
                           @change="fetchData"
                           class="min-w-[60px] border-0 bg-transparent px-2 py-1 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded flex-1 sm:flex-none"
                        >
                           <option value="10">10</option>
                           <option value="25">25</option>
                           <option value="50">50</option>
                           <option value="100">100</option>
                        </select>
                        <span
                           class="text-sm text-gray-500 dark:text-gray-400 hidden sm:block"
                           >Entries</span
                        >
                     </div>

                     <!-- Bulk Actions -->
                     <div
                        class="flex items-center gap-2 bg-white dark:bg-gray-800 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm w-full sm:w-auto"
                        v-if="selectedRows.length > 0"
                     >
                        <i
                           class="fa-solid fa-layer-group text-green-500 text-sm"
                        ></i>
                        <span
                           class="text-sm font-medium text-gray-700 dark:text-gray-300"
                        >
                           {{ selectedRows.length }}
                        </span>
                        <select
                           v-model="bulkAction"
                           class="border-0 bg-transparent px-2 py-1 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 rounded flex-1 sm:flex-none min-w-24"
                        >
                           <option value="">Actions</option>
                           <option value="activate">Activate</option>
                           <option value="deactivate">Deactivate</option>
                           <option value="delete">Delete</option>
                           <option value="export">Export</option>
                        </select>
                        <button
                           @click="executeBulkAction"
                           class="px-3 py-1 bg-green-500 hover:bg-green-600 text-white text-sm rounded-lg transition-colors duration-200 flex items-center gap-1"
                        >
                           <i class="fa-solid fa-play text-xs"></i>
                           <span class="hidden sm:block">Apply</span>
                        </button>
                     </div>
                  </div>
               </div>
            </div>

            <!-- Data Table -->
            <div
               class="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-lg"
            >
               <!-- Desktop Table -->
               <table
                  class="min-w-full divide-y divide-gray-200 dark:divide-gray-700 hidden sm:table"
               >
                  <thead
                     class="bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-800 dark:to-blue-900/20"
                  >
                     <tr>
                        <!-- S/N Column -->
                        <th
                           class="w-16 px-4 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider"
                        >
                           S/N
                        </th>

                        <!-- Checkbox Column -->
                        <th class="w-12 px-4 py-4 text-center">
                           <input
                              type="checkbox"
                              v-model="selectAll"
                              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                           />
                        </th>

                        <!-- Data Columns -->
                        <th
                           v-for="column in columns"
                           :key="column.key"
                           class="px-4 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider cursor-pointer hover:text-gray-900 dark:hover:text-gray-200 transition-colors duration-200"
                           @click="sortTable(column.key)"
                        >
                           <div class="flex items-center gap-2">
                              {{ column.label }}
                              <i
                                 v-if="sortColumn === column.key"
                                 class="fa-solid text-blue-500 text-xs"
                                 :class="
                                    sortDirection === 'asc'
                                       ? 'fa-arrow-up'
                                       : 'fa-arrow-down'
                                 "
                              ></i>
                              <i
                                 v-else
                                 class="fa-solid fa-sort text-gray-400 text-xs"
                              ></i>
                           </div>
                        </th>

                        <!-- Action Column -->
                        <th
                           class="w-32 px-4 py-4 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider"
                        >
                           Actions
                        </th>
                     </tr>
                  </thead>
                  <tbody
                     class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700"
                  >
                     <!-- Loading State -->
                     <tr v-if="loading">
                        <td
                           :colspan="columns.length + 3"
                           class="px-6 py-8 text-center"
                        >
                           <div
                              class="flex justify-center items-center space-x-3"
                           >
                              <i
                                 class="fa-solid fa-spinner fa-spin text-blue-500 text-xl"
                              ></i>
                              <span class="text-gray-600 dark:text-gray-400"
                                 >Loading companies...</span
                              >
                           </div>
                        </td>
                     </tr>

                     <!-- No Data State -->
                     <tr v-else-if="!apiData?.results?.length">
                        <td
                           :colspan="columns.length + 3"
                           class="px-6 py-8 text-center"
                        >
                           <div class="flex flex-col items-center space-y-3">
                              <i
                                 class="fa-solid fa-inbox text-gray-400 text-4xl"
                              ></i>
                              <span
                                 class="text-gray-600 dark:text-gray-400 text-lg font-medium"
                                 >No companies found</span
                              >
                              <p
                                 class="text-gray-500 dark:text-gray-500 text-sm"
                              >
                                 Try adjusting your search or filter criteria
                              </p>
                           </div>
                        </td>
                     </tr>

                     <!-- Data Rows -->
                     <tr
                        v-else
                        v-for="(item, index) in apiData.results"
                        :key="item.id"
                        class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200"
                        :class="{
                           'bg-blue-50 dark:bg-blue-900/20':
                              selectedRows.includes(item.id),
                           'bg-gray-50/50 dark:bg-gray-800/50': index % 2 === 1,
                           'bg-white dark:bg-gray-800': index % 2 === 0,
                        }"
                     >
                        <!-- S/N -->
                        <td
                           class="px-4 py-4 text-sm font-medium text-gray-700 dark:text-gray-300 text-center"
                        >
                           {{ apiData.pagination?.showing_from + index }}
                        </td>

                        <!-- Checkbox -->
                        <td class="px-4 py-4 text-center">
                           <input
                              type="checkbox"
                              :value="item.id"
                              v-model="selectedRows"
                              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                           />
                        </td>

                        <!-- Company Name with text wrapping -->
                        <td
                           class="px-4 py-4 text-sm text-gray-800 dark:text-gray-200 font-medium max-w-[200px]"
                        >
                           <div class="break-words line-clamp-2">
                              {{ item.name }}
                           </div>
                        </td>

                        <!-- Email with text wrapping -->
                        <td
                           class="px-4 py-4 text-sm text-blue-600 dark:text-blue-400 max-w-[220px]"
                        >
                           <div class="break-all line-clamp-2">
                              {{ item.email }}
                           </div>
                        </td>

                        <!-- Status -->
                        <td class="px-4 py-4 text-sm">
                           <span
                              class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap"
                              :class="getStatusClass(item.status)"
                           >
                              <i
                                 class="fa-solid fa-circle text-[10px] mr-1"
                              ></i>
                              {{ item.status }}
                           </span>
                        </td>

                        <!-- Subscription Plan -->
                        <td class="px-4 py-4 text-sm">
                           <span
                              class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 text-purple-800 dark:text-purple-300 whitespace-nowrap"
                           >
                              <i
                                 class="fa-solid fa-crown mr-1 text-yellow-500"
                              ></i>
                              {{ item.subscription_plan }}
                           </span>
                        </td>

                        <!-- Created Date -->
                        <td
                           class="px-4 py-4 text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap"
                        >
                           {{ formatDate(item.created_date) }}
                        </td>

                        <!-- Actions -->
                        <td class="px-4 py-4 text-sm">
                           <div
                              class="flex items-center justify-center space-x-2"
                           >
                              <button
                                 @click="editItem(item)"
                                 class="p-2 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-900/30 rounded-lg transition-colors duration-200"
                                 title="Edit"
                              >
                                 <i
                                    class="fa-solid fa-pen-to-square text-sm"
                                 ></i>
                              </button>
                              <button
                                 @click="viewItem(item)"
                                 class="p-2 text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-300 hover:bg-green-100 dark:hover:bg-green-900/30 rounded-lg transition-colors duration-200"
                                 title="View"
                              >
                                 <i class="fa-solid fa-eye text-sm"></i>
                              </button>
                              <button
                                 @click="deleteItem(item)"
                                 class="p-2 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-lg transition-colors duration-200"
                                 title="Delete"
                              >
                                 <i class="fa-solid fa-trash text-sm"></i>
                              </button>
                           </div>
                        </td>
                     </tr>
                  </tbody>
               </table>

               <!-- Mobile Cards -->
               <div class="sm:hidden space-y-3 p-4">
                  <!-- Loading State -->
                  <div v-if="loading" class="text-center py-8">
                     <div class="flex justify-center items-center space-x-3">
                        <i
                           class="fa-solid fa-spinner fa-spin text-blue-500 text-xl"
                        ></i>
                        <span class="text-gray-600 dark:text-gray-400"
                           >Loading...</span
                        >
                     </div>
                  </div>

                  <!-- No Data State -->
                  <div
                     v-else-if="!apiData?.results?.length"
                     class="text-center py-8"
                  >
                     <div class="flex flex-col items-center space-y-3">
                        <i class="fa-solid fa-inbox text-gray-400 text-4xl"></i>
                        <span
                           class="text-gray-600 dark:text-gray-400 text-lg font-medium"
                           >No companies found</span
                        >
                        <p class="text-gray-500 dark:text-gray-500 text-sm">
                           Try adjusting your search
                        </p>
                     </div>
                  </div>

                  <!-- Mobile Data Cards -->
                  <div
                     v-else
                     v-for="(item, index) in apiData.results"
                     :key="item.id"
                     class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 shadow-sm transition-all duration-200"
                     :class="{
                        'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20':
                           selectedRows.includes(item.id),
                        'bg-gray-50/50 dark:bg-gray-800/50': index % 2 === 1,
                     }"
                  >
                     <!-- Card Header -->
                     <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-3">
                           <input
                              type="checkbox"
                              :value="item.id"
                              v-model="selectedRows"
                              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                           />
                           <span
                              class="text-sm font-medium text-gray-500 dark:text-gray-400"
                           >
                              #{{ apiData.pagination?.showing_from + index }}
                           </span>
                        </div>
                        <div class="flex items-center gap-2">
                           <span
                              class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                              :class="getStatusClass(item.status)"
                           >
                              <i class="fa-solid fa-circle text-[8px] mr-1"></i>
                              {{ item.status }}
                           </span>
                           <div class="flex items-center space-x-1">
                              <button
                                 @click="editItem(item)"
                                 class="p-1 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                              >
                                 <i
                                    class="fa-solid fa-pen-to-square text-xs"
                                 ></i>
                              </button>
                              <button
                                 @click="viewItem(item)"
                                 class="p-1 text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-300"
                              >
                                 <i class="fa-solid fa-eye text-xs"></i>
                              </button>
                              <button
                                 @click="deleteItem(item)"
                                 class="p-1 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
                              >
                                 <i class="fa-solid fa-trash text-xs"></i>
                              </button>
                           </div>
                        </div>
                     </div>

                     <!-- Card Content -->
                     <div class="space-y-2">
                        <div class="flex items-center justify-between">
                           <span
                              class="text-sm font-semibold text-gray-800 dark:text-gray-200 break-words flex-1 mr-2"
                              >{{ item.name }}</span
                           >
                           <span
                              class="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 text-purple-800 dark:text-purple-300 whitespace-nowrap flex-shrink-0"
                           >
                              <i
                                 class="fa-solid fa-crown mr-1 text-yellow-500 text-xs"
                              ></i>
                              {{ item.subscription_plan }}
                           </span>
                        </div>
                        <div
                           class="text-xs text-gray-600 dark:text-gray-400 flex items-center gap-2 break-all"
                        >
                           <i class="fa-solid fa-envelope text-gray-400"></i>
                           {{ item.email }}
                        </div>
                        <div
                           class="text-xs text-gray-500 dark:text-gray-500 flex items-center gap-2"
                        >
                           <i class="fa-solid fa-calendar text-gray-400"></i>
                           Created: {{ formatDate(item.created_date) }}
                        </div>
                     </div>
                  </div>
               </div>
            </div>

            <!-- Table Info and Pagination -->
            <div
               class="flex flex-col lg:flex-row justify-between items-center gap-3 p-3 sm:p-2 bg-gray-50 dark:bg-gray-900/30 rounded-lg border border-gray-200 dark:border-gray-700"
            >
               <!-- Showing Info -->
               <div
                  class="text-xs sm:text-sm text-gray-600 dark:text-gray-400 font-medium text-center sm:text-left"
               >
                  Showing {{ apiData?.pagination?.showing_from || 0 }} to
                  {{ apiData?.pagination?.showing_to || 0 }} of
                  {{ apiData?.total_items || 0 }}
                  <span
                     v-if="selectedRows.length > 0"
                     class="text-blue-600 dark:text-blue-400"
                  >
                     ({{ selectedRows.length }} selected)
                  </span>
               </div>

               <!-- Pagination -->
               <div
                  class="flex items-center space-x-1 sm:space-x-2"
                  v-if="apiData?.pagination"
               >
                  <!-- First Page -->
                  <button
                     @click="goToPage(1)"
                     :disabled="currentPage === 1"
                     class="p-1 sm:p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200"
                     title="First Page"
                  >
                     <i class="fa-solid fa-angles-left text-xs sm:text-sm"></i>
                  </button>

                  <!-- Previous Page -->
                  <button
                     @click="goToPage(currentPage - 1)"
                     :disabled="currentPage === 1"
                     class="p-1 sm:p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200"
                     title="Previous Page"
                  >
                     <i class="fa-solid fa-angle-left text-xs sm:text-sm"></i>
                  </button>

                  <!-- Page Numbers -->
                  <button
                     v-for="page in visiblePages"
                     :key="page"
                     @click="goToPage(page)"
                     :class="[
                        'px-2 sm:px-3 py-1 sm:py-2 rounded-lg border text-xs sm:text-sm font-medium transition-all duration-200 min-w-8 sm:min-w-10',
                        currentPage === page
                           ? 'bg-gradient-to-r from-blue-500 to-blue-600 border-blue-500 text-white shadow-lg shadow-blue-500/25'
                           : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600',
                     ]"
                  >
                     {{ page }}
                  </button>

                  <!-- Next Page -->
                  <button
                     @click="goToPage(currentPage + 1)"
                     :disabled="currentPage === apiData.pagination.total_pages"
                     class="p-1 sm:p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200"
                     title="Next Page"
                  >
                     <i class="fa-solid fa-angle-right text-xs sm:text-sm"></i>
                  </button>

                  <!-- Last Page -->
                  <button
                     @click="goToPage(apiData.pagination.total_pages)"
                     :disabled="currentPage === apiData.pagination.total_pages"
                     class="p-1 sm:p-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200"
                     title="Last Page"
                  >
                     <i class="fa-solid fa-angles-right text-xs sm:text-sm"></i>
                  </button>
               </div>
            </div>
         </div>

         <!-- Card Footer -->
         <div
            class="px-3 py-2 sm:px-4 sm:py-3 border-t border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row justify-between items-center gap-2 bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-900/20"
         >
            <div
               class="text-xs sm:text-sm text-gray-600 dark:text-gray-400 text-center sm:text-left"
            >
               Last updated: {{ lastUpdated }}
            </div>
            <button
               @click="refreshData"
               class="px-3 sm:px-4 py-1.5 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors duration-200 flex items-center gap-2 text-sm sm:text-base"
            >
               <i class="fa-solid fa-rotate text-xs sm:text-sm"></i>
               <span>Refresh</span>
            </button>
         </div>
      </div>
   </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import {DEMO_USER_API_URL} from '../routes';

const loading = ref(false);
const apiData = ref(null);

// Table configuration
const entriesPerPage = ref(10);
const currentPage = ref(1);
const searchQuery = ref('');
const selectedRows = ref([]);
const selectAll = ref(false);
const bulkAction = ref('');
const sortColumn = ref('name');
const sortDirection = ref('asc');

// Table columns configuration
const columns = ref([
   { key: 'name', label: 'Company Name' },
   { key: 'email', label: 'Email Address' },
   { key: 'status', label: 'Status' },
   { key: 'subscription_plan', label: 'Subscription Plan' },
   { key: 'created_date', label: 'Created Date' },
]);

// Computed properties
const visiblePages = computed(() => {
   if (!apiData.value?.pagination) return [];

   const totalPages = apiData.value.pagination.total_pages;
   const maxVisible = window.innerWidth < 640 ? 3 : 5;
   let startPage = Math.max(1, currentPage.value - Math.floor(maxVisible / 2));
   let endPage = Math.min(totalPages, startPage + maxVisible - 1);

   if (endPage - startPage + 1 < maxVisible) {
      startPage = Math.max(1, endPage - maxVisible + 1);
   }

   const pages = [];
   for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
   }

   return pages;
});

const lastUpdated = computed(() => {
   return new Date().toLocaleString();
});

// Methods
const fetchData = async () => {
   
   console.log("------------------------------------------");   
   console.log("Fetching URL = ", DEMO_USER_API_URL)
   console.log("------------------------------------------");

   loading.value = true;
   try {
      const params = new URLSearchParams({
         page: currentPage.value,
         page_size: entriesPerPage.value,
         ...(searchQuery.value && { search: searchQuery.value }),
         ...(sortColumn.value && {
            ordering:
               sortDirection.value === 'desc'
                  ? `-${sortColumn.value}`
                  : sortColumn.value,
         }),
      });

      const response = await fetch(`${DEMO_USER_API_URL}?${params}`);

      if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      apiData.value = data;
   } catch (error) {
      console.error('Error fetching data:', error);
      // Fallback to empty data
      apiData.value = {
         total_items: 0,
         results: [],
         pagination: {
            showing_from: 0,
            showing_to: 0,
            total_pages: 0,
         },
      };
   } finally {
      loading.value = false;
   }
};

const goToPage = (page) => {
   if (page >= 1 && page <= (apiData.value?.pagination?.total_pages || 1)) {
      currentPage.value = page;
      fetchData();
   }
};

const onSearchInput = debounce(() => {
   currentPage.value = 1;
   fetchData();
}, 500);

const clearSearch = () => {
   searchQuery.value = '';
   currentPage.value = 1;
   fetchData();
};

const sortTable = (column) => {
   if (sortColumn.value === column) {
      sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
   } else {
      sortColumn.value = column;
      sortDirection.value = 'asc';
   }
   fetchData();
};

const getStatusClass = (status) => {
   const classes = {
      active:
         'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300',
      inactive: 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300',
      pending:
         'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300',
      suspended:
         'bg-gray-100 dark:bg-gray-900/30 text-gray-800 dark:text-gray-300',
   };
   return (
      classes[status] ||
      'bg-gray-100 dark:bg-gray-900/30 text-gray-800 dark:text-gray-300'
   );
};

const formatDate = (dateString) => {
   const date = new Date(dateString);
   return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
   });
};

const executeBulkAction = () => {
   if (!bulkAction.value) return;

   console.log(`Executing ${bulkAction.value} on:`, selectedRows.value);

   // Reset after execution
   bulkAction.value = '';
   selectedRows.value = [];
};

const editItem = (item) => {
   console.log('Edit item:', item);
};

const viewItem = (item) => {
   console.log('View item:', item);
};

const deleteItem = (item) => {
   console.log('Delete item:', item);
};

const refreshData = () => {
   fetchData();
};

// Watch for selectAll changes
watch(selectAll, (newVal) => {
   if (newVal && apiData.value?.results) {
      selectedRows.value = apiData.value.results.map((item) => item.id);
   } else {
      selectedRows.value = [];
   }
});

// Watch for selectedRows changes
watch(selectedRows, (newVal) => {
   if (apiData.value?.results) {
      selectAll.value =
         newVal.length === apiData.value.results.length &&
         apiData.value.results.length > 0;
   }
});

// Utility function for debouncing
function debounce(func, wait) {
   let timeout;
   return function executedFunction(...args) {
      const later = () => {
         clearTimeout(timeout);
         func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
   };
}

// Load initial data
onMounted(() => {
   fetchData();
});
</script>

<style scoped>
/* Custom responsive breakpoints */
@media (max-width: 475px) {
   .xs\:block {
      display: block !important;
   }
   .xs\:hidden {
      display: none !important;
   }
   .xs\:flex-row {
      flex-direction: row !important;
   }
   .xs\:items-center {
      align-items: center !important;
   }
}
</style>
