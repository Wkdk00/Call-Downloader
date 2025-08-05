import Vue from 'vue'
import VueRouter from 'vue-router'
import axios from 'axios'

Vue.use(VueRouter)

const routes = [
  { path: '/about', component: () => import('./views/About.vue'), meta: { requiresAuth: true } },
  { path: '/control', component: () => import('./views/Control.vue'), meta: { requiresAuth: true } },
  { path: '/auto_params', component: () => import('./views/AutoParams.vue'), meta: { requiresAuth: true } },
  { path: '/hand_send', component: () => import('./views/HandSend.vue'), meta: { requiresAuth: true } },
  { path: '/login', component: () => import('./views/Login.vue') },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

router.beforeEach(async (to, from, next) => {
  if (!to.matched.some(record => record.meta.requiresAuth)) {
    return next() 
  }

  const token = localStorage.getItem('token')
  if (!token) return next('/login')

  try {
    await axios.get('/api/protected', {
      headers: { Authorization: `Bearer ${token}` }
    })
    next()
  } catch {
    localStorage.removeItem('token')
    next('/login')
  }
})

export default router