<template>
  <div class="container mt-5 d-flex align-items-center justify-content-center text-center">
    <div>
      <h1 class="display-1 fw-bold text-primary">404</h1>
      <h2 class="display-6 mb-3">Page Not Found</h2>
      <p class="lead text-muted mb-4">
        Oops! The page you're looking for doesn't exist.
      </p>
      <router-link to="/" class="btn btn-primary px-4 py-2">
        <i class="bi bi-house-door me-2"></i>Back to Home
      </router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.text-primary {
  color: #FF671F !important;
}

.btn-primary {
  background-color: #FF671F;
  border-color: #FF671F;
}

.btn-primary:hover {
  background-color: #ec5205;
  border-color: #ec5205;
}
</style>