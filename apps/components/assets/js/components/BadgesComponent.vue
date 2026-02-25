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
               <i class="fa-solid fa-tags text-purple-500"></i>
               Badge Component
            </h4>
            <span class="text-xs text-gray-500 dark:text-gray-400 italic"
               >All badge examples with ActionBadge magic</span
            >
         </div>

         <!-- Card Body -->
         <div class="flex-1 overflow-y-auto px-6 py-8 space-y-12">
            <!-- Basic Solid Badges -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Solid Badges
               </h2>
               <div class="flex flex-wrap gap-3 items-center">
                  <Badge variant="primary">Primary</Badge>
                  <Badge variant="success">Success</Badge>
                  <Badge variant="danger">Danger</Badge>
                  <Badge variant="warning">Warning</Badge>
                  <Badge variant="info">Info</Badge>
                  <Badge variant="secondary">Secondary</Badge>
                  <Badge variant="light">Light</Badge>
                  <Badge variant="dark">Dark</Badge>
                  <Badge variant="purple">Purple</Badge>
                  <Badge variant="pink">Pink</Badge>
                  <Badge variant="orange">Orange</Badge>
                  <Badge variant="teal">Teal</Badge>
               </div>
            </section>

            <!-- Outline Badges -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Outline Badges
               </h2>
               <div class="flex flex-wrap gap-3 items-center">
                  <Badge variant="outline-primary">Primary</Badge>
                  <Badge variant="outline-success">Success</Badge>
                  <Badge variant="outline-danger">Danger</Badge>
               </div>
            </section>

            <!-- Gradient Badges -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Gradient Badges
               </h2>
               <div class="flex flex-wrap gap-3 items-center">
                  <Badge variant="gradient-primary">Premium</Badge>
                  <Badge variant="gradient-success">Verified</Badge>
                  <Badge variant="gradient-danger">Hot Deal</Badge>
               </div>
            </section>

            <!-- Sizes -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Badge Sizes
               </h2>
               <div class="flex flex-wrap items-center gap-4">
                  <Badge variant="primary" size="xs">XS</Badge>
                  <Badge variant="success" size="sm">SM</Badge>
                  <Badge variant="info" size="md">MD</Badge>
                  <Badge variant="warning" size="lg">LG</Badge>
               </div>
            </section>

            <!-- With Icons -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Badges with Icons
               </h2>
               <div class="flex flex-wrap gap-3 items-center">
                  <Badge variant="success" icon-left="fa-solid fa-check">
                     Approved
                  </Badge>
                  <Badge variant="danger" icon-right="fa-solid fa-xmark">
                     Rejected
                  </Badge>
                  <Badge variant="info" icon-left="fa-solid fa-eye">
                     1.2k Views
                  </Badge>
                  <Badge variant="purple" icon-left="fa-solid fa-crown">
                     VIP
                  </Badge>
               </div>
            </section>

            <!-- With Counter -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Badges with Counter
               </h2>
               <div class="flex flex-wrap gap-3 items-center">
                  <Badge variant="danger" :count="99"> Notifications </Badge>
                  <Badge variant="primary" :count="5"> Messages </Badge>
                  <Badge variant="warning" :count="123"> Tasks </Badge>
                  <Badge variant="success" :count="999" :max-count="500">
                     Orders
                  </Badge>
               </div>
            </section>

            <!-- With Dot Indicator -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Dot Indicator (Status)
               </h2>
               <div class="flex flex-wrap gap-4 items-center">
                  <Badge variant="success" dot> Online </Badge>
                  <Badge variant="danger" dot pulse> Live Now </Badge>
                  <Badge variant="warning" dot> Away </Badge>
                  <Badge variant="secondary" dot> Offline </Badge>
               </div>
            </section>

            <!-- Closable Badges (Tags) -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Closable Tags
               </h2>
               <div class="flex flex-wrap gap-3">
                  <Badge variant="primary" closable @close="removeTag('React')"
                     >React</Badge
                  >
                  <Badge variant="info" closable @close="removeTag('Vue')"
                     >Vue.js</Badge
                  >
                  <Badge
                     variant="success"
                     closable
                     @close="removeTag('Laravel')"
                     >Laravel</Badge
                  >
                  <Badge
                     variant="purple"
                     closable
                     @close="removeTag('Tailwind')"
                     >Tailwind</Badge
                  >
               </div>
            </section>

            <!-- Rounded Variations -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Rounded Styles
               </h2>
               <div class="flex flex-wrap gap-3 items-center">
                  <Badge variant="primary" :rounded="false">Square</Badge>
                  <Badge variant="success" rounded="sm">Small</Badge>
                  <Badge variant="info" rounded="md">Medium</Badge>
                  <Badge variant="warning" rounded="lg">Large</Badge>
                  <Badge variant="danger" rounded="full">Pill</Badge>
               </div>
            </section>

            <!-- ActionBadge - The Magic One-Liner -->
            <section>
               <h2
                  class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2 text-purple-600"
               >
                  ActionBadge - One Line Status Badges (Most Used)
               </h2>
               <div class="space-y-8">
                  <!-- User & Account Status -->
                  <div>
                     <h3 class="text-xl font-semibold mb-4 text-gray-700">
                        User Status
                     </h3>
                     <div class="flex flex-wrap gap-3">
                        <ActionBadge status="active" />
                        <ActionBadge status="inactive" />
                        <ActionBadge status="pending" />
                        <ActionBadge status="online" />
                        <ActionBadge status="offline" />
                        <ActionBadge status="new" />
                        <ActionBadge status="premium" />
                        <ActionBadge status="pro" />
                        <ActionBadge status="beta" />
                     </div>
                  </div>

                  <!-- Content Status -->
                  <div>
                     <h3 class="text-xl font-semibold mb-4 text-gray-700">
                        Content Status
                     </h3>
                     <div class="flex flex-wrap gap-3">
                        <ActionBadge status="published" />
                        <ActionBadge status="draft" />
                        <ActionBadge status="archived" />
                        <ActionBadge status="featured" />
                        <ActionBadge status="live" />
                        <ActionBadge status="scheduled" />
                        <ActionBadge status="completed" />
                        <ActionBadge status="failed" />
                     </div>
                  </div>

                  <!-- E-commerce & Inventory -->
                  <div>
                     <h3 class="text-xl font-semibold mb-4 text-gray-700">
                        E-commerce
                     </h3>
                     <div class="flex flex-wrap gap-3">
                        <ActionBadge status="low-stock" />
                        <ActionBadge status="sold-out" />
                        <ActionBadge status="urgent" />
                        <ActionBadge status="new" :count="12" />
                        <ActionBadge status="featured" />
                     </div>
                  </div>

                  <!-- With Counter -->
                  <div>
                     <h3 class="text-xl font-semibold mb-4 text-gray-700">
                        With Counter
                     </h3>
                     <div class="flex flex-wrap gap-3">
                        <ActionBadge status="pending" :count="8" />
                        <ActionBadge status="new" :count="42" />
                        <ActionBadge status="online" :count="156" />
                        <ActionBadge status="live" :count="999" />
                     </div>
                  </div>

                  <!-- Custom Label Override -->
                  <div>
                     <h3 class="text-xl font-semibold mb-4 text-gray-700">
                        Custom Label
                     </h3>
                     <div class="flex flex-wrap gap-3">
                        <ActionBadge status="premium">VIP Member</ActionBadge>
                        <ActionBadge status="pro">Enterprise Plan</ActionBadge>
                        <ActionBadge status="active"
                           >Account Active</ActionBadge
                        >
                     </div>
                  </div>

                  <!-- Closable Tags with ActionBadge -->
                  <div>
                     <h3 class="text-xl font-semibold mb-4 text-gray-700">
                        Removable Tags
                     </h3>
                     <div class="flex flex-wrap gap-3">
                        <ActionBadge
                           status="active"
                           closable
                           @close="removeUserTag('admin')"
                        />
                        <ActionBadge
                           status="premium"
                           closable
                           @close="removeUserTag('vip')"
                        />
                        <ActionBadge
                           status="beta"
                           closable
                           @close="removeUserTag('tester')"
                        />
                     </div>
                  </div>
               </div>
            </section>

            <!-- Real World Examples -->
            <section>
               <h2 class="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">
                  Real World Usage Examples
               </h2>

               <!-- User Profile Card -->
               <div
                  class="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-gray-900 dark:to-gray-800 p-6 rounded-xl shadow-lg"
               >
                  <div class="flex items-center justify-between">
                     <div class="flex items-center gap-4">
                        <div
                           class="w-16 h-16 bg-gray-300 dark:bg-gray-700 rounded-full"
                        ></div>
                        <div>
                           <h3 class="text-xl font-bold">John Doe</h3>
                           <p class="text-gray-600 dark:text-gray-400">
                              john@example.com
                           </p>
                        </div>
                     </div>
                     <div class="flex gap-2">
                        <ActionBadge status="premium" />
                        <ActionBadge status="online" />
                        <ActionBadge status="active" />
                     </div>
                  </div>
               </div>

               <!-- Notification Bell -->
               <div
                  class="mt-6 p-6 bg-white dark:bg-gray-800 rounded-xl shadow-md border"
               >
                  <div class="flex items-center justify-between">
                     <h3 class="text-lg font-semibold">Notifications</h3>
                     <Badge variant="danger" :count="7" rounded="full">
                        <i class="fa-solid fa-bell mr-1"></i>
                     </Badge>
                  </div>
               </div>

               <!-- Product Card -->
               <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div class="border rounded-lg p-4 bg-white dark:bg-gray-800">
                     <div
                        class="bg-gray-200 dark:bg-gray-700 h-40 rounded mb-4"
                     ></div>
                     <h4 class="font-semibold">Premium Plan</h4>
                     <p class="text-2xl font-bold mt-2">
                        $99<span class="text-sm text-gray-500">/month</span>
                     </p>
                     <div class="mt-4 flex flex-wrap gap-2">
                        <ActionBadge status="featured" />
                        <ActionBadge status="new" />
                        <ActionBadge status="premium" />
                     </div>
                  </div>
               </div>

               <!-- Table Row Status -->
               <div class="mt-8 overflow-x-auto">
                  <table class="w-full table-auto border-collapse">
                     <thead>
                        <tr class="bg-gray-50 dark:bg-gray-800">
                           <th class="px-4 py-3 text-left">Order ID</th>
                           <th class="px-4 py-3 text-left">Customer</th>
                           <th class="px-4 py-3 text-left">Amount</th>
                           <th class="px-4 py-3 text-left">Status</th>
                        </tr>
                     </thead>
                     <tbody class="divide-y dark:divide-gray-700">
                        <tr>
                           <td class="px-4 py-3">#1001</td>
                           <td class="px-4 py-3">Alice Johnson</td>
                           <td class="px-4 py-3">$299</td>
                           <td class="px-4 py-3">
                              <ActionBadge status="completed" />
                           </td>
                        </tr>
                        <tr>
                           <td class="px-4 py-3">#1002</td>
                           <td class="px-4 py-3">Bob Smith</td>
                           <td class="px-4 py-3">$149</td>
                           <td class="px-4 py-3">
                              <ActionBadge status="pending" :count="2" />
                           </td>
                        </tr>
                        <tr>
                           <td class="px-4 py-3">#1003</td>
                           <td class="px-4 py-3">Charlie Brown</td>
                           <td class="px-4 py-3">$899</td>
                           <td class="px-4 py-3">
                              <ActionBadge status="live" pulse />
                           </td>
                        </tr>
                     </tbody>
                  </table>
               </div>
            </section>

            <!-- Subscription Plans (তোমার Django Model অনুযায়ী) -->
            <div class="mt-12">
               <h3 class="text-xl font-semibold mb-4 text-gray-700">
                  Subscription Plans
               </h3>
               <div class="flex flex-wrap gap-3">
                  <ActionBadge status="FREE" size="sm" rounded="full" />
                  <ActionBadge status="BASIC" size="sm" rounded="full" />
                  <ActionBadge status="PRO" size="sm" rounded="full" />
                  <ActionBadge status="PREMIUM" size="sm" rounded="full" />
                  <ActionBadge status="ENTERPRISE" size="sm" rounded="full" />
               </div>
               <p class="text-sm text-gray-500 mt-3">
                  Backend থেকে যেকোনো কেসে আসুক (FREE / Free / free) — সব কাজ
                  করবে
               </p>
            </div>

            <!-- Plan with Custom Label (রিয়েল-ওয়ার্ল্ড ইউজ) -->
            <div class="mt-8">
               <h3 class="text-xl font-semibold mb-4 text-gray-700">
                  Plan with Custom Label
               </h3>
               <div class="flex flex-wrap gap-3">
                  <ActionBadge status="PREMIUM" size="sm" rounded="full">
                     <i class="fa-solid fa-crown mr-1"></i> 
                     VIP Member
                  </ActionBadge>
                  <ActionBadge status="ENTERPRISE" size="sm" rounded="full">
                     <i class="fa-solid fa-building mr-1"></i> Enterprise Client
                  </ActionBadge>
                  <ActionBadge status="FREE" size="sm" rounded="full">
                     <i class="fa-solid fa-gift mr-1"></i> Free Forever
                  </ActionBadge>
               </div>
            </div>

            <!-- E-commerce Order Status (2025 Ready) -->
            <div class="mt-12">
               <h3 class="text-xl font-semibold mb-4 text-gray-700">
                  E-commerce Order Flow
               </h3>
               <div class="flex flex-wrap gap-3 items-center">
                  <ActionBadge status="pending" />
                  <ActionBadge status="processing" />
                  <ActionBadge status="paid" />
                  <ActionBadge status="shipped" />
                  <ActionBadge status="intransit" />
                  <ActionBadge status="delivered" />
                  <ActionBadge status="cancelled" />
                  <ActionBadge status="refunded" />
               </div>
            </div>

            <!-- Stock Status -->
            <div class="mt-8">
               <h3 class="text-xl font-semibold mb-4 text-gray-700">
                  Inventory Status
               </h3>
               <div class="flex flex-wrap gap-3">
                  <ActionBadge status="instock" />
                  <ActionBadge status="lowstock" />
                  <ActionBadge status="outofstock" />
               </div>
            </div>

            <!-- User Verification & Account Status -->
            <div class="mt-12">
               <h3 class="text-xl font-semibold mb-4 text-gray-700">
                  User Account Status
               </h3>
               <div class="flex flex-wrap gap-3">
                  <ActionBadge status="verified" />
                  <ActionBadge status="unverified" />
                  <ActionBadge status="suspended" />
                  <ActionBadge status="active" />
                  <ActionBadge status="inactive" />
               </div>
            </div>

            <!-- Real Product Card with Multiple Badges -->
            <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
               <div
                  class="border rounded-xl overflow-hidden shadow-lg bg-white dark:bg-gray-800"
               >
                  <div
                     class="h-48 bg-gradient-to-br from-purple-400 to-pink-400"
                  ></div>
                  <div class="p-5">
                     <h4 class="font-bold text-lg">Ultimate Pro Plan</h4>
                     <p class="text-3xl font-bold mt-2">
                        $299<span class="text-sm text-gray-500">/year</span>
                     </p>
                     <div class="mt-4 flex flex-wrap gap-2">
                        <ActionBadge status="featured" />
                        <ActionBadge status="new" />
                        <ActionBadge status="pro" size="sm" rounded="full" />
                        <ActionBadge
                           status="premium"
                           size="sm"
                           rounded="full"
                        />
                     </div>
                     <button
                        class="mt-4 w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition"
                     >
                        Upgrade Now
                     </button>
                  </div>
               </div>

               <div
                  class="border rounded-xl overflow-hidden shadow-lg bg-white dark:bg-gray-800"
               >
                  <div
                     class="h-48 bg-gradient-to-br from-emerald-400 to-teal-400"
                  ></div>
                  <div class="p-5">
                     <h4 class="font-bold text-lg">Enterprise Solution</h4>
                     <p class="text-3xl font-bold mt-2">Custom</p>
                     <div class="mt-4 flex flex-wrap gap-2">
                        <ActionBadge
                           status="enterprise"
                           size="sm"
                           rounded="full"
                        />
                        <ActionBadge status="verified" />
                        <ActionBadge status="live" />
                     </div>
                     <button
                        class="mt-4 w-full bg-emerald-600 text-white py-2 rounded-lg hover:bg-emerald-700 transition"
                     >
                        Contact Sales
                     </button>
                  </div>
               </div>

               <div
                  class="border rounded-xl overflow-hidden shadow-lg bg-white dark:bg-gray-800"
               >
                  <div
                     class="h-48 bg-gradient-to-br from-gray-300 to-gray-400"
                  ></div>
                  <div class="p-5">
                     <h4 class="font-bold text-lg">Free Plan</h4>
                     <p class="text-3xl font-bold mt-2">
                        $0<span class="text-sm text-gray-500">/forever</span>
                     </p>
                     <div class="mt-4 flex flex-wrap gap-2">
                        <ActionBadge status="free" size="sm" rounded="full" />
                        <ActionBadge status="active" />
                     </div>
                     <button
                        class="mt-4 w-full bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-700 transition"
                     >
                        Current Plan
                     </button>
                  </div>
               </div>
            </div>
         </div>
      </div>
   </div>
</template>

<script setup>
import { inject } from 'vue';
const toast = inject('toast');

const removeTag = (tag) => {
   toast.info(`Tag "${tag}" removed`);
};

const removeUserTag = (role) => {
   toast.warning(`User role "${role}" removed`);
};
</script>
