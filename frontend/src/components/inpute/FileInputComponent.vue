<template>
  <div class="w-full">
    <!-- Label -->
    <label v-if="label" :for="computedId" class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-200">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1" aria-hidden="true">*</span>
      <span v-if="helpText" class="text-purple-500 text-xs">({{ helpText }})</span>
    </label>

    <div class="space-y-3">
      <!-- Current Image/File -->
      <div v-if="showCurrentFile"
        class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-100 dark:border-gray-800">
        <div class="overflow-hidden border border-gray-200 dark:border-gray-700 rounded-lg flex-shrink-0">
          <img v-if="isCurrentImage" :src="currentImageUrl" alt="current" class="w-12 h-12 object-cover" />
          <div v-else class="w-12 h-12 flex items-center justify-center bg-blue-100 dark:bg-blue-900/30">
            <i class="fa-solid fa-file text-blue-500 text-lg"></i>
          </div>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-xs font-semibold text-gray-700 dark:text-gray-300">Current File</p>
          <p class="text-xs text-gray-400 truncate">{{ currentFileName }}</p>
          <a v-if="currentImageUrl" :href="currentImageUrl" target="_blank"
            class="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 flex items-center gap-1 mt-1">
            <i class="fa-solid fa-external-link-alt"></i>
            View File
          </a>
        </div>
      </div>

      <!-- Preview Container -->
      <div v-if="previewUrl" class="relative rounded-xl overflow-hidden border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
        
        <!-- Image Preview -->
        <div v-if="isImageFile" class="flex items-center justify-center bg-gray-100 dark:bg-gray-800 py-6">
          <img :src="previewUrl" alt="preview"
            class="max-w-full max-h-64 rounded-lg border-4 border-white dark:border-gray-900 object-contain shadow-md" />
        </div>

        <!-- PDF Preview -->
        <div v-else-if="isPdfFile">
          <div class="p-4">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-file-pdf text-red-500"></i>
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">PDF Preview</span>
              </div>
              <button v-if="!disabled" @click="removePreview" type="button" class="text-red-500 hover:text-red-700">
                <i class="fa-solid fa-times"></i>
              </button>
            </div>
            <iframe :src="previewUrl" class="w-full h-96" frameborder="0" title="PDF Preview"></iframe>
          </div>
        </div>

        <!-- Office Documents Preview (docx, xlsx etc) using Microsoft Viewer -->
        <div v-else-if="isOfficeFile">
          <div class="p-4">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <i :class="fileIconClass" class="text-xl"></i>
                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Document Preview</span>
              </div>
              <button v-if="!disabled" @click="removePreview" type="button" class="text-red-500 hover:text-red-700">
                <i class="fa-solid fa-times"></i>
              </button>
            </div>
            <iframe :src="officeViewerUrl" class="w-full h-96" frameborder="0" title="Office Document Preview"></iframe>
          </div>
        </div>

        <!-- Generic File Info + Download -->
        <div v-else class="p-6">
          <div class="flex flex-col items-center text-center">
            <i :class="fileIconClass" class="text-6xl mb-4 text-gray-400"></i>
            <p class="text-lg font-medium text-gray-800 dark:text-gray-200 mb-1">{{ fileName }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ formatFileSize(fileSize) }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">Preview not available for this file type</p>
            <a :href="previewUrl" download
              class="inline-flex items-center px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
              <i class="fa-solid fa-download mr-2"></i>
              Download File
            </a>
          </div>
        </div>

        <!-- File Info Bar -->
        <div class="flex items-center justify-between px-4 py-2.5 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700">
          <div class="flex items-center gap-3 min-w-0">
            <i :class="fileIconClass"></i>
            <span class="text-xs font-medium text-gray-600 dark:text-gray-300 truncate">{{ fileName }}</span>
            <span class="text-xs text-gray-400">{{ formatFileSize(fileSize) }}</span>
          </div>
          <button v-if="!disabled" @click="removePreview" type="button"
            class="w-8 h-8 rounded-full hover:bg-red-50 dark:hover:bg-red-900/30 flex items-center justify-center transition-colors group">
            <i class="fa-solid fa-trash text-sm text-gray-400 group-hover:text-red-500"></i>
          </button>
        </div>
      </div>

      <!-- Upload Area - shown when no preview -->
      <div v-if="!previewUrl" class="space-y-3">
        <div :class="[
          'border-2 border-dashed rounded-xl transition-colors duration-200 cursor-pointer',
          isDragging ? 'border-indigo-600 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-700',
          disabled ? 'opacity-60 pointer-events-none bg-gray-100 dark:bg-gray-800' : 'hover:border-indigo-600 dark:hover:border-gray-100',
        ]" @dragover.prevent="handleDragOver" @dragleave.prevent="handleDragLeave" @drop.prevent="handleDrop"
          @click="triggerFileInput">
          <div class="text-center p-8">
            <div class="w-16 h-16 rounded-2xl bg-gray-100 dark:bg-gray-800 flex items-center justify-center mx-auto mb-4">
              <i class="fa-solid fa-cloud-arrow-up text-2xl text-gray-400"></i>
            </div>
            <p class="text-base font-medium text-gray-700 dark:text-gray-300 mb-2">
              Drag & drop or click to upload
            </p>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ acceptDescription }}
              <span v-if="maxSize"> • Max {{ formatFileSize(maxSize) }}</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Multiple Files List -->
      <div v-if="multiple && selectedFiles.length > 0" class="space-y-2">
        <div v-for="(file, index) in selectedFiles" :key="index"
          class="flex items-center justify-between p-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800">
          <div class="flex items-center gap-3">
            <i class="fa-solid text-xl" :class="getFileIcon(file)"></i>
            <div>
              <p class="text-sm font-medium truncate max-w-xs">{{ file.name }}</p>
              <p class="text-xs text-gray-500">{{ formatFileSize(file.size) }}</p>
            </div>
          </div>
          <button v-if="!disabled" @click="removeFileAtIndex(index)" type="button"
            class="text-red-500 hover:text-red-700 p-1">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
      </div>

      <!-- Error -->
      <p v-if="error" class="mt-2 text-sm text-red-600 dark:text-red-400">
        <i class="fa-solid fa-circle-exclamation mr-1"></i> {{ error }}
      </p>
    </div>

    <input :id="computedId" :name="name" type="file" :accept="acceptString" :multiple="multiple" :disabled="disabled"
      :required="required && !previewUrl" @change="handleFileChange" ref="fileInput" class="hidden" />
  </div>
