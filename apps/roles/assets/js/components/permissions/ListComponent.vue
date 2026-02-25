<template>
    <MasterCardLayout :is-loading="loadingStates.loading">
        <!-- Loading -->
        <template #loading>
            <div class="flex items-center justify-center py-20">
                <i class="fa-solid fa-spinner fa-spin text-3xl text-blue-500"></i>
            </div>
        </template>

        <!-- Main Content Card -->
        <MainContentCard :error="error">
            <!-- Header Icon -->
            <template #icon>
                <i class="fa-solid fa-shield-alt text-blue-500 dark:text-blue-400"></i>
            </template>

            <!-- Header Title -->
            <template #title>
                All Permissions
            </template>

            <!-- Header Right Side -->
            <template #header-right>
                <div class="w-80">
                    <InputeComponent placeholder="Search permissions..." id="search" name="search" type="search"
                        v-model="searchQuery" />
                </div>
            </template>

            <template #body>
                <div class="flex-1 overflow-y-auto px-3 py-3 sm:px-6 sm:py-6 space-y-6">
                    <!-- Permissions Grouped by Module -->
                    <div v-for="(permissions, module) in filteredGroupedPermissions" :key="module"
                        class="border rounded-lg p-4 bg-gray-50 dark:bg-gray-800">
                        <!-- Module Title -->
                        <h4
                            class="text-blue-600 dark:text-white font-bold text-lg mb-4 flex items-center gap-2 border-b pb-2">
                            <i class="fa-solid fa-lock"></i>
                            {{ makeCapital(module) }}
                        </h4>

                        <!-- Permissions Grid -->
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                            <div v-for="permission in permissions" :key="permission.id"
                                class="flex items-center gap-2 p-2 bg-white dark:bg-gray-700 rounded shadow-sm hover:shadow transition">
                                <i class="fa-solid fa-lock-open text-green-500 text-sm"></i>
                                <span class="text-sm text-gray-700 dark:text-gray-200">{{ permission.name }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </MainContentCard>
    </MasterCardLayout>
</template>

<script setup>
import { ref, onMounted, reactive, inject, computed, watch } from 'vue';
import { RoleApiURL, RolePageURL, PermissionApiURL } from '../../routes';

// ===================================================================
// =========================== 1. INJECTIONS =========================
// ===================================================================
const toast = inject('toast');
const axios = inject('axios');

// ===================================================================
// =========================== 2. PROPS ==============================
// ===================================================================
const props = defineProps({
    itemId: {
        type: [Number, String],
        default: null
    }
});

// ===================================================================
// =========================== 3. DATA ================================
// ===================================================================
const loadingStates = reactive({
    loading: false,
    save: false
});
const error = ref(null);
const permissionsList = ref([]);
const searchQuery = ref('');
// ===================================================================
// =========================== 4. COMPUTED ============================
// ===================================================================
const groupedPermissions = computed(() => {
    const groups = {};
    permissionsList.value.forEach(permission => {
        const module = permission.module || 'other';
        if (!groups[module]) {
            groups[module] = [];
        }
        groups[module].push(permission);
    });

    // Sort permissions by name in each group
    Object.keys(groups).forEach(module => {
        groups[module].sort((a, b) => a.name.localeCompare(b.name));
    });

    return groups;
});

const filteredGroupedPermissions = computed(() => {
    if (!searchQuery.value) return groupedPermissions.value;

    const query = searchQuery.value.toLowerCase();
    const filtered = {};

    Object.entries(groupedPermissions.value).forEach(([module, permissions]) => {
        const matchedPermissions = permissions.filter(p =>
            p.name.toLowerCase().includes(query) ||
            p.codename.toLowerCase().includes(query) ||
            module.toLowerCase().includes(query)
        );

        if (matchedPermissions.length > 0) {
            filtered[module] = matchedPermissions;
        }
    });

    return filtered;
});

// ===================================================================
// =========================== 5. MOUNTED ============================
// ===================================================================
onMounted(() => {
    fetchPermissions();
});

// ===================================================================
// =========================== 6. METHODS ============================
// ===================================================================
const fetchPermissions = async () => {
    loadingStates.loading = true;
    try {
        const response = await axios.get(PermissionApiURL.List);
        if (response.data.success) {
            permissionsList.value = response.data.results;
        }
    } catch (err) {
        console.error(err);
        toast.error('Failed to load permissions');
    } finally {
        loadingStates.loading = false;
    }
};

const makeCapital = (v) => {
    if (v) return v.charAt(0).toUpperCase() + v.slice(1);
    return '';
};
// ===================================================================
// =========================== 7. WATCHERS ============================
// ===================================================================

</script>