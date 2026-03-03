<template>
    <footer class="bg-gray-900 dark:bg-black text-gray-300">
        <!-- Main Footer -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <!-- Company Info -->
                <div>
                    <h3 class="text-white text-lg font-bold mb-4">a2zItem</h3>
                    <p class="text-sm mb-4">Your one-stop shop for everything you need. Quality products at the best
                        prices.</p>
                    <div class="flex gap-4">
                        <a v-for="social in socialLinks" :key="social.name" :href="social.url" target="_blank"
                            class="text-gray-400 hover:text-white transition">
                            <svg class="w-5 h-5" fill="currentColor" :viewBox="social.viewBox"
                                v-html="social.icon"></svg>
                        </a>
                    </div>
                </div>

                <!-- Quick Links -->
                <div>
                    <h3 class="text-white text-lg font-bold mb-4">Quick Links</h3>
                    <ul class="space-y-2">
                        <li v-for="link in quickLinks" :key="link.text">
                            <router-link :to="link.url" class="text-sm hover:text-white transition">
                                {{ link.text }}
                            </router-link>
                        </li>
                    </ul>
                </div>

                <!-- Customer Service -->
                <div>
                    <h3 class="text-white text-lg font-bold mb-4">Customer Service</h3>
                    <ul class="space-y-2">
                        <li v-for="link in customerLinks" :key="link.text">
                            <router-link :to="link.url" class="text-sm hover:text-white transition">
                                {{ link.text }}
                            </router-link>
                        </li>
                    </ul>
                </div>

                <!-- Contact Info -->
                <div>
                    <h3 class="text-white text-lg font-bold mb-4">Contact Us</h3>
                    <ul class="space-y-2">
                        <li class="flex items-start gap-2">
                            <svg class="w-5 h-5 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z">
                                </path>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                            <span class="text-sm">123 Business Ave, Suite 100<br>New York, NY 10001</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z">
                                </path>
                            </svg>
                            <span class="text-sm">+1 (555) 123-4567</span>
                        </li>
                        <li class="flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z">
                                </path>
                            </svg>
                            <span class="text-sm">support@a2zitem.com</span>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Bottom Bar -->
            <div class="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
                <p class="text-sm text-gray-400">© {{ currentYear }} a2zItem. All rights reserved.</p>
                <div class="flex gap-4 mt-4 md:mt-0">
                    <img v-for="payment in paymentMethods" :key="payment.alt" :src="payment.src" :alt="payment.alt"
                        class="h-6">
                </div>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: 'FooterComponent',
    data() {
        return {
            currentYear: new Date().getFullYear(),
            socialLinks: [
                {
                    name: 'Facebook',
                    url: 'https://facebook.com',
                    viewBox: '0 0 24 24',
                    icon: '<path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"></path>'
                },
                {
                    name: 'Twitter',
                    url: 'https://twitter.com',
                    viewBox: '0 0 24 24',
                    icon: '<path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>'
                },
                {
                    name: 'Instagram',
                    url: 'https://instagram.com',
                    viewBox: '0 0 24 24',
                    icon: '<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zM5.838 12a6.162 6.162 0 1112.324 0 6.162 6.162 0 01-12.324 0zM12 16a4 4 0 110-8 4 4 0 010 8zm4.965-10.405a1.44 1.44 0 112.881.001 1.44 1.44 0 01-2.881-.001z"></path>'
                }
            ],
            quickLinks: [
                { text: 'About Us', url: '/about' },
                { text: 'Contact Us', url: '/contact' },
                { text: 'Terms & Conditions', url: '/terms' },
                { text: 'Privacy Policy', url: '/privacy' },
                { text: 'FAQs', url: '/faqs' }
            ],
            customerLinks: [
                { text: 'My Account', url: '/profile' },
                { text: 'Order Tracking', url: '/order-tracking' },
                { text: 'Wishlist', url: '/wishlist' },
                { text: 'Returns', url: '/returns' },
                { text: 'Shipping Info', url: '/shipping' }
            ],
            paymentMethods: [
                { src: 'https://via.placeholder.com/40x25/ffffff/4a5568?text=Visa', alt: 'Visa' },
                { src: 'https://via.placeholder.com/40x25/ffffff/4a5568?text=MC', alt: 'Mastercard' },
                { src: 'https://via.placeholder.com/40x25/ffffff/4a5568?text=Amex', alt: 'Amex' },
                { src: 'https://via.placeholder.com/40x25/ffffff/4a5568?text=bkash', alt: 'bkash' }
            ]
        }
    }
}
</script>