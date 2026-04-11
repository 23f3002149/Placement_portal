<template>
  <div class="student-profile">
     <h1>My Profile</h1>

     <h3>Update Your Profile</h3>

     <div>
      <fieldset>
        <legend>Personal Information</legend>
        <label for="name">Name:</label>
        <input type="text" id="name"  v-model="name" ><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email"  v-model="email" ><br><br>
      
        <label for="company_name">Company Name:</label>
        <input type="text" id="company_name"  v-model="company_name" ><br><br>

        <label for="industry">Industry:</label>
        <input type="text" id="industry"  v-model="industry" ><br><br>

        <label for="description">Description:</label>
        <textarea id="description"  v-model="description" ></textarea><br><br>

        <label for="website">Website:</label>
        <input type="url" id="website"  v-model="website" ><br><br>

      </fieldset>

      <fieldset>
        <legend>Password & Security</legend>
        <button class="btn-change-pwd" @click="changePassword">Change Password</button>
      </fieldset>

      <!-- <fieldset>
        <legend>Resume</legend>
        <p>Upload your resume</p>
        <input type="file" @change="uploadResume">
      </fieldset> -->

      <div class="btn-row">
        <button class="btn-cancel" @click="cancel">Cancel</button>
        <button class="btn-save" @click="save">Save Changes</button>
      </div>


     </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      email: "",
      company_name: "",
      industry: "",
      description: "",
      website: ""
      
    };
  },


  async mounted() {
    try{
      const response = await fetch("http://127.0.0.1:5000/company/info", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token")
        }
      });
      const data = await response.json();
      this.name = data.name;
      this.email = data.email;
      this.company_name = data.company_name;
      this.industry = data.industry;
      this.description = data.description;
      this.website = data.website;
    } catch (error) {
      console.error("Error fetching company info:", error);
    }

  },




  methods: {
    changePassword() {
      // logic to change password
      this.$router.push("/company/change-password");
    },

    cancel() {
      // logic to cancel changes
      this.$router.push("/company/dashboard");
    },
    async save() {
      // logic to save changes
      const response = await fetch("http://127.0.0.1:5000/company/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify({
          name: this.name,
          email: this.email,
          company_name: this.company_name,
          industry: this.industry,
          description: this.description,
          website: this.website
        })
      }); 
    }
  }
};
</script>

<style scoped>
.student-profile {
  width: 100%;
  padding: 28px;
  background-color: #f5f6fa;
}

h1 {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 4px;
}

h3 {
  font-size: 14px;
  color: #888;
  font-weight: 400;
  margin-bottom: 24px;
}

fieldset {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

legend {
  font-size: 14px;
  font-weight: 700;
  color: #0c2db3;
  padding: 0 8px;
  letter-spacing: 0.5px;
}

label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #444;
  margin-bottom: 5px;
  margin-top: 12px;
}

input,
textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  background-color: #fafafa;
  color: #333;
  box-sizing: border-box;
  transition: border 0.2s ease;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #0c2db3;
  background-color: #fff;
}

textarea {
  resize: vertical;
  min-height: 90px;
}

.btn-row {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

button {
  padding: 10px 22px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.btn-save {
  background: linear-gradient(to right, #0c2db3, #041e94);
  color: white;
}

.btn-save:hover {
  transform: scale(1.04);
  background: linear-gradient(to right, #1a3fcc, #0c2db3);
}

.btn-cancel {
  background: #e0e0e0;
  color: #444;
}

.btn-cancel:hover {
  background: #c8c8c8;
}

.btn-change-pwd {
  background: #4e4edf;
  color: white;
}

.btn-change-pwd:hover {
  background: #4242e4;
  transform: scale(1.04);
}


</style>