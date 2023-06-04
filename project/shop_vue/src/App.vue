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

            <!-- <router-link to="/about" class="navbar-item">Магазины</router-link> -->
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

              <template v-if="$store.state.isStaff">
                <router-link class="button is-primary" to="/managment">Менеджмент</router-link>
              </template>

              <template v-if="$store.state.isAuthentificated">
                <div class="dropdown is-active" style="margin-right: 0.5rem;">
                  <div class="dropdown-trigger">
                      <button class="button" aria-haspopup="true" aria-controls="dropdown-menu"  @click="hidden = !hidden">
                      <span>{{ username }}</span>
                      <span class="icon is-small">
                          <i class="fas fa-angle-down" aria-hidden="true"></i>
                      </span>
                      </button>
                  </div>
                  <div class="dropdown-menu" :class="{'is-hidden': hidden}" role="menu">
                    <div class="dropdown-content">
                      <a class="dropdown-item" @click="$router.push('/myacc'), hidden = !hidden">
                          Личный кабинет
                      </a>
                      <hr class="dropdown-divider">
                      <a class="dropdown-item" @click="logout(), hidden = !hidden">
                          Выход
                      </a>
                    </div>
                  </div>
                </div>

                <!-- <router-link class="button is-link is-light" to="/myacc">Личный кабинет</router-link> -->
              </template>
              
              <template v-if="true">
                <router-link to="/cart" class="button is-dark">
                  <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                  <span>Корзина ({{cartTotalLength}})</span>
                </router-link>
              </template>
            </div>
          </div>

        </div>

      </div>
    </nav>


  <section class="section">
    <router-view/>   
  </section>
  <hr>
  <template v-if="$store.state.shop_name !== 'Название магазина отсутсвует'">
    <footer class="has-text-centered">Магазин техники {{ $store.state.shopName }}.</footer>
  </template>
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
        items: [],
        group: ''
      },
      username: '',

      hidden: true
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
  async mounted(){
    this.cart = this.$store.state.cart
    await this.getUserEmail()
    await this.getPermissions()
    await this.getShopName()
  },
  methods:{
    async getUserEmail(){
      // console.log(axios.defaults.headers.common["Authorization"])
      await axios
          .get('api/users/me/')
          .then(response=>{
              this.username = response.data.username
          })
          .catch(error=>{
              console.log(error)
          })
      },
    async getPermissions(){
        const getPermissionsResponse = await axios.post('api/get_permissions/', {username: this.username});
        console.log(getPermissionsResponse.data['groups']);
        const group = getPermissionsResponse.data['groups'];
        if(group === 'Staff')
          this.$store.commit('setStaff', group);
    },
    logout(){
          axios.defaults.headers.common["Authorization"] = ""

          localStorage.removeItem("token")
          localStorage.removeItem("username")

          this.$store.commit("removeToken")
          this.$store.commit("offStaff")
          this.$store.commit("removeUsername")

          this.$router.push('/')
      },
    async getShopName(){
       const { data } = await axios.get('api/get_shop_name/')
       this.$store.commit('setShopName', data.shop_name)
    }
}
}
</script>


<style lang="scss">
@import '../node_modules/bulma';

</style>
