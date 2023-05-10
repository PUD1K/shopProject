<template>
    
    <div class="column is-12">
         <div class="mt-4">
            <div class="field has-addons mb-4">
                <div class="control">
                    <input type="text" class="input" v-model="number" placeholder="Поиск заказа по номеру">
                </div>

                <div class="control">
                    <button class="button is-dark" @click="getAllOrders()">
                        Поиск
                    </button>  
                </div>
            </div>

            <OrderItemManagment
                v-for="order in orders" 
                v-bind:key ="order.id"
                v-bind:order="order" />
         </div>
     </div>
</template>
 
<script>
 import axios from 'axios'
 import OrderItemManagment from './OrderItemManagment.vue'
 
 export default {
    name: 'AllOrders',
    components:{
        OrderItemManagment,
    },
    data(){
         return{
             orders:[],
             number: ''
         }
    },
    async mounted(){
        document.title = 'Мои заказы'
        await this.getAllOrders()
    },
    methods:{
        async getAllOrders(){
            console.log({number: this.number})
            await axios
                .post('/api/all_orders_list/', {number: this.number})
                .then(response =>{
                    this.orders = response.data
                    // console.log(this.orders)
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