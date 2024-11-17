<template>
  <div>
    <!-- 상단 배너 -->
    <header>
      <v-card
        href="/expense-analysis"
        color="amber-lighten-4"
        class="text-left pa-2"
      >
        <v-row>
          <v-card-item class="ma-2">
            <v-card-title>
              <span class="card-title" v-html="formattedTitle"></span>
            </v-card-title>
            <v-card-subtitle
              >비상금 대출, 혹시나 연체될까 걱정된다면?<br />
              I'm not LOANly와 함께하세요!</v-card-subtitle
            >
          </v-card-item>
        </v-row>
      </v-card>
    </header>
    <!-- 비상금 충전 완료 화면 -->
    <main>
      <v-col class="mt-6">
        <v-img
          cover
          class="mx-auto"
          :width="160"
          aspect-ratio="1/1"
          src="/src/assets/luna_thumbsup.png"
        ></v-img>
        <v-col>
          <h1 class="pb-3">비상금 충전 완료</h1>
          <v-divider class="border-opacity-100"></v-divider>
          <v-row class="pa-5" justify="space-between">
            <h3>상품명</h3>
            <span>{{ productName }}</span>
          </v-row>
          <v-divider class="border-opacity-25"></v-divider>
          <v-row class="pa-5" justify="space-between">
            <h3>충전 금액</h3>
            <span>{{ displayAmount }} 원</span>
          </v-row>
          <v-divider class="border-opacity-100"></v-divider>
        </v-col>
      </v-col>
    </main>
    <!-- 확인 버튼 -->
    <ConfirmButton @confirm="handleConfirm" />
  </div>
</template>

<script setup>
import ConfirmButton from "@/components/ConfirmButton.vue";
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const productName = route.query.productName;
const loanAmount = route.query.loanAmount;

const displayAmount = new Intl.NumberFormat("ko-KR").format(loanAmount);

const title = "You're LOANly? I'm not LOANly!";
const formattedTitle = ref(title);

const handleResize = () => {
  if (window.innerWidth < 370) {
    formattedTitle.value = title.replace("? ", "?<br>");
  } else {
    formattedTitle.value = title;
  }
};

onMounted(() => {
  window.addEventListener("resize", handleResize);
  handleResize(); // 초기 로드 시 크기 확인
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
});

const handleConfirm = () => {
  // 비상금 충전 완료 페이지에서 확인 버튼 클릭 시
};
</script>

<style scoped>
.card-title {
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

@media (max-width: 430px) {
  .card-title {
    white-space: normal;
  }
}
</style>
