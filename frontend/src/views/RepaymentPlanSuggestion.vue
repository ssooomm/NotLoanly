<template>
  <v-app>
    <v-main>
      <v-container class="mt-5" fluid>
        <!-- 상환 플랜 제목 -->
        <h1 class="title text-center">상환 플랜 선택</h1>

        <!-- 플랜 카드 리스트 -->
        <v-row dense>
          <v-col cols="12" class="justify-center" v-for="(plan, index) in plans" :key="index">
            <v-card class="plan-card" outlined>
              <div class="card-header">
                <v-card-title class="plan-title">{{ plan.title }}</v-card-title>
              </div>
              <div class="card-body">
                <!-- 왼쪽: 해시태그, 오른쪽: 이미지 -->
                <div class="left-content">
                  <v-card-subtitle class="plan-hashtags">
                    <p v-for="(hashtag, idx) in plan.hashtags" :key="idx" class="hashtag">{{ hashtag }}</p>
                  </v-card-subtitle>
                </div>
                <div class="right-content">
                  <img :src="plan.image" class="plan-image" alt="Plan Image" />
                </div>
              </div>
              <!-- 아래에 상세보기 버튼 -->
              <v-card-actions class="card-actions">
                <v-btn text class="details-button">상세보기</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';

// Importing images directly for Vite
import shoppingImage from '@/assets/shopping.png';
import foodImage from '@/assets/food.png';
import leisureImage from '@/assets/leisure.png';
import alcoholImage from '@/assets/alcohol.png';
import trafficImage from '@/assets/traffic.png';

const plans = ref([
  {
    title: '쇼핑 절약 플랜',
    hashtags: ['# ootd', '# 중고로 저렴하게', '# 패션 리폼'],
    image: shoppingImage,
  },
  {
    title: '식비 절약 플랜',
    hashtags: ['# 냉장고 파먹기', '# 배달 금지!', '# 백종원 레시피'],
    image: foodImage,
  },
  {
    title: '여가 및 문화생활 절약 플랜',
    hashtags: ['# 산책가자', '# 친구 OTT 같이보자', '# 집에서 노래나 듣자'],
    image: leisureImage,
  },
  {
    title: '술/유흥 절약 플랜',
    hashtags: ['# 혼자 놀자', '# 건강을 생각해', '# 인생에 해독을'],
    image: alcoholImage,
  },
  {
    title: '교통비 절약 플랜',
    hashtags: ['# 걸어다니자', '# 대중교통을 이용하자', '# 내가 바른 환경 지킴이'],
    image: trafficImage,
  },
]);
</script>

<style scoped>
.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 30px;
}

.plan-card {
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-radius: 12px;
  background-color: #f7f7f7;
  height: auto;
  margin: 0 auto 16px;
}

.card-header {
  margin-bottom: 8px;
}

.plan-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  text-align: left;
}

.card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-content {
  flex: 1;
}

.plan-hashtags {
  margin: 0;
  padding: 0;
  text-align: left; /* Ensures hashtags are aligned to the left */
}

.hashtag {
  font-size: 16px;
  color: #666;
  margin-bottom: 4px;
}

.right-content {
  flex-shrink: 0;
  margin-left: 16px;
}

.plan-image {
  width: 100px;
  height: auto;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
}

.details-button {
  color: #3f51b5;
}
</style>
