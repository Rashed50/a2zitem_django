<template>
   <button
      :class="buttonClasses"
      :disabled="disabled || loading"
      @click="$emit('click', $event)"
      :type="type"
   >
      <div class="button-content">
         <!-- Loading Spinner -->
         <div v-if="loading" class="spinner-container">
            <div class="spinner"></div>
         </div>

         <!-- Icon (left) -->
         <span v-if="iconLeft" class="icon-left">
            <i :class="iconLeft"></i>
         </span>

         <!-- Button Text -->
         <span
            class="button-text"
            :class="{ 'opacity-0': loading && hideTextOnLoad }"
         >
            <slot>{{ label }}</slot>
         </span>

         <!-- Icon (right) -->
         <span v-if="iconRight" class="icon-right">
            <i :class="iconRight"></i>
         </span>
      </div>

      <!-- Ripple Effect -->
      <span v-if="ripple" class="ripple" :class="rippleClass"></span>
   </button>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
   // Variants
   variant: {
      type: String,
      default: 'primary',
      validator: (value) =>
         [
            'primary',
            'secondary',
            'success',
            'danger',
            'warning',
            'info',
            'light',
            'dark',
            'link',
            'outline-primary',
            'outline-secondary',
            'outline-success',
            'outline-danger',
            'outline-warning',
            'outline-info',
            'outline-dark',
            'gradient-primary',
            'gradient-success',
            'gradient-danger',
         ].includes(value),
   },

   // Sizes
   size: {
      type: String,
      default: 'md',
      validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value),
   },

   // States
   disabled: Boolean,
   loading: Boolean,
   active: Boolean,

   // Content
   label: String,
   iconLeft: String,
   iconRight: String,

   // Styles
   rounded: {
      type: String,
      default: 'md',
      validator: (value) =>
         ['none', 'sm', 'md', 'lg', 'full', 'pill'].includes(value),
   },
   shadow: {
      type: Boolean,
      default: false,
   },
   ripple: {
      type: Boolean,
      default: true,
   },
   block: {
      type: Boolean,
      default: false,
   },
   hideTextOnLoad: {
      type: Boolean,
      default: false,
   },

   // HTML button type
   type: {
      type: String,
      default: 'button',
      validator: (value) => ['button', 'submit', 'reset'].includes(value),
   },
});

const emit = defineEmits(['click']);

// Dynamic classes
const buttonClasses = computed(() => {
   const baseClasses = [
      'btn',
      'transition-all',
      'duration-300',
      'ease-out',
      'transform',
      'focus:outline-none',
      'focus:ring-2',
      'focus:ring-offset-2',
      'disabled:opacity-60',
      'disabled:cursor-not-allowed',
      'active:scale-95',
      'overflow-hidden',
      'relative',
      sizeClasses.value,
      roundedClasses.value,
      variantClasses.value,
      shadowClass.value,
      blockClass.value,
      activeClass.value,
   ];

   return baseClasses.filter(Boolean).join(' ');
});

// Size classes
const sizeClasses = computed(() => {
   const sizes = {
      xs: 'px-2 py-1 text-xs font-medium',
      sm: 'px-3 py-1.5 text-sm font-medium',
      md: 'px-5 py-2.5 text-base font-semibold',
      lg: 'px-6 py-3 text-lg font-semibold',
      xl: 'px-8 py-4 text-xl font-bold',
   };
   return sizes[props.size];
});

// Rounded classes
const roundedClasses = computed(() => {
   const rounded = {
      none: 'rounded-none',
      sm: 'rounded-sm',
      md: 'rounded-md',
      lg: 'rounded-lg',
      full: 'rounded-full',
      pill: 'rounded-full px-8',
   };
   return rounded[props.rounded];
});

