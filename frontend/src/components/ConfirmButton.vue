<template>
  <v-btn
    class="bg-yellow-darken-2 fixed-bottom"
    size="x-large"
    rounded="0"
    variant="flat"
    @click="handleClick"
  >
    <h3>확인</h3>
  </v-btn>
</template>

<script setup>
import { defineEmits } from "vue";

const emit = defineEmits(["confirm"]);

const handleClick = () => {
  emit("confirm");
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
