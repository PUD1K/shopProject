<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Регистрация</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Логин</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Пароль</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="field">
                        <label>Повтор пароля</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password2">
                        </div>
                    </div>

                     <div class="field">
                        <label>E-mail</label>
                        <div class="control">
                            <input type="text" class="input" v-model="email">
                        </div>
                    </div>


                    <div class="notification is-danger" v-if="errors.length">
                        <p 
                        v-for="error in errors" 
                        v-bind:key="error">
                        {{error}}</p> 
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Регистрация</button>
                        </div>
                    </div>

                    <hr>

                    Или <router-link to="/login">нажмите здесь</router-link> для логина.   
                </form>
            </div>
        </div>
    </div>
</template>
// submit - обработчик события отправки формы
<script>
import axios from 'axios'

export default {
    name: 'SignUp',
    data() {
        return{
            username:'',
            password: '',
            password2: '',
            email: '',
            errors: []
        }
    },
    mounted(){
        document.title = 'Регистрация'
    },
    methods:{
        submitForm(){

            this.errors = []

            if(this.username === ''){
                this.errors.push('Имя пропущено.')
            }
            if(!this.email.includes('@')){
                this.errors.push('Неверный формат e-mail.')
            }
            if(this.password.length < 6){
                this.errors.push('Ваш пароль должен содержать не менее 6 символов.')
            }
            if(this.password2 !== this.password){
                this.errors.push('Ваши пароли не совпадают.')
            }
            
            if(!this.errors.length){
                const formData = {
                    username: this.username,
                    password: this.password,
                    email: this.email
                }

                axios 
                    .post("api/users/", formData)
                    .then(response=>{
                        this.$router.push('/login')
                    })
                    .catch(error=>{
                        console.log(error)
                    })
            }
            
        }
    }
}
</script>
