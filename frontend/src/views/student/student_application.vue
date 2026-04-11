<template>
  <div class="box">

    <!-- Header -->
    <div class="header">
      <div>
        <h1>My Applications</h1>
        <p>Track the status of your placement applications</p>
      </div>
      <button class="btn_download" @click="downloadReport">⬇️ Download CSV</button>
    </div>

    <!-- Error -->
    <p v-if="error" class="error_msg">⚠️ {{ error }}</p>

    <!-- Stats cards -->
    <div class="stats_row">
      <div class="stat_card">
        <p>Total</p>
        <h2>{{ applications.length }}</h2>
      </div>
      <div class="stat_card applied_stat">
        <p>Applied</p>
        <h2>{{ countByStatus('applied') }}</h2>
      </div>
      <div class="stat_card shortlisted_stat">
        <p>Shortlisted</p>
        <h2>{{ countByStatus('shortlisted') }}</h2>
      </div>
      <div class="stat_card selected_stat">
        <p>Selected</p>
        <h2>{{ countByStatus('selected') }}</h2>
      </div>
      <div class="stat_card rejected_stat">
        <p>Rejected</p>
        <h2>{{ countByStatus('rejected') }}</h2>
      </div>
    </div>

    <!-- Applications list -->
    <div class="app_list">

      <div
        class="app_card"
        v-for="app in applications"
        :key="app.application_id"
      >
        <!-- Left: avatar + info -->
        <div class="app_left">
          <div class="avatar">{{ app.company_name.charAt(0).toUpperCase() }}</div>

          <div class="app_info">
            <h3>{{ app.job_title }}</h3>
            <p class="company_name">🏢 {{ app.company_name }}</p>
            <p class="applied_date">Applied on {{ app.applied_date || 'N/A' }}</p>
            <div class="details_row" v-if="app.package || app.location">
              <span v-if="app.package">₹ {{ app.package }}</span>
              <span v-if="app.location">📍 {{ app.location }}</span>
            </div>
          </div>
        </div>

        <!-- Right: status badge -->
        <div class="app_right">
          <span class="status_badge" :class="app.status">
            <span v-if="app.status === 'applied'">🕐 Applied</span>
            <span v-else-if="app.status === 'shortlisted'">🔖 Shortlisted</span>
            <span v-else-if="app.status === 'selected'">✅ Selected</span>
            <span v-else-if="app.status === 'rejected'">❌ Rejected</span>
          </span>
        </div>
      </div>

      <!-- Empty state -->
      <div class="empty_state" v-if="applications.length === 0 && !error && !loading">
        <p>📋 You haven't applied to any drives yet.</p>
        <p class="empty_sub">Go to Browse Drives to find and apply to opportunities.</p>
      </div>

      <p v-if="loading" class="loading_msg">Loading your applications...</p>

    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      applications: [],
      loading: false,
      error: ''
    };
  },

  methods: {

    countByStatus(status) {
      return this.applications.filter(a => a.status === status).length;
    },

    async fetchApplications() {
      this.loading = true;
      this.error = '';
      try {
        const res = await fetch('http://127.0.0.1:5000/student/applications', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });
        const data = await res.json();
        if (res.ok) {
          this.applications = data;
        } else {
          this.error = data.msg || 'Failed to load applications.';
        }
      } catch (err) {
        this.error = "Backend se connect nahi ho pa raha! 'python app.py' chalu karo.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

  async downloadReport() {
      try {
        const res = await fetch('http://127.0.0.1:5000/student/report', {
          method: 'GET',
          headers: { Authorization: 'Bearer ' + localStorage.getItem('token') }
        });
        if (!res.ok) {
          const t = await res.text();
          alert(t || 'Failed to download report');
          return;
        }
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'student_applications.csv';
        a.click();
        URL.revokeObjectURL(url);
      } catch (err) {
        alert('Download failed.');
      }
    },

  },

  async mounted() {
    await this.fetchApplications();
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

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.btn_download {
  background: #0cb330;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
  font-weight: 600;
}
.btn_download:hover { background: #0ed70a; }

.header p {
  color: #888;
  font-size: 14px;
  margin-bottom: 20px;
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

/* Stats */
.stats_row {
  display: flex;
  gap: 14px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.stat_card {
  background: white;
  border-radius: 10px;
  padding: 14px 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  flex: 1;
  min-width: 90px;
}

.stat_card p {
  font-size: 12px;
  color: #888;
  margin-bottom: 6px;
}

.stat_card h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
}

.applied_stat h2     { color: #f59e0b; }
.shortlisted_stat h2 { color: #7c3aed; }
.selected_stat h2    { color: #16a34a; }
.rejected_stat h2    { color: #dc2626; }

/* Cards */
.app_list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.app_card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  padding: 18px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.app_left {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  flex: 1;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: linear-gradient(135deg, #0cb32e, #049421);
  color: white;
  font-size: 20px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.app_info h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 3px;
}

.company_name {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}

.applied_date {
  font-size: 12px;
  color: #aaa;
  margin-bottom: 6px;
}

.details_row {
  display: flex;
  gap: 14px;
  font-size: 13px;
  color: #555;
}

/* Status badges */
.app_right { flex-shrink: 0; }

.status_badge {
  font-size: 13px;
  font-weight: 700;
  padding: 7px 16px;
  border-radius: 20px;
  white-space: nowrap;
}

.status_badge.applied     { background: #fef3c7; color: #b45309; }
.status_badge.shortlisted { background: #ede9fe; color: #6d28d9; }
.status_badge.selected    { background: #d1fae5; color: #065f46; }
.status_badge.rejected    { background: #fee2e2; color: #b91c1c; }

/* Empty / loading */
.empty_state {
  text-align: center;
  padding: 50px 20px;
  color: #888;
}

.empty_state p {
  font-size: 16px;
  font-weight: 600;
}

.empty_sub {
  font-size: 13px !important;
  font-weight: 400 !important;
  margin-top: 8px;
}

.loading_msg {
  text-align: center;
  color: #aaa;
  padding: 40px;
  font-size: 15px;
}
</style>