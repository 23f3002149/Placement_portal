<template >
  <div class="company_container">

    <h2>Company Register</h2>
    <div class="registration_form">

            <label for="companyName">Company Name</label>
            <input type="text" id="companyName" v-model="companyName" placeholder="Company Name" required />

            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" placeholder="Email" required />

            <label for="password">Password</label>
            <div class="password">
            <input :type="show_password ? 'text': 'password'"  id="password" v-model="password" placeholder="Password" required  />
            <span @click="togglePassword" style="cursor: pointer;">👁️</span>
            </div>

            <label for="name">HR Name</label>
            <input type="text" id="name" v-model="name" placeholder="HR Name" required   />

            <p class="error" v-if="error" style="color: crimson; text-align: center; margin-top: 10px;">{{ error }}</p>
            <p class="success" v-if="success_msg" style="color: green; text-align: center; margin-top: 10px;">{{ success_msg }}</p>

            <button @click="registerCompany">Register</button>
            <button @click="login">Login</button>


    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      companyName: "",
      email: "",
      password: "",
      name: "",
      error: "",
      success_msg: "",
      show_password: false
    };
  },

  methods: {
      login() {
        this.$router.push("/");
      },

      togglePassword() {
          this.show_password = !this.show_password;
        },

    async registerCompany() {
      try {

        // #vallidation
          if (!this.companyName || !this.email || !this.password || !this.name) {
            this.error = "All fields are required.";
            return;
          }

        const res = await fetch("http://127.0.0.1:5000/company/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            company_name: this.companyName,
            email: this.email,
            password: this.password,
            name: this.name
          })
        });

        const data = await res.json();

        if (res.ok) {
          alert(data.success_msg);
          this.success_msg = data.success_msg;
          this.$router.push("/");
        } else {
          this.error = data.msg;
         
        }

      } catch (err) {
        this.error = "Server error";
      }
    }
  }
};
</script>







<style scoped>
*{
    margin: 0;
    padding: 0;
}


.company_container{
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    height: 100vh;
    width: 100%;
    background: linear-gradient(to bottom, #2cb7a9, #e0eafc);
    /* background-color: white; */
}
h2{
    margin-top: 100px;
    margin-bottom: 50px;
    color: #42ffec;
    transform: scale(1.5)
;
}

.registration_form{
    display: flex;
    flex-direction: column;
    width: 500px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background:linear-gradient(to bottom ,rgb(0, 119, 255),rgb(135, 232, 235));
    box-shadow: 0px 0px 40px rgba(75, 51, 195, 0.755);  
    border: #007BFF solid 2px;
}
.registration_form label {
    margin-top: 10px;
}

.registration_form input {
    padding: 10px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

button{
    margin: 20px 10px;
    padding: 10px ;
    border-radius: 5px;
    border: none;
    background-color: #007BFF;
    color: white;
    cursor: pointer;
    box-shadow:  10px 10px 40px rgba(106, 227, 233, 0.755);
    transition: all 0.3s ease;

}

label{
    color: #fff;
}

/*transition*/
button:hover{
    background-color: #0056b3;
    box-shadow: 10px 10px 40px rgba(0, 86, 179, 0.755);
    transform: scale(1.05);
}

.password input{
    width: 90%;
    

}





</style>