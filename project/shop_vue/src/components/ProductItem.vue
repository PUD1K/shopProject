<template>
    <div class="column is-3">
        <div class="box">
            <figure class="image mb-4">
                <img :src="product.get_image">
            </figure>

            <h3 class="is-size-6 has-text-black">{{product.name}}</h3>
            <p class="is-size-6 has-text-gray">{{product.price}} ₽</p>
            
            <div class="has-text-right">
                <router-link v-bind:to="product.get_absolute_url" class="button is-dark mt-4">Подробнее</router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ProductItem',
    props:{
        product: Object
    }
}
</script>

<style>

</style>