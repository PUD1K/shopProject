<template>
   <div class="column is-12">
        <div class="mt-4">
            <OrderSummary
                v-for="order in orders" 
                v-bind:key ="order.id"
                v-bind:order="order" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import OrderSummary from '@/components/OrderSummary.vue'

export default {
    name: 'MyOrders',
    components:{
        OrderSummary,
    },
    data(){
        return{
            orders:[]
        }
    },
    mounted(){
        document.title = 'Мои заказы'
        this.getMyOrders()
    },
    methods:{
        getMyOrders(){
            axios
                .get('/api/orders/')
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