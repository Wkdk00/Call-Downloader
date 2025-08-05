<script>
import BtnPanel from '../components/BtnPanel.vue';
import AuParamIcon from '../components/AuParamIcon.vue';
import ControlIcon from '../components/ControlIcon.vue';

import axios from 'axios';

export default {
  components: { BtnPanel },
  data() {
    return {
      buttons: [
        { text: 'Отслеживание файлов', icon: ControlIcon, path: '/control' },
        { text: 'Параметры отправки', icon: AuParamIcon, path: '/auto_params' }
      ],
      activeIndex: 1,
      hoveredBtnIndex: null,
      QuestionID: '',
      ButtonAlias: '',
      HubComputerName: '',
      POS: '',
      UserText: ''
    }
  },
  methods: {
    async submit() {
      try {
        const jsonData = {
          'QuestionID': this.QuestionID,
          'ButtonAlias': this.ButtonAlias,
          'HubComputerName': this.HubComputerName,
          'POS': this.POS,
          'UserText': this.UserText,
        };

        const apiUrl = 'api/save_auto_params/';

        const response = await axios.post(apiUrl, jsonData, {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.data.status === 'success') {
          alert('Параметры успешно сохранены!');
        } else {
          alert('Ошибка при сохранении: ' + (response.data.message || 'неизвестная ошибка'));
        }
      }
      catch(error) {
        alert('Ошибка сети: ' + error.message);
      }
    }
  }
}
</script>

<template>
  <div>
    <BtnPanel
      :buttons="buttons"
      v-model:activeIndex="activeIndex"
      v-model:hoveredBtnIndex="hoveredBtnIndex"
    />
    <div class="wrapper">
      <h1>Параметры</h1>
      <hr>
      <div class="input-block">
        <input type="text" v-model="QuestionID" placeholder="ID вопроса">        
      </div>
      <div class="input-block">
        <input type="text" v-model="ButtonAlias" placeholder="Псевдоним ответа">        
      </div>
      <div class="input-block">
        <input type="text" v-model="HubComputerName" placeholder="Имя компьютера">        
      </div>
      <div class="input-block">
        <input type="text" v-model="POS" placeholder="ID POS" @keyup.enter="submit">        
      </div>
      <div class="btn-box">
        <div class="btn-input">
          <input type="text" v-model="UserText" placeholder="Комментарий"> 
        </div>
        <button type="submit" class="btn" @click="submit()">Сохранить</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  height: 570px;
  width: 600px;
  border-radius: 0 50px 50px 50px;
  background: #ffffff;
  text-align: center;
  color: #1E293B;
  position: relative;
  padding-top: 27px;
}

.wrapper h1 {
  font-size: 42px;
  margin-bottom: 22px;
}

.wrapper hr {
  border-top: 1px solid #ccc;
  margin: 0;
  margin-bottom: 40px;
}

.input-block {
  margin: 30px auto 0;
  background: #F5F5F5;
  border-radius: 50px;
  width: 240px;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 2px solid transparent;
  transition: border 0.8s ease;
}

.input-block input {
  margin-left: 3px;
  background: transparent;
  border: 0;
  color: #333333;
  font-size: 16px;
  padding: 5px 8px;
  outline: none;
}

.input-block:hover {
  background: #E0E0E0;
  border: 2px solid #00B4D8;
  transition: border 0.8s ease;
}

.input-block:hover input {
  color: #00B4D8;
  transition: color 0.3s ease;
}

.input-block:hover input::placeholder {
  color: #00B4D8;
  transition: color 0.3s ease;
}

.btn-box {
  margin: 30px auto 0;
  width: 264px;
  height: 44px;
  display: flex;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  gap: 20px;
}

.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  
  height: 44px;
  width: 150px;
  padding: 0 16px;
  
  background: #00B4D8;
  border: 0;
  border-radius: 30px;
  color: #fff;
  font-size: 16px;
  line-height: 44px;
  
  cursor: pointer;
  transition: width 0.8s ease, font-size 0.8s ease;
  outline: none;
}

.btn:hover {
  width: 180px;
  font-size: 20px;
}

.btn-input{
  flex-grow: 1;
  background: #F5F5F5;
  border-radius: 50px;
  padding: 6px;
  display: flex;
  align-items: center;
  border: 2px solid transparent;
  transition: border 0.8s ease;
}

.btn-input input {
  margin-left: 3px;
  background: transparent;
  width: 100%;
  border: 0;
  color: #333333;
  font-size: 12px;
  padding: 5px 8px;
  outline: none;
}

.btn-input:hover {
  background: #E0E0E0;
  border: 2px solid #00B4D8;
  transition: border 0.8s ease;
}

.btn-input:hover input {
  color: #00B4D8;
  transition: color 0.3s ease;
}

.btn-input:hover input::placeholder {
  color: #00B4D8;
  transition: color 0.3s ease;
}
</style>