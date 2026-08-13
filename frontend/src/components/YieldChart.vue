<template>
  <article class="panel">
    <small>Rentabilidade</small>
    <h3>Evolução mensal</h3>
    <div ref="chartRef" class="chart"></div>
  </article>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  series: {
    type: Array,
    default: () => [],
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

  const values = props.series?.length ? props.series : [0.5, 0.7, 0.9, 1.0, 1.1, 1.2]

  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    },
    yAxis: {
      type: 'value',
      axisLabel: { formatter: '{value}%' },
    },
    series: [
      {
        data: values,
        type: 'bar',
        itemStyle: { color: '#c8a96a' },
      },
    ],
  })
}

onMounted(renderChart)
watch(() => props.series, renderChart, { deep: true })
onBeforeUnmount(() => chart?.dispose())
</script>
