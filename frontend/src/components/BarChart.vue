<template>
  <Bar
    :data="data"
    :options="chartOptions"
    style="width: 100%; height: 300px"
  />
</template>

<script setup>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

// Chart.js에 필요한 플러그인 등록
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

// Props 정의
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

// Bar 차트 옵션 설정
const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: "top",
      onClick: null,
    },
  },
};
</script>
