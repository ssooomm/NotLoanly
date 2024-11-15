<template>
    <div class="mobile-container">
        <header class="header">
            <button class="back-button text-white">◀</button>
            <h1 class="title">I’m not LOANly</h1>
            <div class="icons">
                <span class="icon">🔔</span>
                <span class="icon">🏠</span>
                <span class="icon">☰</span>
            </div>
        </header>
        <div class="background-image-container">
            <img src="../../assets/img/loanInfo.png" alt="background" class="background-image">
        </div>

        <!-- 하단 고정 버튼 -->
        <div class="fixed-container">
            <button class="action-button">
                시작하기
            </button>
            <button class="action-button">
                시작하기
            </button>
        </div>
    </div>
</template>

<script>
</script>

<style>
.mobile-container {
    position: relative;
    max-width: var(--max-width);
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
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    /* padding: 16px; */
    background: transparent;
    z-index: 1000;
    /* padding-bottom: calc(16px + env(safe-area-inset-bottom, 0px)); */
    max-width: var(--max-width);
    margin: 0 auto;
}

.action-button {
    width: 100%;
    height: 56px;
    /* border-radius: 28px; */
    background-color: #007AFF;
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