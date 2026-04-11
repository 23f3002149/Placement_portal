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


      </fieldset>


      <fieldset>
        <legend>Academic Information</legend>

        <label for="roll_no">Roll Number:</label>
        <input type="text" id="roll_no"  v-model="roll_no" ><br><br>

        <!-- dropdown for branches -->
         <label for="branch">Branch</label>          
            <!-- <input v-model="branch" placeholder="Branch" /> -->
             <select v-model="branch" id="branch">
               <option  disabled selected>Select Branch</option>
               <option value="CSE">CSE</option>
               <option value="ECE">ECE</option>
               <option value="ME">ME</option>
             </select>

        <label for="cgpa">CGPA:</label>
        <input type="number" id="cgpa" v-model="cgpa" step="0.01" max="10.00" min="0.00"><br><br>

        <label for="year_of_passing">Year of Passing:</label>
        <input type="number" id="year_of_passing"  v-model="year_of_passing" ><br><br>

        <label for="skills">Skills:</label>
        <textarea id="skills"  v-model="skills" ></textarea><br><br>
      </fieldset>

      <fieldset>
        <legend>Password & Security</legend>
        <p>password</p>
        <button class="btn-change-pwd" @click="changePassword">Change Password</button>
      </fieldset>

      <fieldset>
          <p v-if="resume_url">
          Current Resume:
          <a :href="resume_url" target="_blank" class="resume-link">📄 View Uploaded Resume</a>
        </p>
        <p v-else style="color:#888; font-size:13px;">Koi resume upload nahi hua abhi tak.</p>

        <label for="resume_file" style="margin-top:12px;">PDF Upload karo:</label>
        <input type="file" id="resume_file" accept=".pdf" @change="onFileChange" />

        <button
          class="btn-upload"
          @click="uploadResume"
          :disabled="!selectedFile"
          style="margin-top:12px;"
        >
          📤 Upload Resume
        </button>

        <p v-if="uploadMsg" style="margin-top:8px; color:#0cb32e; font-weight:600;">{{ uploadMsg }}</p>
        <p v-if="uploadError" style="margin-top:8px; color:red; font-weight:600;">{{ uploadError }}</p>
      </fieldset>

      <div class="btn-row">
        <button class="btn-cancel" @click="cancel">Cancel</button>
        <button class="btn-save" @click="save">Save Changes</button>
      </div>
      <p v-if="saveMsg" style="margin-top:10px; color:#0cb32e; font-weight:600;">{{ saveMsg }}</p>
      <p v-if="saveError" style="margin-top:10px; color:red; font-weight:600;">{{ saveError }}</p>

     </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      email: "",
      roll_no: "",
      branch: "",
      cgpa: null,
      year_of_passing: null,
      skills: "",
      resume_url: null,
      selectedFile: null,
      uploadMsg: "",
      uploadError: "",
      saveMsg: "",
      saveError: ""
      
    };
  },


  async mounted() {
    try{
      const response = await fetch("http://127.0.0.1:5000/student/info", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token")
        }
      });
      const data = await response.json();
      this.name = data.name;
      this.email = data.email;
      this.roll_no = data.roll_no;
      this.branch = data.branch;
      this.cgpa = data.cgpa;
      this.year_of_passing = data.year_of_passing;
      this.skills = data.skills;
      this.resume_url = data.resume_url || null;
    } catch (error) {
      console.error("Error fetching student info:", error);
    }

  },




  methods: {
    changePassword() {
      // logic to change password
      this.$router.push("/student/change-password");
    },

      // logic to upload resume
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
      this.uploadMsg = "";
      this.uploadError = "";
    },

    async uploadResume() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append("resume", this.selectedFile);

      try {
        const res = await fetch("http://127.0.0.1:5000/student/resume", {
          method: "POST",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
            // Content-Type mat dena — browser khud set karta hai FormData ke liye
          },
          body: formData
        });
        const data = await res.json();
        if (res.ok) {
          this.uploadMsg = "Resume upload ho gaya! ✅";
          this.resume_url = data.resume_url;
          this.selectedFile = null;
        } else {
          this.uploadError = data.msg || "Upload fail ho gaya.";
        }
      } catch (err) {
        this.uploadError = "Backend se connect nahi ho pa raha!";
      }
    },
    cancel() {
      // logic to cancel changes
      this.$router.push("/student/dashboard");
    },
    async save() {
      try {
        const response = await fetch("http://127.0.0.1:5000/student/profile", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("token")
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            roll_no: this.roll_no,
            branch: this.branch,
            cgpa: this.cgpa,
            year_of_passing: this.year_of_passing,
            skills: this.skills
          })
        });
        const data = await response.json();
        if (response.ok) {
          alert("✅ Profile saved successfully!");
        } else {
          alert(data.msg || "Profile save fail ho gaya.");
        }
      } catch (err) {
        alert("Backend se connect nahi ho pa raha!");
      }
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
  color: #0cb32e;
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
select,
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
select:focus,
textarea:focus {
  outline: none;
  border-color: #0cb32e;
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
  background: linear-gradient(to right, #0cb32e, #049421);
  color: white;
}

.btn-save:hover {
  transform: scale(1.04);
  background: linear-gradient(to right, #0dcc33, #0cb32e);
}

.btn-cancel {
  background: #e0e0e0;
  color: #444;
}

.btn-cancel:hover {
  background: #c8c8c8;
}

.btn-change-pwd {
  background: #23ea62;
  color: white;
}

.btn-change-pwd:hover {
  background: #0fe52b;
  transform: scale(1.04);
}

.btn-upload {
  background: linear-gradient(to right, #0c2db3, #7c3aed);
  color: white;
  padding: 10px 22px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.btn-upload:hover {
  transform: scale(1.04);
  background: linear-gradient(to right, #7c3aed, #0c2db3);
}

.btn-upload:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.resume-link {
  color: #0c2db3;
  font-weight: 600;
  text-decoration: none;
  margin-left: 6px;
}

.resume-link:hover {
  text-decoration: underline;
}

</style>