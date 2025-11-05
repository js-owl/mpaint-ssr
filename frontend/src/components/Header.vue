<template>
  <header class="header">
    <nav class="nav">
      <router-link to="/" class="nav-link">Home</router-link>
      <router-link to="/products" class="nav-link">Products</router-link>
    </nav>
  </header>
</template>

<script setup lang="ts"></script>

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
  justify-content: center;
  gap: 2.5rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  height: 44px;
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

@media (max-width: 768px) {
  .nav {
    gap: 1.5rem;
    padding: 0.75rem 1rem;
  }

  .nav-link {
    font-size: 11px;
  }
}
</style>

