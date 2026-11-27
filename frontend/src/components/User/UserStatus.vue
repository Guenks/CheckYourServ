<script setup>
import { onMounted, ref } from "vue"
import { useAuth } from "@/composables/useAuth.js"

//imported
const { token, clearToken } = useAuth()

//vars
const user = ref(null)

async function loadUser() {
  //to get the connected user, we check the token
  if (!token.value) return null

  try {
    const res = await fetch("/api/auth/me", {
      headers: { Authorization: `Bearer ${token.value}` },
    })

    if (!res.ok) throw new Error(`Error : ${res.status}`)
    user.value = await res.json()
  } catch {
    //if invalid or expired token -> clean token to show login link
    logout()
  }
}

function logout() {
  clearToken()
  user.value = null
}

//trigger when component is loaded
onMounted(loadUser)
</script>

<template>
  <div v-if="user">
    <p>
      Logged in as <strong>{{ user.username }}</strong>
    </p>
    <button type="button" @click="logout">Log out</button>
  </div>
  <RouterLink v-else to="/auth">Log in / Register</RouterLink>
</template>
