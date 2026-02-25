<template>
   <Button
      :variant="variant"
      :size="size"
      :disabled="disabled"
      :loading="loading"
      :icon-left="icon" 
      :rounded="rounded"
      :shadow="shadow"
      :block="block"
      :type="type"
      @click="$emit('click', $event)"
      :class="customClass"
      class="justify-center"
   >
      <!-- <slot>{{ label }}</slot> -->

      <span class="hidden sm:inline">
         {{ fullLabel }}
      </span>

      <span class="sm:hidden">
         {{ mobileLabel }}
      </span>
   </Button>
</template>

<script setup>
import { computed } from 'vue'; // computed import করুন
import Button from './Button.vue';

const props = defineProps({
   action: {
      type: String,
      default: 'default',
      validator: (value) =>
         [
            'create',
            'add',
            'new',
            'draft',
            'edit',
            'update',
            'save',
            'delete',
            'remove',
            'trash',
            'download',
            'export',
            'upload',
            'import',
            'view',
            'show',
            'preview',
            'search',
            'filter',
            'refresh',
            'reset',
            'cancel',
            'back',
            'submit',
            'confirm',
            'approve',
            'reject',
            'send',
            'copy',
            'duplicate',
            'clone',
            'print',
            'share',
         ].includes(value),
   },
   variant: String,
   size: {
      type: String,
      default: 'md',
   },
   disabled: Boolean,
   loading: Boolean,
   label: String,
   rounded: {
      type: String,
      default: 'md',
   },
   shadow: {
      type: Boolean,
      default: true,
   },
   block: Boolean,
   type: {
      type: String,
      default: 'button',
      validator: (value) => ['button', 'submit', 'reset'].includes(value),
   },
});

defineEmits(['click']);

// Action-based configurations
const actionConfig = {
   // Create/Add/New
   create: { icon: 'fa-solid fa-plus', variant: 'success', label: 'Create' },
   add: { icon: 'fa-regular fa-square-plus', variant: 'success', label: 'Add' },
   new: { icon: 'fas fa-file-circle-plus', variant: 'success', label: 'New' },
   draft: { icon: 'fa-regular fa-floppy-disk', variant: 'success', label: 'Draft' },

   // Edit/Update/Save
   edit: { icon: 'fas fa-edit', variant: 'warning', label: 'Edit' },
   update: { icon: 'fas fa-sync', variant: 'warning', label: 'Update' },
   save: { icon: 'fas fa-save', variant: 'success', label: 'Save' },

   // Delete/Remove/Trash
   delete: { icon: 'fas fa-trash', variant: 'danger', label: 'Delete' },
   remove: { icon: 'fas fa-times-circle', variant: 'danger', label: 'Remove' },
   trash: {
      icon: 'fas fa-trash-alt',
      variant: 'outline-danger',
      label: 'Move to Trash',
   },

   // Download/Export
   download: { icon: 'fas fa-download', variant: 'info', label: 'Download' },
   export: {
      icon: 'fas fa-file-export',
      variant: 'outline-info',
      label: 'Export',
   },

   // Upload/Import
   upload: { icon: 'fas fa-upload', variant: 'primary', label: 'Upload' },
   import: {
      icon: 'fas fa-file-import',
      variant: 'outline-primary',
      label: 'Import',
   },

   // View/Show/Preview
   view: { icon: 'fas fa-eye', variant: 'info', label: 'View' },
   show: { icon: 'fas fa-expand', variant: 'info', label: 'Show' },
   preview: {
      icon: 'fas fa-search',
      variant: 'outline-info',
      label: 'Preview',
   },

   // Search/Filter
   search: { icon: 'fas fa-search', variant: 'primary', label: 'Search' },
   filter: {
      icon: 'fas fa-filter',
      variant: 'outline-primary',
      label: 'Filter',
   },

   // Refresh/Reset
   refresh: { icon: 'fas fa-refresh', variant: 'info', label: 'Refresh' },
   reset: { icon: 'fas fa-undo', variant: 'outline-secondary', label: 'Reset' },

   // Cancel
   cancel: {
      icon: 'fas fa-times',
      variant: 'outline-secondary',
      label: 'Cancel',
   },

   // Back
   back: { icon: 'fas fa-arrow-left', variant: 'outline-secondary', label: 'Back' },

   // Submit/Confirm
   submit: { icon: 'fas fa-paper-plane', variant: 'success', label: 'Submit' },
   confirm: {
      icon: 'fas fa-check-circle',
      variant: 'success',
      label: 'Confirm',
   },

   // Approve/Reject
   approve: { icon: 'fas fa-check', variant: 'success', label: 'Approve' },
   reject: { icon: 'fas fa-ban', variant: 'danger', label: 'Reject' },

   // Send
   send: { icon: 'fas fa-paper-plane', variant: 'primary', label: 'Send' },

   // Copy/Duplicate/Clone
   copy: { icon: 'fas fa-copy', variant: 'outline-info', label: 'Copy' },
   duplicate: {
      icon: 'fas fa-clone',
      variant: 'outline-info',
      label: 'Duplicate',
   },
   clone: { icon: 'fas fa-copy', variant: 'info', label: 'Clone' },

   // Print/Share
   print: {
      icon: 'fas fa-print',
      variant: 'outline-secondary',
      label: 'Print',
   },
   share: { icon: 'fas fa-share-alt', variant: 'primary', label: 'Share' },

   // Default
   default: { icon: 'fas fa-cog', variant: 'primary', label: 'Action' },
};

// Computed properties
const config = computed(() => actionConfig[props.action] || actionConfig.default);
const fullLabel = computed(() => props.label || config.value.label || 'Action')
const mobileLabel = computed(() => {
   const full = fullLabel.value

   const shortMap = {
      'Create Plan': 'Create',
      'Save as Draft': 'Draft',
      'Move to Trash': 'Trash',
      'Update Plan': 'Update',
      'Edit Profile': 'Edit',
      'Add New Item': 'Add'
   }

   return shortMap[full] || full.split(' ')[0] || full
})

const icon = computed(() => config.value.icon);
const variant = computed(() => props.variant || config.value.variant);
const label = computed(() => props.label || config.value.label);
const customClass = computed(() => {
   return props.action === 'delete' || props.action === 'remove'
      ? 'hover:scale-105'
      : '';
});
</script>
