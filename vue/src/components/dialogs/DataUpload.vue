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

const delimiter = ref({name: 'Comma', char: ','})
const otherDel = ref('')

const file = ref()

const delimiterList = ref([
    {name: 'Comma', char: ','},
    {name: 'Tab', char: '\t'},
    {name: 'Tilde', char: '~'},
    {name: 'Other', char: null},
])

function uploadFile(event) {
    console.log(event.files[0])
    let file = event.files[0]
    let reader = new FileReader()
    reader.readAsText(file)
    reader.onload = function(event) {
        let csvdata = event.target.result
        let rowdata = csvdata.split('\n')
        console.log(rowdata.map(row => row.trim()))
    }
}

watch(delimiter, () => {
    console.log(delimiter.value)
})

watch(file, () => {
    console.log(file.value)
    console.log(file.value.files)
})

// watch(model, () => {
//     if (!model.value) {
//         matchText.value = ''
//     }
// })
</script>

<template>
    <Dialog v-model:visible="model" :style="{width: '450px'}" header="Upload Data" :modal="true">
        <div class="field">
            <FileUpload name="file[]" :url="`http://localhost:5050/api/sources/upload`" @upload="uploadFile" auto> 
                <!-- accept="*csv*"> -->
                <template #empty>
                    <p>Drag and drop file here to upload</p>
                </template>
            </FileUpload>
        </div>
        <div class="field">
            <label>Delimiter</label>
            <div class="flex flex-column gap-2">
                <div class="flex justify-content-between">
                    <div v-for="delim in delimiterList" class="field-radiobutton">
                        <RadioButton v-model="delimiter" :value="delim" />
                        <label>{{ delim.name }}</label>
                    </div>
                </div>
                <div>
                    <InputText v-model="otherDel" placeholder="Delimiter" :disabled="delimiter.char == null ? false : true"></InputText>
                </div>
            </div>
        </div>
        <div>
            Preview Table
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" text @click="model = false" />
            <!-- <Button label="Yes" icon="pi pi-check" text @click="emit('delete')" 
            :disabled="disableDelete"/> -->
        </template>
    </Dialog>

</template>

<style>
</style>