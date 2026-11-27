<script setup>
import { ref } from "vue"
import ServerDetails from "@/components/ServerDetails.vue"

const address = ref("")
const edition = ref("java")
const result = ref(null)
const error = ref("")
const loading = ref(false)

//var if opened by MyServers.vue
const emit = defineEmits(["close"])

async function checkServer() {
  const value = address.value.trim()
  if (!value) return

  loading.value = true
  error.value = ""
  result.value = null

  try {
    // encodeURIComponent to protect from ipv6 (with :)
    const res = await fetch(`/api/servers/${encodeURIComponent(value)}?edition=${edition.value}`)
    if (!res.ok) throw new Error(`Error ${res.status}`)
    result.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function toggleEdition() {
  edition.value = edition.value === "java" ? "bedrock" : "java"
}

function resetForm() {
  address.value = ""
  //We don't reset edition, only the text input
  result.value = null
  error.value = ""
}

function cancel() {
  resetForm()
  emit("close") //only do something if another component is listening
}
</script>

<template>
  <section>
    <form class="mc-form" style="margin: 2rem auto 0" @submit.prevent="checkServer">
      <h2>Direct Check</h2>

      <label class="mc-label" for="target">Server Address</label>
      <input
        id="address"
        v-model="address"
        type="text"
        placeholder="example.com or 192.168.1.10"
        required
      />

      <button type="button" @click="toggleEdition">
        Edition: {{ edition === "java" ? "Java" : "Bedrock" }}
      </button>

      <div class="mc-gap" />

      <button type="submit" :disabled="loading || !address.trim()">
        {{ loading ? "Checking..." : "Check Server" }}
      </button>
      <button type="button" @click="cancel">Cancel</button>

      <p v-if="error" style="color: #ff5555; text-align: center">{{ error }}</p>
      <ServerDetails v-if="result" :status="result" />
    </form>
  </section>
</template>
