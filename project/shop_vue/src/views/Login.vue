<template>
    <div class="page-login">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Авторизация</h1>

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

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{error}}</p> 
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Войти</button>
                        </div>
                    </div>

                    <hr>

                    Или <router-link to="/signup">нажмите здесь</router-link> чтобы зарегистрироваться.   
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Login',
    data() {
        return{
            username:'',
            password:'',
            errors:[]
        }
    },
    mounted(){
        document.title = 'Авторизация'
    },
    methods:{
        async submitForm(){
            this.errors = []
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")

            const formData = {
                username: this.username,
                password: this.password
            }
            
            await axios
                .post('api/token/login/', formData)
                .then(response => {
                    const token = response.data.auth_token
                    this.$store.commit("setToken", token)
                    axios.defaults.headers.common["Authorization"] = "Token " + token
                    localStorage.setItem("token", token)
                    localStorage.setItem("username", formData.username)
                })
                .catch(error => {
                    this.errors.push('Неверное имя пользователя или пароль.')
                    console.log(error)
                })
            const getPermissionsResponse = await axios.post('api/get_permissions/', {username: this.username});
            const group = getPermissionsResponse.data['groups'];
            this.$store.commit('setStaff', group);
            this.$router.push('/')
        }
    }
}
</script>
