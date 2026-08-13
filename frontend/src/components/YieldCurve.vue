<template>
  <article class="panel">
    <small>Curva de juros</small>
    <h3>Yield Curve</h3>
    <div ref="chartRef" class="chart"></div>
  </article>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  curve: {
    type: Array,
    default: () => [12.9, 13.1, 13.35, 13.48, 13.62],
  },
})

const chartRef = ref(null)
let chart

const renderChart = async () => {
  await nextTick()
  if (!chartRef.value) return

  if (!chart) {
    chart = echarts.init(chartRef.value)
  }

  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['30d', '60d', '90d', '180d', '360d'],
    },
    yAxis: {
      type: 'value',
      axisLabel: { formatter: '{value}%' },
    },
    series: [
      {
        data: props.curve,
        type: 'line',
        smooth: true,
        areaStyle: {},
        color: '#1f3b63',
      },
    ],
  })
}

onMounted(renderChart)
watch(() => props.curve, renderChart, { deep: true })
onBeforeUnmount(() => chart?.dispose())
</script>
