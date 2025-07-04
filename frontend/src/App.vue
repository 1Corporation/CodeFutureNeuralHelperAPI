<template>
  <div class="app-container">
    <router-view />
  </div>
</template>

<script setup>
// Корневой компонент приложения
</script>

<style>
/* Глобальные стили */
body {
  margin: 0;
  padding: 0;
  font-family: 'Roboto', Arial, sans-serif;
  background-color: #fffbf2;
  color: #333333;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  height: 100vh;
}
</style>
