<template>
  <div class="box">

    <!-- Header -->
    <div class="header">
      <h1>Student Dashboard</h1>
      <p>Track your placement applications and opportunities</p>
    </div>

    <p v-if="error" class="error_msg">⚠️ {{ error }}</p>
    <p v-if="loading" class="loading_msg">Loading dashboard...</p>

    <template v-if="data && !loading">

      <!-- 4 Stat Cards -->
      <div class="stats_row">

        <div class="stat_card">
          <div class="icon_box blue">📄</div>
          <h2>{{ data.stats.total }}</h2>
          <p>Applications Sent</p>
        </div>

        <div class="stat_card">
          <div class="icon_box orange">🕐</div>
          <h2>{{ data.stats.applied }}</h2>
          <p class="orange_text">Under Review</p>
        </div>

        <div class="stat_card">
          <div class="icon_box green">✅</div>
          <h2>{{ data.stats.shortlisted }}</h2>
          <p class="green_text">Shortlisted</p>
        </div>

        <div class="stat_card">
          <div class="icon_box purple">🏅</div>
          <h2>{{ data.stats.cgpa ?? 'N/A' }}</h2>
          <p>Current CGPA</p>
        </div>

      </div>

      <!-- Two column: Recent Applications + Upcoming Drives -->
      <div class="two_col">

        <!-- Recent Applications -->
        <div class="panel">
          <div class="panel_header">
            <h3>Recent Applications</h3>
            <span class="view_all" @click="$router.push('/student/applications')">View All →</span>
          </div>

          <div v-if="data.recent_applications.length === 0" class="no_data">
            No applications yet.
          </div>

          <div
            class="list_item"
            v-for="app in data.recent_applications"
            :key="app.application_id"
          >
            <div class="item_info">
              <p class="item_name">{{ app.job_title }}</p>
              <p class="item_company">{{ app.company_name }}</p>
              <p class="item_date">Applied on {{ app.applied_date || 'N/A' }}</p>
            </div>
            <span class="status_badge" :class="app.status">
              <span v-if="app.status === 'applied'">🕐 Under Review</span>
              <span v-else-if="app.status === 'shortlisted'">🔖 Shortlisted</span>
              <span v-else-if="app.status === 'selected'">✅ Selected</span>
              <span v-else-if="app.status === 'rejected'">❌ Rejected</span>
            </span>
          </div>
        </div>

        <!-- Upcoming Drives -->
        <div class="panel">
          <div class="panel_header">
            <h3>Upcoming Drives</h3>
            <span class="view_all" @click="$router.push('/student/drives')">Browse All →</span>
          </div>

          <div v-if="data.upcoming_drives.length === 0" class="no_data">
            No new eligible drives at the moment.
          </div>

          <div
            class="drive_item"
            v-for="drive in data.upcoming_drives"
            :key="drive.drive_id"
            @click="$router.push('/student/drives')"
          >
            <div class="drive_info">
              <p class="item_name">{{ drive.job_title }}</p>
              <p class="drive_company">{{ drive.company_name }}</p>
              <p class="item_date">Deadline: {{ drive.application_deadline || 'N/A' }}</p>
            </div>
            <span class="drive_icon">💼</span>
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
        const res = await fetch('http://127.0.0.1:5000/student/dashboard', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });

        // Try to parse JSON — if server returns HTML (500 error page), this throws
        let json;
        try {
          json = await res.json();
        } catch {
          this.error = 'Server error! Flask terminal mein dekho kya error aaya.';
          return;
        }

        if (res.ok) {
          this.data = json;
        } else {
          this.error = json.msg || 'Failed to load dashboard.';
        }

      } catch (err) {
        // Ye tab aata hai jab fetch hi fail ho jaye (backend band ho)
        this.error = "Network error! 'python app.py' se backend chalu karo.";
        console.error(err);
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

/* Stat cards */
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
  min-width: 130px;
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
.icon_box.orange { background: #ffedd5; }
.icon_box.green  { background: #d1fae5; }
.icon_box.purple { background: #ede9fe; }

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

.orange_text { color: #f59e0b !important; font-weight: 600; }
.green_text  { color: #16a34a !important; font-weight: 600; }

/* Two column */
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
  margin-bottom: 16px;
}

.panel_header h3 {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a2e;
}

.view_all {
  font-size: 13px;
  font-weight: 600;
  color: #0cb32e;
  cursor: pointer;
  transition: opacity 0.2s;
}

.view_all:hover { opacity: 0.7; }

/* Application items */
.list_item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.list_item:last-child { border-bottom: none; }

.item_name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
}

.item_company {
  font-size: 12px;
  color: #0c2db3;
  font-weight: 600;
  margin-top: 2px;
}

.item_date {
  font-size: 12px;
  color: #aaa;
  margin-top: 2px;
}

/* Status badges */
.status_badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  white-space: nowrap;
  flex-shrink: 0;
}

.status_badge.applied     { background: #fef3c7; color: #b45309; }
.status_badge.shortlisted { background: #d1fae5; color: #065f46; }
.status_badge.selected    { background: #d1fae5; color: #065f46; }
.status_badge.rejected    { background: #fee2e2; color: #b91c1c; }

/* Upcoming drive items */
.drive_item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border-radius: 10px;
  background: #f0fdf4;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.drive_item:last-child { margin-bottom: 0; }

.drive_item:hover { background: #dcfce7; }

.drive_company {
  font-size: 12px;
  color: #0cb32e;
  font-weight: 600;
  margin-top: 2px;
}

.drive_icon {
  font-size: 20px;
  flex-shrink: 0;
}

.no_data {
  text-align: center;
  color: #ccc;
  padding: 30px 0;
  font-size: 14px;
}
</style>