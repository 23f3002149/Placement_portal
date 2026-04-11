<template>
  <div class="box">

    <!-- Header -->
    <div class="header">
      <h1>Applications</h1>
      <div class="header_actions">
        <p>Review and manage student applications</p>
        <button class="btn_download" @click="downloadCompanyReport">⬇️ Monthly CSV</button>
      </div>
    </div>

    <!-- Error -->
    <p v-if="error" class="error_msg">⚠️ {{ error }}</p>

    <!-- Stats cards -->
    <div class="stats_row">
      <div class="stat_card">
        <p>Total</p>
        <h2>{{ applications.length }}</h2>
      </div>
      <div class="stat_card new">
        <p>New</p>
        <h2>{{ countByStatus('applied') }}</h2>
      </div>
      <div class="stat_card shortlisted">
        <p>Shortlisted</p>
        <h2>{{ countByStatus('shortlisted') }}</h2>
      </div>
      <div class="stat_card selected">
        <p>Selected</p>
        <h2>{{ countByStatus('selected') }}</h2>
      </div>
      <div class="stat_card rejected">
        <p>Rejected</p>
        <h2>{{ countByStatus('rejected') }}</h2>
      </div>
    </div>

    <!-- Search + Drive filter + Status tabs -->
    <div class="filter_bar">
      <span class="search_icon">🔍</span>
      <input type="text" v-model="search" placeholder="Search by student name..." />

      <select v-model="selectedDrive">
        <option value="">All Drives</option>
        <option v-for="drive in uniqueDrives()" :key="drive.id" :value="drive.id">
          {{ drive.title }}
        </option>
      </select>

      <div class="status_tabs">
        <button
          v-for="tab in ['All', 'applied', 'shortlisted', 'selected', 'rejected']"
          :key="tab"
          :class="['tab_btn', { active: selectedStatus === tab }]"
          @click="selectedStatus = tab"
        >
          {{ tab === 'applied' ? 'Applied' : tab.charAt(0).toUpperCase() + tab.slice(1) }}
        </button>
      </div>
    </div>

    <!-- Applications list -->
    <div class="app_list">

      <div
        class="app_card"
        v-for="app in filteredList()"
        :key="app.application_id"
      >
        <!-- Left: avatar + info -->
        <div class="app_left">
          <div class="avatar">{{ app.student_name.charAt(0).toUpperCase() }}</div>

          <div class="app_info">
            <h3>{{ app.student_name }}</h3>
            <p class="job_title">{{ app.job_title }}</p>
            <div class="details_row">
              <span>🎓 {{ app.branch || 'N/A' }}</span>
              <span>🏅 CGPA: {{ app.cgpa ?? 'N/A' }}</span>
              <span>📅 Applied: {{ app.applied_date || 'N/A' }}</span>
            </div>



            <!-- Resume Button -->
            <div class="resume_row">
              <a
                v-if="app.resume_url"
                :href="app.resume_url"
                target="_blank"
                class="btn_resume"
              >
                📄 View Resume
              </a>
              <span v-else class="no_resume">📭 No Resume</span>
            </div>



            <!-- Action buttons based on current status -->
            <div class="btn_row" v-if="app.status === 'applied'">
              <button class="btn_shortlist" @click="shortlist(app)">🔖 Shortlist</button>
              <button class="btn_reject" @click="reject(app)">❌ Reject</button>
            </div>

            <div class="btn_row" v-if="app.status === 'shortlisted'">
              <button class="btn_schedule" @click="scheduleInterview(app)">📅 Schedule</button>
              <button class="btn_select" @click="finalDecision(app, 'selected')">✅ Select</button>
              <button class="btn_reject" @click="finalDecision(app, 'rejected')">❌ Reject</button>
            </div>
          </div>
        </div>

        <!-- Right: status badge -->
        <div class="app_right">
          <span class="status_badge" :class="app.status">
            <span v-if="app.status === 'applied'">New</span>
            <span v-else-if="app.status === 'shortlisted'">🔖 Shortlisted</span>
            <span v-else-if="app.status === 'selected'">✅ Selected</span>
            <span v-else-if="app.status === 'rejected'">❌ Rejected</span>
          </span>
        </div>
      </div>

      <!-- Empty state -->
      <div class="empty_state" v-if="filteredList().length === 0 && !error && !loading">
        <p>No applications found.</p>
      </div>

      <p v-if="loading" class="loading_msg">Loading applications...</p>

    </div>
  </div>

