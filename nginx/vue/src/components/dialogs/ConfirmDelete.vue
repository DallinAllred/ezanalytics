<script setup>
import { computed, ref } from 'vue'
const emit = defineEmits(['delete'])
const model = defineModel()
const props = defineProps(['match'])

const matchText = ref()
const disableDelete = computed(() => {
    if (props.match) {
        return !(matchText.value == props.match)
    }
    return false
})
</script>

<template>
    <Dialog v-model:visible="model" :style="{width: '450px'}" header="Confirm Delete" :modal="true" @after-hide="matchText = ''">
        <div class="flex flex-column gap-5">
            <div>
                <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                <span>This action is permanent. Are you sure you wish to continue?</span>
            </div>
            <div v-if="props.match">
                <div>Enter "{{ props.match }}"" to delete.</div>
                <InputText type="text" v-model="matchText" :placeholder="props.match" autofocus/>
            </div>
        </div>
        <template #footer>
            <Button label="No" severity="danger" icon="pi pi-times" @click="model = false" />
            <Button label="Yes" icon="pi pi-check" @click="emit('delete')" 
            :disabled="disableDelete"/>
        </template>
    </Dialog>

</template>

<style>
</style>