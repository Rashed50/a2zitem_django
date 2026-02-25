<template>
   <div class="flex flex-col h-full w-full space-y-4">
      <!-- 🔹 Page Header -->
      <div class="border-b border-gray-200 dark:border-gray-700 pb-3">
         <div class="flex justify-between items-center">
            <div>
               <h2
                  class="text-2xl font-semibold text-gray-800 dark:text-gray-100 flex items-center gap-2"
               >
                  <i class="fa-solid fa-house-chimney text-blue-600"></i>
                  Dashboard Overview
               </h2>
               <p class="text-sm text-gray-500 dark:text-gray-400">
                  Welcome back, Rakib 👋
               </p>
            </div>
            <button
               class="px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition text-sm"
            >
               <i class="fa-solid fa-plus mr-1"></i> New Task
            </button>
         </div>
      </div>

      <!-- 🔹 Stats Section -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
         <div
            v-for="card in stats"
            :key="card.title"
            class="bg-white dark:bg-gray-800 rounded-md shadow-sm border border-gray-200 dark:border-gray-700 p-4 flex items-center gap-3 hover:shadow-md transition"
         >
            <div class="p-3 rounded-full text-white" :class="card.bg">
               <i :class="card.icon"></i>
            </div>
            <div>
               <h4 class="text-sm text-gray-500 dark:text-gray-400">
                  {{ card.title }}
               </h4>
               <p
                  class="text-xl font-semibold text-gray-800 dark:text-gray-100"
               >
                  {{ card.value }}
               </p>
            </div>
         </div>
      </div>

      <!-- 🔹 Recent Activity & Quick Form -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
         <!-- Recent Activity -->
         <div
            class="col-span-2 bg-white dark:bg-gray-800 rounded-md shadow-sm border border-gray-200 dark:border-gray-700"
         >
            <div
               class="px-5 py-3 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center bg-gray-50 dark:bg-gray-900/40"
            >
               <h3
                  class="text-lg font-semibold text-gray-800 dark:text-gray-100 flex items-center gap-2"
               >
                  <i class="fa-solid fa-clock-rotate-left text-blue-500"></i>
                  Recent Activities
               </h3>
            </div>

            <ul class="divide-y divide-gray-200 dark:divide-gray-700">
               <li
                  v-for="(activity, index) in activities"
                  :key="index"
                  class="px-5 py-3 flex items-start gap-3 hover:bg-gray-50 dark:hover:bg-gray-900/40 transition"
               >
                  <div
                     class="w-10 h-10 flex items-center justify-center rounded-full text-white"
                     :class="activity.color"
                  >
                     <i :class="activity.icon"></i>
                  </div>
                  <div class="flex-1">
                     <p class="text-sm text-gray-800 dark:text-gray-100">
                        {{ activity.text }}
                     </p>
                     <span class="text-xs text-gray-500 dark:text-gray-400">{{
                        activity.time
                     }}</span>
                  </div>
               </li>
            </ul>
         </div>

         <!-- Quick Contact Form -->
         <div
            class="bg-white dark:bg-gray-800 rounded-md shadow-sm border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden"
         >
            <div
               class="px-5 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/40 flex items-center gap-2"
            >
               <i class="fa-solid fa-envelope text-blue-500"></i>
               <h3
                  class="text-lg font-semibold text-gray-800 dark:text-gray-100"
               >
                  Quick Contact
               </h3>
            </div>

            <div class="p-5 space-y-4">
               <InputeComponent
                  label="Full Name"
                  placeholder="Enter your name"
                  v-model="form.name"
               />
               <InputeComponent
                  label="Email"
                  placeholder="example@mail.com"
                  type="email"
                  v-model="form.email"
               />
               <InputeComponent
                  label="Subject"
                  placeholder="Subject"
                  v-model="form.subject"
               />
               <InputeComponent
                  label="Message"
                  type="textarea"
                  placeholder="Write something..."
                  v-model="form.message"
                  :rows="3"
               />

               <button
                  type="submit"
                  class="w-full py-2.5 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition"
               >
                  <i class="fa-solid fa-paper-plane mr-1"></i> Send Message
               </button>
            </div>
         </div>
      </div>
   </div>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({
   name: 'Rakib Hasan',
   email: 'rakib@example.com',
   subject: 'Support Request',
   message: 'Hi, I need help with my account setup.',
});

const stats = [
   {
      title: 'Total Users',
      value: '1,240',
      icon: 'fa-solid fa-users',
      bg: 'bg-blue-500',
   },
   {
      title: 'Sales Today',
      value: '$3,980',
      icon: 'fa-solid fa-dollar-sign',
      bg: 'bg-green-500',
   },
   {
      title: 'Active Orders',
      value: '56',
      icon: 'fa-solid fa-cart-shopping',
      bg: 'bg-orange-500',
   },
   {
      title: 'Pending Tasks',
      value: '12',
      icon: 'fa-solid fa-list-check',
      bg: 'bg-purple-500',
   },
];

const activities = [
   {
      icon: 'fa-solid fa-user-plus',
      text: 'New user <b>John Doe</b> registered.',
      time: '5 mins ago',
      color: 'bg-green-500',
   },
   {
      icon: 'fa-solid fa-cart-arrow-down',
      text: 'Order <b>#1042</b> placed by <b>Emily</b>.',
      time: '30 mins ago',
      color: 'bg-blue-500',
   },
   {
      icon: 'fa-solid fa-credit-card',
      text: '<b>$120</b> payment received from <b>Michael</b>.',
      time: '1 hr ago',
      color: 'bg-indigo-500',
   },
   {
      icon: 'fa-solid fa-triangle-exclamation',
      text: 'Server usage reached <b>90%</b> capacity.',
      time: '2 hrs ago',
      color: 'bg-red-500',
   },
];
</script>

<style scoped>
/* Optional subtle scrollbar */
::-webkit-scrollbar {
   width: 6px;
}
::-webkit-scrollbar-thumb {
   background-color: rgba(156, 163, 175, 0.4);
   border-radius: 3px;
}
</style>
