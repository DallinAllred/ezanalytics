<script setup>
import { computed, ref, onMounted } from 'vue'
import axios from '@/axiosConfig'

const emit = defineEmits('updateApp')

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const showLogin = ref(false)
const loginTitle = ref('Session Timed Out')
const accountInfo = ref({
  username: '',
  firstName: '',
  middleName: '',
  lastName: '',
  userEmail: ''
})
const proposedInfo = ref({
  username: '',
  firstName: '',
  middleName: '',
  lastName: '',
  userEmail: ''
})

const oldPassword = ref()
const newPassword1 = ref()
const newPassword2 = ref()

const submitted = ref(false)
const submittedPassword = ref(false)

const changesMade = computed(() => {
  let changes = false
  for (let key in proposedInfo.value) {
    if (key === 'username') continue
    let current = accountInfo.value[key]
    let proposed = proposedInfo.value[key]
    if (current != proposed) {
      changes = true
      break
    }
  }
  return changes
})

async function loadUserInfo() {
  if (!currentUser.value.username) {
        currentUser.value = JSON.parse(localStorage.getItem('eza-user')) ?? {}
        if (!currentUser.value?.username) {
            loginTitle.value = null
            showLogin.value = true
            return
        }
    }
    loginTitle.value = 'Session Timed Out'
    try {
      let response = await axios.get(`/api/users/${currentUser.value['user_id']}`)
      let userData = response.data
      accountInfo.value = {
        username: userData.username,
        firstName: userData.firstName,
        middleName: userData.middleName ?? '',
        lastName: userData.lastName,
        userEmail: userData.userEmail
      }
      Object.assign(proposedInfo.value, accountInfo.value)
    } catch (err) {
      if (err.response?.status === 401) {
        showLogin.value = true
      }
    }
}

function undoPendingChanges() {
  Object.assign(proposedInfo.value, accountInfo.value)
}

async function updatePassword() {

}

async function updateUserInfo() {
  if (!changesMade) return
  delete proposedInfo.value.username
  console.log(proposedInfo.value)
  submitted.value = true
  if (!(proposedInfo.value.firstName
        && proposedInfo.value.lastName
        && proposedInfo.value.userEmail)) { return }
  try {
    let response = await axios.put(
      `/api/users/${currentUser.value['user_id']}`,
      {userId: currentUser.value['user_id'], ...proposedInfo.value}
    )
  } catch (err) {
    if (err.response?.status === 401) {
      showLogin.value = true
    }
  }
}

onMounted(() => {
  loadUserInfo()
})
</script>

<template>
  <div class="flex justify-content-center w-full">
    <div class="flex flex-column w-8">
      <div class="flex justify-content-start w-full">
        <h2>User Settings for {{ currentUser.username }}</h2>
      </div>
      <div class="flex gap-8">
        <div class="p-fluid w-5">
          <div>
            <h3>User Info</h3>
          </div>
          <div class="field">
            <label for="username">Username</label>
            <InputText disabled type="text" v-model="accountInfo.username" />
          </div>
          <div class="field">
            <label for="firstName">First Name*</label>
            <InputText id="firstName" v-model.trim="proposedInfo.firstName" required="true" :class="{'p-invalid': submitted && !proposedInfo.firstName}" />
            <small class="p-error" v-if="submitted && !proposedInfo.firstName">First name is required</small>
          </div>
          <div class="field">
            <label for="middleName">Middle Name</label>
            <InputText id="middleName" v-model.trim="proposedInfo.middleName" />
          </div>
          <div class="field">
            <label for="lastName">Last Name*</label>
            <InputText id="lastName" v-model.trim="proposedInfo.lastName" required="true" :class="{'p-invalid': submitted && !proposedInfo.lastName}" />
            <small class="p-error" v-if="submitted && !proposedInfo.lastName">Last name is required</small>
          </div>
          <div class="field">
            <label for="userEmail">Email*</label>
            <InputText id="userEmail" v-model.trim="proposedInfo.userEmail" required="true" :class="{'p-invalid': submitted && !proposedInfo.userEmail}" />
            <small class="p-error" v-if="submitted && !proposedInfo.userEmail">Email is required</small>
          </div>
          <div class="field flex gap-5">
            <Button label="Reset" severity="danger" :disabled="!changesMade" @click="undoPendingChanges"/>
            <Button label="Save Changes" :disabled="!changesMade" @click="updateUserInfo"/>
          </div>
        </div>
        <div class="p-fluid w-5">
          <div>
            <h3>Change Password</h3>
          </div>
          <div class="field">
            <label for="oldPassword">Old Password</label>
            <InputText id="oldPassword" type="password" v-model.trim="oldPassword" :class="{'p-invalid': submittedPassword && !oldPassword}" />
          </div>
          <div class="field">
            <label for="newPassword1">New Password</label>
            <InputText id="newPassword1" type="password" v-model.trim="newPassword1" :class="{'p-invalid': submittedPassword && !newPassword1}" />
            <small class="p-error" v-if="newPassword1 != newPassword2">Passwords must match</small>
          </div>
          <div class="field">
            <label for="newPassword2">Confirm New Password</label>
            <InputText id="newPassword2" type="password" v-model.trim="newPassword2" :class="{'p-invalid': submittedPassword && !newPassword2}" />
            <small class="p-error" v-if="newPassword1 != newPassword2">Passwords must match</small>
          </div>
          <div class="field">
            <Button label="Update Password" :disabled="!oldPassword || !newPassword1 || (newPassword1 != newPassword2) "/>
          </div>
        </div>
      </div>
    </div>
    <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false; loadUserInfo(); emit('updateApp')"></Login>
  </div>
</template>
