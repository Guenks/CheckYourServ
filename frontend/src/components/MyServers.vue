<script setup>
import { onMounted, reactive, ref } from "vue"
import { useAuth } from "@/composables/useAuth.js"

//imported
const { token, clearToken, loggedIn } = useAuth()

//vars
const servers = ref({})
const statuses = reactive({}) // id server -> status JSON or error
const checking = reactive({}) // id server -> true while loading

//form
const name = ref("")
const address = ref("")
const edition = ref("java")
const error = ref("")

async function api(path, options = {}) {
  const res = await fetch(`/api/my-servers${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token.value}`,
    },
  })
  if (res.status === 204) return null
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(typeof data.detail === "string" ? data.detail : `Error ${res.status}`)
  }
  return data
}

async function loadServers() {
  try {
    servers.value = await api("")
  } catch (e) {
    error.value = e.message
  }
}

async function addServer() {
  error.value = ""
  try {
    //add server to list in backend
    const create = await api("", {
      method: "POST",
      body: JSON.stringify({
        name: name.value.trim(),
        address: address.value.trim(),
        edition: edition.value,
      }),
    })
    //add server in front-end list
    servers.value.push(create)
    //reset form
    name.value = ""
    address.value = ""
  } catch (e) {
    error.value = e.message
  }
}

async function removeServer(id) {
  error.value = ""
  try {
    //delete backend
    await api(`/${id}`, { method: "DELETE" })
    //delete in frontend
    servers.value = servers.value.filter((s) => s.id !== id)
    delete statuses[id]
  } catch (e) {
    error.value = e.message
  }
}

async function checkServer(id) {
  checking[id] = true
  try {
    statuses[id] = await api(`/${id}/status`)
  } catch (e) {
    statuses[id] = { error: e.message }
  } finally {
    checking[id] = false
  }
}

onMounted(() => {
  if (loggedIn) loadServers()
})
</script>

<template>
  <section v-if="loggedIn">
    <h2>My servers</h2>

    <form @submit.prevent="addServer">
      <input v-model="name" type="text" placeholder="Name" required maxlength="50" />
      <input
        v-model="address"
        type="text"
        placeholder="DNS or IP (ex. example.com:25565)"
        required
      />
      <select v-model="edition">
        <option value="java">Java</option>
        <option value="bedrock">Bedrock</option>
      </select>
      <button type="submit" :disabled="!name.trim() || !address.trim()">Add</button>
    </form>

    <p v-if="error" style="color: red">{{ error }}</p>
    <p v-if="!servers.length">No server saved yet.</p>

    <ul>
      <li v-for="s in servers" :key="s.id">
        <strong>{{ s.name }}</strong> — {{ s.address }} ({{ s.edition }})
        <button type="button" :disabled="checking[s.id]" @click="checkServer(s.id)">
          {{ checking[s.id] ? "Checking..." : "Check" }}
        </button>
        <button type="button" @click="removeServer(s.id)">Delete</button>

        <div v-if="statuses[s.id]">
          <span v-if="statuses[s.id].error" style="color: red">{{ statuses[s.id].error }}</span>
          <span v-else-if="statuses[s.id].online">
            🟢 Online — {{ statuses[s.id].players?.online }}/{{ statuses[s.id].players?.max }}
            players
            <span v-if="statuses[s.id].motd"> — {{ statuses[s.id].motd.clean?.join(" ") }}</span>
          </span>
          <span v-else>🔴 Offline</span>
        </div>
      </li>
    </ul>
  </section>
</template>
