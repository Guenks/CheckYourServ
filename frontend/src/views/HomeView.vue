<script setup>
import TestApi from "@/components/testApi.vue"
import UserStatus from "@/components/User/UserStatus.vue"
import MyServers from "@/components/MyServers.vue"
</script>

<template>
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
  <UserStatus />
  <MyServers />
  <TestApi />
</template>

<style scoped></style>
