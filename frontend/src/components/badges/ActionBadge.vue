<template>
   <Badge
      :variant="variant"
      :size="size"
      :rounded="rounded"
      :icon-left="icon"
      :count="count"
      :dot="dot"
      :pulse="pulse"
      :closable="closable"
      :class="customClasses"
      class="font-medium whitespace-nowrap"
      @close="$emit('close')"
      @click="$emit('click')"
   >
      <slot>{{ label }}</slot>
   </Badge>
</template>

<script setup>
import { computed } from 'vue';
import { useSlots } from 'vue';
import Badge from './Badge.vue';

const slots = useSlots();

const props = defineProps({
   status: { type: [String, null, undefined], default: null },
   size: { type: String, default: 'md' },
   rounded: { type: [Boolean, String], default: true },
   count: Number,
   dot: Boolean,
   pulse: Boolean,
   closable: Boolean,
   iconLeft: { type: String, default: null },
   isIcon : { type: Boolean, default: true },
});

defineEmits(['click', 'close']);

const BADGE_CONFIG = {
   // ── Subscription Plans (তোমার Django Model) ─────────────────────────────
   free: {
      label: 'Free',
      variant: 'light',
      class: 'bg-gray-100 dark:bg-gray-700/50 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600',
      icon: 'fa-solid fa-gift',
   },
   basic: {
      label: 'Basic',
      variant: 'light',
      class: 'bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-300 border border-blue-300 dark:border-blue-700',
      icon: 'fa-solid fa-tag',
   },
   pro: {
      label: 'Pro',
      variant: 'light',
      class: 'bg-orange-100 dark:bg-orange-900/40 text-orange-800 dark:text-orange-300 border border-orange-300 dark:border-orange-700',
      icon: 'fa-solid fa-medal',
   },
   premium: {
      label: 'Premium',
      variant: 'light',
      class: 'bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900/50 dark:to-pink-900/50 text-purple-800 dark:text-purple-300 border border-purple-300 dark:border-purple-600',
      icon: 'fa-solid fa-crown',
   },
   enterprise: {
      label: 'Enterprise',
      variant: 'light',
      class: 'bg-gradient-to-r from-emerald-100 to-teal-100 dark:from-emerald-900/50 dark:to-teal-900/50 text-emerald-800 dark:text-emerald-300 border border-emerald-400 dark:border-emerald-600',
      icon: 'fa-solid fa-building',
   },

   // ── Billing Cycle (তোমার Django Model অনুযায়ী) ───────────────────────
   monthly: {
      label: 'Monthly',
      variant: 'light',
      class: 'bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 text-purple-800 dark:text-purple-300',
      icon: 'fa-solid fa-calendar-alt',
   },
   quarterly: {
      label: 'Quarterly',
      variant: 'light',
      class: 'bg-gradient-to-r from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 text-indigo-800 dark:text-indigo-300',
      icon: 'fa-solid fa-calendar-alt',
   },
   yearly: {
      label: 'Yearly',
      variant: 'light',
      class: 'bg-gradient-to-r from-emerald-100 to-cyan-100 dark:from-emerald-900/30 dark:to-cyan-900/30 text-emerald-800 dark:text-emerald-300',
      icon: 'fa-solid fa-calendar-alt',
   },
   lifetime: {
      label: 'Lifetime',
      variant: 'light',
      class: 'bg-gradient-to-r from-rose-100 to-orange-100 dark:from-rose-900/30 dark:to-orange-900/30 text-rose-800 dark:text-rose-300',
      icon: 'fa-solid fa-infinity',
   },

   // ── Order & Payment Status (E-commerce / POS) ───────────────────────────
   pending: {
      label: 'Pending',
      variant: 'warning',
      icon: 'fa-solid fa-clock',
      dot: true,
   },
   processing: {
      label: 'Processing',
      variant: 'info',
      icon: 'fa-solid fa-cog',
      pulse: true,
   },
   paid: {
      label: 'Paid',
      variant: 'success',
      icon: 'fa-solid fa-check-circle',
   },
   unpaid: {
      label: 'Unpaid',
      variant: 'danger',
      icon: 'fa-solid fa-times-circle',
   },
   cancelled: { label: 'Cancelled', variant: 'dark', icon: 'fa-solid fa-ban' },
   refunded: {
      label: 'Refunded',
      variant: 'secondary',
      icon: 'fa-solid fa-undo',
   },
   partial: {
      label: 'Partial',
      variant: 'warning',
      icon: 'fa-solid fa-adjust',
   },
   onhold: {
      label: 'On Hold',
      variant: 'light',
      icon: 'fa-solid fa-pause-circle',
   },

   // ── Shipping & Delivery ───────────────────────────────────────────────
   shipped: { label: 'Shipped', variant: 'info', icon: 'fa-solid fa-truck' },
   delivered: {
      label: 'Delivered',
      variant: 'success',
      icon: 'fa-solid fa-box-open',
   },
   returned: {
      label: 'Returned',
      variant: 'danger',
      icon: 'fa-solid fa-undo-alt',
   },
   intransit: {
      label: 'In Transit',
      variant: 'primary',
      icon: 'fa-solid fa-shipping-fast',
      pulse: true,
   },

   // ── Stock & Inventory ───────────────────────────────────────────────
   instock: {
      label: 'In Stock',
      variant: 'success',
      icon: 'fa-solid fa-check',
   },
   lowstock: {
      label: 'Low Stock',
      variant: 'warning',
      icon: 'fa-solid fa-exclamation-triangle',
   },
   outofstock: {
      label: 'Out of Stock',
      variant: 'danger',
      icon: 'fa-solid fa-times',
   },

   // ── User & Account Status ─────────────────────────────────────────────
   // bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300
   active: {
      label: 'Active', 
      class: 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300',
      icon: 'fa-solid fa-check fa-xs fa-fw text-green-600 dark:text-green-400',
   },
   inactive: {
      label: 'Inactive',
      class: 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300',
      icon: 'fa-solid fa-ban fa-xs fa-fw text-rose-600 dark:text-rose-400',
   },
   suspended: {
      label: 'Suspended',
      variant: 'danger',
      icon: 'fa-solid fa-user-lock',
   },
   verified: {
      label: 'Verified',
      variant: 'success',
      icon: 'fa-solid fa-badge-check',
   },
   unverified: {
      label: 'Unverified',
      variant: 'warning',
      icon: 'fa-solid fa-exclamation-circle',
   },

   // ── Content & General Status ─────────────────────────────────────────
   draft: { label: 'Draft', variant: 'light', icon: 'fa-solid fa-file-lines' },
   published: {
      label: 'Published',
      variant: 'success',
      icon: 'fa-solid fa-check-double',
   },
   archived: {
      label: 'Archived',
      variant: 'secondary',
      icon: 'fa-solid fa-archive',
   },
   featured: {
      label: 'Featured',
      variant: 'gradient-danger',
      icon: 'fa-solid fa-star',
   },
   new: {
      label: 'New',
      variant: 'gradient-primary',
      icon: 'fa-solid fa-sparkles',
      dot: true,
      pulse: true,
   },
   live: {
      label: 'Live',
      variant: 'danger',
      icon: 'fa-solid fa-circle',
      dot: true,
      pulse: true,
   },
   beta: { label: 'Beta', variant: 'info', icon: 'fa-solid fa-flask' },
   urgent: { label: 'Urgent', variant: 'danger', pulse: true },
};

// সেফ নরমালাইজেশন
const key = computed(() => {
   if (!props.status) return null;
   return props.status.toString().toLowerCase().trim();
});

const config = computed(() => {
   const k = key.value;
   return k && BADGE_CONFIG[k]
      ? BADGE_CONFIG[k]
      : {
           label: props.status || 'Unknown',
           variant: 'light',
           class: 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300',
           icon: 'fa-solid fa-question',
        };
});

// ফাইনাল আউটপুট
const variant = computed(() => config.value.variant || null)
const customClasses = computed(() => config.value.class || '');
const label = computed(() => config.value.label);
const icon = computed(() => {
   // যদি icon disable করা থাকে → কিছুই দেখাবে না
   if (!props.isIcon) return null;
   
   if (slots.default && slots.default()) {
      return null;
   }
   return props.iconLeft || config.value.icon || null;
});
</script>
