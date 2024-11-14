<template>
    <div class="spending-analysis">
      <h2>오수민의 월 평균 소비</h2>
      <h3>{{ totalSpending }}원</h3>
      <DoughnutChart v-if="doughnutChartData" :data="doughnutChartData" />
      <h3>20대 평균 소비 TOP3</h3>
      <BarChart v-if="barChartData" :data="barChartData" /> 
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import DoughnutChart from './DoughnutChart.vue'
  import BarChart from './BarChart.vue';
  
  // 데이터 설정
  const totalSpending = 1824235;
  
  // Doughnut 차트 데이터
  const doughnutChartData = ref({
    labels: ['쇼핑/의류비', '식비', '여가/취미비'],
    datasets: [
      {
        label: '소비 비율',
        data: [638465, 241881, 170940],
        backgroundColor: ['#4bc0c0', '#36a2eb', '#ff6384'],
        hoverOffset: 4,
      },
    ],
  });
  
  // Bar 차트 데이터
  const barChartData = ref({
    labels: ['쇼핑/의류비', '여가/취미비', '식비'],
    datasets: [
      {
        label: '나의 소비',
        data: [638465, 170940, 241881],
        backgroundColor: '#ffcc00',
      },
      {
        label: '20대 평균',
        data: [700000, 200000, 250000],
        backgroundColor: '#4caf50',
      },
    ],
  });
  </script>
  
  <style scoped>
  .spending-analysis {
    padding: 20px;
    text-align: center;
  }
  h2 {
    margin-bottom: 10px;
  }
  h3 {
    margin: 20px 0;
  }
  </style>
  