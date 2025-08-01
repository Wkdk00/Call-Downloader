<template>
  <div class="about">
    <h1>О нас</h1>
    <p>Это страница с информацией о нас.</p>
    <button @click="logout">Выйти</button>
  </div>
</template>

<script>
export default {
  name: 'About',
  methods: {
    logout() {
      localStorage.removeItem('token');  // Удаляем токен из localStorage
      this.$router.push('/login');       // Перенаправляем на страницу логина
    }
  }
}
</script>

