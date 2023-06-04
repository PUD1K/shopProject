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
        <div class="bottomright">
            <h3 class="is-size-5">Статус: <strong>{{ order.status }}</strong></h3>
        </div>
    </div>
</template>

<script>
export default {
  name: "OrderSummary",
  data(){
      return{
          total: 0,
      }
  },
  props: {
      order: Object
  },
  mounted(){
  },
  methods: {
      
  }
};
</script>
