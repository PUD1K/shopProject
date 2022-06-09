<template>
  <div class="home">
    <!-- <Slidebar/> -->
    
    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-1 has-text-centered"><strong>TIMURSHOP</strong></h2>
      </div>
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">Новинки:</h2>
      </div>
      <div class="column is-2">
        <AsideMenu class="box"/>
      </div>

    <ProductItem
        v-for="product in NewProducts"
        v-bind:key="product.id"
        v-bind:product="product" />
        </div>

  </div>
</template>

<script>
import axios from 'axios'
import ProductItem from '@/components/ProductItem'
import AsideMenu from '@/components/AsideMenu'

export default {
  name: 'HomeView',
  data(){
    return{
      NewProducts: []
    }
  },
  components:{
    ProductItem,
    AsideMenu
  },
  mounted(){
    this.getNewItems()

    document.title = 'Главная'

  },
  methods:{
    getNewItems(){ 
      axios 
        .get('api/new-products/')
        .then(response =>{
          this.NewProducts = response.data
          // console.log(this.NewProducts)
        })
        .catch(error =>{
          console.log(error)
        })
    }
    }
  
}
</script>

<style>

</style>