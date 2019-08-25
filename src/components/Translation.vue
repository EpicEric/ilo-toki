<template>
  <div class="flex justify-center">
    <div class="flex flex-grow flex-col max-w-xl">

      <div id="english-sentence" class="flex items-end my-1" v-bind:class="{ 'order-first': show_english_first, 'invisible': !show_english_first && !reveal_translation }">
        <div class="bg-white rounded-full h-10 w-10 flex-none flex items-center justify-center text-gray-900 ml-2">en</div>
        <div class="bg-blue-300 rounded-t-lg rounded-br-lg text-gray-900 mx-3 my-2">
          <div class="px-2 py-1">{{ translation.english_text }}</div>
        </div>
        <div class="flex-grow"></div>
      </div>

      <div id="toki-pona-sentence" class="flex items-end my-1" v-bind:class="{ 'order-first': !show_english_first, 'invisible': show_english_first && !reveal_translation }">
        <div class="flex-grow"></div>
        <div class="bg-green-300 rounded-t-lg rounded-bl-lg text-gray-900 mx-3 my-2">
          <div class="px-2 py-1">
            <div class="float-right mt-1 ml-2" v-bind:class="{ 'invisible': !reveal_translation }">
              <a class="focus:outline-none focus:shadow-outline" target="_blank" v-bind:href='"https://tatoeba.org/eng/sentences/show/" + translation.toki_pona_id' title="Improve sentence on Tatoeba">
                <svg class="fill-current w-3 h-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M12.3 3.7l4 4L4 20H0v-4L12.3 3.7zm1.4-1.4L16 0l4 4-2.3 2.3-4-4z"/></svg>
              </a>
            </div>
            {{ translation.toki_pona_text }}
          </div>
          
        </div>
        <div class="bg-white rounded-full h-10 w-10 flex-none flex items-center justify-center text-gray-900 mr-2">tp</div>
      </div>

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
