<template>
  <div class="mt-10 flex justify-center">
    <div class="max-w-2xl w-full">

      <div class="flex flex-row-reverse items-center m-3" v-if="!reveal_translation">
        <button id="button-reveal" class="text-center text-3xl font-bold bg-green-600 hover:bg-green-500 border-b-4 border-green-700 hover:border-green-600 rounded py-2 flex-grow focus:outline-none focus:shadow-outline" v-on:click="$emit('action-reveal')">
          Reveal
        </button>
        <button id="button-skip" class="text-center items-center py-1 flex-grow-0 mr-3 hover:underline focus:outline-none focus:shadow-outline" v-on:click="$emit('action-skip')">
          Skip
        </button>
      </div>

      <div class="flex flex-row items-center m-3" v-else>
        <button id="button-next" class="text-center text-3xl font-bold bg-green-600 hover:bg-green-500 border-b-4 border-green-700 hover:border-green-600 rounded py-2 flex-grow focus:outline-none focus:shadow-outline" v-on:click="$emit('action-next')">
          Next
        </button>
      </div>

    </div>
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
