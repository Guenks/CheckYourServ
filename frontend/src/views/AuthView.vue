<script setup>
import { useRouter } from "vue-router"
import { ref } from "vue"

const router = useRouter()

//vars
const mode = ref("login") // 'login' | 'register'
const username = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)
</script>

<template>
  <section>
    <h2>{{ mode === "login" ? "Log in" : "Register" }}</h2>
    <div>
      <button type="button" :disabled="mode === 'login'" @click="mode = 'login'">Log in</button>
      <button type="button" :disabled="mode === 'register'" @click="mode = 'register'">
        Register
      </button>
    </div>

    <form @submit.prevent="submit">
      <input v-model="username" type="text" placeholder="Username" required minlength="6" />
      <input v-model="password" type="password" placeholder="Password" required minlength="6" />
      <button type="submit" :disabled="loading">
        {{ loading ? "Please wait..." : mode === "login" ? "Log in" : "Create account" }}
      </button>
    </form>

    <p v-if="error" style="color: red">{{ error }}</p>
    <RouterLink to="/">Back</RouterLink>
  </section>
</template>
