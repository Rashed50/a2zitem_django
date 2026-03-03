<template>
    <header class="bg-white dark:bg-gray-800 shadow-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <!-- Top Header -->
            <div class="flex items-center justify-between h-16">
                <!-- Logo -->
                <div class="flex-shrink-0">
                    <router-link to="/" class="text-2xl font-bold text-purple-600 dark:text-purple-400">
                        a2z<span class="text-gray-800 dark:text-gray-200">Item</span>
                    </router-link>
                </div>

                <!-- Search Bar (Desktop) -->
                <div class="hidden md:flex flex-1 max-w-lg mx-8">
                    <div class="relative w-full">
                        <input type="text" v-model="searchQuery" @keyup.enter="handleSearch"
                            placeholder="Search products, brands & categories..."
                            class="w-full px-4 py-2 pr-10 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-white">
                        <button @click="handleSearch"
                            class="absolute right-2 top-2 text-gray-400 hover:text-purple-600 dark:hover:text-purple-400">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                            </svg>
                        </button>
                    </div>
                </div>

                <!-- Right Icons & User Menu -->
                <div class="flex items-center gap-4">
                    <!-- Cart Icon -->
                    <button @click="goToCart"
                        class="relative p-2 text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                        </svg>
                        <span v-if="cartCount > 0"
                            class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-500 rounded-full cart-badge">
                            {{ cartCount }}
                        </span>
                    </button>

                    <!-- Wishlist Icon -->
                    <button @click="goToWishlist"
                        class="hidden md:block p-2 text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z">
                            </path>
                        </svg>
                    </button>

                    <!-- User Menu / Login Button -->
                    <div v-if="isAuthenticated" class="relative">
                        <button @click="toggleUserMenu"
                            class="flex items-center gap-2 p-2 text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition">
                            <div
                                class="w-8 h-8 bg-purple-100 dark:bg-purple-900 rounded-full flex items-center justify-center">
                                <span class="text-sm font-semibold text-purple-600 dark:text-purple-300">
                                    {{ userInitial }}
                                </span>
                            </div>
                            <svg class="w-4 h-4 transition-transform" :class="{ 'rotate-180': userMenuOpen }"
                                fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </button>

                        <!-- Dropdown Menu -->
                        <div v-if="userMenuOpen"
                            class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg py-1 border border-gray-200 dark:border-gray-700 z-50">
                            <router-link to="/profile"
                                class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-purple-50 dark:hover:bg-gray-700">
                                <div class="flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z">
                                        </path>
                                    </svg>
                                    My Profile
                                </div>
                            </router-link>
                            <router-link to="/orders"
                                class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-purple-50 dark:hover:bg-gray-700">
                                <div class="flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                                    </svg>
                                    My Orders
                                </div>
                            </router-link>
                            <router-link to="/wishlist"
                                class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-purple-50 dark:hover:bg-gray-700">
                                <div class="flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z">
                                        </path>
                                    </svg>
                                    Wishlist
                                </div>
                            </router-link>
                            <div class="border-t border-gray-200 dark:border-gray-700 my-1"></div>
                            <button @click="handleLogout"
                                class="block w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20">
                                <div class="flex items-center gap-2">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1">
                                        </path>
                                    </svg>
                                    Logout
                                </div>
                            </button>
                        </div>
                    </div>

                    <!-- Login Button (when not authenticated) -->
                    <router-link v-else to="/login"
                        class="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1">
                            </path>
                        </svg>
                        <span class="hidden md:inline">Login</span>
                    </router-link>

                    <!-- Mobile Menu Button -->
                    <button @click="toggleMobileMenu" class="md:hidden p-2 text-gray-600 dark:text-gray-300">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Mobile Search (Hidden on Desktop) -->
            <div class="md:hidden py-3">
                <div class="relative">
                    <input type="text" v-model="searchQuery" @keyup.enter="handleSearch"
                        placeholder="Search products..."
                        class="w-full px-4 py-2 pr-10 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-white">
                    <button @click="handleSearch" class="absolute right-2 top-2 text-gray-400">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Navigation Menu -->
            <nav class="hidden md:flex items-center gap-6 py-3 border-t border-gray-200 dark:border-gray-700">
                <router-link v-for="category in categories" :key="category.id" :to="`/category/${category.slug}`"
                    class="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition">
                    {{ category.name }}
                </router-link>
                <router-link to="/sale" class="text-sm font-medium text-purple-600 dark:text-purple-400 ml-auto">
                    Sale 🔥
                </router-link>
            </nav>

            <!-- Mobile Menu -->
            <div v-if="mobileMenuOpen" class="md:hidden py-3 border-t border-gray-200 dark:border-gray-700">
                <div class="flex flex-col space-y-2">
                    <router-link v-for="category in categories" :key="category.id" :to="`/category/${category.slug}`"
                        @click="mobileMenuOpen = false"
                        class="px-2 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition">
                        {{ category.name }}
                    </router-link>
                    <router-link to="/sale" @click="mobileMenuOpen = false"
                        class="px-2 py-2 text-sm font-medium text-purple-600 dark:text-purple-400">
                        Sale 🔥
                    </router-link>
                </div>
            </div>
        </div>
    </header>
</template>

<script>
export default {
    name: 'HeaderComponent',
    data() {
        return {
            searchQuery: '',
            userMenuOpen: false,
            mobileMenuOpen: false,
            isAuthenticated: false, // This should come from your auth store
            cartCount: 3, // This should come from your cart store
            categories: [
                { id: 1, name: 'Electronics', slug: 'electronics' },
                { id: 2, name: 'Fashion', slug: 'fashion' },
                { id: 3, name: 'Home & Living', slug: 'home-living' },
                { id: 4, name: 'Books', slug: 'books' },
                { id: 5, name: 'Sports', slug: 'sports' },
                { id: 6, name: 'Gadgets', slug: 'gadgets' }
            ]
        }
    },
    computed: {
        userInitial() {
            // This should come from your auth store
            return 'U'
        }
    },
    methods: {
        toggleUserMenu() {
            this.userMenuOpen = !this.userMenuOpen
        },
        toggleMobileMenu() {
            this.mobileMenuOpen = !this.mobileMenuOpen
        },
        handleSearch() {
            if (this.searchQuery.trim()) {
                this.$router.push(`/search?q=${encodeURIComponent(this.searchQuery)}`)
            }
        },
        goToCart() {
            this.$router.push('/cart')
        },
        goToWishlist() {
            this.$router.push('/wishlist')
        },
        handleLogout() {
            // Implement logout logic
            console.log('Logging out...')
        }
    },
    mounted() {
        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.$el.contains(e.target)) {
                this.userMenuOpen = false
            }
        })
    }
}
</script>

<style scoped>
.cart-badge {
    animation: pulse 2s infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.1);
    }
}
</style>