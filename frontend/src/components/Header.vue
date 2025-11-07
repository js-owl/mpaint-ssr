<template>
  <header class="header">
    <nav class="nav">
      <router-link to="/" class="logo">
        <img :src="beaverImageUrl" alt="Beaver logo" class="logo-img" />
      </router-link>
      <div class="nav-right">
        <div class="nav-desktop">
          <router-link to="/" class="nav-link">Главная</router-link>
          <router-link to="/products" class="nav-link">Продукты</router-link>
          <router-link to="/users" class="nav-link">Пользователи</router-link>
        </div>
        <button 
          class="mobile-menu-toggle" 
          @click="toggleMobileMenu"
          :aria-expanded="isMobileMenuOpen"
          aria-label="Toggle menu"
        >
          <span class="hamburger-line" :class="{ 'open': isMobileMenuOpen }"></span>
          <span class="hamburger-line" :class="{ 'open': isMobileMenuOpen }"></span>
          <span class="hamburger-line" :class="{ 'open': isMobileMenuOpen }"></span>
        </button>
      </div>
      <div class="mobile-menu" :class="{ 'open': isMobileMenuOpen }">
        <router-link to="/" class="mobile-nav-link" @click="closeMobileMenu">Главная</router-link>
        <router-link to="/products" class="mobile-nav-link" @click="closeMobileMenu">Продукты</router-link>
        <router-link to="/users" class="mobile-nav-link" @click="closeMobileMenu">Пользователи</router-link>
      </div>
    </nav>
    <div 
      v-if="isMobileMenuOpen" 
      class="mobile-menu-overlay" 
      @click="closeMobileMenu"
    ></div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import beaverImageUrl from '@/icons/beaver.jpg'

const isMobileMenuOpen = ref(false)

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: background-color 0.3s ease;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  height: 44px;
  position: relative;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  transition: opacity 0.3s ease;
}

.logo:hover {
  opacity: 0.7;
}

.logo-img {
  width: 32px;
  height: 32px;
}

.nav-right {
  display: flex;
  align-items: center;
}

.nav-desktop {
  display: flex;
  align-items: center;
  gap: 2.5rem;
}

.nav-link {
  color: #1d1d1f;
  text-decoration: none;
  font-size: 12px;
  font-weight: 400;
  letter-spacing: -0.01em;
  transition: opacity 0.3s ease;
  position: relative;
  padding: 0.5rem 0;
}

.nav-link:hover {
  opacity: 0.65;
}

.nav-link.router-link-active {
  opacity: 1;
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background-color: #1d1d1f;
  opacity: 0.5;
}

/* Mobile Menu Toggle Button */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 24px;
  height: 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
  position: relative;
}

.hamburger-line {
  width: 24px;
  height: 1.5px;
  background-color: #1d1d1f;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

.hamburger-line:nth-child(1) {
  transform: translateY(0);
}

.hamburger-line:nth-child(2) {
  opacity: 1;
}

.hamburger-line:nth-child(3) {
  transform: translateY(0);
}

.mobile-menu-toggle .hamburger-line.open:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.mobile-menu-toggle .hamburger-line.open:nth-child(2) {
  opacity: 0;
}

.mobile-menu-toggle .hamburger-line.open:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

/* Mobile Menu */
.mobile-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: rgba(255, 255, 255, 0.98);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  flex-direction: column;
  padding: 1rem 0;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, opacity 0.3s ease;
  opacity: 0;
}

.mobile-menu.open {
  max-height: 300px;
  opacity: 1;
}

.mobile-nav-link {
  color: #1d1d1f;
  text-decoration: none;
  font-size: 17px;
  font-weight: 400;
  letter-spacing: -0.01em;
  padding: 0.75rem 1.5rem;
  transition: background-color 0.2s ease;
  position: relative;
}

.mobile-nav-link:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.mobile-nav-link.router-link-active {
  background-color: rgba(0, 0, 0, 0.05);
}

.mobile-nav-link.router-link-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #1d1d1f;
}

/* Mobile Menu Overlay */
.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 999;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Responsive Styles */
@media (max-width: 768px) {
  .nav {
    padding: 0.75rem 1.5rem;
  }

  .nav-desktop {
    display: none;
  }

  .mobile-menu-toggle {
    display: flex;
  }

  .mobile-menu {
    display: flex;
  }
}

@media (min-width: 769px) {
  .mobile-menu-overlay {
    display: none;
  }
}
</style>

