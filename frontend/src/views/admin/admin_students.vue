<template>
<div class="box">
    <div class="header">
      <h1>Manage Students</h1>
      <p>View and manage registered students</p>
    </div>

    <!-- Error message - agar kuch galat ho -->
    <p v-if="error" style="color: red; padding: 10px;">⚠️ {{ error }}</p>

    <div class="stats_row">
      <div class="stat_card"> 
        <p>Total Students</p>
        <!-- <h2>{{ student_list.length }}</h2> yee bhi sahi hai vaise -->
         <h2>{{ totalStudents() }}</h2>
      </div>
      <div class="stat_card">
        <p>Average CGPA</p>
        <h2>{{ avgCgpa() }}</h2>
      </div>
      <div class="stat_card">
        <p>Unique Branches</p>
        <h2>{{ uniqueBranchCount() }}</h2>
      </div>
    </div>

    <div class="search_bar">
      <input type="text" v-model="search" placeholder="Search by name, roll no, email..." />
      <select v-model="selectedBranch">
        <option value="">All Branches</option>
        <option value="CSE">CSE</option>
        <option value="ECE">ECE</option>
        <option value="ME">ME</option>
      </select>
    </div>

    <div class="student_list">
      <!-- for loop to show the list of students -->
       <div class="student_card"   v-for="student in filteredList()" :key="student.student_id">
        <div class="avatar">{{ student.name.charAt(0) }}</div>
        <div class="student_info">
          <h3>{{ student.name }} <span class="roll_badge">{{ student.roll_no }}</span></h3>
          <p>🎓 {{ student.branch }} &nbsp; | &nbsp; 🏅 CGPA: {{ student.cgpa ?? 'N/A' }} &nbsp; | &nbsp; ✉️ {{ student.email }}</p>
          <p>Skills: {{ student.skills || 'N/A' }}</p>
        </div>
        <div class="card_actions">
          <a
            v-if="student.resume_url"
            :href="student.resume_url"
            target="_blank"
            class="btn_resume"
          >
            📄 Resume
          </a>
          <span v-else class="no_resume">📭 No Resume</span>
        <button class="btn_deactivate" @click="deactivateStudent(student)">🚫 Deactivate</button>
      </div>
      </div>
    </div>
</div>
</template>







<script>

export default {
  data() {
    return {
      student_list: [],
      search: "",
      selectedBranch: "",
      error:""
    };
  },

 methods: {

    // Search + branch filter
    filteredList() {

      // Normal function ke andar this. kaam nahi karta
      // Isliye pehle local variables mein save kar lo
      const search = this.search;
      const selectedBranch = this.selectedBranch;

      return this.student_list.filter(function(student) {

        const matchSearch =
          !search ||
          student.name.toLowerCase().includes(search.toLowerCase()) ||
          student.roll_no.toLowerCase().includes(search.toLowerCase()) ||
          student.email.toLowerCase().includes(search.toLowerCase());

        const matchBranch = !selectedBranch || student.branch === selectedBranch;

        return matchSearch && matchBranch;
      });
    },

    // Total students count
    totalStudents() {
      return this.student_list.length;
    },

    // Average CGPA calculate karo
    avgCgpa() {
      const withCgpa = this.student_list.filter(s => s.cgpa);
      if (!withCgpa.length) return "N/A";
      const total = withCgpa.reduce((sum, s) => sum + s.cgpa, 0);
      return (total / withCgpa.length).toFixed(2);
    },

    // Unique branch count
    uniqueBranchCount() {
      const branches = this.student_list.map(s => s.branch).filter(Boolean);
      return new Set(branches).size;
    },

    // Deactivate button
    deactivateStudent(student) {
      alert(student.name + " deactivate karna chahte ho? (Feature coming soon)");
    },

    // API se students fetch karo
    async fetchStudents() {
      const token = localStorage.getItem("token");
            console.log("Token hai ya nahi:", token);   // debug step 1

      try { 
      const res = await fetch("http://127.0.0.1:5000/admin/students", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token
        }
      });

      const data = await res.json();
       console.log("Backend se aaya:", data);//ye debug step hai

      if (res.ok) {
        this.student_list = data;
      } else {
        // Backend ne error diya (jaise 403 Unauthorized)
          this.error = data.msg || "Students load nahi ho sake";


      }

    } catch (err) {
      // Backend chalu hi nahi hai — fetch crash ho gaya
        this.error = "Backend se connect nahi ho pa raha! 'python app.py' chalu karo.";
        console.error("Fetch crash:", err);
      }
    }

  },

  async mounted() {
    await this.fetchStudents();
  }

};
















</script>






/* .box{
  width: 100%;
  height: 100vh;
  margin:20px;
  padding: 20px;
} */



<style scoped>
.box {
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats_row {
  display: flex;
  gap: 16px;
}

.stat_card {
  background: white;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  flex: 1;
}

.search_bar {
  display: flex;
  gap: 12px;
}

.search_bar input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.search_bar select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.student_card {
  background: white;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #2ecc71;
  color: white;
  font-size: 22px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.student_info {
  flex: 1;
}

.roll_badge {
  background: #dbeafe;
  color: #2563eb;
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 20px;
  margin-left: 8px;
}

.btn_deactivate {
  padding: 8px 16px;
  background: #e63946;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}



.card_actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.btn_resume {
  display: inline-block;
  padding: 8px 16px;
  background: linear-gradient(to right, #0c2db3, #7c3aed);
  color: white;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn_resume:hover {
  transform: scale(1.04);
  background: linear-gradient(to right, #7c3aed, #0c2db3);
}

.no_resume {
  font-size: 12px;
  color: #aaa;
  white-space: nowrap;
}
</style>