// Variant classes
const variantClasses = computed(() => {
   const variants = {
      // Solid variants
      primary:
         'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500 border border-blue-600',
      secondary:
         'bg-gray-600 hover:bg-gray-700 text-white focus:ring-gray-500 border border-gray-600',
      success:
         'bg-green-600 hover:bg-green-700 text-white focus:ring-green-500 border border-green-600',
      danger:
         'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500 border border-red-600',
      warning:
         'bg-yellow-500 hover:bg-yellow-600 dark:bg-yellow-600 text-white focus:ring-yellow-500 border border-yellow-500',
      info: 'bg-cyan-500 hover:bg-cyan-600 text-white focus:ring-cyan-500 border border-cyan-500',
      light: 'bg-gray-100 hover:bg-gray-200 text-gray-800 focus:ring-gray-300 border border-gray-200',
      dark: 'bg-gray-800 hover:bg-gray-900 text-white focus:ring-gray-700 border border-gray-800',
      link: 'bg-transparent hover:bg-blue-50 text-blue-600 focus:ring-blue-300 underline border border-transparent',

      // Outline variants
      'outline-primary':
         'bg-transparent hover:bg-blue-600 text-blue-600 hover:text-white border border-blue-600 focus:ring-blue-500',
      'outline-secondary':
         'bg-transparent hover:bg-gray-600 text-gray-100 hover:text-white border border-gray-600 focus:ring-gray-500',
      'outline-success':
         'bg-transparent hover:bg-green-600 text-green-600 hover:text-white border border-green-600 focus:ring-green-500',
      'outline-danger':
         'bg-transparent hover:bg-red-600 text-red-600 hover:text-white border border-red-600 focus:ring-red-500',
      'outline-warning':
         'bg-transparent hover:bg-yellow-500 text-yellow-500 hover:text-white border border-yellow-500 focus:ring-yellow-500',
      'outline-info':
         'bg-transparent hover:bg-cyan-500 text-cyan-500 hover:text-white border border-cyan-500 focus:ring-cyan-500',
      'outline-dark':
         'bg-transparent hover:bg-gray-800 text-gray-800 hover:text-white border border-gray-800 focus:ring-gray-700',

      // Gradient variants
      'gradient-primary':
         'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white focus:ring-purple-500 border-0',
      'gradient-success':
         'bg-gradient-to-r from-green-400 to-green-600 hover:from-green-500 hover:to-green-700 text-white focus:ring-green-500 border-0',
      'gradient-danger':
         'bg-gradient-to-r from-red-400 to-pink-600 hover:from-red-500 hover:to-pink-700 text-white focus:ring-pink-500 border-0',
   };

   return variants[props.variant];
});

// Shadow class
const shadowClass = computed(() => {
   return props.shadow
      ? 'shadow-lg hover:shadow-xl'
      : 'shadow-sm hover:shadow-md';
});

// Block class
const blockClass = computed(() => {
   return props.block ? 'w-full flex justify-center' : '';
});

// Active class
const activeClass = computed(() => {
   return props.active ? 'ring-2 scale-95' : '';
});

// Ripple class based on variant
const rippleClass = computed(() => {
   if (props.variant.includes('outline')) {
      return 'bg-gray-200';
   }
   if (props.variant.includes('gradient')) {
      return 'bg-white/20';
   }
   return 'bg-white/30';
});

/*
// Example:-
// ============== [Complete usage example] ======================================
   <!-- Complete usage example -->
   <Button 
      type="submit"             <!-- button, submit, reset -->
      variant="success"         <!-- primary, success, danger, etc. -->
      size="lg"                 <!-- xs, sm, md, lg, xl -->
      :loading="isLoading"      <!-- Boolean -->
      :disabled="isDisabled"    <!-- Boolean -->
      icon-left="fas fa-save"   <!-- Font Awesome icon -->
      icon-right="fas fa-arrow-right"
      rounded="lg"              <!-- none, sm, md, lg, full, pill -->
      :shadow="true"            <!-- Boolean -->
      :block="true"             <!-- Boolean -->
      :ripple="false"           <!-- Boolean -->
      :hide-text-on-load="true"
      label="Custom Label"      <!-- String -->
      @click="handleClick"      <!-- Event -->
   >
      <!-- Slot content --> 
      Submit Form
  </Button>

*/
</script>

<style scoped>
.btn {
   position: relative;
   transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
   backface-visibility: hidden;
}

.button-content {
   display: flex;
   align-items: center;
   justify-content: center;
   gap: 0.5rem;
   position: relative;
   z-index: 2;
}

.spinner-container {
   display: flex;
   align-items: center;
}

.spinner {
   width: 1.25rem;
   height: 1.25rem;
   border: 2px solid transparent;
   border-top: 2px solid currentColor;
   border-radius: 50%;
   animation: spin 0.8s linear infinite;
}

.icon-left,
.icon-right {
   display: flex;
   align-items: center;
   transition: transform 0.2s ease;
}

.btn:hover .icon-left {
   transform: translateX(-2px);
}

.btn:hover .icon-right {
   transform: translateX(2px);
}

.button-text {
   transition: opacity 0.2s ease;
}

/* Ripple effect */
.ripple {
   position: absolute;
   border-radius: 50%;
   background-color: rgba(255, 255, 255, 0.7);
   transform: scale(0);
   animation: ripple 0.6s linear;
   pointer-events: none;
   z-index: 1;
}

@keyframes ripple {
   to {
      transform: scale(4);
      opacity: 0;
   }
}

@keyframes spin {
   0% {
      transform: rotate(0deg);
   }
   100% {
      transform: rotate(360deg);
   }
}

/* Special hover effects */
.btn:hover {
   transform: translateY(-1px);
}

.btn:active {
   transform: translateY(0);
}

/* Disabled state improvements */
.btn:disabled {
   transform: none !important;
}
</style>