</template>

<script>
export default {
  name: 'FileInputComponent',

  props: {
    label: { type: String, default: '' },
    name: { type: String, default: '' },
    id: { type: String, default: '' },
    error: { type: [String, Boolean], default: '' },
    helpText: { type: String, default: '' },
    disabled: { type: Boolean, default: false },
    required: { type: Boolean, default: false },

    modelValue: { type: [File, Array, String], default: null },
    accept: { type: Array, default: () => ['image/*'] },
    multiple: { type: Boolean, default: false },
    maxSize: { type: Number, default: 5 * 1024 * 1024 },
    maxFiles: { type: Number, default: 10 },

    currentImageUrl: { type: String, default: '' },
    showPdfPreview: { type: Boolean, default: true },
  },

  emits: ['update:modelValue', 'change', 'error', 'file-added', 'file-removed'],

  data() {
    return {
      selectedFiles: [],
      previewUrl: null,
      fileName: '',
      fileSize: 0,
      fileType: '',
      isDragging: false,
      blobUrl: null,
    }
  },

  computed: {
    computedId() {
      return this.id || this.name || `file-input-${Math.random().toString(36).slice(2, 10)}`
    },

    acceptString() {
      return this.accept.join(',')
    },

    acceptDescription() {
      if (this.accept.includes('image/*')) return 'Images (JPG, PNG, WEBP, GIF)'
      if (this.accept.includes('application/pdf')) return 'PDF documents'
      return this.accept.map(a => a.replace('.', '').toUpperCase()).join(', ')
    },

    isImageFile() {
      return this.fileType?.startsWith('image/')
    },

    isPdfFile() {
      return this.fileType === 'application/pdf' || this.fileName?.toLowerCase().endsWith('.pdf')
    },

    isOfficeFile() {
      const ext = this.fileName?.toLowerCase().split('.').pop()
      return ['doc', 'docx', 'xls', 'xlsx'].includes(ext)
    },

    fileIconClass() {
      const ext = this.fileName?.toLowerCase().split('.').pop()
      if (this.isImageFile) return 'fa-file-image text-blue-500'
      if (this.isPdfFile) return 'fa-file-pdf text-red-500'
      if (['doc', 'docx'].includes(ext)) return 'fa-file-word text-blue-600'
      if (['xls', 'xlsx'].includes(ext)) return 'fa-file-excel text-green-600'
      return 'fa-file text-gray-500'
    },

    officeViewerUrl() {
      if (!this.previewUrl || !this.isOfficeFile) return ''
      // Microsoft Office Online Viewer
      return `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(this.previewUrl)}`
    },

    showCurrentFile() {
      return this.currentImageUrl && !this.previewUrl && this.selectedFiles.length === 0
    },

    isCurrentImage() {
      const url = this.currentImageUrl?.toLowerCase() || ''
      return /\.(jpg|jpeg|png|gif|webp)$/i.test(url)
    },

    currentFileName() {
      return this.currentImageUrl?.split('/').pop() || 'Current File'
    },
  },

  watch: {
    modelValue: {
      immediate: true,
      handler(newVal) {
        if (!newVal) {
          this.clearSelection()
          return
        }

        if (newVal instanceof File) {
          this.selectedFiles = [newVal]
          this.generatePreview(newVal)
        } else if (Array.isArray(newVal) && newVal.length > 0) {
          this.selectedFiles = newVal
          this.generatePreview(newVal[0])
        } else if (typeof newVal === 'string' && newVal) {
          this.previewUrl = newVal
          this.fileName = newVal.split('/').pop() || 'Current File'
          this.fileSize = 0 // unknown
        }
      },
    },
  },

  methods: {
    triggerFileInput() {
      if (!this.disabled) this.$refs.fileInput.click()
    },

    handleFileChange(e) {
      const files = Array.from(e.target.files || [])
      if (files.length) this.processFiles(files)
      e.target.value = ''
    },

    handleDragOver(e) {
      if (this.disabled) return
      e.preventDefault()
      this.isDragging = true
    },

    handleDragLeave() {
      this.isDragging = false
    },

    handleDrop(e) {
      if (this.disabled) return
      e.preventDefault()
      this.isDragging = false
      const files = Array.from(e.dataTransfer.files || [])
      if (files.length) this.processFiles(files)
    },

    processFiles(files) {
      if (this.multiple && this.selectedFiles.length + files.length > this.maxFiles) {
        this.$emit('error', `Maximum ${this.maxFiles} files allowed`)
        return
      }

      const validFiles = files.filter(file => {
        if (file.size > this.maxSize) {
          this.$emit('error', `File too large (max ${this.formatFileSize(this.maxSize)})`)
          return false
        }
        return true
      })

      if (!validFiles.length) return

      if (this.multiple) {
        this.selectedFiles.push(...validFiles)
      } else {
        this.selectedFiles = [validFiles[0]]
      }

      this.generatePreview(this.selectedFiles[0])

      const value = this.multiple ? this.selectedFiles : this.selectedFiles[0]
      this.$emit('update:modelValue', value)
      this.$emit('change', value)
    },

    generatePreview(file) {
      if (!file) return

      this.fileName = file.name
      this.fileSize = file.size
      this.fileType = file.type

      // Clean up old blob URL
      if (this.blobUrl) {
        URL.revokeObjectURL(this.blobUrl)
      }

      this.blobUrl = URL.createObjectURL(file)
      this.previewUrl = this.blobUrl
    },

    removePreview() {
      this.clearSelection()
    },

    removeFileAtIndex(index) {
      this.selectedFiles.splice(index, 1)
      if (this.selectedFiles.length === 0) {
        this.clearSelection()
      } else {
        this.generatePreview(this.selectedFiles[0])
      }
      this.$emit('update:modelValue', this.multiple ? this.selectedFiles : null)
    },

    clearSelection() {
      if (this.blobUrl) {
        URL.revokeObjectURL(this.blobUrl)
        this.blobUrl = null
      }
      this.previewUrl = null
      this.selectedFiles = []
      this.fileName = ''
      this.fileSize = 0
      this.fileType = ''
      this.$emit('update:modelValue', this.multiple ? [] : null)
    },

    formatFileSize(bytes) {
      if (!bytes) return '—'
      const units = ['B', 'KB', 'MB', 'GB']
      let size = bytes
      let unitIndex = 0
      while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024
        unitIndex++
      }
      return `${size.toFixed(1)} ${units[unitIndex]}`
    },

    getFileIcon(file) {
      const ext = file.name.split('.').pop()?.toLowerCase()
      if (file.type.startsWith('image/')) return 'fa-file-image text-blue-500'
      if (file.type === 'application/pdf' || ext === 'pdf') return 'fa-file-pdf text-red-500'
      if (['doc', 'docx'].includes(ext)) return 'fa-file-word text-blue-600'
      if (['xls', 'xlsx'].includes(ext)) return 'fa-file-excel text-green-600'
      return 'fa-file text-gray-500'
    },
  },

  beforeUnmount() {
    if (this.blobUrl) {
      URL.revokeObjectURL(this.blobUrl)
    }
  },
}
</script>



