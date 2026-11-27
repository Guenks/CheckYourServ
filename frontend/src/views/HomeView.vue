<script setup>
import DirectCheck from "@/components/DirectCheck.vue"
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
    <DirectCheck v-else />
  </main>
</template>

<style scoped></style>
