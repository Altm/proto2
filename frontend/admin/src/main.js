/**
 * Main entry point for the Wine Inventory Admin Panel
 */
import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { createStore } from 'vuex';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';

// Import i18n
import { createI18n } from 'vue-i18n';
import enLocale from 'element-plus/es/locale/lang/en';
import ruLocale from 'element-plus/es/locale/lang/ru';

// Import components
import App from './App.vue';
import HomeView from './views/HomeView.vue';
import WineListView from './views/WineListView.vue';
import WineEditView from './views/WineEditView.vue';
import InventoryView from './views/InventoryView.vue';
import SalesView from './views/SalesView.vue';
import OrdersView from './views/OrdersView.vue';
import ReportsView from './views/ReportsView.vue';

// Import API service
import api from './api/api';

// Import store
import store from './store';

// Import styles
import './styles/index.css';

// Create i18n instance
const messages = {
  en: {
    ...enLocale,
    message: {
      hello: 'Hello',
      welcome: 'Welcome to Wine Inventory Admin Panel',
      home: 'Home',
      wine: 'Wine',
      inventory: 'Inventory',
      sales: 'Sales',
      orders: 'Orders',
      reports: 'Reports',
      settings: 'Settings',
      profile: 'Profile',
      logout: 'Logout',
      allRightsReserved: 'All Rights Reserved',
      search: 'Search',
      add: 'Add',
      edit: 'Edit',
      delete: 'Delete',
      save: 'Save',
      cancel: 'Cancel',
      name: 'Name',
      producer: 'Producer',
      country: 'Country',
      region: 'Region',
      vintageYear: 'Vintage Year',
      volume: 'Volume (ml)',
      glassesPerBottle: 'Glasses Per Bottle',
      price: 'Price',
      actions: 'Actions',
      type: 'Type',
      rating: 'Rating',
      description: 'Description',
      color: 'Color',
      grapeVariety: 'Grape Variety',
      alcoholPercentage: 'Alcohol Percentage',
      sku: 'SKU',
      isActive: 'Is Active',
      location: 'Location',
      bottlesCount: 'Bottles Count',
      glassesCount: 'Glasses Count',
      saleType: 'Sale Type',
      quantity: 'Quantity',
      unitPrice: 'Unit Price',
      totalAmount: 'Total Amount',
      saleDate: 'Sale Date',
      customerName: 'Customer Name',
      customerEmail: 'Customer Email',
      shippingAddress: 'Shipping Address',
      status: 'Status',
      paymentMethod: 'Payment Method',
      orderDate: 'Order Date',
      wineName: 'Wine Name',
      totalSoldBottles: 'Total Sold Bottles',
      totalSoldGlasses: 'Total Sold Glasses',
      totalRevenue: 'Total Revenue',
      locationType: 'Location Type',
      warehouse: 'Warehouse',
      barRestaurant: 'Bar/Restaurant',
      bottle: 'Bottle',
      glass: 'Glass',
      red: 'Red',
      white: 'White',
      rose: 'Rose',
      sparkling: 'Sparkling',
      dessert: 'Dessert',
      fortified: 'Fortified',
      pending: 'Pending',
      paid: 'Paid',
      shipped: 'Shipped',
      delivered: 'Delivered',
      cancelled: 'Cancelled',
      succeeded: 'Succeeded',
      failed: 'Failed',
      refunded: 'Refunded',
      addition: 'Addition',
      removal: 'Removal',
      damage: 'Damage',
      reason: 'Reason',
      adjustedBy: 'Adjusted By',
      adjustmentDate: 'Adjustment Date',
      adjustments: 'Adjustments',
      createSale: 'Create Sale',
      createOrder: 'Create Order',
      createAdjustment: 'Create Adjustment',
      inventoryReport: 'Inventory Report',
      salesSummary: 'Sales Summary',
      filter: 'Filter',
      clear: 'Clear',
      export: 'Export',
      import: 'Import',
      refresh: 'Refresh',
      loading: 'Loading...',
      success: 'Success',
      error: 'Error',
      warning: 'Warning',
      info: 'Info',
      confirmDelete: 'Are you sure you want to delete this item?',
      deleteConfirmation: 'Delete Confirmation',
      yes: 'Yes',
      no: 'No',
      createdSuccessfully: 'Created successfully',
      updatedSuccessfully: 'Updated successfully',
      deletedSuccessfully: 'Deleted successfully',
      operationFailed: 'Operation failed',
      pleaseTryAgain: 'Please try again',
      noData: 'No data available',
      pagination: {
        total: 'Total {total}',
        page: 'Page {page}',
        size: '{size} per page'
      }
    }
  },
  ru: {
    ...ruLocale,
    message: {
      hello: 'Привет',
      welcome: 'Добро пожаловать в административную панель управления винами',
      home: 'Главная',
      wine: 'Вино',
      inventory: 'Инвентарь',
      sales: 'Продажи',
      orders: 'Заказы',
      reports: 'Отчеты',
      settings: 'Настройки',
      profile: 'Профиль',
      logout: 'Выйти',
      allRightsReserved: 'Все права защищены',
      search: 'Поиск',
      add: 'Добавить',
      edit: 'Редактировать',
      delete: 'Удалить',
      save: 'Сохранить',
      cancel: 'Отмена',
      name: 'Название',
      producer: 'Производитель',
      country: 'Страна',
      region: 'Регион',
      vintageYear: 'Год урожая',
      volume: 'Объем (мл)',
      glassesPerBottle: 'Бокалов в бутылке',
      price: 'Цена',
      actions: 'Действия',
      type: 'Тип',
      rating: 'Рейтинг',
      description: 'Описание',
      color: 'Цвет',
      grapeVariety: 'Сорт винограда',
      alcoholPercentage: 'Процент алкоголя',
      sku: 'Артикул',
      isActive: 'Активен',
      location: 'Местоположение',
      bottlesCount: 'Количество бутылок',
      glassesCount: 'Количество бокалов',
      saleType: 'Тип продажи',
      quantity: 'Количество',
      unitPrice: 'Цена за единицу',
      totalAmount: 'Общая сумма',
      saleDate: 'Дата продажи',
      customerName: 'Имя клиента',
      customerEmail: 'Email клиента',
      shippingAddress: 'Адрес доставки',
      status: 'Статус',
      paymentMethod: 'Метод оплаты',
      orderDate: 'Дата заказа',
      wineName: 'Название вина',
      totalSoldBottles: 'Всего продано бутылок',
      totalSoldGlasses: 'Всего продано бокалов',
      totalRevenue: 'Общий доход',
      locationType: 'Тип местоположения',
      warehouse: 'Склад',
      barRestaurant: 'Бар/Ресторан',
      bottle: 'Бутылка',
      glass: 'Бокал',
      red: 'Красное',
      white: 'Белое',
      rose: 'Розовое',
      sparkling: 'Игристое',
      dessert: 'Десертное',
      fortified: 'Крепленое',
      pending: 'В ожидании',
      paid: 'Оплачено',
      shipped: 'Отправлено',
      delivered: 'Доставлено',
      cancelled: 'Отменено',
      succeeded: 'Успешно',
      failed: 'Неудачно',
      refunded: 'Возвращено',
      addition: 'Пополнение',
      removal: 'Списание',
      damage: 'Повреждение',
      reason: 'Причина',
      adjustedBy: 'Кем изменено',
      adjustmentDate: 'Дата изменения',
      adjustments: 'Корректировки',
      createSale: 'Создать продажу',
      createOrder: 'Создать заказ',
      createAdjustment: 'Создать корректировку',
      inventoryReport: 'Отчет по инвентарю',
      salesSummary: 'Сводка по продажам',
      filter: 'Фильтр',
      clear: 'Очистить',
      export: 'Экспорт',
      import: 'Импорт',
      refresh: 'Обновить',
      loading: 'Загрузка...',
      success: 'Успех',
      error: 'Ошибка',
      warning: 'Предупреждение',
      info: 'Информация',
      confirmDelete: 'Вы уверены, что хотите удалить этот элемент?',
      deleteConfirmation: 'Подтверждение удаления',
      yes: 'Да',
      no: 'Нет',
      createdSuccessfully: 'Успешно создано',
      updatedSuccessfully: 'Успешно обновлено',
      deletedSuccessfully: 'Успешно удалено',
      operationFailed: 'Операция не выполнена',
      pleaseTryAgain: 'Пожалуйста, попробуйте снова',
      noData: 'Нет доступных данных',
      pagination: {
        total: 'Всего {total}',
        page: 'Страница {page}',
        size: '{size} на странице'
      }
    }
  }
};

const i18n = createI18n({
  locale: localStorage.getItem('lang') || 'en',
  fallbackLocale: 'en',
  messages
});

// Define routes
const routes = [
  { path: '/', component: HomeView },
  { path: '/wines', component: WineListView },
  { path: '/wines/new', component: WineEditView },
  { path: '/wines/:id/edit', component: WineEditView },
  { path: '/inventory', component: InventoryView },
  { path: '/sales', component: SalesView },
  { path: '/orders', component: OrdersView },
  { path: '/reports', component: ReportsView }
];

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes
});

// Create app
const app = createApp(App);

// Register icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// Provide API to the app
app.config.globalProperties.$api = api;

// Use plugins
app.use(store);
app.use(router);
app.use(i18n);
app.use(ElementPlus);

// Mount app
app.mount('#app');