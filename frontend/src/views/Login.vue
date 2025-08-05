<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      message: '',
      error: '',
      success: false,
      errorVisible: false,
      errorTimeoutId: null,
    }
  },
methods: {
  login() {
    if (!this.username || !this.password) {
      this.showError("Заполните все поля");
      return;
    }
    this.error = "";
    this.errorVisible = false;
    this.message = "";
    this.success = false;
    if (this.errorTimeoutId) {
      clearTimeout(this.errorTimeoutId);
      this.errorTimeoutId = null;
    }
    
    const apiUrl = '/api/token';
    
    axios.post(apiUrl,
    {
      username: this.username,
      password: this.password
    },
    {
      headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
      localStorage.setItem("token", response.data.access_token)
      this.message = "Успешный вход!";
      this.success = true;
      setTimeout(() => this.$router.push('/control'), 1000);
    })
    .catch(error => {
      if(error.response) {
        this.showError(error.response.data.detail || "Ошибка авторизации");
      } else {
        this.showError("Ошибка сети");
      }
    });
  },
  
  showError(message) {
    this.error = message;
    this.errorVisible = true;
    if (this.errorTimeoutId) clearTimeout(this.errorTimeoutId);
    this.errorTimeoutId = setTimeout(() => {
      this.errorVisible = false;
      setTimeout(() => {
        this.errorTimeoutId = null;
        this.error = '';
      });
    }, 2500);
  }
}
}

</script>

<template>
  <div class="wrapper">
    <h1>Авторизация</h1>
    <hr>
    <div class="input-block">
      <svg class="login-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
        <path d="M12 12C14.7614 12 17 9.76142 17 7C17 4.23858 14.7614 2 12 2C9.23858 2 7 4.23858 7 7C7 9.76142 9.23858 12 12 12Z"/>
        <path d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"/>
      </svg>
      <input type="text" v-model="username" placeholder="Логин" @keyup.enter="login">
    </div>
    <div class="input-block">
      <svg class="login-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
        <path d="M12 3a5 5 0 0 0-5 5v3H5v10h14V11h-2V8a5 5 0 0 0-5-5zm0 2a3 3 0 0 1 3 3v3H9V8a3 3 0 0 1 3-3z"/>
      </svg>
      <input type="password" v-model="password" placeholder="Пароль" @keyup.enter="login">
    </div>
    <div class="btn-box">
      <button disabled v-if="username==''||password==''" class="login-btn-lock">Вход</button>
      <button type="submit" v-else @click="login" class="login-btn">Вход</button>
      <div class="error" :class="{ visible: errorVisible }">
        <p>{{ error }}</p>
      </div>
      <div class="success" :class="{ visible: success }">
        <p>{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  margin-top: 30px;
  height: 400px;
  width: 450px;
  border-radius: 50px;
  padding: 20px 0;
  background: #ffffff;
  text-align: center;
  color: #1E293B;
}

.wrapper h1 {
  margin-top: 15px;
  font-size: 42px;
  margin-bottom: 20px;
}

.wrapper hr {
  border-top: 1px solid #ccc;
  margin: 0;
}

.input-block {
  margin: 30px auto 0;
  background: #F5F5F5;
  border-radius: 50px;
  width: 240px;
  padding: 6px 12px;
  display: flex;
  align-items: center;
}

.wrapper input {
  background: transparent;
  border: 0;
  color: #333333;
  font-size: 16px;
  padding: 5px 8px;
  outline: none;
}

.input-block:hover {
  background: #E0E0E0;
}

.input-block:hover .login-icon {
  color: #00B4D8;
  transition: color 0.3s ease;
}

.login-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  color: #888888;
  display: block;  
}

.login-btn{
  line-height: 40px;
  font-size: 16px;
  background: #00B4D8;
  border: 0;
  border-radius: 30px;
  color:#ffffff;
  width: 100px;
  height: 40px;
  cursor: pointer;
  transition: width 0.8s ease, font-size 0.8s ease;
  outline: none;
}

.login-btn-lock{
  line-height: 40px;
  font-size: 16px;
  background: #F5F5F5;
  border: 0;
  border-radius: 30px;
  color:#888888;
  width: 100px;
  height: 40px;
}

.login-btn:hover {
  width: 130px;
  font-size: 20px;
}

.btn-box {
  margin: 30px auto 0;
  width: 264px;
  display: flex;
  justify-content: flex-end;
  position: relative;
  overflow: hidden;
}

.error {
  position: absolute;
  box-sizing: border-box;

  height: 40px;
  width: 0;
  overflow: hidden;
  line-height: 40px;
  background: #E57373;
  color: #fff;
  font-size: 14px;
  border-radius: 50px;
  padding: 0 20px;
  text-align: left;
  right: 5px;

  transition: width 0.8s ease;
  z-index: 5;
}

.error.visible {
  width: 259px;
  opacity: 1;
  border-radius: 30px;
}

.login-btn, .login-btn-lock {
  position: relative;
  z-index: 10;
}

.error p {
  margin: 0;
  padding: 0;
  white-space: nowrap;
}

.success {
  position: absolute;
  box-sizing: border-box;

  height: 40px;
  width: 0;
  overflow: hidden;
  line-height: 40px;
  background: #2e7d32;
  color: #fff;
  font-size: 14px;
  border-radius: 50px;
  padding: 0 20px;
  text-align: left;
  right: 5px;

  transition: width 0.8s ease;
  z-index: 5;
}

.success.visible {
  width: 259px;
  opacity: 1;
  border-radius: 30px;
}

.success p {
  margin: 0;
  padding: 0;
  white-space: nowrap;
}
</style>