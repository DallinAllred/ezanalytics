<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits('updateApp')

const currentUser = ref(JSON.parse(localStorage.getItem('eza-user')) ?? {})
const showLogin = ref(false)

const activeUser = ref({
  username: 'Test',
  firstName: 'First_Name',
  middleName: 'Middle_Name',
  lastName: 'Last_Name',
  userEmail: 'Email@email.com'
})

const oldPassword = ref()
const newPassword1 = ref()
const newPassword2 = ref()

const submitted = ref(false)
const submittedPassword = ref(false)
</script>

<template>
  <div class="flex justify-content-center w-full">
    <div class="flex flex-column w-8">
      <div class="flex justify-content-start w-full">
        <h2>User Settings for {{ currentUser.username }}</h2>
      </div>
      <div class="flex gap-8">
        <div class="p-fluid w-5">
          <div class="field">
            <label for="username">Username</label>
            <InputText disabled type="text" v-model="activeUser.username" />
          </div>
          <div class="field">
            <label for="firstName">First Name*</label>
            <InputText id="firstName" v-model.trim="activeUser.firstName" required="true" :class="{'p-invalid': submitted && !activeUser.firstName}" />
            <small class="p-error" v-if="submitted && !activeUser.firstName">First name is required</small>
          </div>
          <div class="field">
            <label for="middleName">Middle Name</label>
            <InputText id="middleName" v-model.trim="activeUser.middleName" />
          </div>
          <div class="field">
            <label for="lastName">Last Name*</label>
            <InputText id="lastName" v-model.trim="activeUser.lastName" required="true" :class="{'p-invalid': submitted && !activeUser.lastName}" />
            <small class="p-error" v-if="submitted && !activeUser.lastName">Last name is required</small>
          </div>
          <div class="field">
            <label for="userEmail">Email*</label>
            <InputText id="userEmail" v-model.trim="activeUser.userEmail" required="true" :class="{'p-invalid': submitted && !activeUser.userEmail}" />
            <small class="p-error" v-if="submitted && !activeUser.userEmail">Email is required</small>
          </div>
          <div class="field flex gap-5">
            <Button label="Revert Changes" severity="danger" />
            <Button label="Save Changes" />
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
    <Login v-model="showLogin" title="Session Timed Out" @login="showLogin = false; emit('updateApp')"></Login>
  </div>
</template>
