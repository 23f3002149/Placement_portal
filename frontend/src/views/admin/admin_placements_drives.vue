<template>
<div class="box">
    <div class="header">
      <h1>Manage Placement Drives</h1>
      <p>Review and manage placement drives</p>
    </div>

    <!-- Error message -->
    <p v-if="error" class="error_msg">⚠️ {{ error }}</p>

    <!-- Search + Filter tabs -->
    <div class="search_stats">
      <input type="text" v-model="search" placeholder="Search by job title or company..." />
      <div class="some_stats">
        <div
          v-for="tab in ['All', 'Pending', 'Approved', 'Rejected']"
          :key="tab"
          :class="{ active_tab: selectedStatus === tab }"
          @click="selectedStatus = tab"
        >
          {{ tab }}
        </div>
      </div>
    </div>

    <!-- Drives List -->
    <div class="drive_list">
      <div
        class="drive_card"
        v-for="drive in filteredList()"
        :key="drive.drive_id"
      >
        <!-- Top row: title + status badge -->
        <div class="title_row">
          <div>
            <h3>{{ drive.job_title }}</h3>
            <p class="company_tag">🏢 {{ drive.company_name }}</p>
          </div>
          <span
            class="status_badge"
            :class="drive.drive_approved_status"
          >
            {{ drive.drive_approved_status }}
          </span>
        </div>

        <!-- Details row -->
        <div class="details_row">
          <span>💰 {{ drive.package || 'N/A' }}</span>
          <span>📍 {{ drive.location || 'N/A' }}</span>
          <span>🎓 Min CGPA: {{ drive.cgpa_criteria ?? 'N/A' }}</span>
          <span>📅 Deadline: {{ drive.application_deadline || 'N/A' }}</span>
        </div>

        <!-- Branches -->
        <div class="branches_row">
          <span
            class="branch_chip"
            v-for="branch in drive.branches"
            :key="branch"
          >
            {{ branch }}
          </span>
        </div>

        <!-- Description -->
        <p class="desc" v-if="drive.job_description">
          {{ drive.job_description }}
        </p>

        <!-- Action buttons — pending drives only -->
        <div v-if="drive.drive_approved_status === 'pending'" class="btn_row">
          <button class="btn_approve" @click="updateStatus(drive.drive_id, 'approved')">
            ✅ Approve
          </button>
          <button class="btn_reject" @click="updateStatus(drive.drive_id, 'rejected')">
            ❌ Reject
          </button>
        </div>

        <!-- Already approved — can still reject -->
        <div v-if="drive.drive_approved_status === 'approved'" class="btn_row">
          <button class="btn_reject" @click="updateStatus(drive.drive_id, 'rejected')">
            ❌ Close Drive
          </button>
        </div>

      </div>

      <!-- Empty state -->
      <p v-if="filteredList().length === 0 && !error" class="empty_msg">
        No drives found.
      </p>
    </div>
</div>
</template>






<script>
export default {
  data() {
    return {
      drive_list: [],
      search: '',
      selectedStatus: 'All',
      error: ''
    };
  },

  methods: {

    filteredList() {
      const search = this.search.toLowerCase();
      const status = this.selectedStatus;

      return this.drive_list.filter(function(drive) {
        const matchSearch =
          !search ||
          drive.job_title.toLowerCase().includes(search) ||
          drive.company_name.toLowerCase().includes(search);

        const matchStatus =
          status === 'All' ||
          drive.drive_approved_status === status.toLowerCase();

        return matchSearch && matchStatus;
      });
    },

    async fetchDrives() {
      const token = localStorage.getItem('token');
      try {
        const res = await fetch('http://127.0.0.1:5000/admin/drives', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + token
          }
        });

        if (res.ok) {
          const data = await res.json();
          this.drive_list = data;
        } else {
          const data = await res.json();
          this.error = data.msg || 'Failed to load drives.';
        }

      } catch (err) {
        this.error = "Backend se connect nahi ho pa raha! 'python app.py' chalu karo.";
        console.error('Fetch error:', err);
      }
    },

    async updateStatus(drive_id, status) {
      const token = localStorage.getItem('token');

      const res = await fetch(`http://127.0.0.1:5000/admin/drive/${drive_id}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + token
        },
        body: JSON.stringify({ status: status })
      });

      if (res.ok) {
        await this.fetchDrives(); // list refresh karo
      } else {
        const data = await res.json();
        alert('Error: ' + data.msg);
      }
    }

  },

  async mounted() {
    await this.fetchDrives();
  }
};
</script>


<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.box {
  width: 100%;
  min-height: 100vh;
  padding: 28px;
  background-color: #f5f6fa;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header h1 {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a2e;
}

.header p {
  color: #888;
  font-size: 14px;
  margin-top: 4px;
}

.error_msg {
  color: #c1121f;
  background: #fdecea;
  border: 1px solid #e63946;
  border-radius: 8px;
  padding: 12px 16px;
  font-weight: 600;
  font-size: 14px;
}

/* Search + filter tabs */
.search_stats {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.search_stats input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}

.search_stats input:focus {
  border-color: #f13d29;
}

.some_stats {
  display: flex;
  gap: 8px;
}

.some_stats div {
  padding: 7px 14px;
  border-radius: 20px;
  background-color: #e0e0e0;
  color: #444;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s ease;
  font-weight: 500;
}

.some_stats div:hover {
  background-color: #c0c0c0;
}

.some_stats div.active_tab {
  background-color: #f13d29;
  color: white;
}

/* Drive list */
.drive_list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.drive_card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  padding: 18px 22px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Title row */
.title_row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.title_row h3 {
  font-size: 17px;
  font-weight: 700;
  color: #1a1a2e;
}

.company_tag {
  font-size: 13px;
  color: #666;
  margin-top: 3px;
}

/* Status badge */
.status_badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  text-transform: capitalize;
  white-space: nowrap;
}

.status_badge.pending {
  background-color: #fef3c7;
  color: #b45309;
}

.status_badge.approved {
  background-color: #d1fae5;
  color: #065f46;
}

.status_badge.rejected {
  background-color: #fee2e2;
  color: #b91c1c;
}

/* Details row */
.details_row {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  font-size: 13px;
  color: #555;
}

/* Branch chips */
.branches_row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.branch_chip {
  background: #e0e7ff;
  color: #3730a3;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 12px;
  border-radius: 20px;
}

/* Description */
.desc {
  color: #666;
  font-size: 14px;
}

/* Action buttons */
.btn_row {
  display: flex;
  gap: 10px;
  margin-top: 4px;
}

.btn_approve {
  padding: 8px 16px;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: background 0.2s ease;
}

.btn_approve:hover {
  background-color: #27ae60;
}

.btn_reject {
  padding: 8px 16px;
  background-color: #e63946;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: background 0.2s ease;
}

.btn_reject:hover {
  background-color: #c1121f;
}

.empty_msg {
  text-align: center;
  color: #888;
  padding: 40px 0;
  font-size: 15px;
}
</style>






