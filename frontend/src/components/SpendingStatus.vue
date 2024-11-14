<!-- loanlyManager/src/components/SpendingStatus.vue -->
<template>
    <div>
      <h2>오수민님의 상환현황</h2>
      <p>Completed: 17.3%</p>
      <p>오늘까지 상환 금액은 530,000원입니다.</p>
      <div class="status-circles">
        <div class="circle">1개월</div>
        <div class="circle">2개월</div>
        <div class="circle">3개월</div>
      </div>
    </div>
  </template>
  
  <style scoped>
  .status-circles {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
  }
  
  .circle {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #e0e0e0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  </style>