<template>
    <div class="page-product">
        <Breadcrumb :category_name="this.category_name" :category_url="'/' + this.$route.params.category_slug + '/'" :product_name="this.product.name"/>

        <div class="columns is-multiline mt-3 ml-3">
            <div class="column is-5">
                <h1 class="title">{{product.name}}</h1>

                <figure class="image mb-6">
                    <img v-bind:src="product.get_image">
                </figure>
                <p>{{product.description}}</p>
            </div>
            <div class="column is-15">

                <h2 class="subtitle">Характеристики:</h2>
                <div class="field">
                    <p><strong>Стоимость: </strong>{{product.price}} ₽</p>
                </div>
                 <div class="field">
                    <p><strong>Процессор: </strong>{{product.processor}}</p>
                </div>
                 <div class="field">
                    <p><strong>Видеокарта: </strong>{{product.videocart}}</p>
                </div>
                 <div class="field">
                    <p><strong>HDD: </strong>{{product.hdd}}</p>
                </div>
                 <div class="field">
                    <p><strong>RAM: </strong>{{product.ram}}</p>
                </div>

                <div class="field has-addons mt-6">
                    <div class="control">
                        <input type="number" class="input" min="1" v-model="quantity">
                    </div>
                
                    <div class="control">
                        <a class="button is-dark" @click="addToCart">В корзину</a>
                    </div>
                </div>
            </div>  
            
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Breadcrumb from '@/components/Breadcrumb.vue'

export default {
    name: 'ProductDetail',
    data(){
        return{
            product: {},
            category_name: '',
            category_url: '',

            quantity: 1
        }
    },
    components:{
        Breadcrumb
    },
    beforeCreate(){
        this.category_url = this.$route.params.category_slug
    },
    async mounted(){
        await this.getProduct()
        document.title = this.product.name
    },
    methods:{
        async getProduct(){
            const category_slug = this.$route.params.category_slug
            const product_slug = this.$route.params.product_slug

            await axios
                .get(`api/products/${category_slug}/${product_slug}`)
                .then(response =>{
                    this.product = response.data[0]
                    // console.log(this.product)
                    this.category_name = this.product.category
                })
                .catch(error=>{
                    console.log(error)
                })
        },
        addToCart(){
            if(isNaN(this.quantity) || this.quantity < 1){
                this.quantity = 1
            }

            const item = {
                product: this.product, 
                quantity: this.quantity
            }

            this.$store.commit('addToCart', item)
        }
    }
}
</script>

<style>

</style>