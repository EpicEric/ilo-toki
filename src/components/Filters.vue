<template>
  <div>
    <button id="sidebar-open" type="button" class="absolute top-0 left-0 p-6 items-center text-gray-400 hover:text-gray-200 focus:outline-none focus:shadow-outline"  v-on:click="is_active = !is_active">
      <svg class="fill-current w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
    </button>

    <div class="fixed inset-0 w-full h-screen flex items-center justify-center bg-semi-75 z-10" v-if="is_active">
      <div class="relative p-8 bg-gray-900 w-full max-w-md m-auto mt-20 flex-col rounded flex z-20">

        <button id="sidebar-open" type="button" class="absolute top-0 right-0 text-xl text-gray-400 hover:text-gray-200 my-2 mx-4 focus:outline-none focus:shadow-outline" v-on:click="is_active = false">
          <svg class="fill-current w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"/></svg>
        </button>

        <button id="button-reverse" class="flex flex-row justify-center bg-gray-700 hover:bg-gray-600 text-gray-200 my-2 mx-auto py-2 px-4 max-w-md items-center rounded focus:outline-none focus:shadow-outline" v-on:click='$emit("action-reverse");'>
          <svg class="fill-current h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9 6a4 4 0 1 1 8 0v8h3l-4 4-4-4h3V6a2 2 0 0 0-2-2 2 2 0 0 0-2 2v8a4 4 0 1 1-8 0V6H0l4-4 4 4H5v8a2 2 0 0 0 2 2 2 2 0 0 0 2-2V6z"/></svg>
          <span>Switch to {{ show_english_first ? 'Toki Pona' : 'English' }}</span>
        </button>

        <label class="flex justify-between items-center my-2">
          <span>jan Pije lesson</span>
          <select class="form-select block text-gray-800" v-model="filter_data.filter_maximum_lesson" @input="$emit('update:filter_data', filter_data);">
            <option value=""></option>
            <option v-for="l in lesson_list" :key="l" :value="l">{{ l }}</option>
          </select>
        </label>

        <label class="flex justify-between items-center my-2">
          <span>Allow extinct words</span>
          <input class="form-checkbox" type="checkbox" v-model="filter_data.filter_extinct_words" v-on:keyup.enter="filter_data.filter_extinct_words = !filter_data.filter_extinct_words; $emit('update:filter_data', filter_data);" @input="$emit('update:filter_data', filter_data);">
        </label>

        <a class="flex justify-center items-center mt-6 text-gray-500 hover:text-gray-700 focus:outline-none focus:shadow-outline" href="https://github.com/epiceric/ilo-toki" target="_blank" title="View on GitHub">
          <span class="text-sm pr-1">{{ show_english_first ? 'by Epic Eric' : 'tan jan Eliki' }} @</span>
          <svg class="fill-current h-12 w-12 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12,2.2467A10.00042,10.00042,0,0,0,8.83752,21.73419c.5.08752.6875-.21247.6875-.475,0-.23749-.01251-1.025-.01251-1.86249C7,19.85919,6.35,18.78423,6.15,18.22173A3.636,3.636,0,0,0,5.125,16.8092c-.35-.1875-.85-.65-.01251-.66248A2.00117,2.00117,0,0,1,6.65,17.17169a2.13742,2.13742,0,0,0,2.91248.825A2.10376,2.10376,0,0,1,10.2,16.65923c-2.225-.25-4.55-1.11254-4.55-4.9375a3.89187,3.89187,0,0,1,1.025-2.6875,3.59373,3.59373,0,0,1,.1-2.65s.83747-.26251,2.75,1.025a9.42747,9.42747,0,0,1,5,0c1.91248-1.3,2.75-1.025,2.75-1.025a3.59323,3.59323,0,0,1,.1,2.65,3.869,3.869,0,0,1,1.025,2.6875c0,3.83747-2.33752,4.6875-4.5625,4.9375a2.36814,2.36814,0,0,1,.675,1.85c0,1.33752-.01251,2.41248-.01251,2.75,0,.26251.1875.575.6875.475A10.0053,10.0053,0,0,0,12,2.2467Z"/></svg>
        </a>

      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'Filters',
  props: {
    lesson_list: Array,
    filter_data: {
      filter_maximum_lesson: String,
      filter_extinct_words: Boolean,
    },
    show_english_first: Boolean,
  },
  data() {
    return {
      is_active: false,
    }
  }
}
</script>
