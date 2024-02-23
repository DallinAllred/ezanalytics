<script setup>
const model = defineModel()
const emits = defineEmits(['delete', 'cancel'])
const props = defineProps(['match'])

</script>

<template>
    <Dialog v-model:visible="model" :style="{width: '450px'}" header="Confirm Delete">
        <div>

        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="model = false" />
            <Button label="Yes" icon="pi pi-check" text @click="deleteUser" />
        </template>
    </Dialog>

</template>

<style>
</style>