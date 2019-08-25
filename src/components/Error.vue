<template>
  <div class="px-4 m-auto max-w-sm">
    <h1 class="text-3xl text-red-500 font-semibold">Error!</h1>
    <p class="text-gray-200 text-base">Sorry for the inconvenience, but an error has ocurred. Please try again later!</p>
    <p class="text-gray-500 text-sm">Details: {{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'Error',
  props: {
    error: String,
  },
}
</script>
