"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import FactoryChart from "@/components/factory-chart"
import type { Factory } from "@/lib/types"

export default function Home() {
  const [factories, setFactories] = useState<Factory[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchFactories = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/v1/factories")
        if (!response.ok) {
          throw new Error("Failed to fetch factories")
        }
        const data = (await response.json())["factories"];
        console.log()
        setFactories(data)
      } catch (err) {
        setError("Error loading factories. Make sure the API server is running.")
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchFactories()
  }, [])

  return (
    <main className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-6">Sprocket Factory Dashboard</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <p>{error}</p>
          <p className="text-sm mt-2">Ensure the Flask API is running at http://127.0.0.1:5000</p>
        </div>
      )}

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[...Array(3)].map((_, i) => (
            <Card key={i} className="w-full">
              <CardHeader>
                <Skeleton className="h-8 w-48" />
                <Skeleton className="h-4 w-32" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-[300px] w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {factories.map((factory) => (
            <Card key={factory.id} className="w-full">
              <CardHeader>
                <CardTitle>{factory.name || `Factory ${factory.id}`}</CardTitle>
                <CardDescription>Sprocket Production Overview</CardDescription>
              </CardHeader>
              <CardContent>
                <FactoryChart factory={factory} />
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </main>
  )
}

