<template>
  <div>
    <button v-on:click='$emit("action-reverse")'>
      Reverse
    </button>
    <button v-if='!reveal_translation' v-on:click='$emit("action-reveal")'>
      Reveal
    </button>
    <button v-if='!reveal_translation' v-on:click='$emit("action-skip")'>
      Skip
    </button>
    <button v-if='reveal_translation' v-on:click='$emit("action-next")'>
      Next
    </button>
  </div>
</template>

<script>
export default {
  name: 'Controls',
  props: {
    reveal_translation: Boolean,
  }
}
</script>
