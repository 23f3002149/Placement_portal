<template>
  <div class="sidebar">

    <h2 >{{ title }}</h2>

    <ul>
      <li v-for="item in menu" :key="item" @click="navigation(item)">
        {{ item }}
      </li>
    </ul>

    <div class="logout">
        <hr>
        <div>{{ admin_name }}</div>
        <button @click="handleLogout">Logout</button>
    </div>

  </div>
</template>

<script>
export default {
    props: ["title", "menu"],
    data() {
        return {
            admin_name: "Loading..."
        };
    },
    async mounted() {
        try {
            const res = await fetch("http://127.0.0.1:5000/profile", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + localStorage.getItem("token")
                }
            });
            const data = await res.json();
            if (res.ok) {
                this.admin_name = data.name;
            }
        } catch (err) {
            console.error("Admin name fetch failed:", err);
            this.admin_name = "Admin";
        }
    },
  
  
  
    methods: {
    handleLogout() {
        // Clear user data from localStorage
        localStorage.removeItem("token");
        localStorage.removeItem("role");

        // Redirect to login page
        this.$router.push("/");
            },



    navigation( item) {
        if (item === "Dashboard") {
            this.$router.push("/admin/dashboard");
        } else if (item === "Companies") {
            this.$router.push("/admin/companies");
        } else if (item === "Students") {
            this.$router.push("/admin/students");
        } else if (item === "Placement Drives") {
            this.$router.push("/admin/drives");
        } else if (item === "Report") {
            this.$router.push("/admin/report");
        }
      }

  }




}

</script>




<style scoped>  
.sidebar{
  position: relative;
  width: 250px;
  height: 100vh;
  color: white;
  padding: 250px;
}

.sidebar h2{
  margin-bottom: 30px;
}

.sidebar ul{
  list-style: none;
}

.sidebar ul li{
  margin-bottom: 15px;
  width: 90%;
  cursor: pointer;
  padding: 12px;
  border-radius: 8px;
  transition: background-color 0.2s ease, color 0.2s ease;

}


.logout{
    position:absolute;
    bottom: 20px;
    width: 90%;
  
}
.logout button{
    width: 100%;
    padding: 12px;
    /* background: linear-gradient(to left, rgb(0, 255, 179), rgb(0, 128, 2)); */
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: transform 0.3s ease, background 0.3s ease;
}

.logout div{
    margin: 10px;
    font-size: 18px;
    font-weight: bold;
    text-align:left;
}

</style>
