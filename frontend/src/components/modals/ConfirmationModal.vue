<template>
  <!-- Confirmation Modal -->
  <div v-if="visible" class="modal fade show" tabindex="-1" aria-labelledby="confirmationModalLabel" :aria-hidden=!visible
    style="display: block; background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(6px);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content shadow-lg">
        <div class="modal-header border-0">
          <h5 class="modal-title fw-bold" id="confirmationModalLabel">{{ title }}</h5>
          <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
        </div>
        <div class="modal-body text-secondary">
          {{ message }}
          <slot></slot>
        </div>
        <div class="modal-footer border-0">
          <button type="button" class="btn btn-outline-danger" @click="closeModal">
            {{ cancelText }}
          </button>
          <button type="button" class="btn btn-success" @click="confirmAction">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: 'Confirm Action',
  },
  message: {
    type: String,
    default: 'Are you sure you want to proceed?',
  },
  cancelText: {
    type: String,
    default: 'Cancel',
  },
  confirmText: {
    type: String,
    default: 'Confirm',
  },
});

const emit = defineEmits(['close', 'confirm']);

const closeModal = () => emit('close');
const confirmAction = () => emit('confirm');
</script>

<style scoped>
/* Modal backdrop styling */
.modal.fade.show {
  display: block;
  background: rgba(0, 0, 0, 0.6);
  /* Dark semi-transparent background */
  backdrop-filter: blur(8px);
  /* Blur the background */
  transition: all 0.3s ease-in-out;
}

/* Modal content customizations */
.modal-content {
  border-radius: 6px;
  /* Rounded corners */
  overflow: hidden;
  animation: fadeIn 0.1s ease-in-out;
}

/* Modal shadow and spacing */
.shadow-lg {
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
}

/* Smooth fade-in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Button customizations */
.modal-footer .btn-outline-secondary {
  border-color: #ccc;
  color: #6c757d;
}

.modal-footer .btn-outline-secondary:hover {
  background-color: #f1f1f1;
  color: #000;
}
</style>