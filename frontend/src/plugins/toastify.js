import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

// Default configuration
const defaultOptions = {
    autoClose: 3000,
    position: 'top-right',
    theme: 'light',
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
};

// Custom toast functions with default options
const customToast = {
    success: (message, options = {}) => {
        return toast.success(message, { ...defaultOptions, ...options });
    },
    error: (message, options = {}) => {
        return toast.error(message, { ...defaultOptions, ...options });
    },
    info: (message, options = {}) => {
        return toast.info(message, { ...defaultOptions, ...options });
    },
    warning: (message, options = {}) => {
        return toast.warning(message, { ...defaultOptions, ...options });
    },
    // Original toast function (if needed)
    default: (message, options = {}) => {
        return toast(message, { ...defaultOptions, ...options });
    },
    // You can also expose the original toast if needed
    original: toast,
    // Method to update default options if needed
    updateDefaultOptions: (newOptions) => {
        Object.assign(defaultOptions, newOptions);
    }
};

const ToastifyPlugin = {
    install(app) {
        // Global property হিসেবে add করুন
        app.config.globalProperties.$toast = customToast;

        // Composition API এর জন্য provide করুন
        app.provide('toast', customToast);

        // Remove this line - it's causing the error
        // toast.setDefaultOptions(defaultOptions);
    }
};

export { customToast as toast, ToastifyPlugin, defaultOptions };



/*
#! 👉  Composition API:
<script setup>
import { inject } from 'vue';

const toast = inject('toast');

const showToast = () => {
  toast.success('Success message!'); // Default options ব্যবহার করবে
  // বা
  toast.error('Error!', { autoClose: 5000 }); // Custom options সহ
};
</script>


#! 👉  Options API:
<script>
export default {
  methods: {
    showToast() {
      this.$toast.info('Info message!');
      // বা
      this.$toast.warning('Warning!', { position: 'bottom-left' });
    }
  }
}
</script>
*/