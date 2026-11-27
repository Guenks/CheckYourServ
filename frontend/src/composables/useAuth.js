import { computed, ref } from "vue"

// Module-level -> used by every component that call useAuth()
const token = ref(localStorage.getItem("token"))

export function useAuth() {
  const loggedIn = computed(() => !!token.value)

  function setToken(val) {
    localStorage.setItem("token", val)
    token.value = val
  }

  function clearToken() {
    localStorage.removeItem("token")
    token.value = null
  }

  return { token, loggedIn, setToken, clearToken }
}
