<template>
  <div class="student_container">

    <h2>Student Register</h2>

    <div class="registration_form">

            <label for="name">Name</label>
            <input id="name" v-model="name" placeholder="Name" />

            <label for="email">Email</label>
            <input id="email" type="email"  v-model="email" placeholder="Email" />


            <label for="branch">Branch</label>          
            <!-- <input v-model="branch" placeholder="Branch" /> -->
             <select v-model="branch" id="branch">
               <option value="" disabled selected>Select Branch</option>
               <option value="CSE">CSE</option>
               <option value="ECE">ECE</option>
               <option value="ME">ME</option>
             </select>

            <label for="roll_no">Roll No</label>
            <input id="roll_no" type="text" v-model="roll_no" placeholder="Roll No" />
            



            <label for="password">Password</label>  
            <div class="password">
            <input id="password" :type="show_password ? 'text': 'password'" v-model="password" placeholder="Password" />
            <span @click="togglePassword" style="cursor: pointer;">👁️</span>
            </div>

            
            <p v-if="error">{{ error }}</p>

            <button @click="registerStudent">Register</button>

            <button @click="$router.push('/')">Login</button>
            


     </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      email: "",
      password: "",
      branch: "",
      roll_no: "",
      error: "",
      show_password: false
    };
  },

  methods: {

    togglePassword() {
      this.show_password = !this.show_password;
    },




    async registerStudent() {
      try {

        // #validation
        if (!this.name || !this.email || !this.password || !this.branch || !this.roll_no) {
          this.error = "All fields are required.";
          return;
        }

        const res = await fetch("http://127.0.0.1:5000/students/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name: this.name,
            email: this.email,
            password: this.password,
            branch: this.branch,
            roll_no: this.roll_no
          })
        });

        const data = await res.json();

        if (res.ok) {
          alert(data.message);
          this.$router.push("/");
        } else {
          this.error = data.message;
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
    margin: 0px;
    padding: 0px;
}


.student_container{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* background-color: #f0f0f0; */
    background: linear-gradient(to bottom,  rgb(184, 233, 106), rgb(62, 245, 184));

}
h2{
    margin-bottom: 20px;
    font-size: 40px;
    color: green;
}


.registration_form{
    display: flex;
    flex-direction: column;
    width: 500px;
    padding: 20px;
    background: linear-gradient(to right, rgb(212, 240, 213));
    border-radius: 10px;
    box-shadow: 0 0 600px rgba(243, 250, 29, 0.921);
}

.registration_form input{
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    
}

select{
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
}

.registration_form button{
    margin-top: 10px; 
    padding: 10px ;  
    border-radius: 5px;
    border: none;
    /* background-color: #007BFF; */
    background: linear-gradient(to right ,rgb(184, 233, 106), rgb(62, 245, 184));
    color: white;
    cursor: pointer;
    box-shadow:  10px 10px 40px rgba(106, 227, 233, 0.755);
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.registration_form button:hover{
    box-shadow:  5px 5px 20px rgba(106, 227, 233, 0.755);
    background: linear-gradient( to right , rgb(98, 255, 0), rgb(47, 245, 195));
    transform: scale(1.05);
}

.password input{
    width: 91%;
}

</style>