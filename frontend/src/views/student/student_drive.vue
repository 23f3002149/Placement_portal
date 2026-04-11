<template>
  <div class="box">

    <!-- Header -->
    <div class="header">
      <h1>Browse Placement Drives</h1>
      <p>Find and apply to placement opportunities</p>
    </div>

    <!-- Error message -->
    <p v-if="error" class="error_msg">⚠️ {{ error }}</p>

    <!-- Search bar only (no branch dropdown as discussed) -->
    <div class="search_bar">
      <span class="search_icon">🔍</span>
      <input
        type="text"
        v-model="search"
        placeholder="Search by company or position..."
      />
    </div>

    <!-- Student's profile summary card -->
    <div class="profile_card" v-if="student.branch">
      <p>
        <strong>Your Profile:</strong>
        {{ student.branch }}
        <span v-if="student.cgpa"> • CGPA: {{ student.cgpa }}</span>
        <span v-if="student.year_of_passing"> • Year: {{ student.year_of_passing }}</span>
      </p>
      <p class="eligibility_note">Only showing drives you're eligible for</p>
    </div>

    <!-- Drives List -->
    <div class="drive_list">

      <div
        class="drive_card"
        v-for="drive in filteredDrives()"
        :key="drive.drive_id"
      >
        <!-- Left: Avatar + Info -->
        <div class="drive_left">
          <div class="avatar">{{ drive.company_name.charAt(0).toUpperCase() }}</div>

          <div class="drive_info">
            <h3>{{ drive.job_title }}</h3>
            <p class="company_name">🏢 {{ drive.company_name }}</p>
            <p class="desc" v-if="drive.job_description">{{ drive.job_description }}</p>

            <!-- Details row -->
            <div class="details_row">
              <span>₹ {{ drive.package || 'N/A' }}</span>
              <span>📍 {{ drive.location || 'N/A' }}</span>
              <span>📅 {{ drive.application_deadline || 'N/A' }}</span>
              <span>🎓 Min CGPA: {{ drive.cgpa_criteria ?? 'N/A' }}</span>
            </div>

            <!-- Branch chips -->
            <div class="branches_row">
              <span class="branch_chip" v-for="branch in drive.branches" :key="branch">
                {{ branch }}
              </span>
            </div>
          </div>
        </div>

        <!-- Right: Apply button -->
        <div class="drive_right">
          <button
            v-if="!drive.already_applied"
            class="btn_apply"
            @click="applyToDrive(drive)"
            :disabled="drive.applying"
          >
            {{ drive.applying ? 'Applying...' : 'Apply Now' }}
          </button>

          <span v-else class="applied_badge">✅ Applied</span>
        </div>

      </div>

      <!-- Empty state -->
      <div class="empty_state" v-if="filteredDrives().length === 0 && !error && !loading">
        <p>🎯 No eligible drives found right now.</p>
        <p class="empty_sub">Check back later or update your profile with correct branch & CGPA.</p>
      </div>

      <!-- Loading state -->
      <p v-if="loading" class="loading_msg">Loading drives...</p>

    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      drives: [],
      student: {
        name: '',
        branch: '',
        cgpa: null,
        year_of_passing: null
      },
      search: '',
      loading: false,
      error: ''
    };
  },

  methods: {

    filteredDrives() {
      const search = this.search.toLowerCase();
      return this.drives.filter(function(drive) {
        return (
          !search ||
          drive.job_title.toLowerCase().includes(search) ||
          drive.company_name.toLowerCase().includes(search)
        );
      });
    },

    async fetchDrives() {
      this.loading = true;
      this.error = '';

      try {
        const res = await fetch('http://127.0.0.1:5000/student/drives', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });

        const data = await res.json();

        if (res.ok) {
          this.drives = data.drives;
          this.student = data.student;
        } else {
          this.error = data.msg || 'Failed to load drives.';
        }

      } catch (err) {
        this.error = "Backend se connect nahi ho pa raha! 'python app.py' chalu karo.";
        console.error('Fetch error:', err);
      } finally {
        this.loading = false;
      }
    },

    async applyToDrive(drive) {
      // Optimistically disable the button while calling API
      drive.applying = true;

      try {
        const res = await fetch(`http://127.0.0.1:5000/student/apply/${drive.drive_id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });

        const data = await res.json();

        if (res.ok) {
          drive.already_applied = true; // mark as applied locally
        } else {
          alert(data.msg || 'Could not apply. Please try again.');
        }

      } catch (err) {
        alert("Backend se connect nahi ho pa raha!");
        console.error('Apply error:', err);
      } finally {
        drive.applying = false;
      }
    }

  },

  async mounted() {
    await this.fetchDrives();
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
  margin-bottom: 20px;
}

/* Error */
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

/* Search bar */
.search_bar {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  margin-bottom: 14px;
}

.search_icon {
  font-size: 16px;
  color: #aaa;
}

.search_bar input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  color: #333;
  background: transparent;
}

/* Profile summary card */
.profile_card {
  background: #f0fdf4;
  border: 1px solid #86efac;
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #166534;
}

.profile_card strong {
  font-weight: 700;
}

.eligibility_note {
  font-size: 12px;
  color: #16a34a;
  margin-top: 4px;
}

/* Drive list */
.drive_list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Drive card */
.drive_card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  padding: 18px 22px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

/* Left section */
.drive_left {
  display: flex;
  gap: 16px;
  flex: 1;
}

/* Company initial avatar */
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

/* Drive info */
.drive_info {
  flex: 1;
}

.drive_info h3 {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 3px;
}

.company_name {
  font-size: 13px;
  color: #666;
  margin-bottom: 6px;
}

.desc {
  font-size: 13px;
  color: #555;
  margin-bottom: 10px;
  line-height: 1.5;
}

/* Details row */
.details_row {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  font-size: 13px;
  color: #555;
  margin-bottom: 10px;
}

/* Branch chips */
.branches_row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.branch_chip {
  background: #e0f2fe;
  color: #0369a1;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
}

/* Right: Apply button */
.drive_right {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.btn_apply {
  padding: 10px 22px;
  background: linear-gradient(to right, #0cb32e, #049421);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  white-space: nowrap;
}

.btn_apply:hover:not(:disabled) {
  transform: scale(1.04);
  background: linear-gradient(to right, #0dcc33, #0cb32e);
}

.btn_apply:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.applied_badge {
  font-size: 13px;
  font-weight: 600;
  color: #166534;
  background: #d1fae5;
  padding: 8px 14px;
  border-radius: 8px;
  white-space: nowrap;
}

/* Empty state */
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