<script>
import BtnPanel from '../components/BtnPanel.vue';
import AuParamIcon from '../components/AuParamIcon.vue';
import ControlIcon from '../components/ControlIcon.vue';
import axios from 'axios'

export default {
  components: { BtnPanel },
  data() {
    return {
      buttons: [
        { text: 'Отслеживание файлов', icon: ControlIcon, path: '/control' },
        { text: 'Параметры отправки', icon: AuParamIcon, path: '/auto_params' }
      ],
      activeIndex: 0,
      hoveredBtnIndex: null,
      accept_files: false,
      hand_mode: false,
      received_files: [],
    };
  },
  async mounted() {
    try {
      const response = await axios.get('/api/control_data');
      this.accept_files = response.data.accept_files;
      this.hand_mode = response.data.hand_mode;
      this.received_files = response.data.received_files;
    } catch (error) {console.error('Не удалось получить данные управления:', error);}
  },
  methods: {
    async toggleAcceptance() {
      try {
        const response = await axios.post('/api/toggle_accept');
        if (response.status === 200) {
          this.accept_files = !this.accept_files;
        } else {
          console.error('Ошибка при переключении приема файлов');
        }
      } catch (error) {
        console.error('Ошибка:', error);
      }
    },
    async HandChange() {
      try {
        const response = await axios.post('/api/toggle_hand_mode');
        if (response.status === 200) {
          this.hand_mode = !this.hand_mode;
        } else {
          console.error('Ошибка при переключении приема файлов');
        }
      } catch (error) {
        console.error('Ошибка:', error);
      }
    },
  }
};
</script>

<template>
  <div>
    <BtnPanel
      :buttons="buttons"
      v-model:activeIndex="activeIndex"
    />
    <div class="wrapper">
      <h1>Панель управления</h1>
      <hr>
      
      <button :class="['toggle-btn', accept_files ? 'on-btn' : 'off-btn']" type="button" @click="toggleAcceptance">
        {{ accept_files ? 'Сервис принимает файлы' : 'Сервис не принимает файлы' }}
      </button>

      <button :class="['toggle-btn', hand_mode ? 'off-btn' : 'on-btn']" type="button" @click="HandChange">
        {{ hand_mode ? 'Ручной режим' : 'Автоматический режим' }}
      </button>

      <table v-if="received_files && received_files.length > 0 && !hand_mode" class="control-table">
        <thead>
          <tr>
            <th>Время</th>
            <th>Имя файла</th>
            <th>ID агента</th>
            <th>Статус</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(file, index) in received_files" :key="index">
            <td>{{ file.timestamp }}</td>
            <td>{{ file.filename }}</td>
            <td>{{ file.agent_id }}</td>
            <td>{{ file.download_status }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="notable">Данные еще не получены</p>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  height: 700px;
  width: 600px;
  border-radius: 0 50px 50px 50px;
  background: #ffffff;
  padding: 27px 40px 40px;
  box-sizing: border-box;
  text-align: center;
  color: #1E293B;
  position: relative;
  overflow-y: auto;
  transition: border-radius 0.8s ease;
}

.wrapper h1 {
  font-size: 42px;
  margin-bottom: 22px;
}

.wrapper hr {
  border-top: 1px solid #ccc;
  margin: 0 0 40px 0;  
  width: 100%;
  box-sizing: border-box;
}

.toggle-btn {
  height: 60px;
  width: 320px;
  border-radius: 50px;
  font-size: 18px;
  transition: background-color 0.8s ease, border 0.8s ease, color 0.8s ease, transform 0.3s ease;
  cursor: pointer;
  outline: none;
  border: 2px solid transparent;
  margin-bottom: 30px;
}

.off-btn {
  background: #F5F5F5;
  color: #333333;
  border-color: transparent;
}

.off-btn:hover {
  background: #E0E0E0;
  border-color: #00B4D8;
  color: #00B4D8;
}

.on-btn {
  background: #00B4D8;
  color: #fff;
  border-color: transparent;
  border: 2px solid transparent;
}

.on-btn:hover {
  transform: scale(1.1);
}

.control-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 40px;
  font-size: 16px;
  color: #0F172A;
  user-select: none;
  border-radius: 30px;
  overflow: hidden;
}

.control-table thead {
  background-color: #0F172A;
  color: #ffffff;
  user-select: none;
  transition: background-color 1.5s ease;
}

.control-table thead:hover {
  background: #00B4D8;
}

.control-table thead th {
  padding: 12px 10px;
  text-align: center;
}

.control-table th,
.control-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #E0E0E0;
}

.control-table tbody {
  background-color: #F5F5F5;
  color: #333333;
}

.control-table tbody tr {
  transition: background-color 0.8s ease, border 0.8s ease, color 0.8s ease;
}

.control-table tbody tr:hover {
  background-color: #E0E0E0;
  color:#00B4D8;
  
}

.control-table tbody tr:last-child td {
  border-bottom: none;
}

.notable {
 color: #333333;
 margin-top: 40px;
}
</style>