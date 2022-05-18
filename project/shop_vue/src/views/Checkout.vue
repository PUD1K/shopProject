<template>
    <div class="page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Оформление заказа</h1>
            </div>

            <div class="column is-12 box">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Товар</th>
                            <th>Стоимость</th>
                            <th>Кол-во</th>
                            <th>Общая сумма</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr 
                            v-for="item in cart.items"
                            v-bind:key="item.product.id"
                        >
                            <td>{{item.product.name}}</td>
                            <td>{{item.product.price}} ₽</td>
                            <td>{{item.quantity}}</td>
                            <td>{{getItemTotal(item).toFixed(2)}} ₽</td>
                        </tr>
                    </tbody>

                    <tfoot>
                        <tr>
                            <td colspan="2"><strong>Всего к оплате</strong></td>
                            <td>{{cartTotalLength}}</td>
                            <td>{{cartTotalPrice.toFixed(2)}} ₽</td>
                        </tr>
                    </tfoot>
                </table>
            </div>

            <div class="column is-12 box">
                <h2 class="subtitle">Детали заказа</h2>
            
                <p class="has-text-grey mb-4">* Все поля должны быть заполнены</p>

                <div class="columns is-multiline">

                    <div class="column is-6">
                        <div class="field">
                            <label>Имя*</label>
                            <div class="control">
                                <!-- v-model тут значит, что значение с input будет передано в first_name -->
                                <input type="text" class="input" v-model="first_name">
                            </div>
                        </div>

                        <div class="field">
                            <label>Фамилия*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="last_name">
                            </div>
                        </div>

                        <div class="field">
                            <label>E-mail*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="email">
                            </div>
                        </div>

                        <div class="field">
                            <label>Телефон*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="phone">
                            </div>
                        </div>
                    </div>

                    <div class="column is-6">
                        <div class="field">
                            <label>Адрес*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="address">
                            </div>
                        </div>

                    </div>
                   
                </div>
                 
                    <div class="notification is-danger mb-4" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{error}}</p>
                    </div>

                    <template v-if="cartTotalLength">
                        <hr> 

                        <button class="button is-dark" @click="submitForm">Оплатить</button>
                    </template>
            </div>
        </div>
    </div>

</template>

<script>
import axios from 'axios'
export default {
    name: 'Checkout',
    data(){
        return {
            cart:{
                items:[]
            },
            first_name: '',
            last_name: '',
            email: '',
            phone: '',
            address:'',
            zipcode: '',
            place: '',
            errors: []
        }
    },
    mounted(){
        document.title = "Оформление заказа"

        this.cart = this.$store.state.cart
    },
    methods:{
        getItemTotal(item){
            return item.quantity * item.product.price
        },
        submitForm(){
            this.errors = []
            
            if(this.first_name === '') {
                this.errors.push('Имя пропущено!')
            }

            if(this.last_name === '') {
                this.errors.push('Фамилия пропущена!')
            }
            
            if(this.email === '') {
                this.errors.push('E-mail пропущен!')
            }
            
            if(this.phone === '') {
                this.errors.push('Телефон пропущен!')
            }
            
            if(this.address === '') {
                this.errors.push('Адрес пропущен!')
            }
            
            if(!this.errors.length){
                // создаем stripe токен на основе данных корзины 
                this.TokenHandler()
            }
        },
        async TokenHandler(){
            const items = []
            // помещаем в items все товары из корзины
            for (let i = 0; i<this.cart.items.length; i++){
                const item = this.cart.items[i]
                const obj = {
                    product: item.product.id,
                    quantity: item.quantity,
                    price: item.product.price * item.quantity
                }
                items.push(obj)
            }
            // парсим данные для сериализатора
            const data = {
                'first_name': this.first_name,
                'last_name': this.last_name,
                'email': this.email,
                'address': this.address,
                'phone': this.phone,
                'items': items,
            }
            // console.log(data)

            // используем пост запрос, т.к. нам нужно ЗАПИСАТЬ данные из data в json по http в api/v1/checkout
            await axios
                .post('/api/checkout/', data)
                // если все ок, тогда переадресуем на страничку об успехе
                .then(response => {
                    this.$store.commit('clearCart')
                    this.$router.push('/cart/success')
                })
                .catch(error => {
                    this.errors.push('Something weit wrong. Please try again')

                    console.log(error)
                })

        }
    },
    computed:{
        //аналогично: acc = 0
      //            foreach(item in this.cart.items): 
      //              acc += item.quantity
      //            return acc
    //   общее кол-во товаров
      cartTotalLength(){
            return this.cart.items.reduce((acc, item) => {
                return acc += item.quantity
            }, 0)
        },
        // тотал прайс всех товаров
        cartTotalPrice(){
            return this.cart.items.reduce((acc, item) => {
                return acc += item.product.price * item.quantity
            }, 0)
        }
    }
}
</script>