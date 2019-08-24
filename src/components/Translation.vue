<template>
  <div>
    <div class="flex">
      <div v-bind:class='{ "order-first": show_english_first }' v-if='show_english_first || reveal_translation'>
        {{ translation.english_text }}
      </div>
      <div v-bind:class='{ "order-first": !show_english_first }' v-if='!show_english_first || reveal_translation'>
        {{ translation.toki_pona_text }}
      </div>
    </div>
    <div v-if='reveal_translation'>
      <a target="_blank" v-bind:href='"https://tatoeba.org/eng/sentences/show/" + translation.toki_pona_id'>Improve sentence on Tatoeba</a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Translation',
  props: {
    translation: {
      id: Number,
      toki_pona_id: Number,
      toki_pona_text: String,
      english_id: Number,
      english_text: String,
      lesson: Number,
      has_extinct_words: Boolean,
    },
    show_english_first: Boolean,
    reveal_translation: Boolean,
  },
}
</script>
