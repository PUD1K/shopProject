<template>
  <div>
            <nav class="breadcrumb has-arrow-separator">
                <ul class="container">
                    <li><router-link to='/' class="has-text-dark">Каталог</router-link></li>
                    <li v-if="query"><a  class="has-text-grey">{{query}}</a></li>
 
                    <li v-if="product_name"><router-link :to='category_url' class="has-text-dark">{{category_name}}</router-link></li> 
                    <li v-else-if="category_name"><a class="has-text-grey">{{category_name}}</a></li> 

                    <li v-if="product_name"><a class="has-text-grey">{{product_name}}</a></li> 
                </ul>
            </nav>
        </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Breadcrumb",
    props:{
        category_name: '',
        category_url: '',
        product_name: '',
        query: ''
    },
    methods: {
        getCategorySlug(){
            if(typeof this.$route.params.category_slug != 'undefined'){
                const category_slug = this.$route.params.category_slug

                axios
                    .get(`/api/products/${category_slug}`)
                    .then(response=>{
                        this.category = response.data
                        console.log(this.category)
                    })
                    .catch(error=>{
                        console.log(error)
                    })
            }
        },
        getProductSlug(){
            if(typeof this.$route.params.product_slug != 'undefined'){
                const product_slug = this.$route.params.product_slug
                const category_slug = this.$route.params.category_slug

                axios
                    .get(`/api/products/${category_slug}/${product_slug}`)
                    .then(response=>{
                        this.product = response.data
                    })
                    .catch(error=>{
                           console.log(error)
                    })
            }
        },
    }
}
</script>

<style>

</style>