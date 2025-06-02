<template>
    <div>
        <a-row :gutter="16">
            <a-col :span="4">
                <a-form-item label="秒">
                    <a-select v-model:value="crontabValueObj.second" placeholder="秒">
                        <a-select-option v-for="second in seconds" :key="second" :value="second">{{ second }}</a-select-option>
                    </a-select>
                </a-form-item>
            </a-col>
            <a-col :span="4">
                <a-form-item label="分">
                    <a-select v-model:value="crontabValueObj.min" placeholder="分">
                        <a-select-option v-for="min in minutes" :key="min" :value="min">{{ min }}</a-select-option>
                    </a-select>
                </a-form-item>
            </a-col>
            <a-col :span="4">
                <a-form-item label="时">
                    <a-select v-model:value="crontabValueObj.hour" placeholder="时">
                        <a-select-option v-for="hour in hours" :key="hour" :value="hour">{{ hour }}</a-select-option>
                    </a-select>
                </a-form-item>
            </a-col>
            <a-col :span="4">
                <a-form-item label="天">
                    <a-select v-model:value="crontabValueObj.day" placeholder="天">
                        <a-select-option v-for="day in days" :key="day" :value="day">{{ day }}</a-select-option>
                    </a-select>
                </a-form-item>
            </a-col>
            <a-col :span="4">
                <a-form-item label="周">
                    <a-select v-model:value="crontabValueObj.week" placeholder="周">
                        <a-select-option v-for="week in weeks" :key="week" :value="week">{{ week }}</a-select-option>
                    </a-select>
                </a-form-item>
            </a-col>
        </a-row>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const crontabValueObj = ref({
    second: "*",
    min: "*",
    hour: "*",
    day: "*",
    week: "*",
});

const seconds = ref(Array.from({ length: 60 }, (_, i) => i.toString()));
const minutes = ref(Array.from({ length: 60 }, (_, i) => i.toString()));
const hours = ref(Array.from({ length: 24 }, (_, i) => i.toString()));
const days = ref(Array.from({ length: 31 }, (_, i) => (i + 1).toString()));
const weeks = ref(["*", "1", "2", "3", "4", "5", "6", "7"]);

const handleConfirm = () => {
    const obj = crontabValueObj.value;
    return `${obj.second} ${obj.min} ${obj.hour} ${obj.day} ${obj.week}`
};

// 暴露方法和属性给父组件
defineExpose({ handleConfirm, crontabValueObj })

</script>

<style lang="scss" scoped>
// 样式可以根据需要调整
</style>