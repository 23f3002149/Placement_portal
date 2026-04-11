<template>
<div class="box">
    <div class="header">
      <h1>Manage Companies</h1>
      <p>Review and manage company registrations</p>
    </div>

    
    <p v-if="error" style="color: red; font-weight: bold; padding: 10px;">{{ error }}</p>


    <div class="search_stats">
      <input type="text" v-model="search" placeholder="Search Commpany Name..." />
      <div class="some_stats">
          <div
          v-for="tab in ['All', 'pending', 'approved', 'rejected']"
          :key="tab"
          :class="['tab', { active: selectedStatus === tab }]"
          @click="selectedStatus = tab"
        >
          {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
        </div>
      </div>
    </div>

    <div class="company_list">
      <!-- for loop to show the list of companies -->
       <div class="company" v-for="company in filteredList()" :key="company.company_id" >
            <div class="name_status">
              <h3>{{ company.company_name }}</h3>
              <span  :class="'badge_' + company.company_approved_status" >{{ company.company_approved_status }}</span>

            </div>
                
            <div>
                <p class="desc"> {{ company.description || 'No description available.' }} </p>
                
            </div>

             <div class="contact_row">
              <span>✉️ {{ company.email }}</span>
              <span v-if="company.website">
                🌐 <a :href="company.website" target="_blank">{{ company.website }}</a>
              </span>
            </div>


            <div v-if="company.company_approved_status==='pending'">
                <button class="btn_approve" @click="updateStatus(company.company_id, 'approved')">
              ✅ Approve
            </button>
            <button class="btn_reject" @click="updateStatus(company.company_id, 'rejected')">
              ❌ Reject
            </button>
            </div>


            <button
            v-if="company.company_approved_status === 'approved'"
            class="btn_blacklist"
            @click="updateStatus(company.company_id, 'blacklisted')"
          >
            🚫 Blacklist Company
          </button>







       </div>

       <div class="empty_state" v-if="filteredList().length === 0 && !error">
        <p>No company found.</p>
      </div>

    </div>

</div>
</template>






<script>

export default{
  data(){
    return{
      company_list:[],
      error:"",
      search: "",
      selectedStatus: "All"
      
    }
  },


  methods: {

          filteredList() {
      const search = this.search.toLowerCase();
      const status = this.selectedStatus;

      return this.company_list.filter(company => {
        const matchSearch =
          !search ||
          company.company_name.toLowerCase().includes(search) ||
          company.email.toLowerCase().includes(search);

        const matchStatus =
          status === 'All' || company.company_approved_status === status;

        return matchSearch && matchStatus;
      });
    },
          async updateStatus(company_id, status){
                const token = localStorage.getItem("token");

                const res = await fetch(`http://127.0.0.1:5000/admin/company/${company_id}/status`, {
                  method: "PUT",
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token   
                  },
                  body: JSON.stringify({ status: status })
                });

                if(res.ok){
                  await this.fetchCompanies();
                } else {
                  const data = await res.json();
                  alert("Error: " + data.msg);
                }
              },

              async fetchCompanies(){
                const token = localStorage.getItem("token");

                try {
                  const res = await fetch("http://127.0.0.1:5000/admin/companies", {
                    method: "GET",
                    headers: {
                      "Content-Type": "application/json",
                      Authorization: "Bearer " + token   
                    }
                  });

                  //   res.ok check — agar API error deti hai toh company_list kharab na ho
                  if(res.ok){
                    const data = await res.json();
                    this.company_list = data;
                  } else {
                    const data = await res.json();
                    this.error = data.msg || "Failed to load companies";
                    console.error("API Error:", data);
                  }

                } catch(err) {
                  this.error = "Server se connection nahi ho pa raha. Backend chalu hai?";
                  console.error("Fetch error:", err);
                }
              }
  },


  async mounted() {
    await this.fetchCompanies();
  },

}
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
  transition: all 0.2s ease;
}

.some_stats div:hover {
  background-color: #c0c0c0;
}

.some_stats div.active {
  background-color: #1a1a2e;
  color: white;
}

/* Status badge colors */
.badge_pending   { background: #fef3c7 !important; color: #b45309 !important; }
.badge_approved  { background: #d1fae5 !important; color: #065f46 !important; }
.badge_rejected  { background: #fee2e2 !important; color: #b91c1c !important; }
.badge_blacklisted { background: #e5e7eb !important; color: #374151 !important; }

.empty_state {
  text-align: center;
  padding: 50px 0;
  color: #888;
  font-size: 15px;
}

.company_list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.company {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  padding: 18px 22px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.name_status {
  display: flex;
  align-items: center;
  gap: 12px;
}

.name_status h3 {
  font-size: 17px;
  font-weight: 700;
  color: #1a1a2e;
}

.name_status span {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 12px;
  border-radius: 20px;
  text-transform: capitalize;
  background-color: #fef3c7;
  color: #b45309;
}

.desc {
  color: #666;
  font-size: 14px;
}

.contact_row {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: #555;
  flex-wrap: wrap;
}

.contact_row a {
  color: #2563eb;
  text-decoration: none;
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
  margin-right: 8px;
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
}

.btn_reject:hover {
  background-color: #c1121f;
}

.btn_blacklist {
  padding: 8px 16px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
}

.btn_blacklist:hover {
  background-color: #111;
}


</style>