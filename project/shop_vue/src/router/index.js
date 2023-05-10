import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView from '../views/HomeView.vue'
import About from '../views/About.vue'
import CategoryProducts from '../views/CategoryProducts.vue'
import ProductDetail from '../views/ProductDetail.vue'
import Search from '../views/Search.vue'
import SignUp from '../views/SignUp.vue'
import Login from '../views/Login.vue'
import MyAcc from '../views/MyAcc.vue'
import Cart from '../views/Cart.vue'
import Checkout from '../views/Checkout.vue'
import Success from '../views/Success.vue'
import MyOrders from '../views/MyOrders.vue'
import Managment from '../views/Managment.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: About
  },
  {
    // т.о. мы "вытаскиваем" category_slug из url, c помощью $route.params.
    path: '/:category_slug',
    name: 'CategoryProducts',
    component: CategoryProducts,
  },
  {
    path: '/:category_slug/:product_slug',
    name: 'ProductDetail',
    component: ProductDetail
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/myacc',
    name: 'MyAcc',
    component: MyAcc,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart
  },
  {
    path: '/cart/checkout',
    name: 'Checkout',
    component: Checkout,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/cart/success',
    name: 'Success',
    component: Success,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/myacc/myorders',
    name: 'MyOrders',
    component: MyOrders,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/managment',
    name: 'Managment',
    component: Managment,
    meta: {
      requireLogin: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// еще раз посмотреть
router.beforeEach((to, from, next) => {
  //  проверяем соответствие каждой записи маршрута      И   если отсутствует токен аутентификации
  if(to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthentificated){
    next({name: 'Login', query: { to: to.path } });
  }
  else{
    next()
  }
})

export default router
