<template>
  <div class="box">
        <div class="layout">

          <Sidebar 
            title="Admin Portal"
            :menu="['Dashboard','Companies','Students','Placement Drives','Report']"
            
          />

          <div class="main">
            <router-view />
          </div>

        </div>
  </div>
</template>

<script>
import Sidebar from "../sidebars-headers/admin_sidebar.vue";

export default {
  components: { Sidebar }
};
</script>



<style scoped>      

*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}


.layout{
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}

.sidebar{
  width: 18%;
  height: 100vh;
  background-color: #f13d29e3;
  color: white;
  padding: 20px;
}

:deep(.sidebar ul li:hover){
  background-color : #ff0000;
  color: white;
}


:deep(.sidebar .logout button) {
    width: 100%;
    padding: 12px;
    background: linear-gradient(to left, rgb(255, 47, 0), rgb(249, 15, 54));
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: transform 0.3s ease, background 0.3s ease;
}

:deep(.sidebar .logout button:hover) {
    transform: scale(1.04);
    background: linear-gradient(to right, rgb(255, 0, 119),rgb(234, 25, 25));
    color: rgb(248, 237, 247);
}

.main{
  flex: 1;
  height: 100vh;
  overflow-x: hidden;
  background-color: whitesmoke;
}




</style>
