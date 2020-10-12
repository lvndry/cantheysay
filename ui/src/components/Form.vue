<template>
  <div class="ct-form-container">
    <form id="cantheyform" @submit="onSubmit" @submit.stop.prevent="prevent" class="ct-container" novalidate="true">
        Can <input name="name" minlength="2" type="search" v-model="name" class="ct-input" autocomplete="off" required/><span style="visibilty:hidden"></span> say the n-word ?
    </form>
    <div v-if="canthey !== null" class="ct-resp">
      {{ canthey ? "Yes" : "No" }}
    </div>
    <div v-if="pending">
      <img src="../assets/array.gif" alt="pending.gif">
    </div>
    <div class="error ct-resp" v-if="error === 404">
      User not found
    </div>
    <div class="error ct-resp" v-if="error == 500">
      Something went wrong
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from "vue-property-decorator";

import httpService from "@/services/http.service";
import { ErrorType } from "@/errors";

@Component
export default class Form extends Vue {
  name = ""
  error: ErrorType | null = null;
  canthey: boolean | null = null;
  pending = false;

  mounted() {
    const input = document.querySelector<HTMLInputElement>("input[name='name']")!;

    input.addEventListener("input", function() {
      const span = (input.nextElementSibling as HTMLSpanElement)!;
      span.textContent = input.value;
      this.style.width = (span.offsetWidth + 5) + "px"
      span.textContent = ""
    });

    // must be last
    input.focus()
  }

  onSubmit(e: Event) {
    this.canthey = null;

    e.preventDefault();
    this.pending = true;
    this.error = null;
    if (this.name.length === 0) {
    } else {
      httpService.searchUser(this.name)
      .then(({ data }) => {
          this.canthey = data.canthey;
      })
      .catch((err) => {
        const { status } = err.response;
        if (status === ErrorType.NOT_FOUND) {
          this.error = ErrorType.NOT_FOUND
        } else if (status === ErrorType.INTERNAL) {
          this.error = ErrorType.INTERNAL
        }
      })
      .finally(() => {
        this.pending = false
      })
    }
  }

  prevent = (event: Event) => {
    event.preventDefault();
    event.stopPropagation();
    return false;
  }
}

</script>

<style>
  .ct-container {
    margin-top: 30px;
    font-size: 2.5em;
  }

  .ct-input, .ct-input:focus {
    background: transparent;
    border: none;
    outline-width: 0;
    font-size: 1em;
    align-self: center;
    white-space: pre;
    padding: 0 8px;
    box-sizing: content-box;
  }

  :focus { outline-style: none; -moz-outline-style: none;}

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

  .ct-resp {
    font-size: 8em;
  }

  /* clear the X for IE */
  input[type=search]::-ms-clear { display: none; width : 0; height: 0; }
  input[type=search]::-ms-reveal { display: none; width : 0; height: 0; }

  /* clears the ‘X’ from Chrome */
  input[type="search"]::-webkit-search-decoration,
  input[type="search"]::-webkit-search-cancel-button,
  input[type="search"]::-webkit-search-results-button,
  input[type="search"]::-webkit-search-results-decoration { display: none; }
</style>
