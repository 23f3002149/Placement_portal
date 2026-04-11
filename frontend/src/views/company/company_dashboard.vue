<template>
  <div class="box">

    <!-- Header -->
    <div class="header">
      <div>
        <h1>Company Dashboard</h1>
        <p>Manage your recruitment drives and applications</p>
      </div>
      <button class="btn_create" @click="$router.push('/company/drives')">
        + Create New Placement Drive
      </button>
    </div>

    <p v-if="error" class="error_msg">⚠️ {{ error }}</p>
    <p v-if="loading" class="loading_msg">Loading dashboard...</p>

    <template v-if="data && !loading">

      <!-- 4 Stat Cards -->
      <div class="stats_row">

        <div class="stat_card">
          <div class="icon_box blue">💼</div>
          <h2>{{ data.stats.active_drives }}</h2>
          <p>Active Drives</p>
        </div>

        <div class="stat_card">
          <div class="icon_box green">👥</div>
          <h2>{{ data.stats.total_applications }}</h2>
          <p>Total Applications</p>
        </div>

        <div class="stat_card">
          <div class="icon_box purple">✅</div>
          <h2>{{ data.stats.selected_candidates }}</h2>
          <p>Selected Candidates</p>
        </div>

        <div class="stat_card">
          <div class="icon_box orange">🕐</div>
          <h2>{{ data.stats.pending_review }}</h2>
          <p>Pending Review</p>
        </div>

      </div>

      <!-- Placement Drives list -->
      <div class="panel">
        <div class="panel_header">
          <h3>Your Placement Drives</h3>
          <span class="view_all" @click="$router.push('/company/applications')">View All →</span>
        </div>

        <div v-if="data.drives.length === 0" class="no_data">
          No drives posted yet. Click "Create New Placement Drive" to get started.
        </div>

        <div
          class="drive_row"
          v-for="drive in data.drives"
          :key="drive.drive_id"
        >
          <div class="drive_info">
            <div class="drive_title_row">
              <p class="drive_title">{{ drive.job_title }}</p>
              <span class="status_badge" :class="drive.status">
                <span v-if="drive.status === 'approved'">✅ Live</span>
                <span v-else-if="drive.status === 'pending'">🕐 Pending Approval</span>
                <span v-else-if="drive.status === 'rejected'">❌ Rejected</span>
              </span>
            </div>
            <p class="drive_sub">
              {{ drive.application_count }} application(s)
              <span v-if="drive.application_deadline"> • Deadline: {{ drive.application_deadline }}</span>
            </p>
          </div>
          <button class="btn_details" @click="$router.push('/company/applications')">
            View Details
          </button>
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
        const res = await fetch('http://127.0.0.1:5000/company/dashboard', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });

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

/* Header row with button */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
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
}

.btn_create {
  padding: 12px 22px;
  background: linear-gradient(to right, #0c2db3, #041e94);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  white-space: nowrap;
}

.btn_create:hover {
  transform: scale(1.04);
  background: linear-gradient(to right, #1a3fcc, #0c2db3);
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

/* Drives panel */
.panel {
  background: white;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  padding: 20px 24px;
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
  color: #0c2db3;
  cursor: pointer;
  transition: opacity 0.2s;
}

.view_all:hover { opacity: 0.7; }

/* Drive rows */
.drive_row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid #f5f5f5;
  gap: 16px;
}

.drive_row:last-child { border-bottom: none; }

.drive_info { flex: 1; }

.drive_title_row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.drive_title {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a2e;
}

.drive_sub {
  font-size: 13px;
  color: #aaa;
  margin-top: 4px;
}

/* Status badges */
.status_badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  white-space: nowrap;
}

.status_badge.approved { background: #d1fae5; color: #065f46; }
.status_badge.pending  { background: #fef3c7; color: #b45309; }
.status_badge.rejected { background: #fee2e2; color: #b91c1c; }

/* View Details button */
.btn_details {
  padding: 8px 18px;
  background: #0c2db3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn_details:hover { background: #041e94; }

.no_data {
  text-align: center;
  color: #bbb;
  padding: 30px 0;
  font-size: 14px;
}
</style>