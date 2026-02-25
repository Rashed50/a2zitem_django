// src/composables/useDelete.js
import { inject } from 'vue'
import axios from '@/plugins/axios'

export const useDelete = () => {
    const swal = inject('swal')
    if (!swal) {
        console.error('SweetAlert2 not provided! Add app.provide("swal", Swal) in main.js')
    }

    const deleteItem = async ({
        url,
        id,
        name = 'this item',
        onSuccess = null,
        customTitle = null,
        customText = null
    }) => {
        if (!swal) {
            alert('SweetAlert2 is missing!')
            return { sucess: false }
        }

        try {
            const result = await swal.fire({
                title: customTitle || 'Are you sure?',
                html: customText || `
               <p>You want to delete <strong>"${name}"</strong>?</p>
               <!-- <p class="text-red-600 mt-2">This action cannot be undone!</p> -->
            `,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel',
                reverseButtons: true,
                // width: '420px',
                // height: 'auto',
                // padding: '1.5rem',
            })

            if (!result.isConfirmed) {
                return { success: false, cancelled: true }
            }

            swal.fire({
                title: 'Deleting...',
                allowOutsideClick: false,
                allowEscapeKey: false,
                // width: '380px',
                didOpen: () => swal.showLoading()
            })

            const response = await axios.delete(`${url}/${id}/`)

            const message = response.data.message || `${name} deleted successfully!`

            if (typeof onSuccess === 'function') {
                await onSuccess()
            }

            swal.fire({
                icon: 'success',
                title: 'Deleted!',
                text: message,
                timer: 2000,
                // width: '380px',
                showConfirmButton: false
            })

            return { success: true, message, data: response.data.results || null }

        } catch (error) {
            console.error('Delete failed:', error)

            let errorMsg = 'Failed to delete the item.'
            if (error.response?.data?.message) errorMsg = error.response.data.message
            else if (error.response?.data?.detail) errorMsg = error.response.data.detail
            else if (error.message) errorMsg = error.message

            swal?.fire({
                icon: 'error',
                title: 'Error!',
                text: errorMsg,
                confirmButtonColor: '#d33'
            })

            return { success: false, message: errorMsg }
        }
    }

    return { deleteItem }
}