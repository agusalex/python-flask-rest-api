"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { ArrowLeft } from "lucide-react"
import FactoryChart from "@/components/factory-chart"
import type { Factory, Sprocket } from "@/lib/types"

export default function FactoryPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [factory, setFactory] = useState<Factory | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchFactory = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8080/v1/factory/${params.id}`)
        if (!response.ok) {
          throw new Error("Failed to fetch factory details")
        }
        const data = await response.json()
        setFactory(data)
      } catch (err) {
        setError("Error loading factory details. Make sure the API server is running.")
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchFactory()
  }, [params.id])

  return (
    <main className="container mx-auto py-8 px-4">
      <Button variant="outline" className="mb-6" onClick={() => router.push("/")}>
        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Dashboard
      </Button>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <p>{error}</p>
        </div>
      )}

      {loading ? (
        <div className="space-y-6">
          <Skeleton className="h-12 w-64" />
          <Card>
            <CardHeader>
              <Skeleton className="h-8 w-48" />
              <Skeleton className="h-4 w-32" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-[400px] w-full" />
            </CardContent>
          </Card>
        </div>
      ) : factory ? (
        <div className="space-y-6">
          <h1 className="text-3xl font-bold">{factory.name || `Factory ${factory.id}`}</h1>

          <Card>
            <CardHeader>
              <CardTitle>Production Overview</CardTitle>
              <CardDescription>Sprocket production goals vs. actual production</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <FactoryChart factory={factory} />
              </div>
            </CardContent>
          </Card>

          {factory.sprockets && factory.sprockets.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Sprocket Inventory</CardTitle>
                <CardDescription>Sprockets produced at this factory</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr className="border-b">
                        <th className="text-left py-3 px-4">ID</th>
                        <th className="text-left py-3 px-4">Teeth</th>
                        <th className="text-left py-3 px-4">Pitch Diameter</th>
                        <th className="text-left py-3 px-4">Outside Diameter</th>
                        <th className="text-left py-3 px-4">Pitch</th>
                      </tr>
                    </thead>
                    <tbody>
                      {factory.sprockets.map((sprocket: Sprocket) => (
                        <tr key={sprocket.id} className="border-b">
                          <td className="py-3 px-4">{sprocket.id}</td>
                          <td className="py-3 px-4">{sprocket.teeth}</td>
                          <td className="py-3 px-4">{sprocket.pitch_diameter}</td>
                          <td className="py-3 px-4">{sprocket.outside_diameter}</td>
                          <td className="py-3 px-4">{sprocket.pitch}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      ) : (
        <div className="text-center py-12">
          <h2 className="text-2xl font-semibold">Factory not found</h2>
          <p className="text-muted-foreground mt-2">The factory you're looking for doesn't exist.</p>
        </div>
      )}
    </main>
  )
}

