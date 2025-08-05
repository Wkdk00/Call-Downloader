<template>
  <div class="container">
    <div class="navigation">
      <router-link to="/control" class="nav-button">Получить файлы</router-link>
      <router-link to="/hand_send" class="nav-button active">Отправить файлы</router-link>
      <router-link to="/parametrs" class="nav-button">Параметры SenseTrigger</router-link>
      <router-link to="/cxm_online_params" class="nav-button">Параметры CXM-Online</router-link>
      <router-link to="/delete" class="nav-button">Удалить файлы</router-link>
    </div>

    <div class="content">
      <h1>Отправление файлов</h1>
      <form @submit.prevent="submitForm" id="downloadForm">
        <div class="form-group">
          <label for="agent_id">ID агента (оставьте пустым для всех):</label>
          <input type="text" id="agent_id" v-model="agentId" name="agent_id" />
        </div>
        <div class="form-group">
          <label for="date_from">Дата с:</label>
          <input type="datetime-local" id="date_from" v-model="dateFrom" name="date_from" />
        </div>
        <div class="form-group">
          <label for="date_to">Дата по:</label>
          <input type="datetime-local" id="date_to" v-model="dateTo" name="date_to" />
        </div>

        <button type="button" @click="loadFiles">Загрузить список</button>

        <div v-if="files.length" id="filesTable" style="margin-top: 20px;">
          <table>
            <thead>
              <tr>
                <th>Выбрать</th>
                <th>ID файла</th>
                <th>Дата</th>
                <th>Размер</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="file in files" :key="file.fileId">
                <td><input type="checkbox" v-model="selectedFiles" :value="file.fileId" /></td>
                <td>{{ file.fileId }}</td>
                <td>{{ formatDate(file.date) }}</td>
                <td>{{ formatSize(file.file_size) }}</td>
              </tr>
            </tbody>
          </table>

          <div class="form-group" style="margin: 20px 0;">
            <label style="display: inline-block; margin-right: 20px;">
              <input type="checkbox" v-model="sendToSenseTrigger" />
              Отправить в SenseTrigger
            </label>
            <label style="display: inline-block;">
              <input type="checkbox" v-model="sendToCxmOnline" />
              Отправить в CXM-Online
            </label>
          </div>

          <button 
            type="submit" 
            :disabled="!canSubmit" 
            :style="{ backgroundColor: canSubmit ? '#2ecc71' : '#cccccc' }"
          >
            Отправить выбранные
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      agentId: '',
      dateFrom: '',
      dateTo: '',
      files: [],
      selectedFiles: [],
      sendToSenseTrigger: false,
      sendToCxmOnline: false,
    };
  },
  computed: {
    canSubmit() {
      return (this.sendToSenseTrigger || this.sendToCxmOnline) && this.selectedFiles.length > 0;
    },
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      return new Date(dateString).toLocaleString();
    },
    formatSize(sizeBytes) {
      return Math.round(sizeBytes / 1024) + ' KB';
    },
    async loadFiles() {
      let url = '/api/get_files_list?';
      const params = [];
      if (this.agentId) params.push(`agent_id=${encodeURIComponent(this.agentId)}`);
      if (this.dateFrom) params.push(`date_from=${encodeURIComponent(this.dateFrom)}`);
      if (this.dateTo) params.push(`date_to=${encodeURIComponent(this.dateTo)}`);
      url += params.join('&');

      try {
        const response = await axios.get(url);
        this.files = response.data;  // обновляем реактивное свойство
      } catch (error) {
        console.error('Ошибка при загрузке файлов:', error);
      }
    },
    async submitForm() {
      if (!this.canSubmit) return;

      const data = {
        selected_files: this.selectedFiles,
        send_to_sense_trigger: this.sendToSenseTrigger,
        send_to_cxm_online: this.sendToCxmOnline,
        agent_id: this.agentId,
        date_from: this.dateFrom,
        date_to: this.dateTo,
      };

      try {
        const response = await axios.post('api/download_files', data);
        if (response.status === 200) {
          alert('Файлы успешно отправлены');
          this.selectedFiles = [];
          this.sendToSenseTrigger = false;
          this.sendToCxmOnline = false;
        } else {
          alert('Ошибка при отправке файлов');
        }
      } catch (error) {
        alert('Ошибка сети: ' + error.message);
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: 50px auto;
  padding: 20px 40px;
  border-radius: 0 50px 50px 50px;
  background: #ffffff;
  color: #1E293B;
  box-sizing: border-box;
  text-align: center;
}

.navigation {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
}

.nav-button {
  padding: 10px 25px;
  border-radius: 50px;
  background: #F5F5F5;
  color: #333333;
  text-decoration: none;
  font-weight: 600;
  user-select: none;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-button:hover {
  background: #00B4D8;
  color: #fff;
}

.nav-button.active {
  background: #00B4D8;
  color: #fff;
}

.content h1 {
  font-size: 42px;
  margin-bottom: 22px;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
  font-size: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
}

input[type="text"],
input[type="datetime-local"] {
  width: 100%;
  padding: 8px 12px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  outline-color: #00B4D8;
}

button {
  height: 45px;
  border-radius: 50px;
  font-size: 18px;
  cursor: pointer;
  border: none;
  color: white;
  background-color: #00B4D8;
  transition: background-color 0.3s ease;
  padding: 0 25px;
  margin-top: 10px;
  user-select: none;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 16px;
  color: #0F172A;
  border-radius: 12px;
  overflow: hidden;
}

thead {
  background-color: #0F172A;
  color: #ffffff;
  user-select: none;
  transition: background-color 0.3s ease;
}

thead:hover {
  background-color: #00B4D8;
}

th,
td {
  padding: 12px 15px;
  border-bottom: 1px solid #E0E0E0;
  text-align: center;
}

tbody {
  background-color: #F5F5F5;
  color: #333333;
  user-select: none;
}

tbody tr:hover {
  background-color: #E0E0E0;
  color: #00B4D8;
}

tbody tr:last-child td {
  border-bottom: none;
}
</style>
