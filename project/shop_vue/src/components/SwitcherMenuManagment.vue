<template>
    <template v-if="tab === 'Статистика'">
        <Stats/>
    </template>
    <template v-if="tab === 'Заказы'">
        <AllOrders/>
    </template>
</template>

<script>
import axios from 'axios'
import Stats from '../views/Stats.vue'
import AllOrders from '../components/AllOrders.vue'

export default {
    name:'SwitcherMenu',
    props:{
        tab: String,
    },
    components:{
        Stats,
        AllOrders
    },
    data(){
        return{
            
        }
    },
    mounted(){
        console.log(this.tab)
    },
    methods:{
        
    }
}
</script>

<style>

</style>