<!-- Schedule modal -->
  <div v-if="showScheduleModal" class="modal_backdrop">
    <div class="modal_card">
      <h3>Schedule interview</h3>
      <p class="hint">Time is treated as UTC (e.g., 2026-04-10 14:30).</p>
      <div class="form_row">
        <label>Date</label>
        <input type="date" v-model="scheduleForm.date" />
      </div>
      <div class="form_row">
        <label>Time (24h)</label>
        <input type="time" v-model="scheduleForm.time" step="60" />
      </div>
      <div class="modal_actions">
        <button class="btn_secondary" @click="closeSchedule">Cancel</button>
        <button class="btn_primary" @click="submitSchedule">Send</button>
      </div>
    </div>
  </div>
<!-- company_applications -->
</template>


<script>
export default {
  data() {
    return {
      applications: [],
      search: '',
      selectedDrive: '',
      selectedStatus: 'All',
      loading: false,
      error: '',
      showScheduleModal: false,
      scheduleForm: {
        date: '',
        time: '',
        appId: null
      }
    };
  },

  methods: {
    countByStatus(status) {
      return this.applications.filter(a => a.status === status).length;
    },

    uniqueDrives() {
      const seen = new Set();
      const drives = [];
      this.applications.forEach(app => {
        if (!seen.has(app.drive_id)) {
          seen.add(app.drive_id);
          drives.push({ id: app.drive_id, title: app.job_title });
        }
      });
      return drives;
    },

    filteredList() {
      const search = this.search.toLowerCase();
      const status = this.selectedStatus;
      const driveId = this.selectedDrive;

      return this.applications.filter(app => {
        const matchSearch = !search || app.student_name.toLowerCase().includes(search);
        const matchStatus = status === 'All' || app.status === status;
        const matchDrive = !driveId || app.drive_id === driveId;
        return matchSearch && matchStatus && matchDrive;
      });
    },

    async fetchApplications() {
      this.loading = true;
      this.error = '';
      try {
        const res = await fetch('http://127.0.0.1:5000/company/applications', {
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

    // applied → shortlisted
    async shortlist(app) {
      try {
        const res = await fetch(`http://127.0.0.1:5000/company/application/${app.application_id}/shortlist`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });
        const data = await res.json();
        if (res.ok) {
          app.status = 'shortlisted'; // update locally — no full reload needed
        } else {
          alert(data.msg);
        }
      } catch (err) {
        alert('Something went wrong.');
      }
    },

    // applied → rejected (direct reject without shortlisting)
    async reject(app) {
      try {
        const res = await fetch(`http://127.0.0.1:5000/company/application/${app.application_id}/reject`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });
        const data = await res.json();
        if (res.ok) {
          app.status = 'rejected';
        } else {
          alert(data.msg);
        }
      } catch (err) {
        alert('Something went wrong.');
      }
    },

    // shortlisted → selected / rejected
    async finalDecision(app, decision) {
      try {
        const res = await fetch(`http://127.0.0.1:5000/company/application/${app.application_id}/final`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          },
          body: JSON.stringify({ status: decision })
        });
        const data = await res.json();
        if (res.ok) {
          app.status = decision;
        } else {
          alert(data.msg);
        }
      } catch (err) {
        alert('Something went wrong.');
      }
    },


    // shortlisted → schedule interview
    async scheduleInterview(app) {
      // open modal with pre-filled defaults (today + 1 hour)
      const now = new Date();
      now.setMinutes(0, 0, 0);
      const in60 = new Date(now.getTime() + 60 * 60 * 1000);
      this.scheduleForm = {
        date: in60.toISOString().slice(0, 10),
        time: in60.toISOString().slice(11, 16),
        appId: app.application_id
      };
      this.showScheduleModal = true;
    },

    async submitSchedule() {
      const { date, time, appId } = this.scheduleForm;
      if (!date || !time || !appId) return;
      const iso = `${date}T${time}:00`;
      try {
        const res = await fetch(`http://127.0.0.1:5000/company/application/${appId}/interview`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          },
          body: JSON.stringify({ interview_time: iso })
        });
        const data = await res.json();
        if (res.ok) {
          this.showScheduleModal = false;
          this.scheduleForm = { date: '', time: '', appId: null };
          alert("Interview scheduled. Mail + reminder queued.");
        } else {
          alert(data.msg || "Failed to schedule interview");
        }
      } catch (err) {
        alert('Something went wrong.');
      }
    },

    closeSchedule() {
      this.showScheduleModal = false;
      this.scheduleForm = { date: '', time: '', appId: null };
    },

    async downloadCompanyReport() {
      try {
        const res = await fetch('http://127.0.0.1:5000/company/report/monthly', {
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
        a.download = 'company_monthly_report.csv';
        a.click();
        URL.revokeObjectURL(url);
      } catch (err) {
        alert('Download failed.');
      }
    }
  },

  async mounted() {
    await this.fetchApplications();
  }
};
</script>


