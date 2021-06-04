<template>
  <base-item>
    <h2>Filter</h2>
    
    <input id="textinput" type="text" v-model="search" @keyup="setSearch" placeholder="Search by Firstname"/>

    <div class="flex-container">
      <span class="filter-option" v-for="hobby in hobbies" :key="hobby">
        <input type="checkbox" :id="hobby" checked @change="setFilter" />
        <label :for="hobby">{{ hobby }}</label>
      </span>
    </div>
  </base-item>
</template>

<script>
export default {
  props: ["hobbies"],
  emits: ["change-filter", "change-search"],
  data() {
    return {
      search: "",
    };
  },
  methods: {
    setFilter(event) {
      const clickedId = event.target.id;
      const isActive = event.target.checked;
      const updatedFilters = {
        ...this.filters,
        [clickedId]: isActive,
      };

      this.filters = updatedFilters;
      this.$emit("change-filter", updatedFilters);
    },
    setSearch() {
        this.$emit("change-search", this.search)
    },
  },
  mounted () {
    //stores the search input for revisiting page again
    if(sessionStorage.search) {
        this.search = sessionStorage.search;
      } else {
        this.search = "";
      }
  },
  computed: {
    filters() {
      return this.$store.getters["hobbies/filters"];
    },
    
  }
};
</script>

<style scoped>

#textinput {
  width: 100%;
  padding: 5px;
  margin: 0;
}

h2 {
  margin: 0.5rem 0;
  text-align: center;
}

.flex-container {
  display: flex;
  flex-wrap: wrap;
}

.flex-container span {
  flex-shrink: 2;
}

.filter-option {
  margin-right: 1rem;
}

.filter-option label {
  margin-left: 0.25rem;
}

.filter-option.active label {
  font-weight: bold;
}
</style>
