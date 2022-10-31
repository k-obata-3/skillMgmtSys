<script>
import { Doughnut } from 'vue-chartjs'

export default ({
  extends: Doughnut,
  name: 'DoughnutChart',
  components: {
  },
  props: {
    chartLabel: Array,
    chartData: Array,
  },
  data() {
    return {
      datas: {
        labels: this.chartLabel,
        datasets: [
          {
            data: this.chartData,
            backgroundColor: ['#6384BA', '#3E9AE7', '#B7DCF6', '#C6ADE4', '#B9EFA4'],
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false,
          position: 'bottom'
        },
        tooltips: {
          enabled: false,
        },
        cutoutPercentage: 80  // 中央の円の割合
      },
    }
  },
  beforeCreated() {
  },
  created() {
  },
  beforeMount() {
  },
  mounted() {
    this.addPlugin({
      afterDraw(chart) {
        let ctx = chart.ctx
        chart.tooltip._data.datasets.forEach((dataset, i) => {
          let dataSum = 0
          dataset.data.forEach((element) => {
              dataSum += element
          })
          let meta = chart.getDatasetMeta(i)
          if (!meta.hidden) {
            meta.data.forEach(function (element, index) {
              element._options.hoverBackgroundColor = element._options.backgroundColor;
              element._options.hoverBorderColor = element._options.borderColor;

              // フォントの設定
              ctx.font = '1rem normal'
              // ラベルをパーセント表示に変更
              let num = Math.round(dataset.data[index] / dataSum * 100)
              let labelString = chart.data.labels[index]
              let dataString = num.toString() + '%'

              // positionの設定
              ctx.textAlign = 'center'
              ctx.textBaseline = 'middle'
              ctx.fillStyle = "#333333";
              // let padding = -20
              let position = element.tooltipPosition()
              // ツールチップに変更内容を表示
              // ctx.fillText(labelString, position.x - 5, position.y - padding) // title
              // 5%以上の場合はテキスト表示
              if(num >= 5) {
                  // ctx.fillText(dataString, position.x, position.y)
                  // ctx.fillText(labelString, position.x, position.y)
              }
            });
          }
        });
      }
    })
  },
  beforeUpdate() {
  },
  updated() {
  },
  beforeDestroy() {
  },
  destroyed() {
  },
  methods: {
    draw() {
      this.renderChart(this.datas, this.options)
    }
  }
})
</script>