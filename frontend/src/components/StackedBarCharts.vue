<template>
  <Bar :data="data" :options="chartOptions" style="width: 100%; height: 40vh" />
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
  indexAxis: "y", // Horizontal bar chart
  responsive: true,
  maintainAspectRatio: false,
  maxBarThickness: 15,
  plugins: {
    legend: {
      position: "bottom",
      align: "end",
      labels: {
        boxWidth: 5,
        boxHeight: 5,
        usePointStyle: true,
      },
      onClick: null,
    },
    tooltip: {
      enabled: true,
      mode: "index",
      intersect: false,
    },
  },
  scales: {
    x: {
      stacked: true,
      beginAtZero: true,
      ticks: {
        callback: (value) => `${value / 10000}만원`, // x-axis unit label
      },
    },
    y: {
      stacked: true,
      ticks: {
        callback: function (value) {
          const label = this.getLabelForValue(value);
          // Split the label by spaces, then return as an array to enforce multi-line
          return label.split(" ");
        },
      },
    },
  },
};
</script>
