<template>
    <div class="column is-8">
        <strong>{{name}}</strong>
        <div
            v-for="param in params"
            v-bind:key="param"
        >
            <label class="checkbox ml-1">
                <input type="checkbox">
                {{param}}
            </label>
        </div>
    </div>
</template>


<script>
export default {
    name: "FilterCheckBox",
    props:{
        name: String,
        params: Array
    },
    mounted(){
        this.$emit('getParams', )
    }
}
</script>
