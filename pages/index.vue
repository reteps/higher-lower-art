<template>
<div class="page">

<div class="container">
  <div v-for="(item, index) in items.slice(0, -1)" :key="item.resultID" class="item" :style="{ backgroundImage: `url(${item.artworkUrl})`}">

    <div class="title"> "{{ item.title }}" </div>
    <div v-if="index === 0" class="price" > ${{ item.price.toLocaleString() }} </div>
    <div class="action-button-container" v-if="index == items.length - 2">
      <button class="action-button" @click="next(true)"> Higher </button>
      <button class="action-button" @click="next(false)"> Lower </button>
      <div class="score"> {{ score }} </div>

    </div>
  </div>
  <div :style="{ display: none }">
    <img :src="items[items.length - 1].artworkUrl" width=1 height=1>
  </div>
</div>

</div>
</template>


<script lang="ts">
// import 'firebase/firestore';
import { collection, query, where, limit, getDocs } from 'firebase/firestore'
import { v4 as uuidv4 } from 'uuid';
import db from '../plugins/firebase'
import Vue from 'vue'
// 	$fire.firestore
export default Vue.extend({
  name: 'Index',
  components: {},
  asyncData() {
    const artwork = collection(db, "artwork")
    const queryRef = query(artwork, where("__name__", ">", uuidv4()), limit(3))

    return getDocs(queryRef).then((querySnapshot) => {
      const items = []
      querySnapshot.forEach((doc) => {
        // doc.data() is never undefined for query doc snapshots
        items.push(doc.data())
      });
      return { items }
    });
  },
  data() {
    return {
      items: [],
      score: 0,
    }
  },
  methods: {

    async next(higher) {
      if (higher === (this.items[1].price > this.items[0].price)) {
        this.score += 1
      } else {
        this.score = 0
      }
      const artwork = collection(db, "artwork")
      const queryRef = query(artwork, where("__name__", ">", uuidv4()), limit(1))

      const querySnapshot = await getDocs(queryRef);
      const items = []
      querySnapshot.forEach((d) => items.push(d.data()))
      this.items = this.items.concat(items).slice(1)
      // .splice(0, 1)
      console.log(this.items)
      // console.log(data.data())
    }
  }
})
</script>

<style>
  * {
    padding: 0;
    margin: 0;
  }
</style>
<style scoped lang="scss">
  .page {
    height: 100vh;
  }
  .container {
    display: flex;
    width: 100%;
    height: 100%;
    flex-direction: row;
    // background: red;
  }
  .item {
    display: flex !important;
    flex-direction: column;
    align-items: center;
    width: 50%;
    height: 100%;
    background-size: contain;
    background-repeat: no-repeat;
    justify-content: center;
    background-position: center;
  }
  .title {
    text-align: center;
    font-size: 2em;
    color: black;
  }
  .price {
    font-size: 4em;
    color: rgb(0, 0, 0);
  }
  .score {
    font-size: 4em;
  }
  .action-button {
    margin: 10px;
    padding: 0em 1em 0em 1em;
    border-radius: 2.5em;
    border: .125em solid black;
    background: none;
    color: black;
    font-size: 2em;
  }
  .action-button-container {
    display: flex;
    align-items: center;
    flex-direction: column;
  }
  a {
    text-decoration: none;
  }
</style>
