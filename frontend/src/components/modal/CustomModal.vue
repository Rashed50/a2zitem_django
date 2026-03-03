<!-- components/CustomModal.vue -->
<template>
    <Transition name="modal">
        <div v-if="isOpen" class="fixed inset-0 z-[9999] flex items-center justify-center overflow-hidden">
            <!-- Overlay -->
            <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="closeModal"></div>

            <!-- Modal Content -->
            <div
                ref="modalRef"
                class="@container relative bg-white dark:bg-gray-800 rounded-xl shadow-2xl overflow-hidden flex flex-col transition-all duration-200"
                :class="[
                    modalSizeClass,
                    isFullScreen ? 'w-screen h-screen max-w-none max-h-none rounded-none' : 'w-full max-w-2xl mx-4'
                ]"
                :style="modalPositionStyle"
            >
                <!-- Header -->
                <div class="px-6 py-2 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between bg-gray-50/90 dark:bg-gray-900/30 backdrop-blur-md z-[9999] shrink-0"
                    :class="isFullScreen ? 'fixed top-0 left-0 right-0' : ''">
                    <!-- Draggable Title Area -->
                    <h3 v-if="!isFullScreen"
                        class="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate cursor-move select-none flex-1"
                        @mousedown.left="startDrag">
                        <slot name="header">
                            {{ title || 'Modal Title' }}
                        </slot>
                    </h3>

                    <!-- Title without drag in fullscreen -->
                    <h3 v-else class="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate flex-1">
                        <slot name="header">
                            {{ title || 'Modal Title' }}
                        </slot>
                    </h3>

                    <!-- Buttons -->
                    <div class="flex items-center gap-3">
                        <button @click="toggleFullScreen"
                            class="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300 transition"
                            :title="isFullScreen ? 'Exit Fullscreen' : 'Enter Fullscreen'">
                            <i class="fa-solid text-xl" :class="isFullScreen ? 'fa-compress' : 'fa-expand'"></i>
                        </button>

                        <button @click="closeModal"
                            class="p-2 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/40 text-gray-600 hover:text-red-600 dark:text-gray-300 dark:hover:text-red-400 transition"
                            aria-label="Close">
                            <i class="fa-solid fa-xmark text-xl"></i>
                        </button>
                    </div>
                </div>

                <!-- Body -->
                <div class="flex-1 px-6 py-3 overflow-y-auto"
                    :class="isFullScreen ? 'pt-20 px-8 pb-10' : 'max-h-[calc(100vh-120px)]'">
                    <slot name="body">
                        <p class="text-gray-600 dark:text-gray-300">
                            Modal body content goes here...
                        </p>
                    </slot>
                </div>

                <!-- Footer -->
                <div v-if="$slots.footer"
                    class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3 bg-gray-50/80 dark:bg-gray-900/60 shrink-0">
                    <slot name="footer"></slot>
                </div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
    isOpen: { type: Boolean, required: true },
    title: { type: String, default: '' },
    size: { type: String, default: 'md' },
})

const emit = defineEmits(['update:isOpen', 'close'])

const isFullScreen = ref(false)
const modalRef = ref(null)
const modalPosition = ref({ x: 0, y: 0 })

let isDragging = false
let startX = 0
let startY = 0
let initialX = 0
let initialY = 0

const modalSizeClass = computed(() => {
    if (isFullScreen.value) return ''
    const sizes = {
        sm: 'max-w-md',
        md: 'max-w-2xl',
        lg: 'max-w-4xl',
        xl: 'max-w-6xl',
    }
    return sizes[props.size] || sizes.md
})

const modalPositionStyle = computed(() => {
    if (isFullScreen.value) return {}
    return {
        transform: `translate(${modalPosition.value.x}px, ${modalPosition.value.y}px)`,
    }
})

const toggleFullScreen = () => {
    isFullScreen.value = !isFullScreen.value
    if (isFullScreen.value) {
        modalPosition.value = { x: 0, y: 0 }
    }
}

const closeModal = () => {
    emit('update:isOpen', false)
    emit('close')
    isFullScreen.value = false
    document.body.classList.remove('modal-fullscreen', 'overflow-hidden')
    modalPosition.value = { x: 0, y: 0 }
}

