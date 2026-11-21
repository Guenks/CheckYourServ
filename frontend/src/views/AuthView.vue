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
    localStorage.setItem("token", data.access_token)
    router.push("/")
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
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
