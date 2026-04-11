<template>
    <div class="change-password">
    <h1>Change Password</h1>
    <h3>Update your account password</h3>

    <fieldset>
      <legend>Password Details</legend>
        
        <label for="current_password">Current Password:</label>
        <input type="password" id="current_password" v-model="current_password" placeholder="Enter current password" required><br><br>
    
        <label for="new_password">New Password:</label>
        <input type="password" id="new_password" v-model="new_password" placeholder="Enter new password" required><br><br>
    
        <label for="confirm_password">Confirm New Password:</label>
        <input type="password" id="confirm_password" v-model="confirm_password" placeholder="Re-enter new password" required><br><br>

    </fieldset>

    <div class="btn">
        <button class="btn-cancel" @click="cancelRedirect">cancel</button>
        <button class="btn-save" @click="change_password">Change Password</button>
    </div>

    </div>
</template>


<script>
    export default {
        data() {
            return {
                current_password: "",
                new_password: "",
                confirm_password: ""
            };
        },


        methods: {

            async change_password() {
                if (this.new_password !== this.confirm_password) {
                    alert("New password and confirm password do not match.");
                    return;
                }
                else if(this.new_password==="" || this.current_password===""){
                    alert("Please fill in all fields.");
                    return;
                }

                try {
                    const response = await fetch("http://127.0.0.1:5000/change_password", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: "Bearer " + localStorage.getItem("token")

                        },
                        body: JSON.stringify({
                            old_password: this.current_password,
                            new_password: this.new_password
                        })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        alert("Password changed successfully.");
                        // Redirect based on role from response or localStorage
                        const role = data.role || localStorage.getItem("role");
                        if (role === "company") {
                            this.$router.push("/company/dashboard");
                        } else if (role === "admin") {
                            this.$router.push("/admin/dashboard");
                        } else {
                            this.$router.push("/student/dashboard");
                        }
                    } else {
                        const data = await response.json();
                        alert(data.error || "Failed to change password.");
                    }
                } catch (error) {
                    console.error("Error changing password:", error);
                    alert("An error occurred while changing the password. Please try again later.");
                        }


            },

            cancelRedirect() {
                // Role check karke sahi dashboard pe jaao
                const role = localStorage.getItem("role");
                if (role === "company") {
                    this.$router.push("/company/dashboard");
                } else if (role === "admin") {
                    this.$router.push("/admin/dashboard");
                } else {
                    this.$router.push("/student/dashboard");
                }
            }
        }
    }

</script>



<style scoped>

.change-password {
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
  color: #1a1a2e;
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

input {
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

input:focus {
  outline: none;
  border-color: #1a1a2e;
  background-color: #fff;
}

.btn-row {
  display: flex;
  gap: 10px;
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
  background: linear-gradient(to right, #1a1a2e, #2e2e50);
  color: white;
}

.btn-save:hover {
  transform: scale(1.04);
  background: linear-gradient(to right, #2e2e50, #1a1a2e);
}

.btn-cancel {
  background: #e0e0e0;
  color: #444;
}

.btn-cancel:hover {
  background: #c8c8c8;
}

.btn{
    display:flex;
    gap:10px
}

</style>

