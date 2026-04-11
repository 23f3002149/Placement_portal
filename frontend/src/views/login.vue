<template class="login">
  <div class="login-page">
    <h1>Placement Portal</h1>
    <p class="subtitle">Welcome back! Please login to continue</p>
 

    <!-- login box -->
    <div class="card">


          <h3 class="labels">select role</h3>   
            <div class="roles">
              <div class="role-card" :class="{active: role ==='admin'}" @click="selectRole('admin')"><div class="icon">🛡️</div> Admin</div>
              <div class="role-card" :class="{active: role ==='company'}" @click="selectRole('company')"><div class="icon">🏢</div> Company</div>
              <div class="role-card" :class="{active: role ==='student'}" @click="selectRole('student')"><div class="icon">🎓</div> Student</div>

            </div>
            <p class="role_error" v-if="role_error">{{ role_error }}</p>
          

          <label class="labels" for="email"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Zm0 0c0 1.657 1.007 3 2.25 3S21 13.657 21 12a9 9 0 1 0-2.636 6.364M16.5 12V8.25" /></svg>Email:</label>
          <input type="email" id="email" v-model="email" placeholder="Enter Email" required @click="error_removal"  />
          <label class="labels" for="password">Password:</label>
          <div >
          <input class="password" v-model="password" :type="show_password ? 'text' : 'password'" id="password" placeholder="Enter Password" required @click="error_removal" />
          <span @click="togglePassword" style="cursor: pointer;">👁️</span>
          </div>
          <p class="error" v-if="error">{{ error }}</p>

          <button @click="loginUser">Login</button>

         

          <p class="register" @click="registration" style="cursor:pointer;">
            Go to Register
          </p>
          

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      role: "", // new data property for role
      email: "",
      password: "",
      error: "",
      role_error: "", // new data property for role error
      show_password: false // new data property for password visibility
    };
  },
  methods: {
    error_removal() {
      this.error = "";
    },


    selectRole(selectedRole) {
      this.role = selectedRole;
      this.role_error = "";
      this.error = "";
    },

    togglePassword() {
      this.show_password = !this.show_password;
    },

    registration() {
      if (this.role === "admin") {
        this.error = "Admin registration is not allowed/you cannot register as admin. Please select company or student.";
      } else if (this.role === "company") {
        this.error = "";
        this.$router.push("/register/company");
      } else if (this.role === "student") {
        this.$router.push("/register/student");
        this.error = "";
        this.role_error = "";

      } 
      else {
        this.role_error = "Select role first from Student aur Company to register";
      }
    },


    async loginUser() {
      // validation
      if (!this.role) {
        this.role_error = "Select role first";
        return;
      }
      if(!this.email || !this.password) {
        this.error = "Email and Password are required";
        return;
      }
      try {
        const res = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            role: this.role //  send role
          })
        });

        const data = await res.json();//packed response se json data ko javascript object me convert karkedata nikal lo jo backend ne bheja hai

        if (res.ok) {
          // Token save
          localStorage.setItem("token", data.token);
          localStorage.setItem("role", data.role);

          // Redirect
          this.$router.push(`/${data.role}/dashboard`);

        } 
        else {
          this.error = data.message;
        }

      } catch (err) {
        this.error = "Something went wrong";
      }
    }
  }
};

</script>


<style scoped>
.login-page {
  text-align: center;
  margin-top: 40px;
 
}

svg {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  margin-left: 1px;
  margin-right: 5px;
}

.subtitle {
  color: gray;
}


.labels {
  text-align: left;
  display: block;
  margin-top: 20px;
}
/* Card */
.card {
  width: 400px;
  margin: 20px auto;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 10px 10px 30px rgba(255, 145, 0, 0.482);
  border: 2px solid rgba(255, 0, 0, 0.777);

}

/* Roles */
.roles {
  display: flex;
  justify-content: space-between;
  margin: 20px ;
  gap: 20px;
}

.role-card {
  width: 30%;
  padding: 20px;
  border: 2px solid #ccc;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease;

}

/* Active */
.role-card.active {
  border: 2px solid blue;
  background: #eef;
}

.icon{
    font-size: 30px;
    margin-bottom: 10px;
}

/* Inputs */
input {
  width: 90%;
  padding: 12px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
}

/* Button */
button {
  width: 100%;
  margin: 20px 0;
  padding: 12px;
  background: linear-gradient(to right, blue, purple);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.3s ease, background 0.3s ease;
  
}/*buttons pe color changing animation lagana hai*/

button:hover {
    transform: scale(1.05);
    background: linear-gradient(to right, rgb(0, 255, 170),rgb(114, 230, 114));
    color: seagreen;
}
.role-card:hover {
    transform: scale(1.05);
    border-color: blue;
    
}

.register{
    margin-top: 10px;
    padding: 10px;
    border-radius: 10px;
    /* background: linear-gradient(to right, rgb(114, 230, 114),rgb(0, 255, 170)); */
    transition: all 0.3s ease;
    color: white;
    background:linear-gradient(to right, purple,blue);
}
.register:hover{
    transform: scale(1.05);
    background: linear-gradient(to right, rgb(0, 255, 170),rgb(114, 230, 114));
    color: seagreen;
}

.error{
    color: red;
    margin-top: 10px;
}
.role_error{
    color: red;
    margin-top: 10px;
}

.password{
    width: 85%;
    margin-right: 0px;
}




</style>