<template>
  <vue-scroll class="page-dashboard">
    <resize-observer @notify="__resizeHanlder"/>
    <!-- title card -->
    <div class="page-header header-primary card-base card-shadow--small">
      <h1>전적 검색</h1>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">
          <i class="mdi mdi-home-outline"></i>
        </el-breadcrumb-item>
        <el-breadcrumb-item>Home</el-breadcrumb-item>
        <el-breadcrumb-item>Status</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 소환사 검색 -->
    <div style="margin-top: 15px;">
      <el-input placeholder="소환사 이름을 입력해주세요..." v-model="summonerInput" class="input-with-select">
        <el-select v-model="select" slot="prepend" placeholder="select">
          <el-option
            v-for="list in regionList.list"
            :key="list.regionCode"
            v-on:click.native="setRegion(list)"
          >{{list.regionName}}</el-option>
        </el-select>
        <el-button slot="append" v-on:click="searchStatus(summonerInput)" icon="el-icon-search"></el-button>
      </el-input>
      <p>소환사이름 : {{summonerData['summonerName']}}</p>
      <p>티어 : {{summonerData['tier']}}</p>
      <p>티어 랭크 : {{summonerData['rank']}}</p>
      <p>점수 : {{summonerData['leaguePoints']}}</p>
      <p>리그 이름 : {{summonerData['leagueName']}}</p>
      <p>승 : {{summonerData['wins']}}</p>
      <p>패 : {{summonerData['losses']}}</p>

      <!--
        summonerName: null,
        tier: null,
        rank: null,
        leaguePoints: null,
        leagueName: null,
        win: null,
        losses: null
      -->
    </div>
  </vue-scroll>
</template>

<script>
import echarts from "echarts";
import { Timeline, TimelineItem, TimelineTitle } from "vue-cute-timeline";
import axios from "axios";
//import Promise from 'es6-promise';

export default {
  name: "Dashboard",
  // vue 의 전역변수
  data() {
    return {
      //summonerData: null,
      summonerData: {
        summonerName: null,
        tier: null,
        rank: null,
        leaguePoints: null,
        leagueName: null,
        wins: null,
        losses: null
        /*
          _this.summonerData["summonerName"] = jsonData["summonerName"];
          _this.summonerData["tier"] = jsonData["tier"];
          _this.summonerData["rank"] = jsonData["rank"];
          _this.summonerData["leagueName"] = jsonData["leagueName"];
          _this.summonerData["wins"] = jsonData["wins"];
          _this.summonerData["losses"] = jsonData["losses"];
          _this.summonerData["leaguePoints"] = jsonData["leaguePoints"];
        */
      },
      summonerInput: "",
      select: "",
      regionCode: "kr",
      regionList: {
        list: [
          { regionCode: "kr", regionName: "KR" },
          { regionCode: "na", regionName: "NA" },
          { regionCode: "eu", regionName: "EU" }
        ]
      },
      asyncComponent: "peity",
      asyncChart1: true,
      chart1: null,
      coinData: null,
      resized: false,
      //curCoinName : 'BTC-KRW',
      curCoinName: null,
      times: 60,
      list: [],
      radio1: "Hour",
      radio2: "Week"
    };
  },
  created: function() {
    // 가장먼저 실행이 된다.
  },
  computed: {
    smallWidget() {
      return (
        this.dashboardWidth >= 970 &&
        this.dashboardWidth <= 1412 &&
        this.windowWidth >= 1200
      );
    }
  },
  // 메서드 선언
  methods: {
    // 지역코드 setMethod(파라미터 region List)
    setRegion(regionList) {
      // 전역변수를 수정할 수 있도록 한다.
      var _this = this;
      // select 변수에 지역이름을 대입
      _this.select = regionList.regionName;
      // 현재 지역코드를 regionList 에 매칭된 것으로 변경
      _this.regionCode = regionList.regionCode;
      this.$message(_this.select + "서버로 변경되었습니다.");
    },
    async searchStatus(summonerinput) {
      var _this = this;
      await axios
        .get("http://127.0.0.1:5000/status/" + summonerinput)
        .then(response => {
          var jsonData = eval(response.data);
          _this.summonerData["summonerName"] = jsonData["summonerName"];
          _this.summonerData["tier"] = jsonData["tier"];
          _this.summonerData["rank"] = jsonData["rank"];
          _this.summonerData["leagueName"] = jsonData["leagueName"];
          _this.summonerData["wins"] = jsonData["wins"];
          _this.summonerData["losses"] = jsonData["losses"];
          _this.summonerData["leaguePoints"] = jsonData["leaguePoints"];
        });

      console.log(_this.summonerData);
    },
    __resizeHanlder: _.throttle(function(e) {
      if (this.resized) {
        this.asyncComponent = null;
        this.removePeity();
        setTimeout(() => {
          this.asyncComponent = "peity";
        }, 1000);
      }
      this.resized = true;
    }, 700),
    removePeity() {
      const peityEl = document.querySelectorAll(".widget .peity"); //.forEach((el)=>{el.remove()})
      //ie fix
      for (let i = 0; i < peityEl.length; i++) {
        peityEl[i].parentNode.removeChild(peityEl[i]);
      }
    }
  },
  beforeMount() {},
  mounted() {
    //this.initChart1()
  },
  beforeDestroy() {},
  components: {
    Timeline,
    TimelineItem,
    TimelineTitle
  }
};
</script>

