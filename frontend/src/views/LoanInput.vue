<template>
  <div>
    <v-col>
      <h1 class="pb-3">KB 비상금 대출 신청</h1>
      <div class="text-blue-grey-lighten-3">
        비상금 대출의 시작부터 끝까지, <br />
        사용자 맞춤으로 자동화된 상환 관리 서비스
      </div>
    </v-col>
    <!-- 대출 금액 입력 폼 -->
    <v-form @submit.prevent="handleConfirm">
      <v-col class="pa-5">
        <v-text-field
          required
          label="대출 금액"
          variant="underlined"
          type="text"
          pattern="[0-9]*"
          inputmode="numeric"
          :rules="[minAmountRule, maxAmountRule]"
          hide-details="auto"
          v-model="formattedAmount"
          @input="filterAmount"
          @blur="validateAmount"
        ></v-text-field>
        <v-col
          ><v-row class="py-3" justify="end"
            >{{ displayAmount }} 만원</v-row
          ></v-col
        >
      </v-col>
      <!-- 상품 정보 -->
      <v-col>
        <v-row class="pa-5" justify="space-between">
          <h3>상품명</h3>
          <span>KB 비상금 대출</span>
        </v-row>
        <v-row class="pa-5" justify="space-between">
          <h3>대출금리</h3>
          <span>연 {{ interestRate }}%</span>
        </v-row>
      </v-col>
    </v-form>
    <!-- 확인 버튼 -->
    <ConfirmButton @confirm="handleConfirm" class="full-width-button" />
  </div>
</template>

<script setup>
import ConfirmButton from "@/components/ConfirmButton.vue";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useApiStore } from "../stores/apiStore";

const router = useRouter();
const apiStore = useApiStore();

// 대출 금액
const minAmount = 500000; // 50만원
const maxAmount = 3000000; // 300만원

const amount = ref(0);
const formattedAmount = ref("");

// 대출 금액의 최소값과 최대값을 확인하는 함수
const validateAmount = () => {
  // 콤마 제거 후 숫자로 변환
  const parsedAmount = parseFloat(formattedAmount.value.replace(/,/g, "")) || 0;

  // 금액이 비어있는지 확인
  if (parsedAmount === 0) {
    return false;
  }

  // 만원 이하의 입력값을 올림 처리
  const roundedAmount = Math.ceil(parsedAmount / 10000) * 10000;

  if (roundedAmount < minAmount) {
    amount.value = minAmount;
  } else if (roundedAmount > maxAmount) {
    amount.value = maxAmount;
  } else {
    amount.value = roundedAmount;
  }

  const formatter = new Intl.NumberFormat("ko-KR");
  formattedAmount.value = formatter.format(amount.value);

  return true;
};

// 대출 금액 입력 필터링(숫자만 입력 가능)
const filterAmount = (event) => {
  const value = event.target.value;
  const filteredValue = value.replace(/[^0-9]/g, "");
  formattedAmount.value = filteredValue;
  displayAmount.value = filteredValue.replace(/,/g, "");
};

// 대출 금액의 최소값과 최대값을 확인하는 규칙(유효성 검사)
const minAmountRule = (value) => {
  const parsedAmount = parseFloat(value.replace(/,/g, "")) || 0;
  return (
    parsedAmount >= minAmount ||
    `금액은 최소 ${minAmount.toLocaleString()}원 이상이어야 합니다.`
  );
};

const maxAmountRule = (value) => {
  const parsedAmount = parseFloat(value.replace(/,/g, "")) || 0;
  return (
    parsedAmount <= maxAmount ||
    `금액은 최대 ${maxAmount.toLocaleString()}원 이하여야 합니다.`
  );
};

// 화면에 표시할 금액
const displayAmount = computed(() => {
  let parsedAmount = formattedAmount.value.replace(/\D/g, ""); // 숫자가 아닌 모든 문자 제거
  return parsedAmount.slice(0, -4);
});

// KB 비상금 대출 금리 정보
const interestRate = ref(6.0);

// 확인 버튼 클릭 시 이벤트
const handleConfirm = async () => {
  if (validateAmount()) {
    try {
      const response = await apiStore.applyForLoan(
        1,
        amount.value,
        interestRate.value
      );

      if (response.status === "success") {
        console.log("대출 신청이 완료되었습니다.");
        router.push({
          path: "/loan-complete",
          state: {
            loanAmount: amount.value,
          },
        });
      }
    } catch (error) {
      console.error("대출 신청 중 오류 발생:", error);
      alert("대출 신청에 실패했습니다. 다시 시도해 주세요.");
    }
  } else {
    alert("대출 금액을 입력해주세요.");
  }
};
</script>

<style scoped>
.fixed-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
}

/* 데스크탑 화면에서 가운데 정렬 */
@media (min-width: 768px) {
  .fixed-bottom {
    width: 430px; /* iPhone 14 Pro Max 기준(최대너비 상정) */
    left: 50%;
    transform: translateX(-50%);
  }
}

</style>
