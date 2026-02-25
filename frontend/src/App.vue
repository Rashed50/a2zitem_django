<template>
    <div>
        <div>
            <h1>This is a Vue3 Project with Vite</h1>
        </div>
        <!-- TestComponent-এ প্রপ্স পাঠানো -->
        <TestComponent :title="title" :initial-count="counter" :item-list="items" :is-active="isActive" />
    </div>
</template>

<script setup>
import TestComponent from './components/Test.vue'

// প্রপ্স হিসেবে পাঠানোর ডাটা
const title = "এটি একটি টেস্ট টাইটেল"
const counter = 42
const items = [
    { id: 1, name: "আইটেম ১" },
    { id: 2, name: "আইটেম ২" }
]
const isActive = true
</script>

<style scoped></style>