<style lang="scss" scoped>
@import "../../assets/scss/_variables";

.widget {
  height: 200px;
  position: relative;

  .widget-header {
    .widget-icon-box {
      background: rgba(0, 0, 0, 0.02);
      border: 1px solid rgba(0, 0, 0, 0.02);
      border-radius: 4px;
      text-align: center;
      width: 60px;
      padding: 5px;
    }

    .widget-title {
      font-weight: bold;
    }
  }

  .badge-box {
    .badge {
      //background: rgba(0, 0, 0, .02);
      display: inline-block;
      //padding: 2px 5px;
      //border: 1px solid rgba(0, 0, 0, .02);
      border-radius: 4px;
      font-size: 80%;
    }
  }
}

/*@media (max-width: 768px) {
	.el-row {
		//margin-left: 0 !important;
		//margin-right: 0 !important;

		.el-col-24 {
			//padding-left: 0 !important;
			//padding-right: 0 !important;
		}
	}
}*/

.timeline {
  max-width: 1200px;
  margin: 6px;
}
.timeline,
.timeline-title {
  color: $text-color;
  line-height: 1.4;
  cursor: default;
  font-family: inherit;
}

/*@media (min-width: 1200px) and (max-width: 1850px) {
	.widget {
		.widget-header {
			.widget-icon-box {
				display: none;
			}
		}
	}
}*/
@media (min-width: 768px) and (max-width: 1040px) {
  .radio-switcher {
    display: none;
  }

  .widget {
    .widget-header {
      .widget-icon-box {
        display: none;
      }
    }
  }
}
@media (max-width: 420px) {
  .radio-switcher {
    display: none;
  }
}
</style>

<style lang="scss">
.page-dashboard {
  .widget {
    .peity {
      position: absolute;
      bottom: -1px;
      left: 0;
      border-bottom-left-radius: 5px;
      border-bottom-right-radius: 5px;
    }
  }
  table.styled {
    .peity {
      margin-right: 10px;
    }
  }

  .vb-content {
    padding: 0 20px;
    box-sizing: border-box !important;
    margin-top: -5px;
    margin-left: -20px;
    margin-right: -20px;
    height: calc(100% + 15px) !important;
    width: calc(100% + 40px) !important;
  }
}

@media (max-width: 768px) {
  .page-dashboard {
    .vb-content {
      padding: 0 5px !important;
      margin: -5px;
      width: calc(100% + 10px) !important;
    }
  }
}

.el-select .el-input {
  width: 110px;
}
.input-with-select .el-input-group__prepend {
  background-color: #fff;
}
</style>


