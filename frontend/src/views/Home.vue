<template>
  <div class="vh-100 text-white d-flex pt-5" :style="isNightMode ? 'background: linear-gradient(180deg, #161a2d 0%, #070914 100%);' : ''">
    <div class="container pt-5">
      <div class="row align-items-center">

        <div class="col-lg-6 text-center text-lg-start mb-4">
          <div class="highlight-banner" :class="{ 'show': isVisible }">
            <i class="bi bi-heart-fill text-primary"></i> {{ bannerText }}
          </div>
          <h1 class="main-title mb-3" :class="{ 'show': isVisible }" :style="isNightMode ? 'color: #FF671F' : 'color: #000'">
            {{ title }}
          </h1>

          <p class="subtitle lh-lg mb-3 text-thin" :class="{ 'show': isVisible, 'text-light': isNightMode, 'text-dark': !isNightMode }">
            {{ subtitle }}
          </p>
          <button class="btn btn-primary btn-lg start-button" @click.prevent="router.push({ name: 'BrowsePractice' })"
            :class="{ 'show': isVisible }">
            {{ startText }}
          </button>

        </div>

        <div class="col-lg-6 text-center">
          <img class="svg_img img-fluid" :src="staticSrc.value + 'assets/detailed_analysis.svg'" alt=""
            :class="{ 'show': isVisible }">
        </div>
      </div>
    </div>
  </div>

  <div class="container-fluid" :style="isNightMode ? 'background: #070914' : ''">
    <div class="container">
      <!-- Key Features Section -->
      <section class="mb-5 w-100" id="key_features">
        <h1 class="mb-4 fw-bold text-center" :class="{ 'text-light': isNightMode, 'text-dark': !isNightMode }">Key Features</h1>
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
          <div v-for="(feature, index) in key_features" :key="index" class="col">
            <div class="card h-100 border-1 shadow" :class="{'night-mode border-thin': isNightMode, 'border-1': !isNightMode}">
              <div class="card-body text-center">
                <i :class="feature.icon_class" class="fs-2"></i>
                <h3 class="h4 card-title text-bold">{{ feature.text }}</h3>
                <p class="card-text text-thin">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Testimonials Section -->
      <section class="my-5 py-5 w-100" id="reviews">
        <h1 class="=mb-4 fw-bold text-center" :class=" {'text-light': isNightMode, 'text-dark': !isNightMode} ">Testimonials</h1>
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div v-for="testimonial in testimonials" :key="testimonial.id" class="col">
            <div class="card h-100 shadow" :class="{'night-mode border-thin': isNightMode, 'border-1': !isNightMode}">
              <div class="card-body text-center">
                <img :src="staticSrc.value + 'uploads/profile_pictures/default.jpg'" alt="Testimonial Image"
                  class="img-fluid rounded-circle mb-3" style="max-width: 120px; height: 120px;">
                <p class="card-text text-thin" :class="{'text-light': isNightMode, 'text-dark': !isNightMode}">"{{ testimonial.text }}"</p>
                <p class="card-text fw-bold">- {{ testimonial.author }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Contact and FAQ Section -->
      <section class="w-100">
        <div class="container">
          <div class="row align-items-center mb-5">
            <div class="col-md-6 text-center">
              <img class="img-fluid contact_svg" :src="staticSrc.value + 'assets/faq.svg'"
                style="max-width: 450px; height: auto;">
            </div>

            <!-- FAQ Section -->
            <div class="col-md-6 py-5" id="faqs">
              <h1 class="mb-4 fw-bold" :class="{'text-light': isNightMode, 'text-dark': !isNightMode}">Frequently Asked Questions</h1>
              <div class="accordion" id="accordionExample">
                <div v-for="(according, index) in accordings" :key="index" class="accordion-item text-secondary" :class="{'night-mode border-thin': isNightMode, 'border-1': !isNightMode}">
                  <h2 class="accordion-header" :id="'headingOne' + index">
                    <button class="accordion-button collapsed" :class="{'night-mode' : isNightMode}" :style="{'background: #070914': isNightMode}" type="button" data-bs-toggle="collapse"
                      :data-bs-target="'#collapse' + index" aria-expanded="false" :aria-controls="'collapse' + index">
                      {{ according.question }}
                    </button>
                  </h2>
                  <div :id="'collapse' + index" class="accordion-collapse collapse" :aria-labelledby="'heading' + index"
                    data-bs-parent="#accordionExample">
                    <div class="accordion-body">
                      {{ according.answer }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row align-items-center">
            <!-- Contact Section -->
            <div class="col-md-6 py-5" id="contact">
              <h1 class="mb-4 fw-bold" :class="{'text-light': isNightMode, 'text-dark': !isNightMode}">Contact Us</h1>
              <form @submit.prevent="submitForm">
                <div class="mb-3">
                  <label for="name" class="form-label text-secondary">Name</label>
                  <input v-model="form.name" id="name" type="text" required
                    class="form-control form-control-lg" :class="{'night-mode border-thin': isNightMode, 'border-1': !isNightMode}" />
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label text-secondary">Email</label>
                  <input v-model="form.email" id="email" type="email" required
                    class="form-control form-control-lg" :class="{'night-mode border-thin': isNightMode, 'border-1': !isNightMode}" />
                </div>
                <div class="mb-3">
                  <label for="message" class="form-label text-secondary">Message</label>
                  <textarea v-model="form.message" id="message" required class="form-control form-control-lg" :class="{'night-mode border-thin': isNightMode, 'border-1': !isNightMode}"
                    rows="4"></textarea>
                </div>
                <button type="submit" class="btn btn-primary shadow">Send Message</button>
              </form>
            </div>
            <div class="col-md-6 text-center">
              <img class="img-fluid faq_svg" :src="staticSrc.value + 'assets/inbox.svg'"
                style="max-width: 450px; height: auto;">
            </div>
          </div>

        </div>
      </section>
    </div>

  </div>
</template>

<script setup>
import axios from 'axios';
import { push } from 'notivue';
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNightModeStore } from '../store/nightMode';
const { isNightMode } = useNightModeStore()
const router = useRouter();
const isVisible = ref(false)
const bannerText = 'Get ready to ace your exams!'
const title = 'Prepare for your exams with us'
const subtitle = 'From beginner to advanced, unlock your potential with variety of questions, track progress, see history, get to the top of the leaderboard and conquer your exams.'
const startText = 'Get Started'

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 500)
})

