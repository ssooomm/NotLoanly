<template>
    <Doughnut :data="data" :options="chartOptions" />
  </template>
  
  <script setup>
  import { Doughnut } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js'
  
  // Chart.js에 필요한 플러그인과 컴포넌트를 등록합니다.
  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)
  
  // Props 정의
  const props = defineProps({
    data: { 
      type: Object,
      required: true,
    },
  })
  
  // Chart 옵션 설정
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    cutout: "70%"
  }
  </script>
  