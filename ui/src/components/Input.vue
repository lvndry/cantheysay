<template>
  <form class="container" novalidate>
    Can <input name="name" class="ct-input" /> say the N word
  </form>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Input extends Vue {}

</script>

<style>
</style>
