<template>
  <div class="page-cart">
    <div class="column is-multiline">
      <div class="column is-12">
        <h1 class="title">Корзина</h1>
      </div>

      <div class="column is-12 box">
        <table class="table is-fullwidth" v-if="cartTotalLength">
          <thead>
            <tr>
              <th>Товар</th>
              <th>Цена</th>
              <th>Кол-во</th>
              <th>Всего</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            <CartItem
              v-for="item in cart.items"
              v-bind:key="item.product.id"
              v-bind:initialItem="item"
              v-on:removeFromCart="removeFromCart"
            />
          </tbody>
        </table>

        <p v-else>У вас нет товаров в корзине.</p>
      </div>

      <div class="column is-12 box">
          <h2 class="subtitle">Итог</h2>

          <strong>{{ cartTotalPrice.toFixed(2)}} ₽</strong>, {{ cartTotalLength }} товаров
          <hr>

          <router-link to="/cart/checkout" class="button is-dark" v-if="cartTotalLength">Перейти к оформлению</router-link>
      
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import CartItem from '@/components/CartItem.vue'

export default {
    name: 'Cart',
    components:{
        CartItem
    },
    data() {
        return{
            cart:{
                items: []
            }
        }
    },
    mounted(){
        document.title = 'Корзина'
        this.cart = this.$store.state.cart
    },
    methods:{
    //items = items.фильтр(все элементы, кроме тех, которые передаем в параметр), т.о. удаляем выбранный элемент из cart 
        removeFromCart(item){
          this.cart.items = this.cart.items.filter(i => i.product.id !== item.product.id)
        }
    },
    computed:{
        cartTotalLength(){
            return this.cart.items.reduce((acc, item) =>{
                return acc += item.quantity
            }, 0)
        },
        cartTotalPrice(){
            return this.cart.items.reduce((acc, item) =>{
                return acc += item.product.price * item.quantity
            }, 0)
        }
    }
}
</script>

