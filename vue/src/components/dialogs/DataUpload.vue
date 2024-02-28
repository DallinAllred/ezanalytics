<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router';
const model = defineModel()
// const emit = defineEmits(['delete'])
// const props = defineProps(['match'])

const submitted = ref(false)

const tableTitle = ref('')
const delimiter = ref({name: 'Comma', char: ','})
const otherDel = ref('')

const usedDelim = computed(() => {
    if (delimiter.value.name != 'Other') return delimiter.value.char
    else if (otherDel.value == '') return null
    else return otherDel.value
})

const file = ref()

const dataTypes = ref([
    { name: 'String', code: 'varchar'},
    { name: 'Numeric', code: 'float'},
    { name: 'Datetime', code: 'datetime'}
])
const colTypes = ref([])

const headerRow = ref('Col1,Col2,Col3,Col4')
const headers = computed(() => {
    return headerRow.value.split(usedDelim.value)
})

const sampleDataRows = ref(['R1C1,R1C2,R1C3,R1C4', 'R2C1,R2C2,R2C3,R2C4'])
const sampleData = computed(() => {
    let data = []
    for (let row of sampleDataRows.value) {
        let cols = row.split(usedDelim.value)
        cols = Object.assign({},
            ...headers.value.map((key, i) => ({[key]: cols[i]})))
        data.push(cols)
    }
    return data
})

const delimiterList = ref([
    {name: 'Comma', char: ','},
    {name: 'Tab', char: '\t'},
    {name: 'Tilde', char: '~'},
    {name: 'Other', char: ''},
])

function preUpload(event) {
    console.log(event.files[0])
    file.value = event.files[0]
    let reader = new FileReader()
    reader.readAsText(file.value)
    reader.onload = function(event) {
        let csvdata = event.target.result
        let rows = csvdata.split('\n')
        rows = rows.map(row => row.trim())
        headerRow.value = rows[0]
        sampleDataRows.value = rows.slice(1,4)
        console.log(rows)
    }
}

function uploadData() {
    submitted.value = true
    if (!(tableTitle.value
        && usedDelim.value
        && colTypes.value.length > 0)) { return }

    console.log('Uploading')
}

watch(sampleData, () => {
    let types = []
    for (let col of headers.value) {// of sampleData.value[0].keys) {
        let colType = { name: 'Numeric', code: 'float'}
        for (let row of sampleData.value) {
            if (!Number(row[col])) colType = { name: 'String', code: 'varchar'}
        }
        types.push(colType)
    }
    colTypes.value = types
})

// watch(delimiter, () => {
//     console.log(delimiter.value)
// })

// watch(file, () => {
//     console.log(file.value)
//     console.log(file.value.files)
// })

// watch(model, () => {
//     if (!model.value) {
//         matchText.value = ''
//     }
// })
</script>

<template>
    <Dialog v-model:visible="model" :style="{width: '600px'}" header="Upload Data" :modal="true" class="p-fluid">
        <div class="field">
            <label for="tableTitle">Title</label>
            <InputText id="tableTitle" v-model.trim="tableTitle" required="true" autofocus :class="{'p-invalid': submitted && !tableTitle}" />
            <small class="p-error" v-if="submitted && !tableTitle">Title is required</small>
        </div>
        <div class="field">
            <FileUpload name="file[]" :url="`http://localhost:5050/api/sources/upload`" @select="preUpload"
                :show-upload-button="false" :show-cancel-button="false"> 
                <!-- accept="*csv*"> -->
                <template #empty>
                    <p>Drag and drop file here to upload</p>
                </template>
            </FileUpload>
            <small class="p-error" v-if="submitted && !file">No file has been selected</small>
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
            <DataTable :value="sampleData" scrollable>
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
            <Button label="Upload" icon="pi pi-upload" @click="uploadData" />
        </template>
    </Dialog>

</template>

<style>
</style>