<script setup>
import { useRouter } from "vue-router"
import { ref } from "vue"
import { useAuth } from "@/composables/useAuth.js"

// imported parts
const router = useRouter()
const { setToken } = useAuth()

//vars
const mode = ref("login") // 'login' | 'register'
const username = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

//general function to login/register
async function post(path) {
  //request to backend
  const res = await fetch(`/api/auth/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: username.value.trim(), password: password.value }),
  })

  //get data
  const data = await res.json().catch(() => ({}))
  console.log(data)
  if (!res.ok) {
    //Error details are either just a string or a list of errors
    throw new Error(typeof data.detail === "string" ? data.detail : `Error ${res.status}`)
  }
  return data
}

async function submit() {
  loading.value = true
  error.value = ""

  try {
    //if register, no more check needed, just try to create a user
    if (mode.value === "register") await post("register")
    //login (after register to connect the user if he just create his account)
    const data = await post("login")
    setToken(data.access_token)
    router.push("/")
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="page" style="min-height: 100vh; display: flex; align-items: center">
    <form class="mc-form" style="margin: 0 auto" @submit.prevent="submit">
      <h2>{{ mode === "login" ? "Log in" : "Register" }}</h2>

      <label class="mc-label" for="username">Username</label>
      <input id="username" v-model="username" type="text" required minlength="3" />

      <label class="mc-label" for="password">Password</label>
      <input id="password" v-model="password" type="password" required minlength="6" />

      <div class="mc-gap" />

      <p v-if="error" class="center" style="color: #ff5555">{{ error }}</p>

      <button type="submit" :disabled="loading">
        {{ loading ? "Please wait..." : mode === "login" ? "Log in" : "Create account" }}
      </button>
      <button type="button" @click="mode = mode === 'login' ? 'register' : 'login'">
        {{ mode === "login" ? "Need an account? Register" : "Have an account? Log in" }}
      </button>
      <RouterLink to="/"><button type="button">Cancel</button></RouterLink>
    </form>
  </main>
</template>
