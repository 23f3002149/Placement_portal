<template>
  <div class="new-drive">
    <h1>Create Placement Drive</h1>
    <h3>Fill in the details to post a new drive for students</h3>


    <p v-if="successMsg" class="msg-success">✅ {{ successMsg }}</p>
    <p v-if="errorMsg" class="msg-error">⚠️ {{ errorMsg }}</p>

    <!-- Job Details -->
    <fieldset>
      <legend>Job Details</legend>

      <label for="job_title">Job Title <span class="required">*</span></label>
      <input id="job_title" type="text" v-model="form.job_title" placeholder="e.g. Software Engineer" />

      <label for="job_description">Job Description</label>
      <textarea id="job_description" v-model="form.job_description" placeholder="Describe the role, responsibilities, etc."></textarea>

      <label for="package">Package (LPA) <span class="required">*</span></label>
      <input id="package" type="text" v-model="form.package" placeholder="e.g. 8 LPA" />

      <label for="location">Location <span class="required">*</span></label>
      <input id="location" type="text" v-model="form.location" placeholder="e.g. Bangalore, Remote" />
    </fieldset>


    <!-- Eligibility -->
    <fieldset>
      <legend>Eligibility Criteria</legend>

      <label for="cgpa_criteria">Minimum CGPA <span class="required">*</span></label>
      <input id="cgpa_criteria" type="number" v-model="form.cgpa_criteria" placeholder="e.g. 7.5" step="0.01" min="0" max="10" />

      <label for="application_deadline">Application Deadline <span class="required">*</span></label>
      <input id="application_deadline" type="date" v-model="form.application_deadline" />


    <label>Eligible Branches <span class="required">*</span></label>
      <div class="branch-grid">
        <div v-for="branch in allBranches"  :key="branch" class="branch-chip" :class="{ selected: form.branches.includes(branch) }" @click="toggleBranch(branch)" >
          {{ branch }}
        </div>
      </div>
      <p v-if="form.branches.length" class="selected-info">
        Selected: {{ form.branches.join(', ') }}
      </p>
    </fieldset>

    <!-- Actions -->
    <div class="btn-row">
      <button class="btn-cancel" @click="resetForm">Reset</button>
      <button class="btn-save" @click="createDrive" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Drive' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      allBranches: ['CSE', 'IT', 'ECE', 'ME'],
      form: {
        job_title: '',
        job_description: '',
        package: '',
        location: '',
        cgpa_criteria: '',
        application_deadline: '',
        branches: []

      },
      loading: false,
      successMsg: '',
      errorMsg: ''
    };
  },

  methods: {

    resetForm() {
      this.form = {
        job_title: '',
        job_description: '',
        package: '',
        location: '',
        cgpa_criteria: '',
        application_deadline: '',
        branches: []
      };
      this.successMsg = '';
      this.errorMsg = '';
    },

    validate() {
      if (!this.form.job_title.trim()) return 'Job Title is required.';
      if (!this.form.package.trim()) return 'Package is required.';
      if (!this.form.location.trim()) return 'Location is required.';
      if (!this.form.cgpa_criteria) return 'Minimum CGPA is required.';
      if (!this.form.application_deadline) return 'Application Deadline is required.';
      if (this.form.branches.length === 0) return 'Select at least one eligible branch.';
      return null;
    },








    toggleBranch(branch) {
      const index = this.form.branches.indexOf(branch);
      if (index === -1) {
        this.form.branches.push(branch);
      } else {
        this.form.branches.splice(index, 1);
      }
    },

    async createDrive() {
      this.successMsg = '';
      this.errorMsg = '';

      // Validation
      const validationError = this.validate();
      if (validationError) {
        this.errorMsg = validationError;
        return;
      }

      this.loading = true;

      try{

      const res = await fetch("http://127.0.0.1:5000/company/drives", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("token")
        },
        body: JSON.stringify(this.form)
      });

      const data = await res.json();


      if (res.ok) {
          this.successMsg = 'Drive created successfully! Waiting for admin approval.';
          this.resetForm();
          this.$router.push('/company/dashboard');
        } else {
          this.errorMsg = data.msg || 'Something went wrong. Please try again.';
        }

      } catch (err) {
        console.error('Drive creation error:', err);
        this.errorMsg = "Backend se connect nahi ho pa raha! 'python app.py' chalu karo.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>



<style scoped>

.new-drive {
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
  margin-top: 14px;
}

.required {
  color: #e63946;
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

/* Branch chips */
.branch-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.branch-chip {
  padding: 8px 20px;
  border: 2px solid #ccc;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  color: #555;
  background: #f0f0f0;
  transition: all 0.2s ease;
  user-select: none;
}

.branch-chip:hover {
  border-color: #0c2db3;
  color: #0c2db3;
}

.branch-chip.selected {
  background: #0c2db3;
  border-color: #0c2db3;
  color: white;
}

.selected-info {
  margin-top: 8px;
  font-size: 13px;
  color: #0c2db3;
  font-weight: 600;
}

/* Messages */
.msg-success {
  background: #e6f9ee;
  border: 1px solid #2ecc71;
  color: #1a7a40;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}

.msg-error {
  background: #fdecea;
  border: 1px solid #e63946;
  color: #c1121f;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}

/* Buttons */
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

.btn-save:hover:not(:disabled) {
  transform: scale(1.04);
  background: linear-gradient(to right, #1a3fcc, #0c2db3);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #e0e0e0;
  color: #444;
}

.btn-cancel:hover {
  background: #c8c8c8;
}

</style>