<script setup>
import { computed, ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import axios from '@/axiosConfig'

const emit = defineEmits('updateApp')
const toast = useToast()

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

const passwordComplexity = computed(() => {
  if (newPassword1.value.length < 8) return false
  return true
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
      let response = await axios.get(`/api/profile/${currentUser.value['user_id']}`)
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
  submittedPassword.value = true
  if (!(oldPassword.value
    && newPassword1.value == newPassword2.value
    && passwordComplexity.value)) { return }
  let data = {
    oldPassword: oldPassword.value,
    newPassword: newPassword1.value
  }
  try {
    let response = await axios.put(`/api/profile/password/${currentUser.value['user_id']}`, data)
    oldPassword.value = ''
    newPassword1.value = ''
    newPassword2.value = ''
    submittedPassword.value = false
    toast.add({severity: 'success', summary: 'Successful', detail: 'Password Updated', life: 3000})
  } catch (err) {
    console.log('Error updating password')
    if (err.response?.status === 401) {
      showLogin.value = true
    } else {
      toast.add({severity: 'error', summary: 'Error', detail: 'Unable to update password', life: 3000})
    }
  }
}

async function updateUserInfo() {
  if (!changesMade) return
  delete proposedInfo.value.username
  submitted.value = true
  if (!(proposedInfo.value.firstName
        && proposedInfo.value.lastName
        && proposedInfo.value.userEmail)) { return }
  try {
    let response = await axios.put(
      `/api/profile/${currentUser.value['user_id']}`,
      {userId: currentUser.value['user_id'], ...proposedInfo.value}
    )
    Object.assign(accountInfo.value, proposedInfo.value)
    submitted.value = false
    toast.add({severity: 'success', summary: 'Successful', detail: 'Profile Updated', life: 3000})
  } catch (err) {
    if (err.response?.status === 401) {
      showLogin.value = true
    } else {
      toast.add({severity: 'error', summary: 'Successful', detail: 'Unable to update profile', life: 3000})
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
        <h2>User Settings For: <span style="color: var(--primary-color)">{{ currentUser.username }}</span></h2>
      </div>
      <div class="flex gap-8">
        <div class="p-fluid w-5">
          <div class="flex">
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
            <Password toggleMask id="oldPassword" v-model.trim="oldPassword" :class="{'p-invalid': submittedPassword && !oldPassword}" />
          </div>
          <div class="field">
            <label for="newPassword1">New Password</label>
            <Password toggleMask id="newPassword1" v-model.trim="newPassword1" :class="{'p-invalid': submittedPassword && !newPassword1}" />
            <small class="p-error" v-if="newPassword1 != newPassword2">Passwords must match</small>
            <small class="p-error" v-if="submittedPassword && !passwordComplexity">Password must be at least 8 characters</small>
          </div>
          <div class="field">
            <label for="newPassword2">Confirm New Password</label>
            <Password toggleMask id="newPassword2" v-model.trim="newPassword2" :class="{'p-invalid': submittedPassword && !newPassword2}" />
            <small class="p-error" v-if="newPassword1 != newPassword2">Passwords must match</small>
            <small class="p-error" v-if="submittedPassword && !passwordComplexity">Password must be at least 8 characters</small>

          </div>
          <div class="field">
            <Button label="Update Password" :disabled="!oldPassword || !newPassword1 || (newPassword1 != newPassword2)" @click="updatePassword" />
          </div>
        </div>
      </div>
    </div>
    <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false; loadUserInfo(); emit('updateApp')"></Login>
  </div>
</template>
