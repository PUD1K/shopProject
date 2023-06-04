<template>
    <div class="page-product">
        <Breadcrumb :category_name="this.category_name" :category_url="'/' + this.$route.params.category_slug + '/'" :product_name="this.product.name"/>
        
        <div class="columns is-multiline mt-3 ml-3 box">
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
        <div class="columns is-multiline mt-3 ml-3 box">
            <!-- Статы -->
            <div class="column is-3">
                <div class="field box">Средняя оценка: <strong>{{avgScore}}</strong></div>

                <div class="field box">
                    <p>Покупок этого товара: <strong>{{product.sales}}</strong> </p>
                </div>
            </div>
            <div class="column is-12">
                <!-- форма заполнения комментария -->
                <div class="field">
                <label>Оценка</label>
                    <div class="control">
                        <input type="number" class="input is-info" style="width: 4%"  placeholder="Ваша оценка от 1 до 5" min="1" max="5" v-model="score">
                    </div>
                </div>
                <div class="field">
                    <label>Заголовок</label>
                    <div class="control">
                        <input type="text" class="input is-info" style="width: 40%" placeholder="Заголовок" v-model="heading">
                    </div>
                </div>
                <div class="field">
                    <label>Текст отзыва</label>
                    <div class="control">
                        <textarea type="text" class="textarea is-info" style="min-width: 0%; width: 40%" placeholder="Основное" rows="10" v-model="text"></textarea>
                    </div>
                </div>

                 <div class="control">
                    <a v-if="loading_comments" class="button is-info" @click="createComment">Оставить отзыв</a>
                    <a v-else class="button is-info is-loading">Loading</a>
                </div>

                <!-- обработчик ошибок -->
                <div class="field mt-3" v-if="errors_message.length !== 0"> 
                    <div class="notification is-danger" v-if="errors_message.length !== 0">
                        <p v-for="error in errors_message"
                        v-bind:key="error.id"
                        >{{error}}</p>
                    </div>
                </div>
            </div>

            <div class="column is-6">
                <div class="field">
                    <p>Отзывы: <strong>{{comments_quantity}}</strong></p>
                </div>

                <!-- вывод комментариев -->
                <div class="column is-12 box"
                v-for="comment in product.comments"
                v-bind:key="comment.id"
                v-bind:comment="comment"
                >
                    <div class="field">
                        <p class="is-size-5"> {{comment.user}}</p>
                    </div>
                    <div class="field">
                        <p><strong>Оценка: </strong></p> {{comment.score}}/5
                    </div>
                    <div class="field">
                        <p><strong>Заголовок: </strong></p> {{comment.heading}}
                    </div>
                    <p><strong>Текст отзыва: </strong></p> {{comment.text}}
                    <div class="has-text-right" v-if="comment.user === username">
                        <button class="delete" @click="deleteComment(comment.id)"></button>
                    </div>


                </div>
            </div>
        </div>

    <div class="footer">
        <p class="is-size-3">Вам также может понравится</p>
        <hr>
        <div class="columns is-multiline">
                <ProductSmallItem
                v-for="product in recommendated_products"
                v-bind:key="product.id"
                v-bind:product="product" />
        </div>
    </div>
    
    </div>
</template>

<script>
import axios from 'axios'
import Breadcrumb from '@/components/Breadcrumb.vue'
import ProductSmallItem from '@/components/ProductSmallItem.vue'

export default {
    name: 'ProductDetail',
    data(){
        return{
            product: {},
            category_name: '',
            category_url: '',
            recommendated_products: {},
            quantity: 1,

            comments_quantity: 0,
            username: '',
            score: 1,
            heading: '',
            text: '',

            loading_comments: true,
            errors_message: [],
            avgScore: '',
        }
    },
    components:{
        Breadcrumb,
        ProductSmallItem
    },
    beforeCreate(){
        this.category_url = this.$route.params.category_slug
    },
    // запускается при каждом изменении свойства(в данной случае route)
    watch:{
        $route(to, from){
            if(to.name == "ProductDetail"){
                this.getProduct()
            }
        }
    },
    async mounted(){
        await this.getProduct()
        this.username = localStorage.getItem('username')
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
                    this.category_name = this.product.category
                    this.comments_quantity = this.product.comments.length
                    this.getRecommendations()
                    this.avgScore = this.getAvgScore()
                })
                .catch(error=>{
                    console.log(error)
                })
        },
        addToLatestViews(){
            if(localStorage.getItem('latestViews')){
                let getItem = [JSON.parse(localStorage.getItem('latestViews'))]
                // if(Object.keys(getItem).length <= 5){

                // }
                getItem.push(JSON.stringify(this.product))
                localStorage.setItem("latestViews", getItem)
            }
        },
        addToCart(){
            if(isNaN(this.quantity) || this.quantity < 1){
                this.quantity = 1
            }

            const item = {
                product: this.product, 
                quantity: this.quantity
            }
            console.log(item)
            this.$store.commit('addToCart', item)
        },
        getRecommendations(){
            // рекомендации по типу(игровые, бюджетные, только Apple, etc)
            const formData = {
                query: this.product.type,
                nonQuery: this.product.name
            }
            axios
                .post('api/products/recommendations/', formData)
                .then(response=>{
                    this.recommendated_products = response.data
                })
                .catch(error=>{
                    console.log(error)
                })
        },
        async createComment(){          
            const formData = {
                product_id: this.product.id,
                user: this.username,

                score: this.score,
                heading: this.heading,
                text: this.text
            }
            this.errors_message = []
            
            function checkComments(comment, username){
                return comment.user === username
            }
            
            // проверка, что данный пользователь еще не оставил комментарий
            let ifCommentExist = false
            this.product.comments.forEach(element => {  
                if(checkComments(element, this.username)){
                    ifCommentExist = true
                }
            })

            // если юзер не оставлял комментарии
            if(!ifCommentExist){
                if(formData.heading.length <= 10){
                    this.errors_message.push('Заголовок должен содержать не менее 10 символов.')
                }
                if(formData.text.length <= 30){
                    this.errors_message.push('Основная часть комментария должна содержать не менее 30 символов.')    
                }
                else{
                this.loading_comments = false
                await axios 
                    .post('api/products/comment/', formData)
                    .then(response=>{
                        this.score = ''
                        this.heading = ''
                        this.text = ''
                        this.getProduct()
                    })
                    .catch(error=>{
                        console.log(error)
                    })
                this.loading_comments = true
                }
            }
            else{
                this.errors_message.push('Вы уже оставляли комментарий на этот товар.')
                console.log(this.errors_message)
            }
        },
        // удаление комментариев
        deleteComment(comment_id){
            if(confirm("Вы действительно хотите удалить комментарий?")){
                axios
                    .delete(`api/comments/delete/${comment_id}`)
                    .then(response =>{
                        this.getProduct()
                    })
                    .catch(error=>{
                        console.log(error)
                    })   
            }         
        },
        getAvgScore(){
            if(this.product.comments.length === 0){
                return 'У этого товара еще нет оценок.'
            }
            let count = 0 
            this.product.comments.forEach(elem =>{
                count += elem.score
            })
            return (count/this.product.comments.length).toFixed(2)
        }
    }
}
</script>

<style>
.image img {
  object-fit: scale-down;
  width:500px;
  height: 500px;
}
</style>