// Drag functions
const startDrag = (e) => {
    if (isFullScreen.value) return
    if (e.button !== 0) return

    // Skip if clicking on buttons
    if (e.target.closest('button')) return

    e.preventDefault()
    e.stopPropagation()

    isDragging = true
    startX = modalPosition.value.x
    startY = modalPosition.value.y
    initialX = e.clientX
    initialY = e.clientY

    document.addEventListener('mousemove', doDrag)
    document.addEventListener('mouseup', stopDrag)
}

const doDrag = (e) => {
    if (!isDragging) return

    const deltaX = e.clientX - initialX
    const deltaY = e.clientY - initialY

    modalPosition.value.x = startX + deltaX
    modalPosition.value.y = startY + deltaY

    const width = modalRef.value.offsetWidth
    const height = modalRef.value.offsetHeight

    const minX = -((window.innerWidth / 2) - (width / 2))
    const maxX = (window.innerWidth / 2) - (width / 2)

    const minY = -((window.innerHeight / 2) - (height / 2))
    const maxY = (window.innerHeight / 2) - (height / 2)

    modalPosition.value.x = Math.max(minX, Math.min(modalPosition.value.x, maxX))
    modalPosition.value.y = Math.max(minY, Math.min(modalPosition.value.y, maxY))
}

const stopDrag = () => {
    isDragging = false
    document.removeEventListener('mousemove', doDrag)
    document.removeEventListener('mouseup', stopDrag)
}

// Fullscreen hide sidebar/header
watch(isFullScreen, (val) => {
    if (val) {
        document.body.classList.add('modal-fullscreen', 'overflow-hidden')
    } else {
        document.body.classList.remove('modal-fullscreen', 'overflow-hidden')
    }
})

watch(
    () => props.isOpen,
    (newVal) => {
        if (!newVal) {
            closeModal()
        }
    }
)



</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: all 0.3s ease-out;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
    transform: translateY(-20px) scale(0.96);
}

.modal-enter-to,
.modal-leave-from {
    opacity: 1;
    transform: translateY(0) scale(1);
}

/* Fullscreen hiding */
.modal-fullscreen #sidebar,
.modal-fullscreen #header {
    display: none !important;
}

/* Cursor only on title in normal mode */
.cursor-move {
    cursor: move;
}
</style>

<!-- 1. সিম্পল টেক্সট / ডিটেইলস দেখানো -->
<!-- 
<AppModal :isOpen="showModal" @update:isOpen="showModal = $event" title="Company Owner Details">
  <template #body>
    <div class="space-y-4">
      <p><strong>Name:</strong> Md. Rakib Hasan</p>
      <p><strong>Email:</strong> rakib@example.com</p>
      <p><strong>Phone:</strong> +880 1712-345678</p>
    </div>
  </template>
</AppModal>
-->

<!-- 2. Form ঢোকানো -->
<!-- 
<AppModal :isOpen="showAddOwnerModal" @update:isOpen="showAddOwnerModal = $event" title="Add New Owner">
  <template #body>
    <form @submit.prevent="handleSubmit" class="space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Full Name</label>
        <input
          v-model="form.name"
          type="text"
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
        <input
          v-model="form.email"
          type="email"
          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      ## আরও ফিল্ড যোগ করতে পারো 

      <div class="flex justify-end gap-3 mt-6">
        <button
          type="button"
          @click="showAddOwnerModal = false"
          class="px-4 py-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-lg transition"
        >
          Cancel
        </button>
        <button
          type="submit"
          class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
        >
          Save Owner
        </button>
      </div>
    </form>
  </template>
</AppModal>
-->

<!-- 3. Footer সহ (যেমন: Save / Cancel) -->
<!-- 
<AppModal :isOpen="isOpen" title="Confirm Action">
  <template #body>
    <p class="text-gray-600 dark:text-gray-300">Are you sure you want to delete this owner?</p>
  </template>

  <template #footer>
    <button @click="cancel" class="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-lg">Cancel</button>
    <button @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg">Delete</button>
  </template>
</AppModal>
-->