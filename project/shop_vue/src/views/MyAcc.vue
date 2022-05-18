<template>
    <div class="personal-area">
        <div class="columns is-multiline">              
                <div class="column is-6">
                    <div class="column is-6" v-if="error_message || success_message">
                        <div class="field">
                            <div class="notification is-danger" v-if="error_message">
                            <p>{{error_message}}</p>
                        </div>
                        <div class="notification is-success" v-if="success_message">
                            <p>{{success_message}}</p>
                        </div>
                    </div>
                    </div>


                    <div class="field">
                        <h1>Логин: <strong>{{username}}</strong></h1>
                        <h1>Почта: <strong>{{email}}</strong></h1>
                    </div>

                    <div class="field">
                        <h1>Введите новый пароль:</h1>
                        <input type="password" class="input" placeholder="Введите новый пароль" v-model="pass1">    
                    </div>
                    <div class="field">
                       <h1>Подтвердите старый пароль:</h1>
                        <input type="password" class="input" placeholder="Введите старый пароль" v-model="pass2">    
                    </div>
                    <div class="field">
                        <button @click="change_pass()" class="button is-dark">Изменить</button>
                    </div>
                </div>
                
                <div class="column is-6">
                    <router-link to="/myacc/myorders" class="button is-success">Мои заказы</router-link>
                </div>

                <div class="column is-12">
                    <button @click="logout()" class="button is-danger">Выход</button>
                </div>
            </div>
        </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'MyAcc',
    data(){
        return{
            username: '',
            pass1: '',
            pass2: '',
            success_message: '',
            error_message: '',
            email: ''
        }
    },
    mounted(){
        this.username = localStorage.getItem("username")
        document.title = `Личный кабинет - ${this.username}`

        this.getData()
    },
    methods:{
        logout(){
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")
            localStorage.removeItem("username")

            this.$store.commit("removeToken")

            this.$router.push('/')
        },
        getData(){
            // console.log(axios.defaults.headers.common["Authorization"])
            axios
                .get('api/users/me/')
                .then(response=>{
                    this.email = response.data.email
                    // console.log(response)
                })
                .catch(error=>{
                    console.log(error)
                })
        },
        change_pass(){
            const formData = {
                new_password: this.pass1,
                current_password: this.pass2
            }

            axios
                .post('api/users/set_password/', formData)
                .then(response=>{
                    // console.log(formData)
                    this.error_message = ''
                    this.success_message = 'Пароль успешно изменен.'
                })
                .catch(erorr=>{
                    this.success_message = ''
                    this.error_message = 'Введен неверный пароль.'
                })
        }
    }
}
</script>

