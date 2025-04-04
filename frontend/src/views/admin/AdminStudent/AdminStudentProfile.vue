<template>
    <div class="container my-4 px-0">
        <div class="row">
            <StudentSidebar />
            <div class="col-md-3 mb-4">
                <div class="card">
                    <div class="card-body text-center">
                        <img :src="profilePictureSrc.value + user.profile_picture" :alt="user.name"
                            class="rounded-circle img-fluid mb-3"
                            style="width: 150px; height: 150px; object-fit: cover;">
                        <img v-if="previewImage" :src="previewImage" alt="preview" class="rounded-circle img-fluid mb-3"
                            style="width: 150px; height: 150px; object-fit: cover;">
                        <div v-if="isEditing" class="mb-3">
                            <label for="profile_picture" class="form-label">Change Profile Picture</label>
                            <input type="file" id="profilePicture"
                                ref="fileInput" accept="image/*" @change="onFileSelected" class="form-control">
                            <div v-if="selectedFile" class="mb-3">
                                <button type="button" class="btn btn-outline-success" @click="uploadFile">
                                    Upload Image
                                </button>
                                <button type="button" class="btn btn-outline-danger" @click="removeFile">
                                    Remove File
                                </button>
                            </div>
                        </div>
                        <h3 class="card-title">{{ user.name }}</h3>
                        <p class="card-text">@{{ user.username }}</p>
                        <p class="card-text">{{ user.bio }}</p>
                        <button v-if="isEditing" class="btn btn-danger me-2" @click="cancelEdit">Cancel</button>
                        <button :class="isEditing ? 'btn btn-success' : 'btn btn-primary'" @click="toggleEdit">
                            <i v-if="!isEditing" class="bi bi-pencil-fill"></i>
                            <i v-else class="bi bi-check-circle-fill"></i>
                            {{ isEditing ? 'Save Changes' : 'Edit Profile' }}
                        </button>
                    </div>
                </div>
            </div>
            <div class="col-md-7">
                <div class="card">
                    <div class="card-header">
                        <h4 class="card-title mb-0">Profile Details</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="saveChanges" v-if="isEditing">
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Name</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control"
                                        v-model="user.name" required>
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Email</label>
                                <div class="col-sm-9">
                                    <input disabled type="email"
                                    class="form-control bg-muted" v-model="user.email" required style="opacity: 0.5;">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Username</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control"
                                        v-model="user.username" required>
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Phone</label>
                                <div class="col-sm-9">
                                    <input type="tel" class="form-control"
                                        v-model="user.phone_number">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Address</label>
                                <div class="col-sm-9">
                                    <textarea type="text" class="form-control"
                                        v-model="user.address">
                                    </textarea>
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Bio</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control"
                                        v-model="user.bio">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Gender</label>
                                <div class="col-sm-9">
                                    <select class="form-select"
                                        v-model="user.gender">
                                        <option value="Male">Male</option>
                                        <option value="Female">Female</option>
                                    </select>
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Date of Birth</label>
                                <div class="col-sm-9">
                                    <input type="date" class="form-control"
                                        v-model="user.dob">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Qualification</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control"
                                        v-model="user.qualification">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 col-form-label">Status</label>
                                <div class="col-sm-9">
                                    <select class="form-select"
                                        v-model="user.status">
                                        <option value="Active">Active</option>
                                        <option value="Suspended">Suspended</option>
                                    </select>
                                </div>
                            </div>
                        </form>
                        <div v-else>
                            <p><strong>Email:</strong> {{ user.email }}
                                <span v-if="user.email_verified">
                                    <i class="bi text-success bi-check-circle-fill"></i>
                                </span>
                                <span v-else>
                                    <i class="bi text-danger bi-x-circle-fill"></i>
                                </span>
                            </p>
                            <p><strong>Phone:</strong> {{ user.phone_number }}</p>
                            <p><strong>Address:</strong> {{ user.address }}</p>
                            <p><strong>Gender:</strong> {{ user.gender }}</p>
                            <p><strong>Date of Birth:</strong> {{ user.dob }}</p>
                            <p><strong>Qualification:</strong> {{ user.qualification }}</p>
                            <p><strong>Status:</strong> <span
                                    :class="['badge', user.status.toUpperCase() === 'ACTIVE' ? 'bg-success' : 'bg-danger']">{{
                                        user.status }}</span></p>
                            <p><strong>Member Since:</strong> {{ useDateFormatter().formatDate2(user.date_created) }}
                            </p>
                            <p><strong>Last Login:</strong> {{ useDateFormatter().formatTimeAgo(user.last_login) }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';
import { useDateFormatter } from '../../../utils/useDateFormatter';
import { push } from 'notivue';
import { useRoute } from 'vue-router';
import StudentSidebar from '../../../components/StudentSidebar.vue';

const route = useRoute()
const selectedFile = ref(null)
const previewImage = ref(null)
const fileInput = ref(null)
const isEditing = ref(false);

const onFileSelected = (event) => {
    const file = event.target.files[0]
    if (file) {
        selectedFile.value = file
        previewImage.value = URL.createObjectURL(file)
    }
}

const removeFile = () => {
    selectedFile.value = null
    previewImage.value = null
    if (fileInput.value) {
        fileInput.value.value = null;
    }
}

const uploadFile = async () => {
    if (!selectedFile.value) return
    const formData = new FormData()
    formData.append('file', selectedFile.value);
    formData.append('type', 'profile_picture');
    try {
        const response = await axios.post('/api/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
        })

        push.success("Profile Picture uploaded successfully")
        const response2 = await axios.put(`/api/students/${route.params.id}`, {
            'profile_picture': response.data.filename
        })
        selectedFile.value = null
        previewImage.value = null
        isEditing.value = false;

        getProfile()
    } catch (error) {
        throw error;
    }
};

const user = reactive({
    id: null,
    username: '',
    name: '',
    email: '',
    phone_number: '',
    address: '',
    bio: '',
    gender: '',
    dob: '',
    profile_picture: '',
    email_verified: false,
    status: '',
    date_created: null,
    last_login: null,
    qualification: ''
});

const getProfile = async () => {
    try {
        const response = await axios.get(`/api/students/${route.params.id}`)
        
        user.id = response.data.data.id
        user.username = response.data.data.username
        user.name = response.data.data.name
        user.email = response.data.data.email
        user.phone_number = response.data.data.phone_number
        user.address = response.data.data.address
        user.bio = response.data.data.bio
        user.gender = response.data.data.gender
        user.dob = response.data.data.dob ? new Date(response.data.data.dob * 1000).toISOString().split('T')[0] : null
        user.profile_picture = response.data.data.profile_picture
        user.email_verified = response.data.data.email_verified
        user.status = response.data.data.status
        user.date_created = response.data.data.date_created
        user.last_login = response.data.data.last_login
        user.qualification = response.data.data.qualification
    } catch (error) {
        throw error
    }
}

const cancelEdit = () => {
    isEditing.value = false;
    previewImage.value = null;
    selectedFile.value = null;
    getProfile()
};

const toggleEdit = () => {
    if (isEditing.value) {
        saveChanges();
    }
    isEditing.value = !isEditing.value;
};

const saveChanges = async () => {
    try {
        const response = await axios.put(`/api/students/${route.params.id}`, user)
        getProfile()
        push.success("Profile updated successfully.")
        isEditing.value = false;
    } catch (error) {
        throw error;
    }

};

onMounted(() => {
    getProfile()
    isEditing.value = route.query.edit === 'true'
})

</script>
