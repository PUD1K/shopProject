<template>
    <div class="">
      <div class="is-flex is-justify-content-center is-align-items-center">
        <div class="has-text-centered"  style="width: 600px; height: 600">
          <h1 class="is-size-3">Продаваемость категорий</h1>
          <Doughnut :data="DoughnutData"/>
        </div>
      </div>
      
    <div class="is-flex is-justify-content-center is-align-items-center" style="padding-top: 100px">
      <div class="has-text-centered" style="width: 1500px; height: 1500">
        <h1 class="is-size-3">Продажи по месяцам</h1>
        <Line :data="LineSalesData"></Line>
      </div>
    </div>

    <div class="is-flex is-justify-content-center is-align-items-center" style="padding-top: 100px">
      <div class="has-text-centered" style="width: 1500px; height: 1500">
        <h1 class="is-size-3">Прибыль по месяцам</h1>
        <Line :data="LineTotalSumData"></Line>
      </div>
    </div>

    </div>
</template>

<script>
import { Doughnut } from 'vue-chartjs'
import { Line } from 'vue-chartjs';
import "chart.js/auto";
import axios from 'axios';

export default {
    data(){
      return{
        doughnutData: {
          labels: [],
          data: []
        },
        lineSalesData: {
          labels: [],
          data: []
        },
        lineTotalSumData: {
          labels: [],
          data: []
        }
      }
    },
    components: {
      Doughnut,
      Line
    },
    mounted(){
      this.getStats()
    },
    computed: {
      DoughnutData () {
        return {
          labels: this.doughnutData.labels,
          datasets: [
            {
              backgroundColor: [
                '#B21F00',
                '#C9DE00',
                '#2FDE00',
                '#00A6B4',
                '#6800B4'
              ],
              hoverBackgroundColor: [
                '#501800',
                '#4B5000',
                '#175000',
                '#003350',
                '#35014F'
              ],
              data: this.doughnutData.data
            }
          ]
        }
      },
      LineSalesData(){
        return{
          labels: this.lineSalesData.labels,
          datasets: [
            {
              label: 'Продажи',
              backgroundColor: 'rgba(75,192,192,0.2)',
              borderColor: 'rgba(75,192,192,1)',
              borderWidth: 1,
              data: this.lineSalesData.data
            },        
          ]
        }
      },
      LineTotalSumData(){
        return{
          labels: this.lineTotalSumData.labels,
          datasets: [
            {
              label: 'Прибыль тыс. руб.',
              backgroundColor: 'rgba(75,192,192,0.2)',
              borderColor: 'rgba(75,192,192,1)',
              borderWidth: 1,
              data: this.lineTotalSumData.data
            },        
          ]
        }
      }
    },
    methods: {
      async getStats(){
        const { data } = await axios.get('api/all_orders')

        this.lineSalesData.labels = Object.keys(data.statsSalesPerMonth).reverse()
        this.lineSalesData.data = Object.values(data.statsSalesPerMonth).reverse()
        this.lineTotalSumData.labels = Object.keys(data.statsPricePerMonth).reverse()
        this.lineTotalSumData.data = Object.values(data.statsPricePerMonth).reverse()

        this.doughnutData.labels = Object.keys(data.statsSalesPerCategory)
        this.doughnutData.data = Object.values(data.statsSalesPerCategory)
      }
    }
  }
  </script> 