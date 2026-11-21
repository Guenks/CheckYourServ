<script setup>
import TestApi from "@/components/testApi.vue"
</script>

<template>
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
  <RouterLink to="/auth">Log in / Register</RouterLink>
  <TestApi />
</template>

<style scoped></style>
