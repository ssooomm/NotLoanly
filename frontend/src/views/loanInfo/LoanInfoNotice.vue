<template>

    <!-- 모달 컴포넌트 -->
    <v-dialog v-model="dialog" width="800">
        <v-card>
            <v-card-title class="text-center">처음 배우는 대출

            </v-card-title>
            <!-- <v-card-actions>
                <v-spacer>처음 배우는 대출</v-spacer>
                <v-btn @click="dialog = false" icon="mdi-close"></v-btn>
            </v-card-actions> -->

            <v-carousel cycle height="400" hide-delimiter-background show-arrows="hover">
                <v-carousel-item v-for="(item, i) in slides" :key="i">
                    <v-img :src="item.src" height="100%" cover></v-img>
                </v-carousel-item>
            </v-carousel>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="dialog = false"> 닫기 </v-btn>
            </v-card-actions>

        </v-card>
    </v-dialog>
    <div class="mobile-container">
        <div class="background-image-container">
            <img src="../../assets/img/loanInfo.png" alt="background" class="background-image">
        </div>

        <!-- 하단 고정 버튼 -->
        <div class="fixed-container">
            <div class="d-flex justify-end mb-4 mr-4">
                <v-btn @click="dialog = true" icon="mdi-book-open-page-variant-outline"></v-btn>
            </div>
            <button class="action-button">
                시작하기
            </button>
        </div>
    </div>

</template>


<script setup>
import { ref } from 'vue'
import info1 from '@/assets/img/info1.png'
import info2 from '@/assets/img/info2.png'
import info3 from '@/assets/img/info3.png'
import info4 from '@/assets/img/info4.png'
import info5 from '@/assets/img/info5.png'
import info6 from '@/assets/img/info6.png'
import info7 from '@/assets/img/info7.png'

const dialog = ref(false)
const slides = ref([
    {
        src: info1
    },
    {
        src: info2
    },
    {
        src: info3
    },
    {
        src: info4
    },
    {
        src: info5
    },
    {
        src: info6
    },
    {
        src: info7
    },
])
</script>

<style>
.mobile-container {
    position: relative;
    /* max-width: var(--max-width); */
    min-height: 100vh;
    margin: 0 auto;
    padding: 0;
    background: #ffffff;
    overflow-y: auto;
}

.background-image-container {
    width: 100%;
}

.background-image {
    width: 100%;
    height: auto;
    display: block;
}

.fixed-container {
    max-width: 390px;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    /* padding: 16px; */
    background: transparent;
    z-index: 1000;
    /* padding-bottom: calc(16px + env(safe-area-inset-bottom, 0px)); */
    /* max-width: var(--max-width); */
    margin: 0 auto;
}

.action-button {
    width: 100%;
    height: 56px;
    /* border-radius: 28px; */
    background-color: #FFCC00;
    color: white;
    border: none;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s, box-shadow 0.2s;
}

/* 버튼 호버/액티브 효과 */
.action-button:active {
    transform: scale(0.98);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>