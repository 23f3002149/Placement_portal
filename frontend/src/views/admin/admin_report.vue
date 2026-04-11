<template>
  <div class="box">

    <!-- Header -->
    <div class="header">
      <h1>Placement Report</h1>
      <p>Analytics and statistics for the placement portal</p>
    </div>

    <!-- Error -->
    <p v-if="error" class="error_msg">⚠️ {{ error }}</p>
    <p v-if="loading" class="loading_msg">Loading report...</p>

    <template v-if="report && !loading">

      <!-- Row 1: Overview big stat cards -->
      <div class="section_title">📊 Overview</div>
      <div class="stats_row">
        <div class="big_stat red">
          <p>Total Students</p>
          <h2>{{ report.students.total }}</h2>
        </div>
        <div class="big_stat">
          <p>Total Companies</p>
          <h2>{{ report.companies.total }}</h2>
          <span>{{ report.companies.approved }} approved</span>
        </div>
        <div class="big_stat">
          <p>Total Drives</p>
          <h2>{{ report.drives.total }}</h2>
          <span>{{ report.drives.approved }} approved</span>
        </div>
        <div class="big_stat">
          <p>Total Applications</p>
          <h2>{{ report.applications.total }}</h2>
        </div>
        <div class="big_stat green">
          <p>Placement Rate</p>
          <h2>{{ report.placement_rate }}%</h2>
          <span>{{ report.applications.selected }} students selected</span>
        </div>
      </div>

      <!-- Row 2: Companies + Drives breakdown -->
      <div class="two_col">

        <!-- Companies breakdown -->
        <div class="breakdown_card">
          <h3>🏢 Companies</h3>
          <div class="breakdown_row">
            <span class="label">Total</span>
            <div class="bar_wrap">
              <div class="bar grey" :style="{ width: '100%' }"></div>
            </div>
            <span class="val">{{ report.companies.total }}</span>
          </div>
          <div class="breakdown_row">
            <span class="label">Approved</span>
            <div class="bar_wrap">
              <div class="bar green" :style="barWidth(report.companies.approved, report.companies.total)"></div>
            </div>
            <span class="val green_text">{{ report.companies.approved }}</span>
          </div>
          <div class="breakdown_row">
            <span class="label">Pending</span>
            <div class="bar_wrap">
              <div class="bar yellow" :style="barWidth(report.companies.pending, report.companies.total)"></div>
            </div>
            <span class="val yellow_text">{{ report.companies.pending }}</span>
          </div>
          <div class="breakdown_row">
            <span class="label">Rejected</span>
            <div class="bar_wrap">
              <div class="bar red_bar" :style="barWidth(report.companies.rejected, report.companies.total)"></div>
            </div>
            <span class="val red_text">{{ report.companies.rejected }}</span>
          </div>
        </div>

        <!-- Drives breakdown -->
        <div class="breakdown_card">
          <h3>📋 Drives</h3>
          <div class="breakdown_row">
            <span class="label">Total</span>
            <div class="bar_wrap">
              <div class="bar grey" :style="{ width: '100%' }"></div>
            </div>
            <span class="val">{{ report.drives.total }}</span>
          </div>
          <div class="breakdown_row">
            <span class="label">Approved</span>
            <div class="bar_wrap">
              <div class="bar green" :style="barWidth(report.drives.approved, report.drives.total)"></div>
            </div>
            <span class="val green_text">{{ report.drives.approved }}</span>
          </div>
          <div class="breakdown_row">
            <span class="label">Pending</span>
            <div class="bar_wrap">
              <div class="bar yellow" :style="barWidth(report.drives.pending, report.drives.total)"></div>
            </div>
            <span class="val yellow_text">{{ report.drives.pending }}</span>
          </div>
          <div class="breakdown_row">
            <span class="label">Rejected</span>
            <div class="bar_wrap">
              <div class="bar red_bar" :style="barWidth(report.drives.rejected, report.drives.total)"></div>
            </div>
            <span class="val red_text">{{ report.drives.rejected }}</span>
          </div>
        </div>

      </div>

      <!-- Row 3: Applications breakdown -->
      <div class="section_title">📬 Applications Breakdown</div>
      <div class="stats_row">
        <div class="small_stat">
          <p>Total</p>
          <h3>{{ report.applications.total }}</h3>
        </div>
        <div class="small_stat yellow_border">
          <p>Applied</p>
          <h3 class="yellow_text">{{ report.applications.applied }}</h3>
        </div>
        <div class="small_stat purple_border">
          <p>Shortlisted</p>
          <h3 class="purple_text">{{ report.applications.shortlisted }}</h3>
        </div>
        <div class="small_stat green_border">
          <p>Selected</p>
          <h3 class="green_text">{{ report.applications.selected }}</h3>
        </div>
        <div class="small_stat red_border">
          <p>Rejected</p>
          <h3 class="red_text">{{ report.applications.rejected }}</h3>
        </div>
      </div>

      <!-- Row 4: Branch-wise stats + Top Companies -->
      <div class="two_col">

        <!-- Branch stats -->
        <div class="breakdown_card">
          <h3>🎓 Branch-wise Placement</h3>
          <div v-if="report.branch_stats.length === 0" class="no_data">No branch data yet.</div>
          <div class="branch_row" v-for="b in report.branch_stats" :key="b.branch">
            <div class="branch_name">{{ b.branch }}</div>
            <div class="branch_bar_wrap">
              <div
                class="branch_bar"
                :style="barWidth(b.selected, b.total_students)"
              ></div>
            </div>
            <div class="branch_nums">
              <span class="green_text">{{ b.selected }} selected</span>
              <span class="grey_text">/ {{ b.total_students }} total</span>
            </div>
          </div>
        </div>

        <!-- Top companies -->
        <div class="breakdown_card">
          <h3>🏆 Top Companies</h3>
          <div v-if="report.top_companies.length === 0" class="no_data">No company data yet.</div>
          <div class="company_row" v-for="(c, i) in report.top_companies" :key="c.company_name">
            <div class="rank">{{ i + 1 }}</div>
            <div class="company_info">
              <p class="company_name_text">{{ c.company_name }}</p>
              <p class="company_sub">
                {{ c.total_drives }} drive(s) &nbsp;·&nbsp;
                {{ c.total_applications }} application(s) &nbsp;·&nbsp;
                <span class="green_text">{{ c.selected }} selected</span>
              </p>
            </div>
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
      report: null,
      loading: false,
      error: ''
    };
  },

  methods: {

    // Helper to compute bar width percentage as inline style
    barWidth(value, total) {
      if (!total) return { width: '0%' };
      const pct = Math.round((value / total) * 100);
      return { width: pct + '%' };
    },

    async fetchReport() {
      this.loading = true;
      this.error = '';
      try {
        const res = await fetch('http://127.0.0.1:5000/admin/report', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });
        const data = await res.json();
        if (res.ok) {
          this.report = data;
        } else {
          this.error = data.msg || 'Failed to load report.';
        }
      } catch (err) {
        this.error = "Backend se connect nahi ho pa raha! 'python app.py' chalu karo.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    }

  },

  async mounted() {
    await this.fetchReport();
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

.section_title {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 12px;
  margin-top: 8px;
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

/* ---- Overview stat cards ---- */
.stats_row {
  display: flex;
  gap: 14px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.big_stat {
  background: white;
  border-radius: 12px;
  padding: 18px 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  flex: 1;
  min-width: 120px;
  border-top: 3px solid #e0e0e0;
}

.big_stat.red   { border-top-color: #f13d29; }
.big_stat.green { border-top-color: #2ecc71; }

.big_stat p {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
}

.big_stat h2 {
  font-size: 28px;
  font-weight: 800;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.big_stat span {
  font-size: 12px;
  color: #aaa;
}

/* Small stat cards */
.small_stat {
  background: white;
  border-radius: 10px;
  padding: 14px 18px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  flex: 1;
  min-width: 90px;
}

.small_stat p  { font-size: 12px; color: #888; margin-bottom: 6px; }
.small_stat h3 { font-size: 22px; font-weight: 700; color: #1a1a2e; }

.yellow_border { border-left: 3px solid #f59e0b; }
.purple_border { border-left: 3px solid #7c3aed; }
.green_border  { border-left: 3px solid #16a34a; }
.red_border    { border-left: 3px solid #dc2626; }

/* ---- Two column layout ---- */
.two_col {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.breakdown_card {
  background: white;
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  flex: 1;
  min-width: 260px;
}

.breakdown_card h3 {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 16px;
}

/* Bar rows inside breakdown cards */
.breakdown_row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.label {
  font-size: 13px;
  color: #555;
  width: 70px;
  flex-shrink: 0;
}

.bar_wrap {
  flex: 1;
  background: #f0f0f0;
  border-radius: 20px;
  height: 8px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 20px;
  transition: width 0.4s ease;
  min-width: 4px;
}

.bar.grey    { background: #d0d0d0; }
.bar.green   { background: #2ecc71; }
.bar.yellow  { background: #f59e0b; }
.bar.red_bar { background: #e63946; }

.val { font-size: 13px; font-weight: 700; width: 28px; text-align: right; }

/* Branch stats */
.branch_row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.branch_name {
  width: 50px;
  font-size: 13px;
  font-weight: 600;
  color: #444;
  flex-shrink: 0;
}

.branch_bar_wrap {
  flex: 1;
  background: #f0f0f0;
  border-radius: 20px;
  height: 8px;
  overflow: hidden;
}

.branch_bar {
  height: 100%;
  background: #f13d29;
  border-radius: 20px;
  transition: width 0.4s ease;
  min-width: 4px;
}

.branch_nums {
  font-size: 12px;
  white-space: nowrap;
  display: flex;
  gap: 4px;
}

/* Top companies */
.company_row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.company_row:last-child { border-bottom: none; }

.rank {
  width: 28px;
  height: 28px;
  background: #f13d29;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.company_name_text {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
}

.company_sub {
  font-size: 12px;
  color: #888;
  margin-top: 2px;
}

/* Color utilities */
.green_text  { color: #16a34a; font-weight: 600; }
.yellow_text { color: #b45309; font-weight: 600; }
.purple_text { color: #6d28d9; font-weight: 600; }
.red_text    { color: #dc2626; font-weight: 600; }
.grey_text   { color: #aaa; }

.no_data {
  text-align: center;
  color: #bbb;
  padding: 20px 0;
  font-size: 14px;
}

</style>