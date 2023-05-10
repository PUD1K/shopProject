import { createStore } from 'vuex'

export default createStore({
  state: {
    cart: {
      items:[]
    },
    token: '',
    isAuthentificated: false,
    isStaff: false
  },
  getters: {
  },
  mutations: {
    //если в localStorage есть что-то в корзине
    //то передаем это в state
    //иначе выполняем обратную процедуру
    initializeStore(state){
      if(localStorage.getItem('cart')){
        state.cart = JSON.parse(localStorage.getItem('cart'))
      }else{
        localStorage.setItem('cart', JSON.stringify(state.cart))
      }
      //если в localStorage есть токен,
      //добавляем его в state
      if(localStorage.getItem('token')){
        state.token = localStorage.getItem('token')
        state.isAuthentificated = true
      }else{
        state.token = ''
        state.isAuthentificated = false
      }
    },
    // при успешной авторизации
    setToken(state, token){
      state.token = token
      state.isAuthentificated = true
    },
    // если разлогинился
    removeToken(state){
      state.token = ''
      state.isAuthentificated = false
    },
    setStaff(state){
      state.isStaff = true;
    },
    offStaff(state){
      state.isStaff = false;
    },
    addToCart(state, item){
      const exists = state.cart.items.filter(i => i.product.id === item.product.id)
      // если в корзине уже есть текущий товар
      // то добавляем к количеству 
      if(exists.length){
        exists[0].quantity = parseInt(exists[0].quantity) + parseInt(item.quantity)
      }else{
        state.cart.items.push(item)
      }

      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    clearCart(state){
      // очищаем корзину
      state.cart = { items: [] }
      localStorage.setItem('cart', JSON.stringify(state.cart))
    },
    setCart(state, cart){
      state.cart = cart
    }
  },
  actions: {
  },
  modules: {
  }
})
