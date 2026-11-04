<script setup>
import { ref } from 'vue'

const target = ref('')
const result = ref(null)
const error = ref('')
const loading = ref(false)

async function checkServer() {
  const value = target.value.trim()
  if (!value) return

  loading.value = true
  error.value = ''
  result.value = null

  try {
    // encodeURIComponent to protect from ipv6 (with :)
    const res = await fetch(`/api/servers/${encodeURIComponent(value)}`)
    if (!res.ok) throw new Error(`Erreur ${res.status}`)
    result.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section>
    <h2>Check a server</h2>

    <form @submit.prevent="checkServer">
      <input
          v-model="target"
          type="text"
          placeholder="DNS or IP (ex. example.com, 192.168.1.10)"
          required
      />
      <button type="submit" :disabled="loading || !target.trim()">
        {{ loading ? 'Checking...' : 'Check' }}
      </button>
    </form>

    <p v-if="error" style="color: red">{{ error }}</p>
    <pre v-if="result">{{ JSON.stringify(result, null, 2) }}</pre>
  </section>
</template>