const key_features = ref([
  { icon_class: 'bi bi-journal-check', text: 'Practice Quizzes', description: 'Test your knowledge with quizzes for every subject and chapter.' },
  { icon_class: 'bi bi-trophy', text: 'Mock Exams', description: 'Track your progress with quizzes of varying difficulty levels.' },
  { icon_class: 'bi bi-graph-up', text: 'Leaderboard', description: 'Get to the top of the leaderboard by solving the questions.' },
  { icon_class: 'bi bi-chat-left-text', text: 'Feedback', description: 'Send us feedback and suggestions to help us improve.' },
])

const testimonials = ref([
  { id: 1, text: "ExamBhai helped me ace my exams. The practice quizzes were spot on!", author: "Mayank Poddar" },
  { id: 2, text: "I love how easy it is to find quizzes for specific subjects and chapters.", author: "Jenny" },
  { id: 3, text: "The variety of difficulty levels really helped me progress in my studies.", author: "Virat Kohli" },
])

const accordings = ref([
  { question: 'What is ExamBhai?', answer: 'ExamBhai is an online platform that provides practice quizzes and mock exams for students.' },
  { question: 'How can I access the quizzes?', answer: 'You can access the quizzes by creating an account and logging in to the platform.' },
  { question: 'Are the quizzes free?', answer: 'Yes, all the quizzes on ExamBhai are free to access and attempt.' },
  { question: 'What is the difference between practice mode and exam mode?', answer: 'Practice mode allows you to attempt quizzes with no time limit, while exam mode simulates a real exam environment with a time limit.' },
  { question: 'How can I track my progress?', answer: 'You can track your progress by viewing your scores and leaderboard rankings on the platform.' },
  { question: 'How can I provide feedback?', answer: 'You can provide feedback by filling out the contact form on the platform.' }
])

const form = ref({
  name: '',
  email: '',
  message: ''
})

const submitForm = async () => {
  try {
    await axios.post('/api/contacts', form.value)
    push.success('Message sent successfully!')
    form.value = {
      name: '',
      email: '',
      message: ''
    }
  } catch (error) {
    throw error
  }
}

</script>


<style scoped>
.text-thin {
  font-weight: 200;
}

.text-bold {
  font-weight: 700;
}

.border-primary {
  border-color: #FF671F !important;
}

.border-thin {
  border: 1px solid rgba(255, 255, 255, 0.2);
}


.highlight-banner {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  background: #070914;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}

.main-title {
  font-size: 3.4rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  white-space: pre-line;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
  transition-delay: 0.2s;
}

.subtitle {
  font-size: 1.2rem;
  max-width: 600px;
  opacity: 0.9;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
  transition-delay: 0.4s;
}

.start-button {
  padding: 0.8rem 2.5rem;
  font-weight: 600;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
  transition-delay: 0.6s;
}

.svg_img {
  opacity: 0;
  transform: translateX(20px);
  transition: all 0.6s ease;
  transition-delay: 0.6s;
}

.show {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
  }

  .contact_svg {
    display: none;
  }

  .faq_svg {
    display: none;
  }

  .svg_img {
    display: none;
  }

  .start-button {
    font-size: 1rem;
    padding: 0.7rem 1.5rem;
  }
}
</style>