<script setup>
import axios from '@/axiosConfig'
import { computed, ref, watch } from 'vue'
import { useToast } from 'primevue/usetoast'

const emit = defineEmits(['timeout401'])
const model = defineModel()

const toast = useToast()

const currentUser = JSON.parse(localStorage.getItem('eza-user'))
if (!currentUser) emit('timeout401')

const submitted = ref(false)
const uploading = ref(false)

const file = ref()
const tableTitle = ref('')

const delimiterList = ref([
    {name: 'Comma', char: ','},
    {name: 'Tab', char: '\t'},
    {name: 'Tilde', char: '~'},
    {name: 'Other', char: ''},
])
const delimiter = ref({name: 'Comma', char: ','})
const otherDel = ref('')
const usedDelim = computed(() => {
    if (delimiter.value.name != 'Other') return delimiter.value.char
    else if (otherDel.value == '') return null
    else return otherDel.value
})

const dataTypes = ref([
    { name: 'String', code: 'varchar'},
    { name: 'Numeric', code: 'numeric'},
    { name: 'Datetime', code: 'datetime'}
])
const colTypes = ref([])

const headerRow = ref('')
const headers = computed(() => {
    return headerRow.value.split(usedDelim.value)
})

const rawData = ref([])
const delimitedData = computed(() => {
    let data = []
    for (let row of rawData.value) {
        let cols = row.split(usedDelim.value)
        cols = Object.assign({},
            ...headers.value.map((key, i) => ({[key]: cols[i]})))
        data.push(cols)
    }
    return data
})

function preUpload(event) {
    file.value = event.files[0]
    if (!tableTitle.value) {
        tableTitle.value = file.value.name.split('.')[0]
    }
    let reader = new FileReader()
    reader.readAsText(file.value)
    reader.onload = function(event) {
        let csv = event.target.result
        let rows = csv.split('\n')
        rows = rows.map(row => row.trim())
        headerRow.value = rows[0]
        rawData.value = rows.slice(1)
    }
}

function removeFile() {
    tableTitle.value = ''
    rawData.value = []
    delimiter.value = {name: 'Comma', char: ','}
}

async function uploadData() {
    submitted.value = true
    if (!(tableTitle.value
        && usedDelim.value
        && colTypes.value.length > 0)) { return }
    uploading.value = true
    let columns = Object.assign({},
            ...headers.value.map((key, i) => ({[key]: colTypes.value[i].code})))
    let tableData = {
        columns,
        name: tableTitle.value,
        user: currentUser['user_id']
    }
    let createdTableName = ''
    try {
        let response = await axios.post(`/api/sources/upload/`, tableData)
        createdTableName = response.data.created
    } catch (err) {
        if (err.response?.status === 401) {
            emit('timeout401')
            return
        }
        uploading.value = false
        return
    }
    try {
        let data = delimitedData.value
        let response = await axios.put(`/api/sources/upload/${createdTableName}`, data)
    } catch (err) {
        if (err.response?.status === 401) {
            emit('timeout401')
            return
        }
        console.log(err)
    }
    toast.add({severity: 'success', summary: 'Successful', detail: 'Data uploaded', life: 3000})
    uploading.value = false
    submitted.value = false
    removeFile()
    model.value = false
}

watch(delimitedData, () => {
    let types = []
    for (let col of headers.value) {
        let colType = { name: 'Numeric', code: 'numeric'}
        for (let row of delimitedData.value) {
            if (!Number(row[col])) colType = { name: 'String', code: 'varchar'}
        }
        types.push(colType)
    }
    colTypes.value = types
})
</script>

<template>
    <Dialog v-model:visible="model" :style="{width: '600px'}" header="Upload Data" :modal="true" class="p-fluid">
        <div class="field">
            <FileUpload  name="file[]" @select="preUpload" @remove="removeFile"
            choose-label="Select File to Upload" :show-upload-button="false" :show-cancel-button="false"> 
                <template #empty>
                    <p>Drag and drop file here to upload</p>
                </template>
            </FileUpload>
            <small class="p-error" v-if="submitted && !file">No file has been selected</small>
        </div>
        <div class="field">
            <label for="tableTitle">Title</label>
            <InputText id="tableTitle" v-model.trim="tableTitle" required="true" :class="{'p-invalid': submitted && !tableTitle}" />
            <small class="p-error" v-if="submitted && !tableTitle">Title is required</small>
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
                    <InputText v-model.trim="otherDel" placeholder="Delimiter" :disabled="delimiter.name == 'Other' ? false : true" :class="{'p-invalid': submitted && !usedDelim}"></InputText>
                    <small class="p-error" v-if="submitted && !usedDelim">A delimiter is required</small>
                </div>
            </div>
        </div>
        <div>
            <DataTable v-if="delimitedData.length > 0" :value="delimitedData" scrollable scrollHeight="200px">
                <Column v-for="(col, index) in headers" :field="col">
                    <template #header>
                        <div class="flex flex-column">
                            <div>{{ col }}</div>
                            <div>
                                <Dropdown v-model="colTypes[index]" :options="dataTypes" optionLabel="name" placeholder="Select Data Type" />
                            </div>
                        </div>
                    </template>
                </Column>
            </DataTable>
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" @click="model = false" />
            <Button label="Upload" :icon="uploading ? 'pi pi-spin pi-spinner' : 'pi pi-upload'" @click="uploadData" />
        </template>
    </Dialog>

</template>

<style>
</style>