<template>
    <aside class="menu">
        <p class="menu-label">Категории</p>
        <hr class="navbar-divider">
        <ul class="menu-list">
            <li v-for="category in categories"
            v-bind:key="category.id"
            v-bind:category="category">
                <router-link v-bind:to="category.get_absolute_url">{{category.name}}</router-link>
            </li>
        </ul>
  </aside>
</template>

<script>
import axios from 'axios'

export default {
    name:'AsideMenu',
    data(){
        return{
            categories: []
        }
    },
    mounted(){
        this.getCategories()
    },
    methods:{
        getCategories(){
            axios
                .get('api/all-categories/')
                .then(response =>{
                    this.categories = response.data
                })
                .catch(error=>{
                    console.log(error)
                })
        }
    }
}
</script>

<style>

</style>