<template>
  <div id="app" class="relative flex items-center h-screen w-screen">
    <Filters v-if="lesson_list.length > 0 && !error" :filter_data.sync="filter_data" v-bind:lesson_list="lesson_list" v-bind:show_english_first="show_english_first" v-on:action-reverse="onReverse" />
    <div class="flex-grow">

      <div v-if="error">
        <Error v-bind:error="error" />
      </div>

      <div v-else>
        <div v-if="is_ready">
          <Translation v-bind:translation="current_translation" v-bind:show_english_first="show_english_first" v-bind:reveal_translation="reveal_translation" />
          <Controls v-bind:reveal_translation="reveal_translation" v-on:action-reverse="onReverse" v-on:action-reveal="onReveal" v-on:action-skip="onSkip" v-on:action-next="onNext" />
        </div>
        <div v-else>
          <Loading />
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import urljoin from 'url-join'

import Translation from './components/Translation.vue'
import Controls from './components/Controls.vue'
import Loading from './components/Loading.vue'
import Error from './components/Error.vue'
import Filters from './components/Filters.vue'

export default {
  name: 'app',
  components: {
    Translation,
    Controls,
    Loading,
    Error,
    Filters,
  },
  mounted() {
    let vm = this
    window.addEventListener('keyup', function(event) {
      if (event.key == ' ') {
        event.preventDefault()
        vm.onKeyAdvance()
      }
    })
    axios.get(urljoin(this.VUE_APP_API_URL, '/api/lessons'))
      .then(response => {
        if (response.data.status == 'success') {
          this.lesson_list = response.data.data
          this.nextTranslation()
        } else {
          this.error = response.data.reason
        }
      }).catch(err => this.error = err)
  },
  data() {
    return {
      VUE_APP_API_URL: process.env.VUE_APP_API_URL || 'http://127.0.0.1:5000/',
      error: null,
      is_ready: false,
      translation_list: [],
      lesson_list: [],
      filter_data: {
        filter_maximum_lesson: '',
        filter_extinct_words: false,
      },
      current_translation: {},
      show_english_first: true,
      reveal_translation: false,
    }
  },
  watch: {
    'filter_data.filter_maximum_lesson'() {
      this.is_ready = false
      this.fetchTranslations()
    },
    'filter_data.filter_extinct_words'() {
      this.is_ready = false
      this.fetchTranslations()
    },
  },
  methods: {
    fetchTranslations() {
      const params = {}
      if (this.filter_data.filter_maximum_lesson) {
        params.maximum_lesson = this.filter_data.filter_maximum_lesson
      }
      if (this.filter_data.filter_extinct_words) {
        params.extinct_words = this.filter_data.filter_extinct_words
      }
      axios.get(urljoin(this.VUE_APP_API_URL, '/api/sentences'), {params})
        .then(response => {
          if (response.data.status == 'success') {
            this.translation_list = response.data.data
            this.nextTranslation()
          } else {
            this.error = response.data.reason
          }
        }).catch(err => this.error = err)
    },
    nextTranslation() {
      if (this.translation_list.length > 0) {
        this.current_translation = this.translation_list.shift()
        this.reveal_translation = false
        this.is_ready = true
      } else {
        this.is_ready = false
        this.fetchTranslations()
      }
    },
    onKeyAdvance() {
      if (this.is_ready) {
        if (this.reveal_translation) {
          this.reveal_translation = false
          this.nextTranslation()
        } else {
          this.reveal_translation = true
        }
      }
    },
    onReverse() {
      if (this.is_ready) {
        this.show_english_first = !this.show_english_first
        if (!this.reveal_translation) {
          this.nextTranslation()
        }
      }
    },
    onReveal() {
      if (this.is_ready) {
        this.reveal_translation = true
      }
    },
    onSkip() {
      if (this.is_ready) {
        this.reveal_translation = false
        this.nextTranslation()
      }
    },
    onNext() {
      if (this.is_ready) {
        this.reveal_translation = false
        this.nextTranslation()
      }
    }
  }
}
</script>
