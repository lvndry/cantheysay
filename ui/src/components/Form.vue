<template>
  <div class="ct-form-container">
    <form id="cantheyform" @submit="onSubmit" @submit.stop.prevent="prevent" class="container" novalidate="true">
      Can <input name="name" type="text" v-model="name" class="ct-input" required /> say the N word
    </form>
    <div v-if="canthey !== null" class="ct-resp">
      {{ canthey ? "Yes" : "No" }}
    </div>
    <div class="error" v-if="error === 404">
      User not found
    </div>
    <div class="error" v-if="error == 500">
      Something went wrong
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from "vue-property-decorator";
import axios from "axios";

import { config } from "@/config";
import { ErrorType } from "@/errors";

interface SearchResponse {
  status: number;
  data: {
    canthey: boolean;
  };
}

@Component
export default class Form extends Vue {
  name = ""
  error: ErrorType | null = null;
  canthey: boolean | null = null;
  mounted() {
    const input = document.querySelector<HTMLElement>("input[name='name']")
    if (input) {
      input.focus()
    }
  }

  onSubmit(e: Event) {
    const { BASE_URL } = config;
    this.canthey = null;

    e.preventDefault();
    axios.post(BASE_URL + "/search", { name: this.name })
    .then(({ status, data }: SearchResponse) => {
      if (status === 404) {
        this.error = ErrorType.NOT_FOUND;
      } else {
        this.canthey = data.canthey;
      }
    })
    .catch((err) => {
      const { status } = err.response;
      if (status === ErrorType.NOT_FOUND) {
        this.error = ErrorType.NOT_FOUND
      } else if (status === ErrorType.INTERNAL) {
        this.error = ErrorType.INTERNAL
      }
    })
  }

  prevent = (event: Event) => {
    event.preventDefault();
    event.stopPropagation();
    return false;
  }
}

</script>

<style>
  .ct-input, .ct-input:focus {
    background: transparent;
    border: none;
    outline-width: 0;
  }

  .ct-input:invalid:not(:focus) {
    animation: blink-empty 1.5s infinite;
    background-image: linear-gradient(black,black);
    background-position: 1px center;
    background-repeat: no-repeat;
    background-size: 1px 1.2em;
  }

  @keyframes blink-empty {
    0% { background-size: 1px 1.2em; }
    50% { background-size: 0 1.2em; }
  }
</style>
