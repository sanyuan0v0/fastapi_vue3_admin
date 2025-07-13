<template>
    <div>
        <el-row :gutter="16">
            <el-col :span="4">
                <el-form-item label="秒">
                    <el-select v-model:value="crontabValueObj.second" placeholder="秒">
                        <el-option v-for="second in seconds" :key="second" :value="second">{{ second }}</el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <el-col :span="4">
                <el-form-item label="分">
                    <el-select v-model:value="crontabValueObj.min" placeholder="分">
                        <el-option v-for="min in minutes" :key="min" :value="min">{{ min }}</el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <el-col :span="4">
                <el-form-item label="时">
                    <el-select v-model:value="crontabValueObj.hour" placeholder="时">
                        <el-option v-for="hour in hours" :key="hour" :value="hour">{{ hour }}</el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <el-col :span="4">
                <el-form-item label="天">
                    <el-select v-model:value="crontabValueObj.day" placeholder="天">
                        <el-option v-for="day in days" :key="day" :value="day">{{ day }}</el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <el-col :span="4">
                <el-form-item label="周">
                    <el-select v-model:value="crontabValueObj.week" placeholder="周">
                        <el-option v-for="week in weeks" :key="week" :value="week">{{ week }}</el-option>
                    </el-select>
                </el-form-item>
            </el-col>
        </el-row>
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
// 样式可以根据需要调整</style>
