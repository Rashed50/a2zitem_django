<!-- frontend\src\components\card\AuditInfoCard.vue -->
<template>
    <div class="bg-gray-50 dark:bg-gray-700 rounded-lg divide-y divide-gray-200 dark:divide-gray-600">
        <!-- Created By -->
        <div class="p-4 flex items-start gap-3">
            <div
                class="flex-shrink-0 w-8 h-8 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center">
                <i class="fa-solid fa-user-plus text-green-600 dark:text-green-300 text-sm"></i>
            </div>
            <div class="flex-1">
                <p class="text-sm font-medium text-gray-900 dark:text-gray-100">Created by</p>
                <div class="flex items-center gap-2 mt-1">
                    <span class="text-gray-700 dark:text-gray-300 font-semibold">
                        {{ createdBy || 'System' }}
                    </span>
                    <span class="text-xs text-gray-500 dark:text-gray-400">
                        <i class="fa-regular fa-clock mr-1"></i>
                        {{ createdAt }}
                    </span>
                </div>
            </div>
        </div>

        <!-- Last Updated By -->
        <div class="p-4 flex items-start gap-3">
            <div
                class="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                <i class="fa-solid fa-pen-to-square text-blue-600 dark:text-blue-300 text-sm"></i>
            </div>
            <div class="flex-1">
                <p class="text-sm font-medium text-gray-900 dark:text-gray-100">Last updated by</p>
                <div class="flex items-center gap-2 mt-1">
                    <span class="text-gray-700 dark:text-gray-300 font-semibold">
                        {{ updatedBy || 'Not updated yet' }}
                    </span>
                    <span v-if="showUpdatedAt" class="text-xs text-gray-500 dark:text-gray-400">
                        <i class="fa-regular fa-clock mr-1"></i>
                        {{ updatedAt }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AuditInfoCard',

    props: {
        createdBy: {
            type: String,
            default: 'System'
        },
        createdAt: {
            type: String,
            default: ''
        },
        updatedBy: {
            type: String,
            default: ''
        },
        updatedAt: {
            type: String,
            default: ''
        },
        showUpdatedAt: {
            type: Boolean,
            default: true
        }
    }
}
</script>