<!-- 
================= FileInputComponent ব্যবহারের উদাহরণ =============
১. Single Image Upload (Company Logo) -------------------------

## Company Logo
<FileInputComponent
        label="Company Logo"
        v-model="formData.logo"
        :current-image-url="editingCompany?.logo_url"
        :error="formErrors.logo"
        :accept="['image/*']"
        help-text="Square logo works best (1:1 ratio)"
        :max-size="2 * 1024 * 1024"
        :required="!editingCompany"
      />

## Profile Picture
<FileInputComponent
        label="Profile Picture"
        v-model="formData.profile_pic"
        :current-image-url="userData?.profile_pic_url"
        :error="formErrors.profile_pic"
        :accept="['image/*']"
        help-text="Upload your profile picture"
        :max-size="1 * 1024 * 1024"
      />

২. Multiple Images Upload (Product Gallery) ----------------

## Product Gallery
<FileInputComponent
      label="Product Images"
      v-model="formData.gallery"
      :error="formErrors.gallery"
      :accept="['image/*']"
      :multiple="true"
      :max-files="5"
      help-text="Upload up to 5 product images"
      :max-size="5 * 1024 * 1024"
    />

    ## Product Documents 
    <FileInputComponent
      label="Product Documents"
      v-model="formData.documents"
      :error="formErrors.documents"
      :accept="['.pdf', '.doc', '.docx', '.xls', '.xlsx']"
      :multiple="true"
      :max-files="10"
      help-text="Upload product specifications, manuals, etc."
      :max-size="10 * 1024 * 1024"
    />

