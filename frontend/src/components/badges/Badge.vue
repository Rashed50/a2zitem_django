<template>
  <span
    :class="badgeClasses"
    class="inline-flex items-center justify-center gap-2 font-medium leading-none whitespace-nowrap select-none transition-all duration-200 relative overflow-hidden cursor-default"
    @click="emit('click', $event)"
  >
    <!-- Left Icon -->
    <i v-if="iconLeft" :class="iconLeftClasses"></i>

    <!-- Content -->
    <span class="badge-content">
      <slot>{{ label }}</slot>
    </span>

    <!-- Right Icon -->
    <i v-if="iconRight" :class="iconRightClasses"></i>

    <!-- Close Button -->
    <i
      v-if="closable"
      class="fa-solid fa-xmark badge-close ml-2"
      @click.stop="emit('close')"
    ></i>

    <!-- Counter -->
    <span v-if="count !== null" class="badge-counter">
      {{ formattedCount }}
    </span>

    <!-- Dot Indicator (for status) -->
    <span v-if="dot" class="badge-dot"></span>
  </span>
</template>

<script setup>
import { computed, useAttrs } from 'vue'

const $attrs = useAttrs()

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: v => [
      'primary', 'secondary', 'success', 'danger', 'warning', 'info',
      'light', 'dark', 'purple', 'pink', 'orange', 'teal', 'indigo',
      'outline-primary', 'outline-success', 'outline-danger', 'outline-warning',
      'gradient-primary', 'gradient-success', 'gradient-danger'
    ].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: v => ['xs', 'sm', 'md', 'lg'].includes(v)
  },
  rounded: {
    type: [Boolean, String],
    default: 'lg',
    validator: v => typeof v === 'boolean' || ['sm', 'md', 'lg', 'full'].includes(v)
  },
  label: String,
  iconLeft: String,
  iconRight: String,
  closable: Boolean,
  count: { type: Number, default: null },
  maxCount: { type: Number, default: 99 },
  dot: Boolean,
  pulse: Boolean,
  shadow: { type: Boolean, default: false }
})

const emit = defineEmits(['click', 'close'])

const formattedCount = computed(() =>
  props.count > props.maxCount ? `${props.maxCount}+` : props.count
)

// Dynamic Classes
const isClickable = computed(() => $attrs.onClick !== undefined)
const badgeClasses = computed(() => [
  baseClasses.value,
  sizeClasses.value,
  variantClasses.value,
  roundedClasses.value,
  { 'shadow-sm': props.shadow },
  { 'animate-pulse': props.pulse },
  { 'cursor-pointer hover:scale-105 transition-transform': isClickable.value }
])

const baseClasses = computed(() => 'relative')

const sizeClasses = computed(() => ({
  xs: 'px-1.5 py-0.5 text-xs min-h-5',
  sm: 'px-2 py-1 text-xs min-h-6',
  md: 'px-2.5 py-1 text-sm min-h-7',
  lg: 'px-3 py-1.5 text-base min-h-8'
}[props.size]))

const roundedClasses = computed(() => {
  if (props.rounded === true || props.rounded === 'full') return 'rounded-full'
  const map = { sm: 'rounded', md: 'rounded-md', lg: 'rounded-lg' }
  return props.rounded ? map[props.rounded] : 'rounded-md'
})

const variantClasses = computed(() => {
  const variants = {
    // Solid
    primary: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300',
    success: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
    danger: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
    info: 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900/40 dark:text-cyan-300',
    secondary: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    light: 'bg-gray-50 text-gray-700 dark:bg-gray-800 dark:text-gray-400',
    dark: 'bg-gray-800 text-white',
    purple: 'bg-purple-100 text-purple-800 dark:bg-purple-900/40 dark:text-purple-300',
    pink: 'bg-pink-100 text-pink-800',
    orange: 'bg-orange-100 text-orange-800',
    teal: 'bg-teal-100 text-teal-800',
    indigo: 'bg-indigo-100 text-indigo-800',

    // Outline
    'outline-primary': 'bg-transparent text-blue-700 border border-blue-500 dark:text-blue-400',
    'outline-success': 'bg-transparent text-green-700 border border-green-500',
    'outline-danger': 'bg-transparent text-red-700 border border-red-500',

    // Gradient
    'gradient-primary': 'bg-gradient-to-r from-blue-500 to-purple-600 text-white',
    'gradient-success': 'bg-gradient-to-r from-green-500 to-emerald-600 text-white',
    'gradient-danger': 'bg-gradient-to-r from-red-500 to-pink-600 text-white'
  }
  return variants[props.variant] || variants.primary
})

const iconLeftClasses = computed(() => `${props.iconLeft} text-current opacity-80`)
const iconRightClasses = computed(() => `${props.iconRight} text-current opacity-80`)
</script>

<style scoped>
.badge-close {
  @apply text-xs opacity-60 hover:opacity-100 cursor-pointer transition;
}
.badge-counter {
  @apply min-w-5 h-5 px-1.5 flex items-center justify-center text-xs font-bold rounded-full bg-white/30 border border-white/40 text-current ml-1;
}
.badge-dot {
  @apply absolute -top-1 -right-1 w-3 h-3 bg-current rounded-full ring-2 ring-white dark:ring-gray-900;
}
</style>