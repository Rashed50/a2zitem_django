<template>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
        <!-- Hero Slider Section -->
        <div class="relative bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-800 dark:to-indigo-800">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                    <!-- Left Content -->
                    <div class="text-white space-y-6">
                        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
                            Everything at <span class="text-yellow-300">Your Fingertips</span>
                        </h1>
                        <p class="text-lg md:text-xl text-purple-100">
                            Shop the latest electronics, fashion, and more with exclusive deals
                        </p>
                        <div class="flex flex-wrap gap-4">
                            <router-link to="/shop"
                                class="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition duration-300 shadow-lg">
                                Shop Now
                            </router-link>
                            <router-link to="/offers"
                                class="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-purple-600 transition duration-300">
                                View Offers
                            </router-link>
                        </div>

                        <!-- Stats -->
                        <div class="grid grid-cols-3 gap-4 pt-8">
                            <div v-for="stat in stats" :key="stat.label">
                                <div class="text-2xl font-bold">{{ stat.value }}</div>
                                <div class="text-sm text-purple-200">{{ stat.label }}</div>
                            </div>
                        </div>
                    </div>

                    <!-- Right Image -->
                    <div class="hidden md:block">
                        <img src="https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&h=400&q=80"
                            alt="Shopping" class="rounded-lg shadow-2xl animate-float w-full h-auto object-cover">
                    </div>
                </div>
            </div>

            <!-- Wave Shape -->
            <div class="absolute bottom-0 left-0 right-0">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"
                    class="fill-current text-gray-50 dark:text-gray-900">
                    <path fill-opacity="1"
                        d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,154.7C960,171,1056,181,1152,170.7C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z">
                    </path>
                </svg>
            </div>
        </div>

        <!-- Categories Section -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div class="flex justify-between items-center mb-8">
                <h2 class="text-2xl md:text-3xl font-bold text-gray-800 dark:text-white">
                    Shop by Category
                </h2>
                <router-link to="/categories"
                    class="text-purple-600 hover:text-purple-700 font-semibold flex items-center gap-1">
                    View All
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                </router-link>
            </div>

            <!-- Category Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                <router-link v-for="category in categories" :key="category.id" :to="`/category/${category.slug}`"
                    class="group">
                    <div
                        class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-md hover:shadow-xl transition duration-300 text-center">
                        <div class="w-16 h-16 mx-auto mb-3 rounded-full flex items-center justify-center group-hover:scale-110 transition duration-300"
                            :class="category.bgColor">
                            <svg class="w-8 h-8" :class="category.iconColor" fill="none" stroke="currentColor"
                                v-html="category.icon"></svg>
                        </div>
                        <h3 class="font-semibold text-gray-800 dark:text-white">{{ category.name }}</h3>
                        <p class="text-sm text-gray-500 dark:text-gray-400">{{ category.itemCount }}+ items</p>
                    </div>
                </router-link>
            </div>
        </div>

        <!-- Flash Sale Section -->
        <div class="bg-gradient-to-r from-red-500 to-pink-500 dark:from-red-700 dark:to-pink-700 py-8">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex flex-col md:flex-row justify-between items-center mb-6">
                    <div class="flex items-center gap-3">
                        <span class="text-3xl font-bold text-white">⚡ Flash Sale</span>
                        <span class="bg-white text-red-500 px-3 py-1 rounded-full text-sm font-semibold">Limited Time
                            Offer</span>
                    </div>

                    <!-- Timer -->
                    <div class="flex items-center gap-2 text-white">
                        <span class="text-lg font-semibold">Ends in:</span>
                        <div class="flex gap-1">
                            <div v-for="(unit, index) in timer" :key="index" class="flex items-center">
                                <div class="bg-white bg-opacity-20 rounded-lg px-3 py-1">
                                    <span class="text-2xl font-bold">{{ unit.value }}</span>
                                    <span class="text-sm">{{ unit.label }}</span>
                                </div>
                                <span v-if="index < timer.length - 1" class="text-2xl font-bold mx-1">:</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Flash Sale Products -->
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                    <div v-for="product in flashSaleProducts" :key="product.id"
                        class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden group relative">
                        <span class="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
                            -{{ product.discount }}%
                        </span>
                        <img :src="product.image" :alt="product.name" class="w-full h-48 object-cover">
                        <div class="p-3">
                            <h3 class="font-semibold text-sm text-gray-800 dark:text-white mb-1">{{ product.name }}</h3>
                            <div class="flex items-center gap-1 mb-2">
                                <span class="text-lg font-bold text-red-500">${{ product.salePrice.toFixed(2) }}</span>
                                <span class="text-sm text-gray-400 line-through">${{ product.regularPrice.toFixed(2)
                                    }}</span>
                            </div>
                            <button @click="addToCart(product)"
                                class="w-full bg-purple-600 text-white py-2 rounded-lg text-sm hover:bg-purple-700 transition">
                                Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Featured Products Section -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div class="flex justify-between items-center mb-8">
                <h2 class="text-2xl md:text-3xl font-bold text-gray-800 dark:text-white">
                    Featured Products
                </h2>
                <div class="flex gap-2">
                    <button @click="scrollProducts('prev')"
                        class="p-2 bg-gray-200 dark:bg-gray-700 rounded-full hover:bg-gray-300 dark:hover:bg-gray-600 transition">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7">
                            </path>
                        </svg>
                    </button>
                    <button @click="scrollProducts('next')"
                        class="p-2 bg-gray-200 dark:bg-gray-700 rounded-full hover:bg-gray-300 dark:hover:bg-gray-600 transition">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7">
                            </path>
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Products Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                <div v-for="product in featuredProducts" :key="product.id"
                    class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden group hover:shadow-xl transition duration-300">
                    <div class="relative overflow-hidden">
                        <img :src="product.image" :alt="product.name"
                            class="w-full h-56 object-cover group-hover:scale-110 transition duration-500">
                        <button @click="toggleWishlist(product)"
                            class="absolute top-3 right-3 bg-white dark:bg-gray-800 p-2 rounded-full opacity-0 group-hover:opacity-100 transition">
                            <svg class="w-5 h-5"
                                :class="product.inWishlist ? 'text-red-500 fill-current' : 'text-red-500'" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z">
                                </path>
                            </svg>
                        </button>
                    </div>
                    <div class="p-4">
                        <div class="flex items-center gap-1 text-yellow-400 mb-2">
                            <svg v-for="star in 5" :key="star" class="w-4 h-4"
                                :class="star <= product.rating ? 'fill-current' : 'text-gray-300'"
                                viewBox="0 0 20 20">★</svg>
                            <span class="text-xs text-gray-500 dark:text-gray-400 ml-1">({{ product.reviews }})</span>
                        </div>
                        <h3 class="font-semibold text-gray-800 dark:text-white mb-1">{{ product.name }}</h3>
                        <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">{{ product.description }}</p>
                        <div class="flex justify-between items-center">
                            <span class="text-xl font-bold text-purple-600 dark:text-purple-400">${{
                                product.price.toFixed(2) }}</span>
                            <button @click="addToCart(product)"
                                class="bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-300 p-2 rounded-lg hover:bg-purple-200 dark:hover:bg-purple-800 transition">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Brands Section -->
        <div class="bg-white dark:bg-gray-800 py-12">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <h2 class="text-2xl md:text-3xl font-bold text-center text-gray-800 dark:text-white mb-10">
                    Trusted Brands
                </h2>
                <div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-8 items-center">
                    <div v-for="brand in brands" :key="brand.name"
                        class="grayscale hover:grayscale-0 transition duration-300">
                        <img :src="brand.logo" :alt="brand.name" class="w-full">
                    </div>
                </div>
            </div>
        </div>

        <!-- Features Section -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div v-for="feature in features" :key="feature.title"
                    class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md text-center">
                    <div class="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4"
                        :class="feature.bgColor">
                        <svg class="w-6 h-6" :class="feature.iconColor" fill="none" stroke="currentColor"
                            v-html="feature.icon"></svg>
                    </div>
                    <h3 class="font-semibold text-gray-800 dark:text-white mb-2">{{ feature.title }}</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400">{{ feature.description }}</p>
                </div>
            </div>
        </div>

        <!-- Newsletter Section -->
        <div class="bg-gradient-to-r from-purple-600 to-indigo-600 dark:from-purple-800 dark:to-indigo-800 py-16">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <h2 class="text-3xl font-bold text-white mb-4">Subscribe to Our Newsletter</h2>
                <p class="text-purple-100 mb-8">Get the latest updates on new products and upcoming sales</p>
                <div class="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
                    <input type="email" v-model="newsletterEmail" placeholder="Your email address"
                        class="flex-1 px-4 py-3 rounded-lg focus:outline-none bg-white bg-opacity-20 text-white placeholder-purple-200 border border-purple-300">
                    <button @click="subscribeNewsletter"
                        class="bg-white text-purple-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition">
                        Subscribe
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'HomeComponent',
    data() {
        return {
            stats: [
                { value: '10k+', label: 'Products' },
                { value: '5k+', label: 'Customers' },
                { value: '50+', label: 'Brands' }
            ],
            categories: [
                {
                    id: 1, name: 'Electronics', slug: 'electronics', itemCount: 120,
                    bgColor: 'bg-purple-100 dark:bg-purple-900',
                    iconColor: 'text-purple-600 dark:text-purple-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>'
                },
                {
                    id: 2, name: 'Fashion', slug: 'fashion', itemCount: 250,
                    bgColor: 'bg-pink-100 dark:bg-pink-900',
                    iconColor: 'text-pink-600 dark:text-pink-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>'
                },
                {
                    id: 3, name: 'Home & Living', slug: 'home-living', itemCount: 80,
                    bgColor: 'bg-green-100 dark:bg-green-900',
                    iconColor: 'text-green-600 dark:text-green-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>'
                },
                {
                    id: 4, name: 'Books', slug: 'books', itemCount: 500,
                    bgColor: 'bg-yellow-100 dark:bg-yellow-900',
                    iconColor: 'text-yellow-600 dark:text-yellow-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>'
                },
                {
                    id: 5, name: 'Sports', slug: 'sports', itemCount: 150,
                    bgColor: 'bg-red-100 dark:bg-red-900',
                    iconColor: 'text-red-600 dark:text-red-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2 2 2 4-4 2 2 2-2 2 2 2-2 2 2 2 2M5 10v8h14v-8M5 10h14"></path>'
                },
                {
                    id: 6, name: 'Gadgets', slug: 'gadgets', itemCount: 90,
                    bgColor: 'bg-indigo-100 dark:bg-indigo-900',
                    iconColor: 'text-indigo-600 dark:text-indigo-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>'
                }
            ],
            timer: [
                { value: '02', label: 'h' },
                { value: '15', label: 'm' },
                { value: '30', label: 's' }
            ],
            flashSaleProducts: [
                {
                    id: 1,
                    name: 'Wireless Headphones',
                    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&h=200&q=80',
                    salePrice: 49.99,
                    regularPrice: 69.99,
                    discount: 30
                },
                {
                    id: 2,
                    name: 'Smart Watch',
                    image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&h=200&q=80',
                    salePrice: 89.99,
                    regularPrice: 119.99,
                    discount: 25
                },
                {
                    id: 3,
                    name: 'Travel Backpack',
                    image: 'https://images.unsplash.com/photo-1547949003-9792a18a2601?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&h=200&q=80',
                    salePrice: 39.99,
                    regularPrice: 49.99,
                    discount: 20
                },
                {
                    id: 4,
                    name: 'Running Shoes',
                    image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&h=200&q=80',
                    salePrice: 79.99,
                    regularPrice: 129.99,
                    discount: 40
                },
                {
                    id: 5,
                    name: 'Cotton T-shirt',
                    image: 'https://images.unsplash.com/photo-1583744946564-b52ac1c389c8?ixlib=rb-4.0.3&auto=format&fit=crop&w=200&h=200&q=80',
                    salePrice: 19.99,
                    regularPrice: 23.99,
                    discount: 15
                }
            ],
            featuredProducts: [
                {
                    id: 101,
                    name: 'Gaming Laptop',
                    description: 'Intel i7, 16GB RAM, 512GB SSD',
                    image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&h=300&q=80',
                    price: 999.99,
                    rating: 5,
                    reviews: 123,
                    inWishlist: false
                },
                {
                    id: 102,
                    name: 'Smartphone',
                    description: '5G, 108MP Camera',
                    image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&h=300&q=80',
                    price: 699.99,
                    rating: 4,
                    reviews: 89,
                    inWishlist: true
                },
                {
                    id: 103,
                    name: 'Premium Watch',
                    description: 'Swiss Made, Sapphire Glass',
                    image: 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&h=300&q=80',
                    price: 249.99,
                    rating: 5,
                    reviews: 234,
                    inWishlist: false
                },
                {
                    id: 104,
                    name: 'Noise Cancelling Headphones',
                    description: 'Bluetooth 5.0, 40hr Battery',
                    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&h=300&q=80',
                    price: 149.99,
                    rating: 4,
                    reviews: 156,
                    inWishlist: false
                }
            ],
            brands: [
                { name: 'Apple', logo: 'https://via.placeholder.com/150x50/f9f9f9/4a5568?text=Apple' },
                { name: 'Samsung', logo: 'https://via.placeholder.com/150x50/f9f9f9/4a5568?text=Samsung' },
                { name: 'Nike', logo: 'https://via.placeholder.com/150x50/f9f9f9/4a5568?text=Nike' },
                { name: 'Adidas', logo: 'https://via.placeholder.com/150x50/f9f9f9/4a5568?text=Adidas' },
                { name: 'Sony', logo: 'https://via.placeholder.com/150x50/f9f9f9/4a5568?text=Sony' },
                { name: 'LG', logo: 'https://via.placeholder.com/150x50/f9f9f9/4a5568?text=LG' }
            ],
            features: [
                {
                    title: '100% Authentic',
                    description: 'All products are original',
                    bgColor: 'bg-purple-100 dark:bg-purple-900',
                    iconColor: 'text-purple-600 dark:text-purple-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>'
                },
                {
                    title: 'Fast Delivery',
                    description: 'Within 24 hours in city',
                    bgColor: 'bg-blue-100 dark:bg-blue-900',
                    iconColor: 'text-blue-600 dark:text-blue-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
                },
                {
                    title: 'Secure Payment',
                    description: 'Visa, Mastercard, bkash',
                    bgColor: 'bg-green-100 dark:bg-green-900',
                    iconColor: 'text-green-600 dark:text-green-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path>'
                },
                {
                    title: '7 Days Return',
                    description: 'Easy return policy',
                    bgColor: 'bg-orange-100 dark:bg-orange-900',
                    iconColor: 'text-orange-600 dark:text-orange-300',
                    icon: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>'
                }
            ],
            newsletterEmail: ''
        }
    },
    methods: {
        addToCart(product) {
            // Implement add to cart logic
            console.log('Adding to cart:', product)
        },
        toggleWishlist(product) {
            product.inWishlist = !product.inWishlist
        },
        scrollProducts(direction) {
            // Implement scroll logic for featured products
            console.log('Scrolling:', direction)
        },
        subscribeNewsletter() {
            if (this.newsletterEmail) {
                // Implement newsletter subscription
                console.log('Subscribing email:', this.newsletterEmail)
                this.newsletterEmail = ''
            }
        }
    }
}
</script>

<style scoped>
.animate-float {
    animation: float 3s ease-in-out infinite;
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }
}
</style>