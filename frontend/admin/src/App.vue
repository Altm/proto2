<template>
  <div id="app">
    <!-- Navigation sidebar -->
    <el-container>
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <h3>{{ $t('message.welcome') }}</h3>
        </div>
        <el-menu
          :default-active="$route.path"
          class="sidebar-menu"
          router
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>{{ $t('message.home') }}</span>
          </el-menu-item>
          <el-menu-item index="/wines">
            <el-icon><Menu /></el-icon>
            <span>{{ $t('message.wine') }}</span>
          </el-menu-item>
          <el-menu-item index="/inventory">
            <el-icon><Box /></el-icon>
            <span>{{ $t('message.inventory') }}</span>
          </el-menu-item>
          <el-menu-item index="/sales">
            <el-icon><Money /></el-icon>
            <span>{{ $t('message.sales') }}</span>
          </el-menu-item>
          <el-menu-item index="/orders">
            <el-icon><Document /></el-icon>
            <span>{{ $t('message.orders') }}</span>
          </el-menu-item>
          <el-menu-item index="/reports">
            <el-icon><PieChart /></el-icon>
            <span>{{ $t('message.reports') }}</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <el-container>
        <!-- Header with language switcher and user menu -->
        <el-header class="header">
          <div class="header-content">
            <h2>{{ $route.meta.title || $route.name }}</h2>
            <div class="header-actions">
              <!-- Language switcher -->
              <el-dropdown @command="handleLanguageChange">
                <span class="el-dropdown-link">
                  {{ currentLang.toUpperCase() }}
                  <el-icon><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="en">English</el-dropdown-item>
                    <el-dropdown-item command="ru">Русский</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>

              <!-- User menu -->
              <el-dropdown class="user-menu">
                <span class="el-dropdown-link">
                  <el-icon><User /></el-icon>
                  Admin
                  <el-icon><ArrowDown /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item>{{ $t('message.profile') }}</el-dropdown-item>
                    <el-dropdown-item>{{ $t('message.settings') }}</el-dropdown-item>
                    <el-dropdown-item divided>{{ $t('message.logout') }}</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>

        <!-- Main content area -->
        <el-main class="main-content">
          <router-view />
        </el-main>

        <!-- Footer -->
        <el-footer class="footer">
          <p>&copy; 2026 Wine Inventory Management System. {{ $t('message.allRightsReserved') }}.</p>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';

export default {
  name: 'App',
  setup() {
    const { locale } = useI18n();
    const router = useRouter();
    
    const currentLang = computed(() => locale.value);
    
    const handleLanguageChange = (lang) => {
      locale.value = lang;
      localStorage.setItem('lang', lang);
    };
    
    return {
      currentLang,
      handleLanguageChange
    };
  }
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

#app {
  min-height: 100vh;
}

.sidebar {
  background-color: #545c64;
  color: white;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
}

.logo {
  padding: 20px 10px;
  text-align: center;
  border-bottom: 1px solid #444;
}

.sidebar-menu {
  border: none;
}

.header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-actions {
  display: flex;
  gap: 20px;
  align-items: center;
}

.main-content {
  background-color: #f5f5f5;
  padding: 20px;
}

.footer {
  background-color: #f5f5f5;
  border-top: 1px solid #e0e0e0;
  padding: 10px 20px;
  text-align: center;
  color: #666;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}
</style>