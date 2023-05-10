<template>
    <div class="container" style="margin-left: 0%; margin-right: 0%;">
      <div class="columns">
        <div class="column is-3-desktop is-hidden-mobile">
          <aside class="menu">
            <p class="menu-label">Меню</p>
            <ul class="menu-list">
              <li>
                <a @click="setActiveTab('Статистика')" :class="{ 'is-active': activeTab === 'Статистика' }">Статистика</a>
              </li>
              <li>
                <a @click="setActiveTab('Заказы')" :class="{ 'is-active': activeTab === 'Заказы' }">Заказы</a>
              </li>
            </ul>
          </aside>
        </div>
        <div class="column is-9-desktop">
          <SwitcherMenuManagment :tab="activeTab"/>
        </div>
      </div>
    </div>
</template>

<script>
import SwitcherMenuManagment from '@/components/SwitcherMenuManagment.vue';

export default {
    name: 'Managment',
    components: {
        SwitcherMenuManagment
    },
    data() {
      return {
        activeTab: 'Статистика',
      };
    },
    methods: {
      setActiveTab(tabName) {
        this.activeTab = tabName;
      },
    },
}

  </script> 