<script setup>
import { computed } from "vue"
import { motdLines } from "@/utils/motd.js"
import { iconOf } from "@/utils/icon.js"

const props = defineProps({
  status: { type: Object, default: null },
  showMotd: { type: Boolean, default: true },
})

const online = computed(() => !!props.status?.online && !props.status?.error)
const lines = computed(() => motdLines(props.status))
const players = computed(() => props.status?.players)

const address = computed(() => {
  const s = props.status
  const host = s?.hostname || s?.ip
  return host ?? null
})
</script>
<template>
  <div v-if="status" class="details">
    <p v-if="status.error" class="red">{{ status.error }}</p>

    <template v-else>
      <p class="state" :class="online ? 'green' : 'red'">
        {{ online ? "🟢 Online" : "🔴 Offline" }}
      </p>

      <template v-if="online">
        <div v-if="showMotd && lines.length" class="motd-box">
          <img v-if="iconOf(status)" class="icon" :src="iconOf(status)" alt="" />
          <div v-else class="icon fallback">?</div>
          <div v-for="(line, i) in lines" :key="i" class="motd" v-html="line" />
        </div>

        <dl>
          <dt>Version</dt>
          <dd>{{ status.version ?? "Unknown" }}</dd>

          <dt>Players</dt>
          <dd>{{ players?.online ?? 0 }}<span class="dark">/</span>{{ players?.max ?? 0 }}</dd>

          <template v-if="status.software">
            <dt>Software</dt>
            <dd>{{ status.software }}</dd>
          </template>

          <template v-if="status.gamemode /*only for bedrock server*/">
            <dt>Gamemode</dt>
            <dd>{{ status.gamemode }}</dd>
          </template>

          <template v-if="address">
            <dt>Address</dt>
            <dd>{{ address }}</dd>
          </template>
        </dl>
      </template>
    </template>
  </div>
</template>

<style scoped>
.details {
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
  padding: 0.5rem 0.75rem;
  text-align: left;
  background: rgba(0, 0, 0, 0.5);
  border: 2px solid #000;
}

.state {
  margin: 0 0 0.4rem;
}

.motd-box {
  margin-bottom: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: #000;
}

.motd {
  white-space: pre;
  overflow: hidden;
  text-overflow: ellipsis;
}

dl {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 0.15rem 1rem;
  margin: 0;
}

dt {
  color: #aaa;
}

dd {
  margin: 0;
  overflow-wrap: anywhere;
}

p {
  margin: 0;
}
.green {
  color: #55ff55;
}
.red {
  color: #ff5555;
}
.dark {
  color: #6b6b6b;
}
</style>
