<template>
  <div id="app">
    <el-container class="layout-container">
      <el-aside width="200px">
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/dashboard">
            <el-icon><Monitor /></el-icon>
            <span>Dashboard</span>
          </el-menu-item>
          <el-menu-item index="/inventory">
            <el-icon><Box /></el-icon>
            <span>Inventory</span>
          </el-menu-item>
          <el-menu-item index="/products">
            <el-icon><Goods /></el-icon>
            <span>Products</span>
          </el-menu-item>
          <el-menu-item index="/sales">
            <el-icon><ShoppingCart /></el-icon>
            <span>Sales</span>
          </el-menu-item>
          <el-menu-item index="/reports">
            <el-icon><Document /></el-icon>
            <span>Reports</span>
          </el-menu-item>
          <el-menu-item index="/promotions">
            <el-icon><Lightning /></el-icon>
            <span>Promotions</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header>
          <h2>Wine Shop Administration Panel</h2>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { Monitor, Box, Goods, ShoppingCart, Document, Lightning } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleMenuSelect = (index) => {
  router.push(index)
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
}

.layout-container {
  height: 100vh;
}

.el-header {
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
}

.el-aside {
  background-color: #f5f5f5;
}

.el-menu {
  border-right: none;
  height: 100%;
}
</style>