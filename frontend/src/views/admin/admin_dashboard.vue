<template>
  <div class="box">

    <!-- Header -->
    <div class="header">
      <h1>Admin Dashboard</h1>
      <p>Welcome to the Institute Placement Cell Management System</p>
    </div>

    <p v-if="error" class="error_msg">⚠️ {{ error }}</p>
    <p v-if="loading" class="loading_msg">Loading dashboard...</p>

    <template v-if="data && !loading">

      <!-- 4 Stat Cards -->
      <div class="stats_row">

        <div class="stat_card">
          <div class="icon_box blue">🏢</div>
          <h2>{{ data.stats.total_companies }}</h2>
          <p>Total Companies</p>
        </div>

        <div class="stat_card">
          <div class="icon_box green">👥</div>
          <h2>{{ data.stats.total_students }}</h2>
          <p>Total Students</p>
        </div>

        <div class="stat_card">
          <div class="icon_box purple">💼</div>
          <h2>{{ data.stats.active_drives }}</h2>
          <p>Active Drives</p>
        </div>

        <div class="stat_card">
          <div class="icon_box orange">📈</div>
          <h2>{{ data.stats.placement_rate }}%</h2>
          <p>Placement Rate</p>
        </div>

      </div>

      <!-- Two column: Recent Companies + Recent Drives -->
      <div class="two_col">

        <!-- Recent Companies -->
        <div class="panel">
          <div class="panel_header">
            <h3>Recent Company Registrations</h3>
            <span class="view_all" @click="$router.push('/admin/companies')">View All →</span>
          </div>

          <div v-if="data.recent_companies.length === 0" class="no_data">No companies yet.</div>

          <div
            class="list_item"
            v-for="company in data.recent_companies"
            :key="company.company_id"
          >
            <div class="item_left">
              <div class="avatar">{{ company.company_name.charAt(0).toUpperCase() }}</div>
              <div>
                <p class="item_name">{{ company.company_name }}</p>
                <p class="item_sub">{{ company.hr_name }}</p>
              </div>
            </div>
            <span class="status_badge" :class="company.status">
              {{ company.status }}
            </span>
          </div>
        </div>

        <!-- Recent Drives -->
        <div class="panel">
          <div class="panel_header">
            <h3>Recent Placement Drives</h3>
            <span class="view_all" @click="$router.push('/admin/drives')">View All →</span>
          </div>

          <div v-if="data.recent_drives.length === 0" class="no_data">No drives yet.</div>

          <div
            class="list_item drives_item"
            v-for="drive in data.recent_drives"
            :key="drive.drive_id"
          >
            <div class="item_left">
              <div>
                <p class="item_name">{{ drive.job_title }}</p>
                <p class="item_sub company_blue">{{ drive.company_name }}</p>
                <p class="item_sub">{{ drive.application_count }} application(s) received</p>
              </div>
            </div>
            <span class="status_badge" :class="drive.status">
              {{ drive.status }}
            </span>
          </div>
        </div>

      </div>

    </template>
  </div>
</template>


<script>
export default {
  data() {
    return {
      data: null,
      loading: false,
      error: ''
    };
  },

  methods: {
    async fetchDashboard() {
      this.loading = true;
      this.error = '';
      try {
        const res = await fetch('http://127.0.0.1:5000/admin/dashboard', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });
        const json = await res.json();
        if (res.ok) {
          this.data = json;
        } else {
          this.error = json.msg || 'Failed to load dashboard.';
        }
      } catch (err) {
        this.error = "Backend se connect nahi ho pa raha! 'python app.py' chalu karo.";
      } finally {
        this.loading = false;
      }
    }
  },

  async mounted() {
    await this.fetchDashboard();
  }
};
</script>


<style scoped>

.box {
  width: 100%;
  padding: 28px;
  background-color: #f5f6fa;
}

.header h1 {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.header p {
  color: #888;
  font-size: 14px;
  margin-bottom: 24px;
}

.error_msg {
  background: #fdecea;
  border: 1px solid #e63946;
  color: #c1121f;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}

.loading_msg {
  text-align: center;
  color: #aaa;
  padding: 60px;
  font-size: 15px;
}

/* === Stat Cards === */
.stats_row {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.stat_card {
  background: white;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  flex: 1;
  min-width: 140px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.icon_box {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.icon_box.blue   { background: #dbeafe; }
.icon_box.green  { background: #d1fae5; }
.icon_box.purple { background: #ede9fe; }
.icon_box.orange { background: #ffedd5; }

.stat_card h2 {
  font-size: 30px;
  font-weight: 800;
  color: #1a1a2e;
  margin: 0;
}

.stat_card p {
  font-size: 13px;
  color: #888;
  margin: 0;
}

/* === Two column panels === */
.two_col {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.panel {
  background: white;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  padding: 20px 24px;
  flex: 1;
  min-width: 280px;
}

.panel_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.panel_header h3 {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a2e;
}

.view_all {
  font-size: 13px;
  font-weight: 600;
  color: #f13d29;
  cursor: pointer;
  transition: opacity 0.2s;
}

.view_all:hover { opacity: 0.7; }

/* List items */
.list_item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.list_item:last-child { border-bottom: none; }

.item_left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, #7c3aed, #0c2db3);
  color: white;
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.item_name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
}

.item_sub {
  font-size: 12px;
  color: #aaa;
  margin-top: 2px;
}

.company_blue { color: #0c2db3 !important; font-weight: 600; }

.drives_item .item_left { align-items: flex-start; }

/* Status badges */
.status_badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  white-space: nowrap;
  text-transform: capitalize;
}

.status_badge.pending  { background: #fef3c7; color: #b45309; }
.status_badge.approved { background: #d1fae5; color: #065f46; }
.status_badge.rejected { background: #fee2e2; color: #b91c1c; }

.no_data {
  text-align: center;
  color: #ccc;
  padding: 30px 0;
  font-size: 14px;
}
</style>