<template>
  <div>
    <form id="cantheyform" @submit="onSubmit" @submit.stop.prevent="prevent" class="container" novalidate="true">
      Can <input name="name" v-model="name" class="ct-input" /> say the N word
    </form>
    <div v-if="canthey !== null" class="ct-resp">
      {{ canthey ? "Yes" : "No" }}
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios from "axios";

import { config } from "@/config";

@Component
export default class Input extends Vue {
  name = ""
  canthey: boolean = null;

  onSubmit(e) {
    const { BASE_URL } = config;
    this.canthey = null;
    e.preventDefault();
    console.log(this.name);
    axios.post(BASE_URL + "/search", { name: this.name })
    .then(({ status, data }) => {
      console.log(status, data);
      this.canthey = data.canthey;
    })
  }

  prevent = (event) => {
    event.preventDefault();
    event.stopPropagation();
    return false;
  }
}

</script>

<style>
</style>