৩. Single File Upload (PDF/Document) ------------------------
## Single PDF Upload
    <FileInputComponent
      label="Resume/CV"
      v-model="formData.resume"
      :error="formErrors.resume"
      :accept="['application/pdf']"
      help-text="Upload your resume in PDF format"
      :max-size="5 * 1024 * 1024"
      required
    />

## Contract Document 
    <FileInputComponent
      label="Contract Document"
      v-model="formData.contract"
      :current-image-url="contractData?.file_url"
      :error="formErrors.contract"
      :accept="['.pdf', '.doc', '.docx']"
      help-text="Upload contract document"
      :max-size="10 * 1024 * 1024"
    />


  ৪. Mixed File Types ------------------------------- 
   ## Any File Type 
    <FileInputComponent
      label="Any File"
      v-model="formData.any_file"
      :error="formErrors.any_file"
      help-text="Upload any type of file"
      :max-size="10 * 1024 * 1024"
    />

    ## Image or PDF
    <FileInputComponent
      label="Image or PDF"
      v-model="formData.image_or_pdf"
      :error="formErrors.image_or_pdf"
      :accept="['image/*', 'application/pdf']"
      help-text="Upload image or PDF document"
      :max-size="5 * 1024 * 1024"
    />

    ## Specific Extensions
    <FileInputComponent
      label="Office Documents"
      v-model="formData.office_docs"
      :error="formErrors.office_docs"
      :accept="['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']"
      help-text="Upload Word, Excel, PowerPoint files"
      :max-size="20 * 1024 * 1024"
    />
-->
