<template>
  <div class="box">
        <div class="layout">

          <Sidebar 
            title="Company Portal"
            :menu="['Dashboard','Placement Drives','Applications','Profile']"
          />

          <div class="main">
            <router-view />
          </div>

        </div>
  </div>
</template>

<script>
import Sidebar from "../sidebars-headers/company_sidebar.vue";

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
  width: 250px;
  height: 100vh;
  background-color: #0c2db3;
  color: white;
  padding: 20px;
}

:deep(.sidebar ul li:hover){
  background-color: #041e94;
}


:deep(.sidebar .logout button) {
    width: 100%;
    padding: 12px;
    background: linear-gradient(to left, rgb(0, 255, 179), rgb(0, 28, 128));
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: transform 0.3s ease, background 0.3s ease;
}

:deep(.sidebar .logout button:hover) {
    transform: scale(1.04);
    background: linear-gradient(to right, rgb(0, 255, 170),rgb(114, 137, 230));
    color: rgb(46, 72, 139);
}

.main{
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  background-color: whitesmoke;
}



</style>
