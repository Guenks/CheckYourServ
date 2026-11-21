<script>
import { onMounted, ref } from "vue"

const user = ref(null)

async function loadUser() {
  //to get the connected user, we check the token
  const token = localStorage.getItem("token")
  if (!token) return null

  try {
    const res = await fetch("/api/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    })

    if (!res.ok) throw new Error(`Error : ${res.status}`)
    user.value = await res.json()
  } catch {
    //if invalid or expired token -> clean token to show login link
    logout()
  }
}

function logout() {
  localStorage.removeItem("token")
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
