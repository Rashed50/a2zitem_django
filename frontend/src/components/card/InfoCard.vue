<!-- components/InfoCard.vue -->
<template>
  <div class="bg-gray-50 dark:bg-gray-700/50 rounded-md p-3 border border-gray-200 dark:border-gray-600 transition-all"
    :class="colSpan">
    <!-- Label (সবসময় দেখাবে) -->
    <p class="text-xs text-gray-500 dark:text-gray-400 mb-1.5 font-medium">{{ label }}</p>

    <div class="flex items-start gap-3">
      <!-- Icon (যদি showIcon=true হয় তাহলে সবসময় দেখাবে) -->
      <i v-if="showIcon" :class="['fa-solid', getIconClass, 'text-blue-500 text-xl mt-0.5 shrink-0']"></i>

      <!-- Content Area -->
      <div class="flex-1 min-w-0">
        <!-- Media Preview (image/file/video) -->
        <div v-if="isMedia(value)" class="space-y-2">
          <!-- Image -->
          <div v-if="isImage(value)"
            class="rounded overflow-hidden border border-gray-300 dark:border-gray-600 relative group">
            <img :src="value" alt="Preview" class="max-h-40 w-full object-contain" loading="lazy" />
            <a :href="value" target="_blank" rel="noopener noreferrer"
              class="absolute top-2 right-2 bg-black/60 hover:bg-black/80 text-white p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200"
              title="Open in new tab">
              <i class="fa-solid fa-eye text-lg"></i>
            </a>
          </div>


          <!-- PDF -->
          <div v-else-if="isPdf(value)"
            class="rounded overflow-hidden border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-800 h-40 flex flex-col items-center justify-center">
            <i class="fa-solid fa-file-pdf text-red-500 text-7xl mb-3"></i>
            <p class="text-sm font-medium text-gray-700 dark:text-gray-300 truncate max-w-[90%] px-2 text-center">
              {{ getFileName(value) }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">PDF Document</p>
          </div>

          <!-- Video -->
          <div v-else-if="isVideo(value)" class="rounded overflow-hidden border border-gray-300 dark:border-gray-600">
            <video :src="value" controls class="max-h-48 w-full object-contain"></video>
          </div>

          <!-- Other Files -->
          <div v-else class="flex items-center gap-3 text-gray-600 dark:text-gray-300 py-4">
            <i class="fa-solid fa-file text-4xl text-indigo-500"></i>
            <div>
              <p class="text-sm font-medium truncate">{{ getFileName(value) }}</p>
              <p class="text-xs">{{ getFileExtension(value).toUpperCase() }}</p>
            </div>
          </div>
        </div>

        <!-- Normal Text Value -->
        <div v-else>
          <p class="text-md font-semibold text-gray-800 dark:text-gray-100 break-words" :class="extraClass">
            {{ value || '—' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number, Boolean, null], default: '' },
  icon: { type: String, default: 'fa-info-circle' },
  extraClass: { type: String, default: '' },
  showIcon: { type: Boolean, default: true },
  colSpan: { type: String, default: 'col-span-1' }
});

// Icon logic - media হলে type অনুযায়ী আইকন চেঞ্জ করা যায়
const getIconClass = computed(() => {
  if (!props.showIcon) return props.icon;

  if (isImage(props.value)) return 'fa-image';
  if (isPdf(props.value)) return 'fa-file-pdf';
  if (isVideo(props.value)) return 'fa-video';
  if (props.value && typeof props.value === 'string' && props.value.includes('.')) return 'fa-file';

  return props.icon; // default
});

// Helpers
const isImage = (val) => {
  if (typeof val !== 'string') return false;
  const ext = val.split('?')[0].split('.').pop()?.toLowerCase() || '';
  return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'].includes(ext);
};

const isPdf = (val) => {
  if (typeof val !== 'string') return false;
  return val.split('?')[0].toLowerCase().endsWith('.pdf');
};

const isVideo = (val) => {
  if (typeof val !== 'string') return false;
  const ext = val.split('?')[0].split('.').pop()?.toLowerCase() || '';
  return ['mp4', 'webm', 'ogg', 'mov'].includes(ext);
};

const isMedia = (val) => {
  return isImage(val) || isPdf(val) || isVideo(val);
};

const getFileName = (url) => {
  if (!url) return 'File';
  return decodeURIComponent(url.split('/').pop().split('?')[0] || 'File');
};

const getFileExtension = (url) => {
  if (!url) return '';
  return (url.split('?')[0].split('.').pop() || '').toLowerCase();
};
</script>



<!-- 
##! Basic Information grid 
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

  ## আইকন সহ সাধারণ কার্ড 
  <InfoCard label="Company Name" :value="detailsData.name" icon="fa-building" />

  ## আইকন ছাড়া 
  <InfoCard 
    label="Email" 
    :value="detailsData.email" 
    :show-icon="false" 
  />

  ## লম্বা address-এর জন্য col-span-2 বা col-span-full 
  <InfoCard 
    label="Address" 
    :value="detailsData.address" 
    icon="fa-location-dot"
    col-span="col-span-full md:col-span-2 lg:col-span-3"
    extra-class="whitespace-pre-wrap"
  />

  ## অন্যান্য 
  <InfoCard label="Phone" :value="detailsData.phone" icon="fa-phone" />
</div>

<InfoCard 
  label="Company Logo" 
  :value="detailsData.logo" 
  icon="fa-image" 
  :show-icon="true" 
/>

<InfoCard 
  label="Government License (PDF)" 
  :value="detailsData.documents[0]?.document" 
  :show-icon="false" 
  col-span="col-span-full" 
/>

<InfoCard 
  label="Company Intro Video" 
  :value="someVideoUrl" 
  icon="fa-video" 
/>
-->