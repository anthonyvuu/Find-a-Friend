<template>
  <div v-if="show" class="overlay">
    <dialog open v-if="show">
      <header>
        <slot name="header">
          <h3>{{ title }}</h3>
        </slot>
      </header>
      <div class="content">
        <slot></slot>
      </div>
      <div class="menu">
        <base-button @click="exit">Close</base-button>
      </div>
    </dialog>
  </div>
</template>

<script>
export default {
  props: ["show", "title"],

  methods: {
    exit() {
      this.$emit("exit");
    }
  },
};
</script>

<style scoped>
.overlay {
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  z-index: 10;
  background-color: rgba(0, 0, 0, 0.5);
}

header {
  background-color: #3a0061;
  color: white;
  width: 100%;
  padding: 1rem;
  display: flex;
  justify-content: center;
}

dialog div {
  padding: 2px;
  display: flex;
  justify-content: center;
  margin: 0;
}

dialog {
  position: fixed;
  top: 25vh;
  left: 15%;
  width: 70%;
  z-index: 100;
  margin: 0;
  padding: 0;
  background-color: white;
}
</style>
