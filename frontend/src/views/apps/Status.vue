<template>
  <vue-scroll class="page-dashboard">
    <resize-observer @notify="__resizeHanlder"/>
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

    <!-- DropDown code-->
    <div style="margin-top: 15px;">
      <el-input placeholder="소환사 이름을 입력해주세요..." v-model="summonerinput" class="input-with-select">
        <el-select v-model="select" slot="prepend" placeholder="select">
          <el-option
            v-for="list in regionList.list"
            :key="list.regionCode"
            v-on:click.native="setRegion(list)"
          >{{list.regionName}}</el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search"></el-button>
      </el-input>
    </div>
    <!-- DropDown end-->
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
      summonerinput: "",
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
      coinList: {
        list: [
          { coinCode: "btc_krw", coinName: "BTC-KRW" },
          { coinCode: "etc_krw", coinName: "ETC-KRW" },
          { coinCode: "eth_krw", coinName: "ETH-KRW" },
          { coinCode: "xrp_krw", coinName: "XRP-KRW" }
        ]
      },
      times: 60,
      list: [],
      radio1: "Hour",
      radio2: "Week",
      data3: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        datasets: [
          {
            label: "Visitors",
            backgroundColor: "#fff",
            stack: "Stack 0",
            data: [23, 41, 34, 62, 46, 57, 68]
          }
        ]
      },
      options3: {
        maintainAspectRatio: false,
        title: {
          display: false,
          text: "Chart.js Bar Chart - Stacked"
        },
        legend: {
          display: false
        },
        tooltips: {
          mode: "index",
          intersect: false
        },
        responsive: true,
        scales: {
          xAxes: [
            {
              stacked: true,
              gridLines: {
                display: false,
                drawBorder: false
              },
              ticks: {
                fontColor: "#fff"
              }
            }
          ],
          yAxes: [
            {
              stacked: true,
              gridLines: {
                display: false,
                drawBorder: false
              },
              ticks: {
                display: false
              }
            }
          ]
        }
      }
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
      this.$message(_this.regionName + "서버로 변경되었습니다.");
    },
    async loadQuote(coinData, times) {
      //기본 코인 정보 btc_krw
      // _this 해야지 수정이 가능하다.
      var _this = this;
      _this.curCoinName = coinData;
      await axios
        .get(
          "http:/ec2-54-180-81-15.ap-northeast-2.compute.amazonaws.com:5000/dashboard/" +
            _this.curCoinName +
            "/" +
            times
        )
        .then(response => {
          // response.data = 현재 String eval 함수를 사용해서 안에 있는
          //json 데이터 추출
          var jsonData = eval(response.data);
          _this.coinData = jsonData;
        });

      //console.log(_this.coinData);
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
    },
    async initChart1(coinCode = "btc_krw", times = 60) {
      var _this = this;
      //this.getCoinName(coinCode);
      _this.coinCode = coinCode;
      _this.times = times;
      await this.loadQuote(_this.coinCode, _this.times);
      this.chart1 = echarts.init(document.getElementById("chart1"));

      var _this = this;
      let date = [];
      let last = [];
      // chart에 표현할 데이터
      var graphData = _this.coinData;

      graphData.forEach(function(element) {
        var d = new Date(element["time"]["$date"]);
        var l = element["last"];
        date.push(d.toISOString());
        last.push(l);
        //console.log(d.format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}'));
      });

      // json  [{"_id, timestamp, last, bid, ask, low, high, volume, change, changePercent, currency, time "}, ~~~~~
      // Generate data
      let category = [];
      let dottedBase = +new Date();
      let lineData = [];
      let barData = [];

      var yMin = 0;
      var yMax = 0;
      var dateLen = date.length;
      for (let i = times - 1; i >= 0; i--) {
        category.push(date[i]);
        //barData.push(last[i]);
        //barData.push(parseInt(b))
        var lt = last[i];
        if (i == times - 1) {
          yMin = lt;
          yMax = lt;
        }

        if (lt >= yMax) {
          yMax = lt;
        }
        if (lt <= yMin) {
          yMin = lt;
        }

        lineData.push(last[i]);
      }
      //console.log('yMin  :::: '+ yMin);
      //console.log('yMax  :::: '+ yMax);
      this.chart1.setOption({
        grid: {
          show: false,
          left: "20px",
          right: "50px",
          bottom: "20px",
          top: "20px",
          containLabel: true
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross"
          }
        },
        legend: {
          show: false,
          data: ["line", "bar"],
          textStyle: {
            color: "#ccc"
          }
        },
        xAxis: {
          data: category,
          boundaryGap: true,
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,0.5)"
            }
          }
        },
        yAxis: {
          splitLine: { show: false },
          axisLine: {
            lineStyle: {
              color: "rgba(255,255,255,0.5)"
            }
          },

          min: yMin * 0.99,
          max: yMax
        },
        series: [
          {
            //name: 'Data A',
            name: "Data A",
            type: "line",
            smooth: true,
            showAllSymbol: false, // symbol visible/invisible
            symbol: "emptyCircle",
            symbolSize: 10,
            lineStyle: {
              color: "#fff"
            },
            itemStyle: {
              color: "#fff",
              borderColor: "#5f8fdf",
              borderWidth: 3
            },
            areaStyle: {
              color: "rgba(255,255,255,0.2)"
            },
            animationDuration: 2800,
            animationEasing: "cubicInOut",
            data: lineData
          },
          {
            name: "Data B",
            type: "bar",
            barWidth: 10,
            itemStyle: {
              normal: {
                barBorderRadius: 5,
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: "#fff" },
                  { offset: 1, color: "rgba(255,255,255,0)" }
                ])
              }
            },
            data: barData
          }
        ]
      });
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


