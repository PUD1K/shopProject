<template>
    <div class="box mb-4">
        <!-- номер ордера -->
        <div class="">
            <h3 class="is-size-4 mb-6">Заказ №{{ order.id }}</h3>
        </div>

        <table class="table is-fullwidth">
            <thead>
                <tr>
                    <th>Товар</th>
                    <th>Стоимость</th>
                    <th>Кол-во</th>
                    <th>Общая стоимость</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="item in order.items" 
                v-bind:key="item.id">
                    <td>
                        <figure>
                            <img style="height: 200px; width: 230px" v-bind:src="item.product ? item.product.get_image : ''">
                        </figure>
                        {{ item.product.name }}
                    </td>
                    <td>{{ item.product.price }} ₽</td>
                    <td>{{ item.quantity }}</td>
                    <td>{{ item.price }} ₽</td>
                </tr>
                
                <tr>
                    <td colspan="3"><strong>Всего к оплате</strong></td>
                    <td>{{ order.paid_amount }} ₽</td>
                </tr>
            </tbody>

        </table>

        <div class="mt-4">
            <h2 class="is-size-5 mb-3">Детали заказа:</h2>
            <div class="columns">
                <div class="column is-half">
                <div class="card">
                    <header class="card-header">
                    <p class="card-header-title">
                        Имя и фамилия:
                    </p>
                    </header>
                    <div class="card-content">
                    <div class="media">
                        <div class="media-content">
                        <p class="title is-4">{{ order.first_name }} {{ order.last_name }}</p>
                        </div>
                    </div>
                    </div>
                </div>
                <div class="card">
                    <header class="card-header">
                    <p class="card-header-title">
                        Адрес:
                    </p>
                    </header>
                    <div class="card-content">
                    <div class="media">
                        <div class="media-content">
                        <p class="subtitle is-6">{{ order.address }}</p>
                        </div>
                    </div>
                    </div>
                </div>
                </div>
                <div class="column is-half">
                <div class="card">
                    <header class="card-header">
                    <p class="card-header-title">
                        Контактная информация:
                    </p>
                    </header>
                    <div class="card-content">
                    <div class="media">
                        <div class="media-content">
                        <p>Почта: {{ order.email }}</p>
                        <p>Номер телефона: {{ order.phone }}</p>
                        </div>
                    </div>
                    </div>
                </div>
                <div class="card">
                    <header class="card-header">
                    <p class="card-header-title">
                        Дата заказа:
                    </p>
                    </header>
                    <div class="card-content">
                    <div class="media">
                        <div class="media-content">
                            <p class="subtitle is-6">{{ parserData(order.created_at) }}</p>
                        </div>
                    </div>
                    </div>
                </div>
                </div>
            </div>
        </div>

        <div class="mt-4">
            <h3 class="is-size-5 mb-4">Статус: <strong>{{ order.status }}</strong></h3>
            
            <template v-if="change_status">
                <div class="field">
                    <div class="control">
                        <div class="select">
                        <select v-model="status" @change="handleChange">
                            <option value="Создан">Создан</option>
                            <option value="Передано в доставку">Передано в доставку</option>
                            <option value="Прибыло в пункт выдачи">Прибыло в пункт выдачи</option>
                            <option value="Выдан клиенту">Выдан клиенту</option>
                        </select>
                        </div>
                    </div>
                </div>
                
                <div class="field is-grouped buttons mt-4" style="display: flex;">
                    <button @click="cancel()" class="button is-primary">Отмена</button>
                    <button @click="changeStatus()" class="button is-dark">Изменить</button>
                </div>
            </template>

            <template v-else>
                <button class="button is-dark" @click="setStatus(!change_status)">Изменить статус</button>
            </template>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "OrderItemManagment",
  data(){
      return{
          total: 0,
          status: this.$props.order.status,
          hidden: true,
          change_status: false
      }
  },
  props: {
      order: Object
  },
  mounted(){
  },
  methods: {
      parserData(data){
        const months = {
            "01": "Январь",
            "02": "Февраль",
            "03": "Март",
            "04": "Апрель",
            "05": "Май",
            "06": "Июнь",
            "07": "Июль",
            "08": "Август",
            "09": "Сентябрь",
            "10": "Октябрь",
            "11": "Ноябрь",
            "12": "Декабрь",
        }

        const year = data.substring(0,4);
        const month = months[data.substring(5,7)] || '';
        const day = data.substring(8,10);
        const time = data.substring(11,19);
        return `${time} - ${day} ${month} ${year}`
      },
      async changeStatus(){
        if(this.status && this.status.length !== 0){
            this.change_status = false;
            const { data } = await axios.post('api/change_status/', {number: this.$props.order.id, status: this.status})
            this.$props.order.status = data.status
            console.log(data.status)
        }
      },
      cancel(){
        this.status = this.$props.order.status
        this.change_status = false
      },
      setStatus(value){
        this.change_status = value
        console.log(this.change_status)
      }
  }
};
</script>