<style scoped>

.box {
  width: 100%;
  max-width: 100%;
  padding: 28px;
  background-color: #f5f6fa;
  box-sizing: border-box;
  overflow-x: hidden;
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
  margin-bottom: 20px;
}

.header_actions {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.btn_download {
  background: #0c2db3;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
  font-weight: 600;
}
.btn_download:hover { background: #0a2596; }

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

/* Stats row */
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
  min-width: 100px;
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

.stat_card.new h2        { color: #f59e0b; }
.stat_card.shortlisted h2{ color: #7c3aed; }
.stat_card.selected h2   { color: #16a34a; }
.stat_card.rejected h2   { color: #dc2626; }

/* Filter bar */
.filter_bar {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.search_icon { color: #aaa; }

.filter_bar input {
  flex: 1;
  min-width: 160px;
  border: none;
  outline: none;
  font-size: 14px;
  color: #333;
  background: transparent;
}

.filter_bar select {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 13px;
  color: #444;
  outline: none;
  cursor: pointer;
}

.status_tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.tab_btn {
  padding: 7px 14px;
  border-radius: 20px;
  border: none;
  background: #e0e0e0;
  color: #444;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab_btn.active {
  background: #0c2db3;
  color: white;
}

.tab_btn:hover:not(.active) {
  background: #c8c8c8;
}

/* Applications list */
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
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  box-sizing: border-box;
}

/* Left section */
.app_left {
  display: flex;
  gap: 14px;
  flex: 1;
  min-width: 0;
  width: 100%;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0c2db3, #7c3aed);
  color: white;
  font-size: 18px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.app_info {
  flex: 1;
  min-width: 0;
}

.app_info h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 2px;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.job_title {
  font-size: 13px;
  color: #888;
  margin-bottom: 8px;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.details_row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 13px;
  color: #555;
  margin-bottom: 10px;
}

/* Action buttons */
.btn_row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn_shortlist {
  background: #7c3aed;
  color: white;
}
.btn_shortlist:hover { background: #6d28d9; }

.btn_select {
  background: #16a34a;
  color: white;
}
.btn_select:hover { background: #15803d; }

.btn_reject {
  background: #dc2626;
  color: white;
}
.btn_reject:hover { background: #b91c1c; }



.resume_row {
  margin-top: 8px;
}

.btn_resume {
  display: inline-block;
  padding: 6px 14px;
  background: linear-gradient(to right, #0c2db3, #7c3aed);
  color: white;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn_resume:hover {
  transform: scale(1.04);
  background: linear-gradient(to right, #7c3aed, #0c2db3);
}

.no_resume {
  font-size: 12px;
  color: #aaa;
}

/* Status badges */
.app_right { 
  flex-shrink: 0;
  align-self: center;
}

.status_badge {
  font-size: 12px;
  font-weight: 700;
  padding: 5px 14px;
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
  padding: 50px 0;
  color: #888;
  font-size: 15px;
}

.loading_msg {
  text-align: center;
  color: #aaa;
  padding: 40px;
  font-size: 15px;
}


/* Modal styles */
.modal_backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal_card {
  background: #fff;
  width: 360px;
  max-width: 90vw;
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.12);
  padding: 18px 20px;
  box-sizing: border-box;
}
.modal_card h3 { margin: 0 0 6px; }
.hint { color: #666; font-size: 12px; margin-bottom: 14px; }
.form_row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
.form_row label { font-size: 13px; color: #444; }
.form_row input {
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  font-size: 14px;
}
.modal_actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.btn_primary, .btn_secondary {
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
  font-weight: 600;
}
.btn_primary { background: #10b981; color: #fff; }
.btn_primary:hover { background: #0ea271; }
.btn_secondary { background: #f3f4f6; color: #1f2937; }
.btn_secondary:hover { background: #e5e7eb; }

</style>