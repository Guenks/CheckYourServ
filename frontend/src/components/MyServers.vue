<script setup>
import { onMounted, reactive, ref } from "vue"
import DOMPurify from "dompurify"
import { useAuth } from "@/composables/useAuth.js"

//imported
const { token, clearToken, loggedIn } = useAuth()

//vars
const servers = ref([])
const statuses = reactive({}) // id server -> status JSON or error
const updating = ref(false)

//form
const showForm = ref(false)
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
  try {
    statuses[id] = await api(`/${id}/status`)
  } catch (e) {
    statuses[id] = { error: e.message }
  }
}

async function updateAll() {
  updating.value = true
  await Promise.all(servers.value.map((s) => checkServer(s.id)))
  updating.value = false
}

// helper for the template

function state(id) {
  const st = statuses[id]
  if (!st) return "pending"
  return st.online && !st.error ? "online" : "offline"
}

function iconOf(id) {
  const icon = statuses[id]?.icon
  //only accept PNG or data URI (Bedrock servers have no icon)
  return typeof icon === "string" && icon.startsWith("data:image/png;base64,")
}

function motdLines(id) {
  const lines = statuses[id]?.motd?.html ?? []
  return lines.map((line) =>
    //check and clean motd since they're in html
    DOMPurify.sanitize(line, {
      ALLOWED_TAGS: ["span", "b", "i", "u", "s", "em", "strong"],
      ALLOWED_ATTR: ["style"],
    }),
  )
}

onMounted(() => {
  if (loggedIn) loadServers()
})
</script>

<template>
  <section>
    <h2>Play Multiplayer</h2>

    <div class="list">
      <p v-if="!servers.length" class="gray center">No server saved yet.</p>

      <div v-for="s in servers" :key="s.id" class="row">
        <img v-if="iconOf(s.id)" class="icon" :src="iconOf(s.id)" alt="" />
        <div v-else class="icon fallback">?</div>

        <div class="info">
          <div>{{ s.name }}</div>

          <template v-if="state(s.id) === 'online'">
            <div v-for="(line, i) in motdLines(s.id)" :key="i" class="motd" v-html="line" />
          </template>

          <template v-else-if="state(s.id) === 'offline'">
            <div class="red">{{ statuses[s.id].error || "Can't reach server" }}</div>
            <div class="dark">{{ s.address }}</div>
          </template>

          <div v-else class="gray">Pinging...</div>
        </div>

        <div class="side">
          <template v-if="state(s.id) === 'offline'">
            <span class="red">✕</span>
          </template>
          <template v-else>
            <span v-if="state(s.id) === 'online'" class="players">
              {{ statuses[s.id].players?.online ?? 0 }}<span class="dark">/</span
              >{{ statuses[s.id].players?.max ?? 0 }}
            </span>
            <span class="bars" :class="state(s.id)"><i /><i /><i /><i /><i /></span>
          </template>
          <button type="button" class="small" @click="removeServer(s.id)">Delete</button>
        </div>
      </div>
    </div>

    <p v-if="error" class="red center">{{ error }}</p>

    <form v-if="showForm" class="form" @submit.prevent="addServer">
      <input v-model="name" type="text" placeholder="Server name" required maxlength="50" />
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
      <button type="submit" :disabled="!name.trim() || !address.trim()">Done</button>
    </form>

    <div class="bar">
      <button type="button" @click="showForm = !showForm">
        {{ showForm ? "Cancel" : "Add server" }}
      </button>
      <button type="button" :disabled="updating || !servers.length" @click="updateAll">
        {{ updating ? "Updating..." : "Update status" }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.list {
  min-height: 220px;
  max-height: 60vh;
  overflow-y: auto;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.65);
  border-top: 2px solid #000;
  border-bottom: 2px solid #000;
  box-shadow: inset 0 4px 6px rgba(0, 0, 0, 0.5);
}

.row {
  display: grid;
  grid-template-columns: 64px 1fr auto;
  gap: 10px;
  padding: 4px;
  line-height: 1.05;
  border: 2px solid transparent;
}

.row:hover {
  border-color: #8b8b8b;
}

.icon {
  width: 64px;
  height: 64px;
  image-rendering: pixelated;
}

.fallback {
  display: grid;
  place-items: center;
  font-size: 40px;
  color: #777;
  background: #3a3a3a;
}

.info {
  min-width: 0; /* lets long MOTDs be truncated instead of stretching the row */
}

.motd {
  white-space: pre;
  overflow: hidden;
  text-overflow: ellipsis;
}

.side {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.players {
  color: #aaa;
}

.gray {
  color: #aaa;
}
.dark {
  color: #6b6b6b;
}
.red {
  color: #ff5555;
}
.center {
  text-align: center;
}

.bars {
  display: inline-flex;
  align-items: flex-end;
  gap: 1px;
  height: 14px;
}
.bars i {
  width: 3px;
  background: #555;
}
.bars i:nth-child(1) {
  height: 3px;
}
.bars i:nth-child(2) {
  height: 6px;
}
.bars i:nth-child(3) {
  height: 9px;
}
.bars i:nth-child(4) {
  height: 12px;
}
.bars i:nth-child(5) {
  height: 14px;
}
.bars.online i {
  background: #55ff55;
}

.small {
  min-width: 0;
  padding: 0 0.5rem;
  font-size: 18px;
}

.form {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.65);
}
.form input {
  flex: 1 1 200px;
}

.bar {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
}
</style>
