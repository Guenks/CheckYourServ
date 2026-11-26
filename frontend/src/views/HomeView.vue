<script setup>
import TestApi from "@/components/testApi.vue"
import UserStatus from "@/components/User/UserStatus.vue"
import MyServers from "@/components/MyServers.vue"
import { useAuth } from "@/composables/useAuth.js"

const { loggedIn } = useAuth()
</script>

<template>
  <main class="page">
    <h1>CheckYourServ</h1>
    <UserStatus />
    <MyServers v-if="loggedIn" />
    <TestApi v-else />
  </main>
</template>

<style scoped></style>
