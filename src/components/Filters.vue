<template>
  <div>
    <button v-on:click='is_active = !is_active'>x</button>
    <div v-if='is_active'>
      <select v-model='filter_data.filter_maximum_lesson' @input='$emit("update:filter_data", filter_data);'>
        <option value=''></option>
        <option v-for='l in lesson_list' :key='l' :value='l'>{{ l }}</option>
      </select>
      <input type='checkbox' v-model='filter_data.filter_extinct_words' @input='$emit("update:filter_data", filter_data);'>
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
  },
  data() {
    return {
      is_active: false,
    }
  }
}
</script>
