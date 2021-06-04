<template>
  <div>
    <div class="request-mode" v-if="!buttonClicked">
      <i class="fas fa-check" @click="accept"></i>
      <i class="fas fa-times" @click="decline"></i>
    </div>

    <div :class="clicked" v-else>
      <p>{{ clicked }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      buttonClicked: false,
      clicked: "",
    };
  },
  methods: {
    accept() {
      this.buttonClicked = true;
      this.clicked = "Accepted";
    },
    decline() {
      this.buttonClicked = true;
      this.clicked = "Declined";
    },
  },
};
</script>

<style scoped>
.fa-check {
  color: green;
  opacity: 0.4;
}

.fa-check:hover {
  opacity: 1;
}

.fa-times {
  color: red;
  opacity: 0.4;
}

.fa-times:hover {
  opacity: 1;
}

.request-mode {
  font-size: 2em;
  display: flex;
  justify-content: flex-end;
  flex-grow: 1;
}

.request-mode i {
  padding: 0.5em;
}

.Accepted {
  color: green;
}

.Declined {
  color: red;
}
</style>
