<script setup>

</script>

<template>
    <Dialog v-model:visible="userDialog" :style="{width: '450px'}" header="User Details" :modal="true" class="p-fluid">
        <div class="field">
            <label for="firstName">File</label>
            <FileUpload mode="basic" name="demo[]" url="/api/upload" accept="*.csv" :maxFileSize="1000000" @upload="onUpload" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" text @click="hideDialog" />
            <Button label="Save" icon="pi pi-check" text @click="saveUser" />
        </template>
    </Dialog>
</template>

<style>
</style>