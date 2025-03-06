"use client"

import { useEffect, useState } from "react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import { Skeleton } from "@/components/ui/skeleton"
import type { Factory } from "@/lib/types"

interface FactoryChartProps {
  factory: Factory
}

interface ChartDataPoint {
  time: string
  actual: number
  goal: number
}

export default function FactoryChart({ factory }: FactoryChartProps) {
  const [chartData, setChartData] = useState<ChartDataPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8080/v1/factories/${factory.id}`)
        if (!response.ok) {
          throw new Error("Failed to fetch factory details")
        }

        const data = await response.json()

        if (
          data.chart_data &&
          data.chart_data.time &&
          data.chart_data.sprocket_production_actual &&
          data.chart_data.sprocket_production_goal
        ) {
          // Transform the data for the chart
          const formattedData = data.chart_data.time.map((time: number, index: number) => {
            const date = new Date(time * 1000)
            return {
              time: date.toLocaleTimeString(),
              actual: data.chart_data.sprocket_production_actual[index],
              goal: data.chart_data.sprocket_production_goal[index],
            }
          })

          setChartData(formattedData)
        } else {
          setChartData([])
        }
      } catch (err) {
        setError("Error loading chart data")
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    if (factory.id) {
      fetchChartData()
    }
  }, [factory.id])

  if (loading) {
    return <Skeleton className="h-[300px] w-full" />
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p>{error}</p>
      </div>
    )
  }

  if (chartData.length === 0) {
    return (
      <div className="flex items-center justify-center h-[300px] border rounded-md">
        <p className="text-muted-foreground">No chart data available for this factory</p>
      </div>
    )
  }

  return (
    <div className="w-full h-[300px]">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={chartData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="time"
            tick={{ fontSize: 12 }}
            interval="preserveStartEnd"
            tickFormatter={(value) => value.split(":").slice(0, 2).join(":")}
          />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="actual"
            name="Actual Production"
            stroke="hsl(var(--chart-1))"
            activeDot={{ r: 8 }}
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="goal"
            name="Production Goal"
            stroke="hsl(var(--chart-2))"
            strokeWidth={2}
            strokeDasharray="5 5"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

