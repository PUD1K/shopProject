<template>
    <template v-if="tab === 'Мои заказы'">
        <MyOrders/>
    </template>
    <template v-if="tab === 'Настройки аккаунта'">
        <MyAccSetting/>
    </template>
</template>

<script>
import axios from 'axios'
import MyOrders  from '@/views/MyOrders.vue';
import MyAccSetting from './AccSettings.vue'

export default {
    name:'SwitcherMenu',
    props:{
        tab: String,
    },
    components:{
        MyOrders,
        MyAccSetting
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