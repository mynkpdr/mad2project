<template>
  <div class="section m-4">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="card-title mb-0">Message Details</h5>
        <div class="d-flex gap-2">
          <button @click.prevent="openContactDeleteModal(contact.id)" class="btn btn-danger">
            <i class="bi bi-trash2-fill text-white"></i>
          </button>
        </div>
      </div>
      <!-- Stats Cards -->
      <div class="card-body">
        <div class="row">
          <div class="col-md-4 mb-4">
            <div class="contact-info-card p-4 rounded-3 shadow-sm border">
              <div class="text-center mb-4">
                <h4 class="fw-bold mb-1">{{ contact.name }}</h4>
                <a :href="'mailto:' + contact.email" class="text-primary text-decoration-none">
                  <i class="bi bi-envelope me-2"></i>{{ contact.email }}
                </a>
              </div>
              <div class="contact-meta mt-4">
                <div class="d-flex align-items-center mb-3">
                  <i class="bi bi-clock me-2 fs-1"></i>
                  <div>
                    <small class="text-secondary">Sent on</small>
                    <div>{{ useDateFormatter().formatDate2(contact.date_created) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-8">
            <div class="message-card p-4 rounded-3 shadow-sm border h-100">
              <h5 class="border-bottom pb-3 mb-4">
                <i class="bi bi-chat-left-text me-2"></i>Message Content
              </h5>
              <div class="message-content">
                {{ contact.message }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <ConfirmationModal :visible="isContactDeleteModalVisible" :message="ContactDeleteModalMessage"
        :title="'Confirm Deletion?'" :cancelText="'No'" :confirmText="'Yes'" @close="closeContactDeleteModal"
        @confirm="handleContactDeleteConfirm" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { push } from 'notivue'
import { useDateFormatter } from '../../utils/useDateFormatter'
import ConfirmationModal from '../../components/modals/ConfirmationModal.vue'

const route = useRoute()
const router = useRouter()
const contact = ref({})

const isContactDeleteModalVisible = ref(false);
const ContactDeleteModalMessage = ref('');
const deleteContactID = ref(null)
const openContactDeleteModal = (id) => {
    deleteContactID.value = id
    ContactDeleteModalMessage.value = 'Are you sure you want to delete this message?';
    isContactDeleteModalVisible.value = true;
};

const closeContactDeleteModal = () => {
    isContactDeleteModalVisible.value = false;
};

const handleContactDeleteConfirm = async () => {
    try {
        await axios.delete(`/api/contacts/${deleteContactID.value}`);
        push.success("Successfully deleted the message")
        closeContactDeleteModal()
        router.push({ name: 'AdminContacts' })
    } catch (error) {
        closeContactDeleteModal();
        throw error;
    }
};

const getContact = async () => {
  try {
    const response = await axios.get(`/api/contacts/${route.params.id}`)
    contact.value = response.data.data
  } catch (error) {
    throw error
  }
}

onMounted(() => {
  getContact()
})
</script>