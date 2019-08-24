<template>
  <div>
    An error ocurred. Please try again later! Details: {{ error }}
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
