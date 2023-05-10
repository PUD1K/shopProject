<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <Breadcrumb :query="query"/>

                <div class="column is-12">
                    <h1 class="is-size-4"><strong>Поиск</strong></h1>
                    <h2 class="is size-5">Найдено: {{products.length}}</h2>
                </div>

            <!-- Начало сортировки -->
                <div class="columns is-multiline">
                    <template v-if="products.length">
                        <div class="column is-3">
                            <div class="dropdown is-active">
                                <div class="dropdown-trigger">
                                    <button class="button" aria-haspopup="true" aria-controls="dropdown-menu"  @click="hidden = !hidden">
                                    <span>Сортировка</span>
                                    <span class="icon is-small">
                                        <i class="fas fa-angle-down" aria-hidden="true"></i>
                                    </span>
                                    </button>
                                </div>
                                <div class="dropdown-menu" :class="{'is-hidden': hidden}" aria-hidden="true" role="menu">
                                    <div class="dropdown-content">
                                    <a class="dropdown-item" @click="select = '-price', hidden = !hidden">
                                        Сначала дорогие
                                    </a>
                                    <a class="dropdown-item" @click="select = 'price', hidden = !hidden">
                                        Сначала недорогие
                                    </a>
                                    <a class="dropdown-item" @click="select = '-date_added', hidden = !hidden">
                                        Сначала новые
                                    </a>
                                    <a class="dropdown-item" @click="select = 'date_added', hidden = !hidden">
                                        Сначала старые
                                    </a>
                                    <a class="dropdown-item" @click="select = '-sales', hidden = !hidden">
                                        Сначала самые продаваемые
                                    </a>
                                    <a class="dropdown-item" @click="select = 'sales', hidden = !hidden">
                                        Сначала самые непродаваемые
                                    </a>
                                    <hr class="dropdown-divider">
                                    <a class="dropdown-item" @click="select = '', select_param ='Сортировка', hidden = !hidden">
                                        Нет
                                    </a>
                                    </div>
                                </div>
                            </div>
                <!-- Конец сортировки -->
                            <hr>
                            <div class="column is-8 box">
                                <strong>Категория</strong>
                                <div
                                    v-for="cat in categories"
                                    v-bind:key="cat"
                                >
                                    <label class="checkbox ml-1">
                                        <input type="checkbox" :value="cat" v-model="filterCategories">
                                        {{cat}}
                                    </label>
                                </div>
                            </div>  
                            <div class="column is-8 box">
                                <strong>Тип</strong>
                                <div
                                    v-for="sub in subcategories"
                                    v-bind:key="sub"
                                >
                                    <label class="checkbox ml-1">
                                        <input type="checkbox" :value="sub" v-model="filterSubcategories">
                                        {{sub}}
                                    </label>
                                </div>
                            </div>                 

                            <div class="column is-8 box">
                                <strong>Производитель</strong>
                                <div
                                    v-for="manuf in manufacturers"
                                    v-bind:key="manuf"
                                >
                                    <label class="checkbox ml-1">
                                        <input type="checkbox" :value="manuf" v-model="filterManufacturer">
                                        {{manuf}}
                                    </label>
                                </div>
                            </div>

                            <div class="column is-6">
                                <h1 class="">Цена:</h1>
                                <input v-model="price_filter_1" class="input mt-2 ml-1" type="text" placeholder="От" name="price">
                                <input v-model="price_filter_2" class="input mt-2 ml-1" type="text" placeholder="До" name="price">

                                <button type="button" @click="getFilter" class="button is-light mt-5">Применить</button>
                            </div>
                            <hr>
                        </div>
                    </template>
            <!-- <AsideMenu class="is-2"/> -->
                <ProductItem
                    v-for="product in products"
                    v-bind:key="product.id"
                    v-bind:product="product"/>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import AsideMenu from '@/components/AsideMenu.vue'
import ProductItem from "@/components/ProductItem.vue"
import Breadcrumb from "../components/Breadcrumb.vue"

export default {
    name: 'Search',
    components:{
        ProductItem,
        AsideMenu,
        Breadcrumb,
    },
    data(){
        return{
            products:[],
            query: '',
            // параметры для фильтров
            categories: [],
            subcategories: [],
            manufacturers: [],
            // параметры для checkbox
            filterCategories:[],
            filterSubcategories: [],
            filterManufacturer: [],
            price_filter_1:'',
            price_filter_2: '',

            select: '',
            hidden: true
        }
    },
    async mounted(){
        // получаем данные из url формата query={name}
        let url = window.location.search.substring(1)
        let params = new URLSearchParams(url)
        if(params.get('query')){
            // получаем {name}
            this.query = params.get('query')
            await this.Search()
            this.getAllParams()
        }

        document.title = `Поиск - ${this.query}`
    },
    methods:{
        // динамически добавляем параметры к url, если была произведена сортировка
        async Search(param){
            let url = `api/products/?search=${this.query}`
            // добавляем параметры
            if(param){
                url += param
                // console.log(url)
            }            
            
            await axios
                .get(url)
                .then(response =>{
                    this.products = response.data

                })
                .catch(error=>{
                    console.log(error)
                })
        },
        // получаем параметры из object всех товаров на странице
        async getAllParams(){
            this.products.forEach((element)=> {
                if(element.category){
                    this.categories.push(element.category)
                }
                if(element.subcategory){
                    this.subcategories.push(element.subcategory)
                }
                if(element.manufacturer){
                    this.manufacturers.push(element.manufacturer)
                }
            })
            this.categories = this.categories.filter((elem, index, array) => array.indexOf(elem) == index)
            this.subcategories = this.subcategories.filter((elem, index, array) => array.indexOf(elem) == index)
            this.manufacturers = this.manufacturers.filter((elem, index, array) => array.indexOf(elem) == index)
        },
        // получаем фильтры, полученные из checkbox 
        getFilter(){
            let param = '&'
            if(this.filterCategories){
                this.filterCategories.forEach((cat)=>{
                    param+=`category_name=${cat}&`
                })
            }
            if(this.filterManufacturer){
                this.filterManufacturer.forEach((manuf)=>{
                    param+=`manufacturer_name=${manuf}&`
                })
            }
            if(this.filterSubcategories){
                this.filterSubcategories.forEach((sub)=>{
                    param+=`subcategory_name=${sub}&`
                })
            }
            if(this.price_filter_1 >= 0 && this.price_filter_2 > 0){
                param += `min_price=${this.price_filter_1}&max_price=${this.price_filter_2}`
            }
            if(this.select){
                param += `ordering=${this.select}`
            }
            // после получения фильтров заново отправляем запрос на сервер
            this.Search(param)
        }
    }
}
</script>
