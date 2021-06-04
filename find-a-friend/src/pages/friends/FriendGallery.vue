<template>
  <div class="container">

    <div class="gallery" v-if="hasImages">
      <div class="frame" v-for="img in images" :key="img.id">
        <img :src="img.data" @click="select(img.id,img.data)"/>
      </div>
    </div>

    <p v-else>No Images uploaded</p>
  </div>
</template>

<script>
export default {
    props: ["images"],
    emits: ["select"],
    computed: {
        hasImages() {
            return this.images.length > 0; 
        }
    },
    methods: {
      select(imageId, imageData) {
        this.$emit("select", imageId, imageData);
      }
    },
    
};
</script>

<style scoped>
/*
 kilde til css for gallery inspirasjon https://codepen.io/ran0904/pen/bNpLvX
*/

.frame {
  border: solid 2px black;
  text-align: center;
  width: 200px;
  height: 200px;
}

.gallery {
  margin: 0 auto;
  padding: 5px;
  background: #fff;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: center;
}

.gallery > div {
  margin: 5px;
}

.gallery > div > img {
  width: 100%;
  height: 100%;
  transition: 0.1s transform;
  transform: translateZ(0); 
}

.gallery > div:hover {
  z-index: 1;
}

.gallery > div:hover > img {
  transform: scale(1.4, 1.4);
  transition: 0.3s transform;
}



</style>
