<template>
  <div id="app" class="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
    <HeaderComponent />
    <main class="flex-grow">
      <HomeComponent/>
    </main>
    <FooterComponent />
  </div>
</template>

<script>
import HeaderComponent from './components/layouts/HeaderComponent.vue'
import FooterComponent from './components/layouts/FooterComponent.vue'
import HomeComponent from './components/HomeComponent.vue'

export default {
  name: 'App',
  components: {
    HeaderComponent,
    FooterComponent,
    HomeComponent,
  }
}
</script>