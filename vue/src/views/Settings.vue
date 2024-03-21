<script setup>
import { ref } from 'vue'

const emit = defineEmits('updateApp')

const showLogin = ref(false)
</script>

<template>
  <div>
    <div>
      <div>
        Username - not editable
      </div>
      <div>First Name</div>
      <div>Middle Name</div>
      <div>Last Name</div>
      <div>
        Email
      </div>
      <div>
        Old Password
      </div>
      <div>New Password</div>
      <div>Confirm New Password</div>
      <div>Cancel (revert) Button || Save Button (Only enabled if details change)</div>
    </div>
    <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false; emit('updateApp')"></Login>
  </div>
</template>
