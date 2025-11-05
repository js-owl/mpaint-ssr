<template>
  <svg 
    :width="size" 
    :height="size" 
    viewBox="0 0 100 100" 
    fill="none" 
    xmlns="http://www.w3.org/2000/svg"
    class="beaver-icon"
  >
    <!-- Beaver body -->
    <ellipse cx="50" cy="60" rx="35" ry="30" fill="#8B4513" stroke="#654321" stroke-width="2"/>
    <!-- Beaver head -->
    <ellipse cx="50" cy="25" rx="22" ry="20" fill="#8B4513" stroke="#654321" stroke-width="2"/>
    <!-- Beaver tail -->
    <ellipse cx="15" cy="65" rx="12" ry="25" fill="#654321" stroke="#543210" stroke-width="2"/>
    <!-- Beaver ears -->
    <ellipse cx="38" cy="18" rx="6" ry="8" fill="#654321"/>
    <ellipse cx="62" cy="18" rx="6" ry="8" fill="#654321"/>
    <!-- Beaver eyes -->
    <circle cx="44" cy="25" r="3" fill="#1d1d1f"/>
    <circle cx="56" cy="25" r="3" fill="#1d1d1f"/>
    <!-- Beaver nose -->
    <ellipse cx="50" cy="32" rx="4" ry="3" fill="#1d1d1f"/>
    <!-- Beaver teeth -->
    <path d="M48 35 L50 38 L52 35 Z" fill="#ffffff"/>
  </svg>
</template>

<script setup lang="ts">
interface Props {
  size?: number | string
}

withDefaults(defineProps<Props>(), {
  size: 32
})
</script>

<style scoped>
.beaver-icon {
  display: inline-block;
}
</style>

