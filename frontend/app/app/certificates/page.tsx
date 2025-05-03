"use client";

import Image from "next/image";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function Certificates() {
  const certificates = [
    {
      title: "Communication Excellence",
      description: "Mastery in interpersonal communication skills",
      date: "March 2024",
      level: "Advanced",
      skills: ["Active Listening", "Public Speaking", "Conflict Resolution"],
      image: "/Humaniq App.png"
    },
    {
      title: "Leadership Fundamentals",
      description: "Core leadership principles and practices",
      date: "February 2024",
      level: "Intermediate",
      skills: ["Team Management", "Decision Making", "Strategic Thinking"],
      image: "/Humaniq App.png"
    },
    {
      title: "Emotional Intelligence",
      description: "Understanding and managing emotions effectively",
      date: "January 2024",
      level: "Advanced",
      skills: ["Self-awareness", "Empathy", "Relationship Management"],
      image: "/Humaniq App.png"
    },
    {
      title: "Problem Solving",
      description: "Analytical and creative problem-solving techniques",
      date: "December 2023",
      level: "Intermediate",
      skills: ["Critical Thinking", "Innovation", "Decision Making"],
      image: "/Humaniq App.png"
    }
  ];

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold gradient-text">
            Certificates & Achievements
          </h1>
          <p className="text-muted-foreground">
            Your journey of personal and professional growth
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {certificates.map((certificate, index) => (
            <Card key={index} className="card-hover">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <CardTitle>{certificate.title}</CardTitle>
                  <Badge variant="outline" className="bg-primary/20">
                    {certificate.level}
                  </Badge>
                </div>
                <CardDescription>{certificate.description}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative h-48 w-full">
                  <Image
                    src={certificate.image}
                    alt={certificate.title}
                    fill
                    className="object-contain"
                  />
                </div>
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">
                    Earned: {certificate.date}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {certificate.skills.map((skill, skillIndex) => (
                      <Badge key={skillIndex} variant="outline">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button
                    className="flex-1 bg-gradient-to-r from-primary to-secondary"
                  >
                    View Certificate
                  </Button>
                  <Button variant="outline" className="flex-1">
                    Share
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}