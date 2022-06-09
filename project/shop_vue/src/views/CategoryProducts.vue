<template>
  <div class="category-products">    
    <!--  -->
    <div class="columns is-multiline">
            <Breadcrumb :category_url="'/' + this.$route.params.category_slug + '/'" :category_name="this.category.name"/>

        <div class="column is-12">
            <h1 class="is-size-2 has-text-centered">{{category.name}}</h1>
            <h2 class="has-text-centered mr-2 mb-2">Товаров: {{category.products.length}}</h2>

        </div>

        <div class="columns is-multiline">
            <div class="column is-3">
                <!-- Начало сортировки: -->
                <!-- <div class="column is-8"> -->
                    <div class="dropdown is-active">
                        <div class="dropdown-trigger">
                            <button class="button" aria-haspopup="true" aria-controls="dropdown-menu"  @click="hidden = !hidden">
                            <span>{{select_param}}</span>
                            <span class="icon is-small">
                                <i class="fas fa-angle-down" aria-hidden="true"></i>
                            </span>
                            </button>
                        </div>
                        <div class="dropdown-menu" :class="{'is-hidden': hidden}" aria-hidden="true" role="menu">
                            <div class="dropdown-content">
                            <a class="dropdown-item" @click="select = '-price', select_param ='Сначала дорогие' ,hidden = !hidden">
                                Сначала дорогие
                            </a>
                            <a class="dropdown-item" @click="select = 'price', select_param ='Сначала дешевые', hidden = !hidden">
                                Сначала недорогие
                            </a>
                            <a class="dropdown-item" @click="select = '-date_added', select_param ='Сначала новые', hidden = !hidden">
                                Сначала новые
                            </a>
                            <a class="dropdown-item" @click="select = 'date_added', select_param ='Сначала старые', hidden = !hidden">
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
                    <!-- </div> -->
                </div>
                <!-- Конец сортировки -->
                <hr>
                <!-- Фильтры: -->
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
                        v-for="brand in brands"
                        v-bind:key="brand"
                    >
                        <label class="checkbox ml-1">
                            <input type="checkbox" :value="brand" v-model="filterBrands">
                            {{brand}}
                        </label>
                    </div>
                </div>

                <div class="column is-8 box">
                    <h1 class="">Цена:</h1>
                    <input v-model="price_filter_1" class="input mt-2 ml-1" type="text" placeholder="От" name="price">
                    <input v-model="price_filter_2" class="input mt-2 ml-1" type="text" placeholder="До" name="price">

                </div>
                <div class="column is-6">
                    <button type="button" @click="getFilter" class="button is-light mt-5">Применить</button>
                </div>
                <hr>
            </div>
            
            <!--  конец фильтров-->
                    <ProductItem 
                        v-for="product in category.products"
                        v-bind:key="product.id"
                        v-bind:product="product"
                    />
         </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProductItem from '@/components/ProductItem.vue'
import Breadcrumb from '@/components/Breadcrumb.vue'

export default {
    name: 'CategoryProducts',
    data(){
        return{
            category: {
                products:[]
            },
            price_filter_1:'',
            price_filter_2: '',

            brands:[],
            subcategories:[],
            filterBrands:[],
            filterSubcategories:[],

            select: '',
            select_param: 'Сортировка',
            hidden: true
        }
    },
    components:{
    ProductItem,
    Breadcrumb,
},
    // запускается при каждом изменении свойства(в данной случае route)
    watch:{
        $route(to, from){
            if(to.name == "CategoryProducts"){
                this.getProducts()
            }
        }
    },
    async mounted(){
        await this.getProducts()
        this.getSubcategories()
        this.getBrands()
        document.title = this.category.name
    },
    methods:{
        async getProducts(param){
            const category_slug = this.$route.params.category_slug
            let url = `api/products/${category_slug}/`

            if (param){
                url += param
                // console.log(url)
            }

            await axios
                .get(url)
                .then(response => {
                    this.category = response.data[0]
                    document.title = `Товары категории ${this.category.name}`
                })
                .catch(error =>{
                    console.log(error)
                })
        },
        // методы фильтрации
        getBrands(){
            let brands = []
            this.category.products.forEach((product)=>{
                brands.push(product.manufacturer)
            })
            var uniqueBrands = brands.filter((elem, index,array) => array.indexOf(elem) == index)
            this.brands = uniqueBrands
        },
        getSubcategories(){
            let subcategories = []
            this.category.products.forEach((product)=>{
                subcategories.push(product.subcategory)
            })
            var uniqueSubacetgories = subcategories.filter((elem, index,array) => array.indexOf(elem) == index)
            this.subcategories = uniqueSubacetgories
        },
        getFilter(){
            let param = '?'
            if(this.filterBrands){
                this.filterBrands.forEach((brand)=>{
                    param+=`brand=${brand}&`
                })
            }
            if(this.filterSubcategories){
                this.filterSubcategories.forEach((sub)=>{
                    param+=`sub=${sub}&`
                })
            }
            if(this.price_filter_1 >= 0 && this.price_filter_2 > 0){
                param += `price=${this.price_filter_1}-${this.price_filter_2}&`
            }
            if(this.select){
                param += `ordering=${this.select}`
            }
            this.getProducts(param)
        }
    }
}
</script>

<style>

</style>