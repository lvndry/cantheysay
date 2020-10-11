<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/question_mark.png">
    <Input />
  </div>
</template>

<script>
// @ is an alias to /src
import Input from '@/components/Input.vue';

export default {
  name: 'Home',
  components: {
    Input,
  },
};
</script>
