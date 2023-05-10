<template>
    <div class="container" style="margin-left: 0%; margin-right: 0%;">
      <div class="columns">
        <div class="column is-3-desktop is-hidden-mobile">
          <aside class="menu">
            <p class="menu-label">Меню</p>
            <ul class="menu-list">
              <li>
                <a @click="setActiveTab('Настройки аккаунта')" :class="{ 'is-active': activeTab === 'Настройки аккаунта' }">Настройки аккаунта</a>
              </li>
              <li>
                <a @click="setActiveTab('Мои заказы')" :class="{ 'is-active': activeTab === 'Мои заказы' }">Мои заказы</a>
              </li>
            </ul>
          </aside>
        </div>
        <div class="column is-9-desktop">
          <SwitcherMenu :tab="activeTab"/>
        </div>
      </div>
    </div>
  </template>
  
<script>
// import SwitcherShopSetting from '@/components/SwitcherShopSetting.vue';
import SwitcherMenu from './SwitcherMenu.vue' 
  
export default {
    name: 'MyAccMenu',
    components: {
        SwitcherMenu
    },
    data() {
      return {
        activeTab: 'Настройки аккаунта',
      };
    },
    methods: {
      setActiveTab(tabName) {
        this.activeTab = tabName;
      },
    },
  };
</script>

<style>
/* Add Bulma CSS classes here */
</style>