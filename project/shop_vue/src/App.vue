<template>
<div class id="wrapper">
    <nav class="navbar is-white has-shadow" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu">
        <div class="is-size-5">
          <div class="navbar-start">
            <a class="navbar-brand">
              <router-link to="/" class="navbar-item">Главная</router-link>
            </a>

            <router-link to="/about" class="navbar-item">Магазины</router-link>
            <div class="navbar-item">
            <form method="get" action="/search">
              <div class="field has-addons">
                <div class="control">
                 <input type="text" class="input" placeholder="Поиск по сайту" name="query">
                </div>

                <div class="control">
                  <button class="button is-dark">
                    Поиск
                  </button>  
                </div>
              </div>
              </form>
              </div> 

          </div>
        </div>

        <div class="navbar-end">
          <!-- <router-link class="navbar-item" to='about/'>О нас</router-link>  -->
        
          <div class="navbar-item">
            <div class="buttons">

              <template v-if="!$store.state.isAuthentificated">
                <router-link class="button is-primary" to="/login">Вход</router-link>
              </template>

              <template v-else>
                <router-link class="button is-light" to="/myacc">Личный кабинет</router-link>
              </template>
              
              <router-link to="/cart" class="button is-dark">
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                <span>Корзина ({{cartTotalLength}})</span>
              </router-link>
            </div>
          </div>

        </div>

      </div>
    </nav>


  <section class="section">
    <router-view/>   
  </section>
  <hr>
  <footer class="has-text-centered">Магазин техники MyShop.</footer>
  <hr>
</div>
</template>

<script>
import axios from 'axios'

export default {
  data(){
    return {
      categories: [],
      cart: {
        items: []
      }
    }
  },
  beforeCreate(){
    this.$store.commit('initializeStore')
    // если есть токен, то добавляем его в headers
    const token = this.$store.state.token
    
    if(token){
      axios.defaults.headers.common["Authorization"] = "Token " + token
    }else{
      axios.defaults.headers.common["Authorization"] = ""
    }
  },
  computed:{
    // получаем общее кол-во товара в корзине
    cartTotalLength(){
      let totalLength = 0
      for (let i = 0; i < this.cart.items.length; i++){
        totalLength += this.cart.items[i].quantity
      }

      return totalLength
    }
  },
  mounted(){
    this.username = localStorage.getItem("username")

    this.cart = this.$store.state.cart
    // console.log( this.$store.state.cart)
  },
  methods:{
    
  }
}
</script>


<style lang="scss">
@import '../node_modules/bulma';

</style>
