<script setup>
import { computed, ref, watch } from 'vue'
const model = defineModel()
// const emit = defineEmits(['delete'])
// const props = defineProps(['match'])

// const matchText = ref()
// const disableDelete = computed(() => {
//     if (props.match) {
//         return !(matchText.value == props.match)
//     }
//     return false
// })

const delimiter = ref(',')

const delimiterList = ref([
    {name: 'Comma', delimiter: ','},
    {name: 'Tab', delimiter: '\t'},
    {name: 'Tilde', delimiter: '~'},
    {name: 'Other', delimiter: null},
])

function uploadFile() {

}



// watch(model, () => {
//     if (!model.value) {
//         matchText.value = ''
//     }
// })
</script>

<template>
    <Dialog v-model:visible="model" :style="{width: '450px'}" header="Upload Data" :modal="true">
        <div class="field">
            <FileUpload name="file[]" @upload="uploadFile" accept="*.csv">
                <template #empty>
                    <p>Drag and drop file here to upload</p>
                </template>
            </FileUpload>
        </div>
        <div class="field">
            <label>Delimiter</label>
            <div class="formgrid grid">
                <div v-for="delim in delimiterList">
                    <RadioButton v-model="delimiter" :value="delim.name" />
                    <label>{{ delim.name }}</label>
                </div>
            </div>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="model = false" />
            <Button label="Yes" icon="pi pi-check" text @click="emit('delete')" 
            :disabled="disableDelete"/>
        </template>
    </Dialog>

</template>

<style>
</style>